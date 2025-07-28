from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.document_processor import (
    download_pdf_from_url,
    extract_text_from_pdf,
    chunk_text
)

router = APIRouter()

class PDFChunkRequest(BaseModel):
    url: str

@router.post("/chunk-pdf")
def chunk_pdf_endpoint(request: PDFChunkRequest):
    try:
        filepath = download_pdf_from_url(request.url)
        text = extract_text_from_pdf(filepath)
        chunks = chunk_text(text)
        return {
            "filename": filepath,
            "chunk_count": len(chunks),
            "chunks_preview": chunks[:5]  # preview first 5 chunks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
