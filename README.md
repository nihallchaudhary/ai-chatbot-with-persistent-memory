# 🤖 AI Knowledge Assistant

A full-stack **RAG-based Generative AI application** that lets users upload documents and ask questions about their content. The system combines document processing, vector embeddings, semantic retrieval, reranking, conversational memory, caching, and a Gemini-powered response generator.

## ✨ Features

- 📄 PDF/document upload and processing
- 🔎 Semantic search using vector embeddings
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔄 Query normalization and rewriting
- 🎯 Document reranking and context filtering
- 💬 Conversational chat with persistent conversation history
- 📝 Conversation summarization and memory
- ⚡ Response caching
- 📊 Pipeline metrics and evaluation support
- 🚀 FastAPI REST backend
- ⚛️ React + Vite frontend
- 🐳 Docker support
- 🔐 Environment-based API key configuration

## 📸 Demo

### Educational Background

![Educational Background](screenshots/educational-background.png)

### Technical Skills, AI Projects & Internship Experience

![Technical Skills](screenshots/technical-skills.png)

### RAG & Vector Embeddings

![RAG and Vector Embeddings](screenshots/rag-vector-embeddings.png)

## 🏗️ Architecture

```text
User
  │
  ▼
React Frontend
  │
  ▼
FastAPI REST API
  │
  ▼
Chat Service
  │
  ▼
RAG Pipeline
  ├── Query Normalization
  ├── Query Rewriting
  ├── Document Retrieval
  ├── Reranking
  ├── Context Filtering
  └── RAG Generation
          │
          ▼
     Gemini API
          │
          ▼
     Final Response
```

## 🔄 RAG Pipeline

```text
User Query
    ↓
Query Normalization
    ↓
Query Rewriting
    ↓
Vector/Semantic Retrieval
    ↓
Document Reranking
    ↓
Context Filtering
    ↓
Gemini Response Generation
    ↓
Answer + Sources + Metrics
```

## 📚 Document Processing

Uploaded documents are processed into smaller chunks before being converted into vector embeddings.

```text
PDF / Document
      ↓
Document Loader
      ↓
Text Extraction
      ↓
Chunking
      ↓
Embedding Generation
      ↓
Vector Database
      ↓
Semantic Retrieval
```

This allows the assistant to retrieve relevant sections instead of sending an entire document to the language model.

## 🧠 Embeddings & Retrieval

The project uses **Sentence Transformers** to generate semantic vector embeddings and **ChromaDB** for vector storage and retrieval.

The retrieval pipeline is followed by reranking and context filtering so that the generation stage receives more relevant information.

## 💬 Conversational Memory

The assistant maintains conversation history and supports:

- Persistent conversations
- Conversation retrieval
- Conversation deletion
- Conversation summaries
- Memory processing and retrieval
- Context-aware responses

This enables multi-turn interactions instead of treating every question as completely independent.

## ⚡ Response Caching

Frequently repeated requests can be served from cache, reducing unnecessary model calls and improving response speed.

The frontend can also indicate when a response was served from cache.

## 📊 Evaluation & Metrics

The project contains evaluation and pipeline-metrics components for analyzing the behavior of the RAG system.

Metrics can be used to understand retrieval and generation performance during development.

## 🔌 REST API

The backend exposes REST endpoints for:

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/chat/` | POST | Send a chat query |
| `/api/conversations/` | POST | Create a conversation |
| `/api/conversations/{id}` | GET | Retrieve a conversation |
| `/api/conversations/{id}` | DELETE | Delete a conversation |
| `/api/documents/upload` | POST | Upload a document |
| `/api/health` | GET | Health check |

Interactive API documentation is available through FastAPI's Swagger UI at:

```text
http://localhost:8000/docs
```

## 📁 Project Structure

```text
ai-knowledge-assistant-rag/
│
├── backend/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── dependencies.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   └── services/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── tests/
├── evaluation/
├── screenshots/
│
├── context_filter.py
├── conversation_manager.py
├── conversation_summary_manager.py
├── document_embedder.py
├── document_loader.py
├── document_retriever.py
├── document_store.py
├── gemini_client.py
├── memory_manager.py
├── memory_processor.py
├── memory_retriever.py
├── pdf_processor.py
├── pipeline_stats.py
├── query_normalizer.py
├── query_rewriter.py
├── rag_generator.py
├── rag_pipeline.py
├── reranker.py
├── response_cache.py
│
├── config.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🛠️ Technology Stack

### AI / RAG
- Python
- Google Gemini API
- Retrieval-Augmented Generation
- Sentence Transformers
- Vector Embeddings
- Semantic Search

### Backend
- FastAPI
- REST APIs
- Pydantic
- Uvicorn

### Vector & Data
- ChromaDB
- NumPy
- Pandas
- PyPDF

### Frontend
- React
- JavaScript
- Vite

### DevOps
- Git
- GitHub
- Docker
- Docker Compose

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/nihallchaudhary/ai-knowledge-assistant-rag.git
cd ai-knowledge-assistant-rag
```

### 2. Create a Python environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file from `.env.example` and add your Gemini API key.

```env
GEMINI_API_KEY=your_api_key_here
```

**Never commit your real API key to GitHub.**

### 5. Install frontend dependencies

```bash
cd frontend
npm install
```

### 6. Start the backend

From the project root:

```bash
python -m uvicorn backend.main:app --reload
```

Backend:

```text
http://localhost:8000
```

### 7. Start the frontend

In another terminal:

```bash
cd frontend
npm run dev
```

Then open the local Vite URL shown in the terminal.

## 🐳 Docker

The project also includes Docker configuration.

```bash
docker compose up --build
```

## 🧪 Example Questions

After uploading a document, try:

```text
What is the candidate's educational background?
```

```text
Summarize the candidate's technical skills, AI projects, and internship experience.
```

```text
How does the candidate's AI Knowledge Assistant project use RAG and vector embeddings?
```

For multi-turn testing:

```text
What is the candidate's highest educational qualification?
```

Then:

```text
Which institute did they attend?
```

## 🔒 Security & GitHub

Do not commit:

```text
.env
venv/
.venv/
node_modules/
__pycache__/
*.pyc
data/chroma_db/
uploads/
temp/
```

Use `.env.example` to document required environment variables without exposing secrets.

## ⚠️ Current Limitations

- Retrieval quality depends on document quality and chunking.
- Generated answers depend on the selected Gemini model and available API limits.
- Local vector storage is intended for development rather than a production deployment.
- The system should be evaluated further before being used for high-stakes applications.

## 🔮 Future Improvements

- Authentication and user accounts
- Multiple document collections
- Better source citation and deduplication
- Advanced hybrid search
- Production vector database
- Automated RAG evaluation
- Streaming responses
- Cloud deployment
- More robust observability

## 🎯 Project Highlights

This project demonstrates practical experience with:

- Building a complete RAG pipeline
- Working with LLM APIs
- Semantic vector search
- Embedding generation
- Document ingestion
- Retrieval and reranking
- Conversational memory
- Backend API development
- React frontend development
- Docker-based application setup

## 📌 Project Status

**Completed development project — actively improving and extending.**

## 👨‍💻 Author

**Nihal Chaudhary**

Electrical Engineering Student — NIT Delhi

GitHub: `https://github.com/nihallchaudhary`

## 📄 License

This project is available for educational and portfolio purposes.

---

⭐ If you find this project useful, consider giving the repository a star.
