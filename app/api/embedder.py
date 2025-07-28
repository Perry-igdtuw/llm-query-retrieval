from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.document_processor import download_pdf_from_url, extract_text_from_pdf, chunk_text
from app.services.embedding_service import store_chunks_in_pinecone

router = APIRouter()

class EmbedRequest(BaseModel):
    url: str

@router.post("/embed-pdf")
def embed_pdf(request: EmbedRequest):
    try:
        filepath = download_pdf_from_url(request.url)
        text = extract_text_from_pdf(filepath)
        chunks = chunk_text(text)  # TEMP: embed only 10 chunks
        total = store_chunks_in_pinecone(chunks)
        return {
            "filename": filepath,
            "chunks_embedded": total
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
