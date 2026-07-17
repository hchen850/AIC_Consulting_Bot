from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from intake_bot import process_intake_message
from classifier import classify_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "[http://127.0.0.1:5173](http://127.0.0.1:5173)"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/bot")
def bot(req: ChatRequest):
    try:
        reply = process_intake_message(req.session_id, req.message)
        classification = classify_text(req.message)
        return {
            "reply": reply,
            "classification": {
                "category": classification.category,
                "confidence": classification.confidence,
                "rationale": classification.rationale,
            },
        }

    except Exception as e:
        print(f"\n🚨 MASSIVE SERVER CRASH: {str(e)} 🚨\n")
        raise HTTPException(status_code=500, detail=str(e))