import os
import json
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

VECTOR_STORE_FILE = "vector_store.json"
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def save_vector_store(data):
    with open(VECTOR_STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_vector_store():
    if os.path.exists(VECTOR_STORE_FILE):
        with open(VECTOR_STORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def process_and_ingest_files(files) -> int:
    """PDF files se text extract karke local vector store mein embed karke save karta hai."""
    vector_store = load_vector_store()
    total_chunks = 0

    for file in files:
        pdf_reader = PdfReader(file.file)
        text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        if not text.strip():
            continue

        # Text chunking (500 chars window)
        chunks = [text[i:i+500] for i in range(0, len(text), 450)]

        for chunk in chunks:
            if chunk.strip():
                emb = embedding_model.encode(chunk).tolist()
                vector_store.append({
                    "filename": file.filename,
                    "text": chunk,
                    "embedding": emb
                })
                total_chunks += 1

    save_vector_store(vector_store)
    return total_chunks