# main.py

from fastapi import FastAPI
from app.api import pdf_loader, chunking, embedder, query
from app.api import pdf_loader, chunking, embedder, query, run


app = FastAPI(title="HackRx LLM Query-Retrieval API")

app.include_router(run.router, prefix="/api/v1")
app.include_router(pdf_loader.router, prefix="/api/v1")
app.include_router(chunking.router, prefix="/api/v1")
app.include_router(embedder.router, prefix="/api/v1")
app.include_router(query.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "LLM Retrieval System is live 🚀"}
