from fastapi import FastAPI
from pydantic import BaseModel
from classifier import classify_text
from router import route
from fastapi.middleware.cors import CORSMiddleware

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
    classification = classify_text(req.message) 
    reply = route(req.message, classification)  

    return {
        "reply": reply,
        "classification": classification,
    }