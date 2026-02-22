"""
main.py — FastAPI backend
Routes /bot messages to the correct handler based on category classifier.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

from ciocca_module import handle_ciocca_query, is_ciocca_question

# ── Config ──────────────────────────────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

app = FastAPI(title="SCU Chatbot API")

# Allow React frontend on localhost:5173 (Vite default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request Models ───────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    category: str | None = None  # Optional override: "ciocca", "legal", "general"


# ── Health check ─────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "ok", "service": "SCU Chatbot API"}


@app.get("/chat")
def chat():
    return {"message": "Hello from SCU Chatbot API"}


# ── Classifier ───────────────────────────────────────────────────────────────
def classify_message(message: str, override: str | None) -> str:
    """
    Returns category: 'ciocca' | 'legal' | 'general'
    Uses override if provided, otherwise auto-classifies.
    """
    if override:
        return override.lower()
    if is_ciocca_question(message):
        return "ciocca"
    return "general"


# ── General Ollama handler ────────────────────────────────────────────────────
def handle_general_query(message: str) -> dict:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful chatbot for Santa Clara University students and entrepreneurs."},
            {"role": "user", "content": message},
        ],
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return {
        "reply": data["message"]["content"],
        "sources": [],
        "category": "general",
        "used_fallback": False,
    }


# ── Main /bot endpoint ────────────────────────────────────────────────────────
@app.post("/bot")
def bot(req: ChatRequest):
    """
    Main chat endpoint. Classifies the message and routes to the correct handler.
    Returns: { reply, sources, category, used_fallback }
    """
    category = classify_message(req.message, req.category)

    if category == "ciocca":
        result = handle_ciocca_query(req.message)
    else:
        result = handle_general_query(req.message)

    return result


# ── Ciocca-only endpoint (direct) ─────────────────────────────────────────────
@app.post("/ciocca")
def ciocca_direct(req: ChatRequest):
    """Direct endpoint for Ciocca/BEACH questions — skips classifier."""
    return handle_ciocca_query(req.message)
