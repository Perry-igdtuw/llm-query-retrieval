from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.query_service import find_relevant_chunks

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/ask")
def query_pdf(request: QueryRequest):
    try:
        results = find_relevant_chunks(request.question)
        return {
            "question": request.question,
            "relevant_chunks": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
