import os
import chromadb
from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# 1. Load configuration
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 2. Initialize Clients
client_groq = Groq(api_key=GROQ_API_KEY)

# 3. Paths and Configuration
DB_PATH = "./chroma_db"
COLLECTION_NAME = "agriculture_chunks"

# 4. Initialize Knowledge Base
print("Initializing AgriConnect Knowledge Base...")
# all-MiniLM-L6-v2 is efficient and maps semantics well for farming terms
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_collection(name=COLLECTION_NAME)

def retrieve_context(question, top_k=3):
    """Searches the 584 chunks and filters by mathematical distance."""
    query_embedding = embed_model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    # Distance Check (0.0 = Perfect match, 2.0 = Opposite)
    # Threshold 1.5 allows for relevant but slightly broad matches.
    best_match_dist = results['distances'][0][0]
    
    if best_match_dist > 1.5:
        return None, []

    context_text = "\n\n".join(results['documents'][0])
    sources = [m['source'] for m in results['metadatas'][0]]
    return context_text, sources

def is_greeting(text):
    """Captures basic conversational starters."""
    greetings = ["hi", "hello", "hey", "good morning", "ayubowan", "vanakkam", "help"]
    return text.lower().strip() in greetings

def generate_answer(question):
    """Balanced RAG: Expert knowledge for definitions, Strict RAG for instructions."""
    
    # 1. Handle casual greetings immediately
    if is_greeting(question):
        return ("Hello! I am AgriConnect AI, your agricultural expert. "
                "How can I assist you with your crops or farming challenges today?"), []

    # 2. Search your database
    context, sources = retrieve_context(question)

    # 3. Prepare the Prompt
    # We tell the AI it is an 'Expert' so it doesn't fail simple questions like 'What is paddy?'
    system_prompt = (
        "You are AgriConnect AI, a helpful and expert agricultural assistant. "
        "\n\nGUIDELINES:"
        "\n1. For basic definitions or general farming concepts, use your broad expertise."
        "\n2. For specific technical advice (dates, fertilizer amounts, pest control), use the provided CONTEXT."
        "\n3. If the CONTEXT contains specific steps or numbers, prioritize them over general knowledge."
        "\n4. If the question is NOT about agriculture/farming, politely state you only assist with farming."
        "\n5. Respond in Sinhala if the user asks in Sinhala."
    )

    context_content = context if context else "No specific technical manual entry found for this exact query."

    try:
        chat_completion = client_groq.chat.completions.create(
            messages=[
                {"role": "system", "content": f"{system_prompt}\n\nCONTEXT FROM MANUALS:\n{context_content}"},
                {"role": "user", "content": question}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3, # Low enough for accuracy, high enough for natural flow
            max_tokens=1024,
        )
        return chat_completion.choices[0].message.content, sources
    except Exception as e:
        return f"I encountered a technical error: {str(e)}", []

# --- TERMINAL TESTING INTERFACE ---
if __name__ == "__main__":
    print("\n" + "="*50)
    print("AgriConnect AI (Expert RAG) is now Online")
    print("="*50)
    
    while True:
        user_input = input("\nFarmer: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        print("Consulting manuals...")
        answer, used_sources = generate_answer(user_input)
        
        print("\nAgriConnect AI:")
        print("-" * 30)
        print(answer)
        print("-" * 30)
        
        if used_sources:
            # Using set() to remove duplicate source names
            print(f"Sources: {', '.join(set(used_sources))}")