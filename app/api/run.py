from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import List
from app.services.document_processor import download_pdf_from_url, extract_text_from_pdf, chunk_text
from app.services.embedding_service import store_chunks_in_pinecone, embed_text
from app.services.query_service import find_relevant_chunks
from app.services.answer_service import generate_answer
import os

router = APIRouter()

# Set your custom token for Bearer Auth
VALID_TOKEN = os.getenv("TEAM_TOKEN")

class HackRxRunRequest(BaseModel):
    url: str
    questions: List[str]

@router.post("/hackrx/run")
def run_query(request: HackRxRunRequest, authorization: str = Header(None)):
    try:
        # Bearer Token Auth
        if authorization != f"Bearer {VALID_TOKEN}":
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Step 1: Download & process
        filepath = download_pdf_from_url(request.url)
        text = extract_text_from_pdf(filepath)
        chunks = chunk_text(text)

        # Step 2: Embed & store
        store_chunks_in_pinecone(chunks)

        # Step 3: For each question, search + answer
        results = []
        for q in request.questions:
            relevant = find_relevant_chunks(q)
            answer = generate_answer(q, relevant)
            results.append({
                "question": q,
                "answer": answer,
                "justification": relevant[:3]  # top 3 chunks
            })

        return {
            "answers": [r["answer"] for r in results]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
