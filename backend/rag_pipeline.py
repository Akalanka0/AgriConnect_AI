import json
import os
import uuid
from typing import Optional

import chromadb
import redis as redis_lib
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

# 1. Load configuration
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set. Please create backend/.env and add: GROQ_API_KEY=your_key_here"
    )

REDIS_URL = os.getenv("REDIS_URL")

# 2. Initialize Clients
client_groq = Groq(api_key=GROQ_API_KEY)

# 3. Paths and Configuration
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "chroma_db"))
COLLECTION_NAME = "agriculture_chunks"

# 4. Initialize Knowledge Base
print("Initializing AgriConnect Knowledge Base...")
# all-MiniLM-L6-v2 is efficient and maps semantics well for farming terms
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_collection(name=COLLECTION_NAME)

# 5. Redis (optional — app works fine without it)
MAX_HISTORY_MESSAGES = 20  # 10 turns of back-and-forth
MEMORY_TTL_SECONDS = 3600  # sessions expire after 1 hour of inactivity

redis_client: Optional[redis_lib.Redis] = None

if REDIS_URL:
    try:
        redis_client = redis_lib.from_url(
            REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=3,
            socket_timeout=3,
        )
        redis_client.ping()
        print("[OK] Redis connected - conversation memory enabled.")
    except Exception as exc:
        print(f"[WARN] Redis connection failed ({exc}). Running without memory.")
        redis_client = None
else:
    print("[INFO] REDIS_URL not set - conversation memory disabled.")

# 6. FastAPI app and CORS
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None


# 7. Redis helpers
def _redis_key(conversation_id: str) -> str:
    return f"agri:conv:{conversation_id}"


def get_history(conversation_id: str) -> list:
    if not redis_client or not conversation_id:
        return []
    try:
        raw = redis_client.get(_redis_key(conversation_id))
        return json.loads(raw) if raw else []
    except Exception as exc:
        print(f"Redis read error: {exc}")
        return []


def save_history(conversation_id: str, question: str, answer: str) -> None:
    if not redis_client or not conversation_id:
        return
    try:
        history = get_history(conversation_id)
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})
        if len(history) > MAX_HISTORY_MESSAGES:
            history = history[-MAX_HISTORY_MESSAGES:]
        redis_client.set(
            _redis_key(conversation_id), json.dumps(history), ex=MEMORY_TTL_SECONDS
        )
    except Exception as exc:
        print(f"Redis write error: {exc}")


def clear_history(conversation_id: str) -> None:
    if not redis_client or not conversation_id:
        return
    try:
        redis_client.delete(_redis_key(conversation_id))
    except Exception as exc:
        print(f"Redis delete error: {exc}")


# 8. RAG retrieval — original tight settings (top_k=3, threshold=1.5)
def retrieve_context(question, top_k=3):
    """Searches the 584 chunks and filters by mathematical distance."""
    query_embedding = embed_model.encode(question).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    # Distance Check (0.0 = Perfect match, 2.0 = Opposite)
    # Threshold 1.5 allows for relevant but slightly broad matches.
    best_match_dist = results["distances"][0][0]

    if best_match_dist > 1.5:
        return None, []

    context_text = "\n\n".join(results["documents"][0])

    # Clean chunk filenames to original document names
    # e.g. "handbook_01_chunk_47.txt" -> "handbook_01.pdf"
    raw_sources = [m["source"] for m in results["metadatas"][0]]
    sources = []
    for s in raw_sources:
        if "_chunk_" in s:
            base = s[: s.rfind("_chunk_")]
            sources.append(base + ".pdf")
        else:
            sources.append(s)

    return context_text, sources


