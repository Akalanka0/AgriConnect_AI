import os

import chromadb
from sentence_transformers import SentenceTransformer

# Paths - using absolute paths for consistency
chunk_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "chunks")
)
db_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "chroma_db")
)  # Folder where persistent DB will be saved

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Initialize persistent Chroma client
print("Initializing ChromaDB...")
client = chromadb.PersistentClient(path=db_path)

# Create or get collection
collection = client.get_or_create_collection(name="agriculture_chunks")

# Prepare data lists for batching
documents = []
metadatas = []
embeddings = []
ids = []

print("Reading chunks and generating embeddings...")

# Process all chunk files
for filename in os.listdir(chunk_folder):
    if filename.endswith(".txt"):
        file_path = os.path.join(chunk_folder, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Skip empty files
        if not text.strip():
            print(f"Skipping empty file: {filename}")
            continue

        # Generate embedding
        print(f"Generating embedding for: {filename}")
        embedding = model.encode(text).tolist()

        # Add to batch lists
        documents.append(text)
        metadatas.append({"source": filename})
        embeddings.append(embedding)
        ids.append(filename)  # Using filename as unique ID

# Add all chunks to ChromaDB in one batch
if ids:
    collection.upsert(
        documents=documents, metadatas=metadatas, embeddings=embeddings, ids=ids
    )
    print(f"\n✅ Successfully stored {len(ids)} chunks in ChromaDB!")
    print(f"📁 Database saved to: {os.path.abspath(db_path)}")
else:
    print("❌ No chunks found to process.")

print("✨ Embedding generation complete!")
