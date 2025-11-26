# src/services/gemini.py
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

def chat_gemini(prompt: str, model: str | None = None) -> str:
    response = client.models.generate_content(
        model=model or DEFAULT_MODEL,
        contents=prompt,
    )
    return response.text
