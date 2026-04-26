from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from intake_bot import process_intake_message

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
        # Pass the message to the intake loop
        reply = process_intake_message(req.session_id, req.message) 
        return {"reply": reply}
        
    except Exception as e:
        # THIS IS THE MAGIC DETECTIVE! 
        # If your code crashes, it will print exactly why right here.
        print(f"\n🚨 MASSIVE SERVER CRASH: {str(e)} 🚨\n")
        raise HTTPException(status_code=500, detail=str(e))