import os
from dotenv import load_dotenv

load_dotenv()

DOCS_PATH = "docs"
CHROMA_PATH = "chroma_db"
CHROMA_COLLECTION = "cyber_career_docs"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.3-70b-versatile"
N_RESULTS = 4

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")