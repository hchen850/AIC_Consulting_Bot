from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
app = FastAPI()

class ChatRequest(BaseModel):
    message: str

def get_legal_classification(user_text: str):
    system_instruction = (
        "You are a prompt monitor. Classify the prompt as: 'LEGAL', 'BUSINESS', or 'RANDOM'. "
        "LEGAL: Questions about laws, regulations, or litigation. "
        "BUSINESS: Questions about strategy, markets, or operations. "
        "RANDOM: General chat or unrelated topics. "
        "Respond ONLY with the single word category name."
    )
    
    response = llm.invoke([
        SystemMessage(content=system_instruction),
        HumanMessage(content=user_text)
    ])
    return response.content.strip().upper()

@app.post("/bot")
async def bot(req: ChatRequest):
    status = get_legal_classification(req.message)

   
    if "LEGAL" in status:
        return {
            "status": "blocked",
            "decision": status,
            "reply": "I cannot help you with that subject as it is a legal question. "
                     "Would you like me to draft a message to reach out for further help from BEACH assistants?"
        }
    
   
    else:
        expert_response = llm.invoke([
            SystemMessage(content="You are a professional business and general assistant."),
            HumanMessage(content=req.message)
        ])
        return {
            "status": "allowed",
            "decision": status,
            "reply": expert_response.content
        }