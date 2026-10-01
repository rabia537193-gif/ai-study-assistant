# 📚 ai-study-assistant

An interactive, modular Retrieval-Augmented Generation (RAG) web application built with **FastAPI**, **Sentence-Transformers**, **Cosine Similarity Search**, and **Groq API (Llama models)**. The system allows users to upload technical Python chapter PDFs and ask detailed study questions, delivering precise context-backed answers.

---

## ✨ Features

- **Multi-PDF Document Processing**: Ingests multiple technical PDF files, chunks content into optimal text segments, and generates dense vector embeddings.
- **Local Vector Storage**: Saves vectorized document embeddings locally for quick similarity querying (`vector_store.json`).
- **Semantic Search & RAG Pipeline**: Employs `sentence-transformers` (`all-MiniLM-L6-v2`) and `scikit-learn` cosine similarity to retrieve relevant study context.
- **Robust Fallback Loop**: Leverages Groq API with an automatic fallback mechanism across verified Llama models (`llama-3.3-70b-versatile`, `llama-3.1-8b-instant`) to guarantee continuous uptime.
- **Clean Responsive UI**: Bootstrap-powered interface allowing quick file uploads and interactive question-answering with retrieved context visibility.

---

## 🛠️ Project Structure

```text
ai_study_assistant/
│
├── main.py              # FastAPI Web Server & API Endpoints
├── ingest.py            # PDF Extraction, Chunking & Embedding Generation
├── rag_service.py       # Vector Similarity Matching & Context Retrieval
├── groq_rag.py          # Groq LLM API Integration & Robust Fallback Handling
├── requirements.txt     # Python Dependencies List
├── .env                 # Environment Variables (API Keys)
├── .gitignore           # Git Exclusions File
│
└── templates/
    └── index.html       # Web UI Interface