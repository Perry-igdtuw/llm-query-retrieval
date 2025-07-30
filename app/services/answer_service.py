import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def generate_answer(question: str, context_chunks: list) -> str:
    """
    Uses Gemini to answer a question given relevant document context
    """
    context = "\n\n".join(context_chunks)
    
    prompt = f"""
You are a helpful AI assistant for an insurance policy.

Answer the following question using the provided policy context:


Answer:"""

    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text.strip()

