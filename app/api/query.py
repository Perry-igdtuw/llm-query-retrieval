from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.query_service import find_relevant_chunks
from app.services.answer_service import generate_answer


router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/ask")
def query_pdf(request: QueryRequest):
    try:
        chunks = find_relevant_chunks(request.question)
        answer = generate_answer(request.question, chunks)
        return {
            "question": request.question,
            "answer": answer,
            "context_snippets": chunks[:3]  # optional: return top 3 for transparency
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
