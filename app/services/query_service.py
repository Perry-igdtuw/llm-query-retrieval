import os
from dotenv import load_dotenv
import google.generativeai as genai
from pinecone import Pinecone

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

# Init Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Init Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)

def embed_query(text: str) -> list:
    """
    Embed user question for search
    """
    response = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="RETRIEVAL_QUERY"
    )
    return response["embedding"]

def find_relevant_chunks(question: str, namespace: str = "bajaj-policy", top_k: int = 5) -> list:
    """
    Returns top matching chunks for a given question
    """
    query_vector = embed_query(question)
    search_results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )

    return [match['metadata']['text'] for match in search_results['matches']]
