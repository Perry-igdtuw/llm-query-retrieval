import os
from dotenv import load_dotenv
import google.generativeai as genai
from tqdm import tqdm
from pinecone import Pinecone

load_dotenv()

# Load API keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

# Init Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Init Pinecone v3 client
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)

def embed_text(text: str) -> list:
    """
    Generate vector embedding for a string using Gemini
    """
    response = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return response["embedding"]

def store_chunks_in_pinecone(chunks: list, namespace: str = "bajaj-policy"):
    """
    Embeds and upserts chunks into Pinecone under a namespace
    """
    vectors = []

    for i, chunk in enumerate(tqdm(chunks, desc="Embedding chunks (Gemini)")):
        vector = embed_text(chunk)
        vectors.append({
            "id": f"{namespace}-{i}",
            "values": vector,
            "metadata": {"text": chunk}
        })

    for i in range(0, len(vectors), 100):
        batch = vectors[i:i + 100]
        index.upsert(vectors=batch, namespace=namespace)

    return len(vectors)