# 9. Off-topic guard — checked before the LLM is ever called
AGRICULTURE_KEYWORDS = {
    "crop",
    "crops",
    "plant",
    "plants",
    "seed",
    "seeds",
    "seedling",
    "seedlings",
    "paddy",
    "rice",
    "wheat",
    "maize",
    "corn",
    "barley",
    "sorghum",
    "millet",
    "sugarcane",
    "cotton",
    "jute",
    "tea",
    "coffee",
    "cocoa",
    "coconut",
    "rubber",
    "cassava",
    "potato",
    "tomato",
    "onion",
    "garlic",
    "chilli",
    "pepper",
    "bean",
    "lentil",
    "soybean",
    "sunflower",
    "mustard",
    "groundnut",
    "peanut",
    "vegetable",
    "vegetables",
    "fruit",
    "fruits",
    "herb",
    "herbs",
    "spice",
    "spices",
    "mango",
    "banana",
    "papaya",
    "pineapple",
    "citrus",
    "orange",
    "lemon",
    "farm",
    "farming",
    "farmer",
    "farmers",
    "field",
    "fields",
    "land",
    "plot",
    "agriculture",
    "agricultural",
    "agri",
    "agronomy",
    "horticulture",
    "cultivation",
    "cultivate",
    "cultivating",
    "grow",
    "growing",
    "grown",
    "harvest",
    "harvesting",
    "sow",
    "sowing",
    "transplant",
    "transplanting",
    "nursery",
    "germination",
    "germinate",
    "plantation",
    "orchard",
    "garden",
    "gardening",
    "intercrop",
    "intercropping",
    "rotation",
    "maha",
    "yala",
    "chena",
    "soil",
    "clay",
    "loam",
    "compost",
    "manure",
    "mulch",
    "humus",
    "erosion",
    "drainage",
    "irrigation",
    "drip",
    "sprinkler",
    "waterlogging",
    "salinity",
    "acidity",
    "ph",
    "moisture",
    "nutrients",
    "fertilizer",
    "fertiliser",
    "fertilizers",
    "fertilisers",
    "pesticide",
    "pesticides",
    "herbicide",
    "herbicides",
    "fungicide",
    "fungicides",
    "insecticide",
    "insecticides",
    "organic",
    "inorganic",
    "biofertilizer",
    "nitrogen",
    "phosphorus",
    "potassium",
    "npk",
    "urea",
    "dap",
    "micronutrient",
    "zinc",
    "calcium",
    "magnesium",
    "pest",
    "pests",
    "disease",
    "diseases",
    "weed",
    "weeds",
    "insect",
    "insects",
    "fungus",
    "blight",
    "rot",
    "mold",
    "aphid",
    "mite",
    "nematode",
    "ipm",
    "biocontrol",
    "livestock",
    "cattle",
    "cow",
    "buffalo",
    "goat",
    "sheep",
    "poultry",
    "chicken",
    "duck",
    "pig",
    "fish",
    "aquaculture",
    "fishery",
    "yield",
    "variety",
    "hybrid",
    "season",
    "rainfall",
    "climate",
    "greenhouse",
    "hydroponics",
    "pruning",
    "tilling",
    "plowing",
    "photosynthesis",
    "pollination",
    "watershed",
    "agribusiness",
}


def is_agriculture_related(question: str) -> bool:
    text = question.lower()
    return any(kw in text for kw in AGRICULTURE_KEYWORDS)


OFF_TOPIC_REPLY = (
    "I'm AgriConnect AI, your dedicated agricultural assistant. "
    "I'm designed to help with topics like crop cultivation, soil health, "
    "fertilizers, pest management, irrigation, and general farming practices.\n\n"
    "Your question seems to be outside my area of expertise. "
    "Feel free to ask me anything about agriculture - I'm always happy to help!\n\n"
    "For example, you could ask:\n"
    "- How do I improve my soil fertility?\n"
    "- What is the best fertilizer for paddy?\n"
    "- How do I control pests in my vegetable garden?"
)


# 10. Greeting check — original simple list
def is_greeting(text):
    """Captures basic conversational starters."""
    greetings = ["hi", "hello", "hey", "good morning", "ayubowan", "vanakkam", "help"]
    return text.lower().strip() in greetings


