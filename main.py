from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Optional
from classifier import classify_text
from router import route
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://YOUR-FRONTEND-NAME.onrender.com",  # add this once you know the real URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: List[Dict] = []
    collected: Dict = {}
    category: Optional[str] = None
    stage: str = "problem"  # "problem" (first message) -> "routed" (business follow-ups)

@app.get("/chat")
def chat():
    return "Hello world"

@app.post("/bot")
def bot(req: ChatRequest):
    new_history = req.history + [{"role": "user", "content": req.message}]

    # Stage 1: classify the "what do you need help with" answer
    if req.stage == "problem":
        classification = classify_text(req.message)
        reply, updated_fields, progress, category = route(req.message, classification, req.history, req.collected)
        new_history.append({"role": "assistant", "content": reply})

        next_stage = "routed" if (category == "business" and not progress["done"]) else "done"

        return {
            "reply": reply,
            "classification": classification,
            "collected": updated_fields,
            "progress": progress,
            "category": category,
            "history": new_history,
            "stage": next_stage,
        }

    # Stage 2: ongoing business follow-up turns only
    classification = {"category": req.category}
    reply, updated_fields, progress, category = route(req.message, classification, req.history, req.collected)
    new_history.append({"role": "assistant", "content": reply})

    next_stage = "done" if progress.get("done") else "routed"

    return {
        "reply": reply,
        "classification": classification,
        "collected": updated_fields,
        "progress": progress,
        "category": category,
        "history": new_history,
        "stage": next_stage,
    }