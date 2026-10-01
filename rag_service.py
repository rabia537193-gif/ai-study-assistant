import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ingest import load_vector_store, embedding_model
from groq_rag import generate_rag_answer

def retrieve_context_and_answer(question: str):
    vector_store = load_vector_store()
    if not vector_store:
        raise ValueError("No vector store found. Please upload PDFs first.")

    query_emb = embedding_model.encode(question)
    doc_embs = np.array([doc["embedding"] for doc in vector_store])

    similarities = cosine_similarity([query_emb], doc_embs)[0]
    top_indices = np.argsort(similarities)[-3:][::-1]

    retrieved_context = []
    seen = set()
    for i in top_indices:
        if similarities[i] >= 0.2:
            text = vector_store[i]["text"].strip()
            if text not in seen:
                seen.add(text)
                retrieved_context.append(text)

    # Fallback to top matching chunk if similarity is low
    if not retrieved_context and len(top_indices) > 0:
        retrieved_context = [vector_store[top_indices[0]]["text"]]

    answer = generate_rag_answer(question, retrieved_context)

    return {
        "answer": answer,
        "context": retrieved_context
    }