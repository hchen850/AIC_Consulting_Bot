from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/chat")
def chat():
    return "Hello world"

@app.post("/bot")
def bot(req: ChatRequest):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful chatbot."},
            {"role": "user", "content": req.message}
        ],
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    data = response.json()
    return {
        "reply": data["message"]["content"],
        "response": data
    }
