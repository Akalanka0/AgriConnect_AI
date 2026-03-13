# 🌾 AgriConnect AI

An intelligent agricultural assistant powered by AI and RAG (Retrieval-Augmented Generation) technology. Get expert advice on farming, crops, and agriculture from a knowledge base of 584 chunks derived from expert agricultural PDFs.

## 🎯 About

AgriConnect AI is a specialized agricultural knowledge system that combines:
- **RAG Architecture**: Retrieval-Augmented Generation for accurate, context-aware responses
- **Vector Database**: ChromaDB with semantic search capabilities
- **Expert Knowledge Base**: 584 text chunks from agricultural manuals and guides
- **Intelligent Filtering**: Agriculture-specific content filtering with 329+ keywords
- **Conversational Memory**: Optional Redis-based session management
- **Multi-language Support**: Responds in Sinhala when asked in Sinhala

## ✨ Features

- 🤖 **AI-Powered Chat**: Intelligent conversation about agricultural topics using Llama 3.3 70B
- 📚 **Knowledge Base**: 584 document chunks from expert agricultural PDFs
- 🔍 **Smart Search**: Vector-based semantic search with distance filtering (threshold: 1.5)
- 🎨 **Modern UI**: Beautiful, responsive web interface with dark/light themes
- 🌱 **Agricultural Focus**: Specialized in farming and crop management
- 💬 **Conversation Memory**: Session-based context with Redis (optional)
- 🌍 **Multi-language**: English and Sinhala support
- 📊 **Source Attribution**: Shows which documents provided information
- 🚫 **Content Filtering**: Strict agricultural domain enforcement

## 🏗️ Architecture

### Backend (Python FastAPI)
- **FastAPI**: Modern, fast web framework for building APIs
- **ChromaDB**: Vector database for semantic search and retrieval
- **Sentence Transformers**: Text embedding model (all-MiniLM-L6-v2)
- **Groq API**: Llama 3.3 70B model for AI responses
- **Redis**: Optional session management and conversation memory
- **LangChain**: Text splitting and processing utilities

### Frontend (React + Vite)
- **React 19.2.4**: Modern UI framework with hooks
- **Vite 8.0.0**: Fast build tool and development server
- **TailwindCSS 3.4.19**: Utility-first CSS framework
- **Lucide React**: Modern icon library
- **Custom Hooks**: `useChat`, `useTheme` for state management

### Data Pipeline
1. **Ingestion**: PDF text extraction using `pypdf`
2. **Chunking**: Recursive text splitting (500 chars, 50 overlap)
3. **Embedding**: Vector embeddings with Sentence Transformers
4. **Storage**: ChromaDB persistent vector database
5. **Retrieval**: Semantic search with distance filtering

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ 
- Python 3.8+
- Groq API key

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd AgriConnect AI
```

2. **Backend Setup**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp backend/.env.example backend/.env
# Edit backend/.env and add your GROQ_API_KEY
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

4. **Initialize Knowledge Base** (First time only)
```bash
# Run from backend directory
python ingest.py        # Extract text from PDFs
python split_text.py    # Split into chunks
python generate_embeddings.py  # Create vector database
```

5. **Start the Application**
```bash
# From project root
npm start
```

> ⚠️ **Important**: The `npm start` command launches both the frontend and backend together.
> Before running it, make sure your virtual environment is **activated** so that `python` resolves to the venv interpreter:
> - **Windows**: `venv\Scripts\activate`
> - **Mac/Linux**: `source venv/bin/activate`

The application will be available at:
- Frontend: http://localhost:5173
- Backend: http://127.0.0.1:8000

## 📁 Project Structure

```
AgriConnect AI/
├── frontend/                    # React frontend application
│   ├── src/
│   │   ├── components/
│   │   │   └── Chat.jsx        # Main chat interface component
│   │   ├── hooks/
│   │   │   ├── useChat.js      # Chat state management hook
│   │   │   └── useTheme.js     # Theme toggle hook
│   │   ├── utils/
│   │   │   └── constants.js    # API URLs and suggested questions
│   │   └── App.jsx             # Application root component
│   ├── dist/                   # Built production files
│   ├── package.json            # Frontend dependencies and scripts
│   └── vite.config.js          # Vite build configuration
├── backend/                     # Python FastAPI backend
│   ├── rag_pipeline.py         # Main API server with RAG logic
│   ├── ingest.py               # PDF text extraction script
│   ├── split_text.py           # Text chunking script
│   ├── generate_embeddings.py  # Vector database creation script
│   ├── chroma_db/              # Persistent vector database
│   ├── .env.example            # Environment variables template
│   └── .env                    # Local environment variables (gitignored)
├── data/                       # Agricultural documents
│   ├── *.pdf                   # Source agricultural PDFs
│   └── chunks/                 # Processed text chunks
├── requirements.txt            # Python dependencies
├── package.json               # Root package.json for convenience scripts
└── README.md                  # This documentation file
```

## 🔧 Configuration

### Environment Variables
Create `backend/.env` with:
```env
GROQ_API_KEY=your_groq_api_key_here
REDIS_URL=redis://localhost:6379  # Optional - for conversation memory
```

### Get Groq API Key
1. Visit https://console.groq.com/
2. Sign up or log in
3. Navigate to API Keys
4. Copy your API key to the `.env` file

## 📖 Usage

### Core Features
1. **Ask Questions**: Type agricultural questions in the chat interface
2. **Get Expert Advice**: Receive answers based on agricultural documents
3. **View Sources**: See which documents provided the information
4. **Suggested Questions**: Click suggested questions for quick help
5. **Theme Toggle**: Switch between light and dark modes
6. **Clear Chat**: Reset conversation history

### Example Questions
- "What is paddy cultivation?"
- "How to control pests in rice?"
- "Best fertilizer for maize?"
- "When to harvest wheat?"
- "Organic farming benefits"
- "Crop rotation planning"

### Response Types
- **RAG-based**: Technical advice with source attribution
- **Knowledge-based**: General agricultural concepts
- **Off-topic handling**: Graceful redirects for non-agricultural queries
- **Multi-language**: Sinhala responses for Sinhala questions

## 🛠️ Development

### Frontend Development
```bash
cd frontend
npm run dev
```

### Backend Development
```bash
cd backend
python -m uvicorn rag_pipeline:app --reload
```

### Linting
```bash
# Frontend
cd frontend
npm run lint

