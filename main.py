"""
main.py — FastAPI backend
Routes /bot messages to the correct handler based on category classifier.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

from ciocca_module import handle_ciocca_query

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
    Expects category to be set by upstream classifier.
    category="ciocca" → Ciocca/BEACH RAG module
    category="general" → Ollama general handler
    """
    if req.category == "ciocca":
        return handle_ciocca_query(req.message)
    else:
        return handle_general_query(req.message)


# ── Ciocca-only endpoint (direct) ─────────────────────────────────────────────
@app.post("/ciocca")
def ciocca_direct(req: ChatRequest):
    """Direct endpoint for Ciocca/BEACH questions — skips classifier."""
    return handle_ciocca_query(req.message)
