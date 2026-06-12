# DocMind — AI Document Intelligence

> Upload any PDF. Ask questions. Get accurate answers with page citations.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6B35?style=flat)
![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen)

---

## What It Does

1. **Upload** any PDF document (research papers, contracts, manuals, textbooks)
2. **Ask** questions in natural language
3. **Get** accurate answers with exact page citations
4. **Chat** with follow-up questions (maintains conversation context)

## Architecture

```
PDF Upload → PyMuPDF Extract → Recursive Chunking → Sentence-Transformer Embeddings
                                                              ↓
User Query → Embed Query → ChromaDB Similarity Search → Top-K Chunks → Groq LLM → Answer + Citations
```

## Features

- 📄 **PDF Processing** — Extracts text with page numbers using PyMuPDF
- 🧠 **RAG Pipeline** — Retrieval-Augmented Generation with ChromaDB vector store
- 🔍 **Semantic Search** — Sentence-transformer embeddings for accurate retrieval
- 💬 **Chat Memory** — Multi-turn conversations with context window
- 📌 **Page Citations** — Every answer includes source page numbers
- ⚡ **Fast Inference** — Groq API for near-instant LLM responses
- 🌐 **REST API** — FastAPI with auto-generated Swagger docs
- 🖥️ **Web UI** — Clean chat interface for document Q&A

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI, Python |
| LLM | Groq (Llama 3) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector DB | ChromaDB |
| PDF Parser | PyMuPDF (fitz) |
| Frontend | HTML, CSS, JavaScript |
| Framework | LangChain |

## Quick Start

```bash
git clone https://github.com/ansariazad/DocMind.git
cd DocMind

pip install -r requirements.txt

# Set your Groq API key
export GROQ_API_KEY="your-groq-api-key"

python main.py
```

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Web UI: http://localhost:8000

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload a PDF document |
| `POST` | `/ask` | Ask a question about the document |
| `GET` | `/documents` | List all uploaded documents |
| `DELETE` | `/documents/{id}` | Delete a document and its vectors |
| `GET` | `/health` | Health check |

## Author

**Azad Ansari** · [Portfolio](https://ansariazad.github.io/hire.html) · [GitHub](https://github.com/ansariazad)
