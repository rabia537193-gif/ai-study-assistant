import os
from pypdf import PdfReader

def extract_text_from_pdfs(pdf_paths: list[str]) -> list[dict]:
    """
    Extracts text from a list of PDF file paths and splits them into chunks.
    """
    documents = []
    
    for pdf_path in pdf_paths:
        file_name = os.path.basename(pdf_path)
        reader = PdfReader(pdf_path)
        
        full_text = ""
        for page_idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text += f"\n--- Page {page_idx + 1} ---\n" + text
        
        # Simple text chunking (approx 500 characters per chunk with overlap)
        chunks = chunk_text(full_text, chunk_size=700, overlap=100)
        
        for i, chunk in enumerate(chunks):
            documents.append({
                "id": f"{file_name}_chunk_{i}",
                "text": chunk,
                "metadata": {"source": file_name, "chunk_id": i}
            })
            
    return documents

def chunk_text(text: str, chunk_size: int = 700, overlap: int = 100) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks