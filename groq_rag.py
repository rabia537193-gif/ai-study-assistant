import os
import httpx
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

http_client = httpx.Client()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    http_client=http_client
)

def generate_rag_answer(question: str, retrieved_context: list[str]) -> str:
    if retrieved_context:
        context_str = "\n\n".join(retrieved_context)
        prompt_content = f"Context from uploaded notes:\n{context_str}\n\nQuestion: {question}\n\nAnswer using the context above:"
    else:
        prompt_content = f"Answer the following Python programming question clearly and concisely:\n\nQuestion: {question}"

    models_to_try = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama3-8b-8192"
    ]

    for model_name in models_to_try:
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt_content}
                ],
                model=model_name,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception:
            continue

    return "Sorry, unable to reach the AI model right now. Please check your network or Groq API key."