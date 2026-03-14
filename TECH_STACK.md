# 🛠️ Tech Stack Documentation

## Overview

AgriConnect AI is built with a modern, scalable technology stack optimized for AI-powered agricultural assistance. The architecture combines the best of Python backend capabilities with React frontend performance.

## 🐍 Backend Technologies

### Core Framework
- **FastAPI 0.135.1**
  - Modern, fast web framework for building APIs
  - Automatic interactive documentation (Swagger/OpenAPI)
  - Built-in data validation with Pydantic
  - Async support for high performance
  - Type hints for better code quality

### AI & Machine Learning
- **Groq 1.1.1**
  - Llama 3.3 70B model integration
  - High-performance inference API
  - Optimized for conversational AI
  - Low-latency responses

- **Sentence Transformers 5.3.0**
  - Model: `all-MiniLM-L6-v2`
  - 384-dimensional embeddings
  - Optimized for semantic similarity
  - Fast inference for agricultural terminology

- **LangChain 1.2.12**
  - Text splitting utilities
  - Document processing pipeline
  - RAG (Retrieval-Augmented Generation) support
  - Integration with vector databases

### Vector Database
- **ChromaDB 1.5.5**
  - Persistent vector storage
  - Semantic search capabilities
  - Metadata filtering
  - Scalable to millions of vectors
  - In-memory performance with disk persistence

### Data Processing
- **pypdf 6.8.0**
  - PDF text extraction
  - Robust handling of agricultural PDFs
  - Unicode support for multiple languages
  - Error handling for corrupted documents

### Caching & Session Management
- **Redis 5.0.1** (Optional)
  - Conversation memory storage
  - Session management
  - TTL-based expiration (1 hour)
  - High-performance caching

### Web & API
- **FastAPI Middleware**
  - CORS protection
  - Request validation
  - Error handling
  - HTTP status codes

### Development Tools
- **Python 3.8+**
  - Type hints support
  - Async/await syntax
  - Rich ecosystem of libraries

## ⚛️ Frontend Technologies

### Core Framework
- **React 19.2.4**
  - Latest React with concurrent features
  - Hooks-based architecture
  - Automatic batching
  - Improved performance

### Build Tool
- **Vite 8.0.0**
  - Lightning-fast development server
  - Optimized production builds
  - Hot Module Replacement (HMR)
  - ES modules support
  - Plugin ecosystem

### Styling
- **TailwindCSS 3.4.19**
  - Utility-first CSS framework
  - Responsive design utilities
  - Dark mode support
  - Custom component styling
  - Optimized purging in production

- **@tailwindcss/typography 0.5.19**
  - Beautiful typography defaults
  - Prose styling for content
  - Responsive font sizes

### Icons
- **Lucide React 0.577.0**
  - Modern, consistent icon set
  - Tree-shakeable imports
  - SVG-based icons
  - Customizable styling

### Development Tools
- **ESLint 9.39.4**
  - Code quality enforcement
  - React-specific rules
  - Consistent formatting

- **@vitejs/plugin-react 6.0.0**
  - React integration for Vite
  - Fast refresh
  - JSX support

### Package Management
- **npm** (via package.json)
  - Dependency management
  - Script automation
  - Version locking

## 📊 Data Architecture

### Vector Database Schema
```python
# ChromaDB Collection Structure
{
  "id": "document_chunk_id",
  "document": "text_content",
  "embedding": [384_dimensional_vector],  # all-MiniLM-L6-v2 produces 384 dimensions
  "metadata": {
    "source": "original_document.pdf"
  }
}
```

### Text Processing Pipeline
1. **Ingestion**: PDF → Raw Text
2. **Chunking**: 500 chars with 50 overlap
3. **Embedding**: 384-dimensional vectors
4. **Storage**: ChromaDB persistent storage
5. **Retrieval**: Top-K semantic search

### API Data Models
```python
# Request Models
class AskRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None

# Response Models
{
  "answer": "ai_generated_response",
  "sources": ["source_document.pdf"],
  "conversation_id": "session_identifier"
}
```

## 🔧 Development Environment

### Backend Development
```bash
# Virtual Environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Development Server
uvicorn rag_pipeline:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
# Development Server
npm run dev
# Output: http://localhost:5173

# Production Build
npm run build
# Output: dist/ folder

# Preview Production Build
npm run preview
```

### Code Quality Tools
- **Python**: `py_compile` for syntax checking
- **JavaScript**: ESLint for code quality
- **Type Checking**: Pydantic models, PropTypes via React

## 🚀 Performance Optimizations

### Backend Optimizations
- **Vector Search**: Sub-second retrieval from 584 chunks
- **Batch Processing**: Efficient embedding generation
- **Memory Management**: Lazy loading of models
- **Connection Pooling**: Redis connection optimization

### Frontend Optimizations
- **Code Splitting**: Vite automatic chunking
- **Tree Shaking**: Unused code elimination
- **Asset Optimization**: CSS and JS minification
- **Caching**: Browser cache headers

### Database Optimizations
- **Indexing**: ChromaDB vector indexing
- **Distance Filtering**: Cosine similarity threshold (1.5)
- **Top-K Retrieval**: Limited to 3 most relevant chunks
- **Persistence**: Disk-based vector storage

## 🔒 Security Implementation

### Backend Security
- **Environment Variables**: Sensitive data protection
- **Input Validation**: Pydantic model validation
- **CORS Protection**: Configured allowed origins
- **Error Handling**: No sensitive information leakage

### Frontend Security
- **API Key Protection**: No keys in frontend code
- **Content Security**: Trusted API endpoints
- **Input Sanitization**: React XSS protection

## 📈 Scalability Considerations

### Horizontal Scaling
- **Stateless Design**: Backend can be scaled horizontally
- **Session Isolation**: Redis for distributed sessions
- **Load Balancing**: FastAPI ready for load balancers

### Database Scaling
- **Vector Database**: ChromaDB scales to millions of vectors
- **Memory Efficiency**: Streaming processing for large documents
- **Storage**: Persistent disk storage for durability

### Performance Monitoring
- **Response Times**: API endpoint performance tracking
- **Memory Usage**: Model loading optimization
- **Database Performance**: Query optimization

## 🔄 Integration Points

### External APIs
- **Groq API**: AI model inference
  - Endpoint: `https://api.groq.com/openai/v1/chat/completions`
  - Model: `llama-3.3-70b-versatile`
  - Rate limits: Applied automatically

### Internal APIs
- **FastAPI Endpoints**:
  - `POST /ask` - Main chat endpoint
  - `DELETE /conversation/{id}` - Clear conversation history

### Frontend-Backend Communication
- **REST API**: JSON request/response
- **CORS**: Configured for development
- **Error Handling**: Graceful degradation
- **Loading States**: User feedback during processing

## 📚 Technology Choices Rationale

### Why FastAPI?
- Fast performance (comparable to Node.js)
- Automatic API documentation
- Python ecosystem for AI/ML
- Type safety with Pydantic

### Why React + Vite?
- Fast development experience
- Modern build optimization
- Rich ecosystem of hooks
- Component reusability

### Why ChromaDB?
- Native Python integration
- Persistent vector storage
- Semantic search capabilities
- Easy deployment

### Why TailwindCSS?
- Rapid UI development
- Consistent design system
- Responsive utilities
- Small production bundle


*This tech stack is optimized for performance, maintainability, and scalability in agricultural AI applications.*
