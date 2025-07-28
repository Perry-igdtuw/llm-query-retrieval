# app/services/document_processor.py

import os
import requests
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

PDF_DIR = "app/input"

def download_pdf_from_url(url: str, filename: str = "policy.pdf") -> str:
    """
    Downloads the PDF from the given URL and saves it to /app/input/
    """
    os.makedirs(PDF_DIR, exist_ok=True)
    filepath = os.path.join(PDF_DIR, filename)

    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(response.content)
        return filepath
    else:
        raise Exception(f"Failed to download PDF: {response.status_code}")

def extract_text_from_pdf(filepath: str) -> str:
    """
    Extracts and returns all text from the PDF
    """
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> list:
    """
    Splits the given text into manageable chunks for embedding
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_text(text)
    return chunks
