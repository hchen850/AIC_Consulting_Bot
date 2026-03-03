from fastapi import FastAPI
from pydantic import BaseModel
from classifier import classify_text
from router import route

app = FastAPI()

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