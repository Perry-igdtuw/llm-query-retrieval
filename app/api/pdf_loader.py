# app/api/pdf_loader.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.document_processor import download_pdf_from_url, extract_text_from_pdf

router = APIRouter()

class PDFRequest(BaseModel):
    url: str

@router.post("/load-pdf")
def load_pdf_endpoint(request: PDFRequest):
    try:
        filepath = download_pdf_from_url(request.url)
        text = extract_text_from_pdf(filepath)
        return {
            "filename": filepath,
            "preview": text[:1000]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
