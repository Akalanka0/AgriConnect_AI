# AgriConnect AI Backend

This repository contains the backend code for AgriConnect AI, a project focused on agricultural document processing and retrieval using embeddings and vector search.

## Features
- PDF ingestion and text extraction
- Text chunking and embedding generation
- Vector database (ChromaDB) for semantic search
- RAG (Retrieval-Augmented Generation) pipeline

## Setup
1. **Clone the repository**
2. **Create a virtual environment**
3. **Install dependencies**
   - `pip install -r requirements.txt`
4. **Set up environment variables**
   - Copy `.env.example` to `.env` and add your API keys (do NOT commit real keys)

## Usage
- Run scripts in the `backend/` folder for data processing and retrieval.
- Data files go in the `data/` folder.

## Do NOT Commit
- `.env` files with real secrets
- `venv/`, `backend/chroma_db/`, and large data files

## Status
- Backend under active development
- Frontend not included yet

---
*Update this README as the project evolves.*
