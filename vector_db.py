import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize model
model = SentenceTransformer("all-MiniLM-L6-v2")
DB_FILE = "./chroma_db/vector_store.json"
os.makedirs("./chroma_db", exist_ok=True)

def save_chunks_to_chromadb(documents: list[dict]):
    texts = [doc["text"] for doc in documents]
    embeddings = model.encode(texts).tolist()
    
    data_to_save = []
    for doc, emb in zip(documents, embeddings):
        data_to_save.append({
            "id": doc["id"],
            "text": doc["text"],
            "metadata": doc["metadata"],
            "embedding": emb
        })
        
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)

def query_relevant_chunks(query_text: str, n_results: int = 3) -> list[str]:
    if not os.path.exists(DB_FILE):
        return []
        
    with open(DB_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    if not data:
        return []
        
    query_emb = model.encode([query_text])
    doc_embs = np.array([doc["embedding"] for doc in data])
    
    similarities = cosine_similarity(query_emb, doc_embs)[0]
    top_indices = np.argsort(similarities)[::-1][:n_results]
    
    return [data[i]["text"] for i in top_indices]