# 11. Answer generator — original logic + history + off-topic guard
def generate_answer(question, history=None):
    """Balanced RAG: Expert knowledge for definitions, Strict RAG for instructions."""
    if history is None:
        history = []

    # 1. Handle casual greetings immediately
    if is_greeting(question) and not history:
        return (
            "Hello! I am AgriConnect AI, your agricultural expert. "
            "How can I assist you with your crops or farming challenges today?"
        ), []

    # 2. Off-topic guard — runs BEFORE RAG so even questions that
    #    accidentally match farm documents (e.g. "biryani" → rice docs,
    #    "road conditions" → weather docs) are rejected instantly.
    #
    #    Exception: very short follow-ups (≤ 3 words) when a conversation
    #    is already in progress, e.g. "why?", "tell me more", "how long?"
    is_short_followup = len(question.split()) <= 3 and len(history) > 0
    if not is_agriculture_related(question) and not is_short_followup:
        return OFF_TOPIC_REPLY, []

    # 3. Search your database
    context, sources = retrieve_context(question)

    # 4. Prepare the Prompt
    # We tell the AI it is an 'Expert' so it doesn't fail simple questions like 'What is paddy?'
    system_prompt = (
        "You are AgriConnect AI, a helpful and expert agricultural assistant. "
        "\n\nGUIDELINES:"
        "\n1. For basic definitions or general farming concepts, use your broad expertise."
        "\n2. For specific technical advice (dates, fertilizer amounts, pest control), use the provided CONTEXT."
        "\n3. If the CONTEXT contains specific steps or numbers, prioritize them over general knowledge."
        "\n4. STRICT SCOPE: You ONLY answer questions about farming, crops, soil, irrigation, "
        "fertilizers, pest control, livestock, and related agricultural topics. "
        "If a question mentions agricultural equipment or crops but asks about a non-farming topic "
        "(e.g. using a tractor for travel, cooking a recipe, road conditions), "
        "you MUST firmly decline and redirect to agriculture. Do NOT answer such questions."
        "\n5. Respond in Sinhala if the user asks in Sinhala."
        "\n6. Use the conversation history to give coherent, contextual follow-up answers."
    )

    context_content = (
        context
        if context
        else "No specific technical manual entry found for this exact query."
    )

    messages = [
        {
            "role": "system",
            "content": f"{system_prompt}\n\nCONTEXT FROM MANUALS:\n{context_content}",
        }
    ]
    messages.extend(history)
    messages.append({"role": "user", "content": question})

    try:
        chat_completion = client_groq.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.3,  # Low enough for accuracy, high enough for natural flow
            max_tokens=1024,
        )
        return chat_completion.choices[0].message.content, sources
    except Exception as e:
        return f"I encountered a technical error: {str(e)}", []


# 12. API endpoint
@app.post("/ask")
async def ask_endpoint(req: AskRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=422, detail="Question cannot be empty.")
    if len(question) > 1000:
        raise HTTPException(
            status_code=422, detail="Question is too long (max 1000 characters)."
        )

    conversation_id = req.conversation_id or str(uuid.uuid4())
    history = get_history(conversation_id)
    answer, sources = generate_answer(question, history)
    save_history(conversation_id, question, answer)

    seen = set()
    unique_sources = [s for s in sources if not (s in seen or seen.add(s))]
    return {
        "answer": answer,
        "sources": unique_sources,
        "conversation_id": conversation_id,
    }


@app.delete("/conversation/{conversation_id}")
async def delete_conversation(conversation_id: str):
    clear_history(conversation_id)
    return {"status": "cleared", "conversation_id": conversation_id}


# --- TERMINAL TESTING INTERFACE ---
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("AgriConnect AI (Expert RAG) is now Online")
    print("=" * 50)

    session_id = str(uuid.uuid4())

    while True:
        user_input = input("\nFarmer: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        print("Consulting manuals...")
        hist = get_history(session_id)
        answer, used_sources = generate_answer(user_input, hist)
        save_history(session_id, user_input, answer)

        print("\nAgriConnect AI:")
        print("-" * 30)
        print(answer)
        print("-" * 30)

        if used_sources:
            # Using set() to remove duplicate source names
            print(f"Sources: {', '.join(set(used_sources))}")
