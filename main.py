import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from ingest import process_and_ingest_files
from rag_service import retrieve_context_and_answer

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class QueryRequest(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    try:
        total_chunks = process_and_ingest_files(files)
        return {"message": f"Successfully processed {len(files)} files and saved {total_chunks} text chunks into local vector store."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        result = retrieve_context_and_answer(request.question)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)