# Backend
cd backend
python -m py_compile rag_pipeline.py
```

## 📊 Knowledge Base

### Data Processing Pipeline
The system processes agricultural documents through a sophisticated pipeline:

1. **Source Materials**: 5 agricultural PDF documents covering:
   - Rice cultivation guides
   - Pest management manuals
   - Fertilizer recommendations
   - Harvesting techniques
   - Modern farming practices

2. **Text Extraction**: Using `pypdf` for reliable PDF text extraction
3. **Intelligent Chunking**: RecursiveCharacterTextSplitter with:
   - Chunk size: 500 characters
   - Overlap: 50 characters
   - Smart paragraph preservation

4. **Vector Embeddings**: Sentence Transformers model:
   - Model: `all-MiniLM-L6-v2`
   - Optimized for semantic similarity
   - Efficient for agricultural terminology

5. **Semantic Search**: ChromaDB with:
   - Persistent storage
   - Distance-based filtering (threshold: 1.5)
   - Top-K retrieval (K=3)

### Knowledge Statistics
- **Source PDFs**: 5 agricultural documents
- **Text Chunks**: 584 processed segments
- **Embedding Dimensions**: 384 vectors per chunk
- **Search Threshold**: 1.5 cosine distance
- **Retrieval Count**: Top 3 most relevant chunks

### Agricultural Domain Coverage
The system covers 329+ agricultural keywords including:
- **Crops**: Rice, wheat, maize, vegetables, fruits
- **Practices**: Cultivation, irrigation, harvesting, rotation
- **Soil & Nutrients**: Fertilizers, compost, pH, drainage
- **Pest Management**: Pesticides, IPM, biocontrol
- **Livestock**: Cattle, poultry, aquaculture
- **Seasons**: Maha, Yala, seasonal planning

## 🔒 Security

### Data Protection
- Environment variables are never committed to version control
- API keys are properly secured with `.env` files
- No sensitive data stored in frontend code
- CORS protection configured for development origins

### Input Validation
- Question length validation (max 1000 characters)
- Empty input protection
- Agricultural domain filtering with 329+ keywords
- Off-topic query handling with graceful responses

### API Security
- FastAPI with built-in input validation
- Pydantic models for request/response validation
- Error handling without exposing system details
- Optional Redis for session isolation

## 🚀 Performance

### Optimization Features
- **Vector Search**: Sub-second semantic retrieval
- **Caching**: Optional Redis for conversation memory
- **Lazy Loading**: Efficient resource utilization
- **Build Optimization**: Vite production builds with code splitting

### Response Times
- **Vector Search**: < 100ms for 584 chunks
- **AI Generation**: 1-3 seconds depending on query complexity
- **Total Response**: Typically < 5 seconds
- **Frontend Rendering**: Instant with React 19

### Scalability
- **Database**: ChromaDB scales to millions of vectors
- **Memory**: Efficient chunk management
- **Concurrent Users**: Redis session isolation
- **Horizontal Scaling**: Stateless backend design

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**Backend won't start:**
- Check your GROQ_API_KEY in backend/.env
- Ensure virtual environment is activated
- Run the knowledge base initialization scripts

**Frontend errors:**
- Clear browser cache
- Restart development server
- Check Node.js version (16+)

**No search results:**
- Ensure knowledge base is initialized
- Check ChromaDB folder exists
- Verify data files are processed

### Support

For issues and questions:
1. Check the troubleshooting section
2. Review the error logs
3. Create an issue with detailed information

---

*AgriConnect AI - Making agricultural knowledge accessible to everyone* 🌾
