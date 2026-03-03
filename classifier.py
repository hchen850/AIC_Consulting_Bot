from fastapi import FastAPI
from pydantic import BaseModel, Field
import requests
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Literal, Optional, Dict, Any
import re
import json



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

class ClassifyRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class ClassifyResponse(BaseModel):
    category: Literal["legal", "business"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    flags: List[str] = []
    rationale: str = ""  




LEGAL_PATTERNS = [
    (r"\btrademark\b|\btm\b|\b®\b|\bbrand name\b", "trademark"),
    (r"\bpatent\b|\bprovisional patent\b|\bprior art\b", "patent"),
    (r"\bcopyright\b|\bdmca\b", "copyright"),
    (r"\bnda\b|\bnon[- ]disclosure\b|\bconfidentiality\b", "nda"),
    (r"\bcontract\b|\bterms\b|\bagreement\b|\bmsa\b|\bsow\b", "contract"),
    (r"\bllc\b|\binc\b|\bcorporation\b|\bincorporat(e|ion)\b|\bentity\b", "incorporation"),
    (r"\bcompliance\b|\bregulatory\b|\bregulation\b|\bgdpr\b|\bhipaa\b|\bfda\b", "compliance"),
    (r"\btax\b|\b1099\b|\bw-2\b|\bsales tax\b", "tax"),
    (r"\bliability\b|\bindemnif(y|ication)\b|\bhold harmless\b", "liability"),
    (r"\bemployment law\b|\bmisclassification\b|\bcontractor\b", "employment_law"),
]

BUSINESS_HINTS = [
    (r"\bmarketing\b|\bgo-to-market\b|\bgtm\b", "marketing"),
    (r"\bpricing\b|\brevenue\b|\bbusiness model\b", "pricing"),
    (r"\bcustomer\b|\busers?\b|\bmarket\b|\bpersona\b", "customer_market"),
    (r"\bproduct\b|\bmvp\b|\bprototype\b|\bfeature\b", "product"),
    (r"\boperations\b|\bprocess\b|\bhiring\b|\bteam\b", "operations"),
]

def rule_based_classify(text: str) -> Optional[ClassifyResponse]:
    t = text.lower()

    legal_hits = []
    for pat, flag in LEGAL_PATTERNS:
        if re.search(pat, t):
            legal_hits.append(flag)

    if legal_hits:
        return ClassifyResponse(
            category="legal",
            confidence=0.95,
            flags=sorted(list(set(legal_hits))),
            rationale="Detected legal-related topic keywords."
        )

    business_hits = []
    for pat, flag in BUSINESS_HINTS:
        if re.search(pat, t):
            business_hits.append(flag)

    if business_hits:
        return ClassifyResponse(
            category="business",
            confidence=0.75,
            flags=sorted(list(set(business_hits))),
            rationale="Detected business-related topic keywords."
        )

    return None  

CLASSIFIER_SYSTEM_PROMPT = """You are a strict classifier for a university consulting chatbot.

Classify the user's message into exactly one category:
- "legal": trademarks/IP, contracts, incorporation/entity formation, employment law, compliance/regulatory, liability, taxes
- "business": product, customers, marketing, pricing, operations, strategy, fundraising (non-legal framing)

Rules:
- If you are unsure, choose "legal".
- Do not provide advice.
- Output JSON only, exactly matching this schema:
{"category":"legal"|"business","confidence":0.0-1.0,"flags":["..."],"rationale":"..."}
- rationale must be one short sentence, no more than 12 words.
"""

LEGAL_REFUSAL_PROMPT = """You are the BEACH Consulting Assistant.

The user asked a legal question. You must:
- Refuse to provide legal advice.
- Encourage them to consult a qualified legal professional or a BEACH coordinator.
- Offer a safe alternative: you can help them clarify business priorities or prepare a summary for consultants.

Do NOT ask follow-up questions about legal details.
Do NOT provide legal steps, definitions, or recommendations.

Write 4–8 sentences. Professional, calm, no emojis.
"""

BUSINESS_ASSISTANT_PROMPT = """You are the BEACH Consulting Assistant, used to support BEACH clients
(startups and small businesses) before they meet with student consultants.

Your purpose is NOT to give advice. Your purpose is to:
1) Clarify the client’s situation
2) Identify priorities and next steps (at a high level, not prescriptive)
3) Collect concise, relevant information for BEACH consultants

Rules:
- Ask 3–5 targeted follow-up questions max total.
- Use neutral frameworks and plain language.
- Avoid prescriptive advice (avoid “you should”).
- Do not provide legal, tax, or regulatory advice.
- Do not mention internal reasoning.

Output format:
1) A short helpful sentence acknowledging the topic.
2) 3–5 bullet follow-up questions.
3) A short section titled "Summary for BEACH Consultants:" with 3–6 bullets.
"""


def llm_classify(text: str) -> ClassifyResponse:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": CLASSIFIER_SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        "stream": False
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    content = data["message"]["content"].strip()

    # Parse JSON robustly (the model sometimes adds whitespace/newlines)
    try:
        obj = json.loads(content)
    except json.JSONDecodeError:
        # Fail safe: if anything goes wrong, treat as legal.
        return ClassifyResponse(
            category="legal",
            confidence=0.6,
            flags=["parse_error"],
            rationale="Unclear classification; defaulting to legal."
        )

    cat = obj.get("category", "legal")
    conf = obj.get("confidence", 0.6)
    flags = obj.get("flags", [])
    rationale = obj.get("rationale", "")

    # Hard safety: enforce allowed values + bounds
    if cat not in ("legal", "business"):
        cat = "legal"
    try:
        conf = float(conf)
    except Exception:
        conf = 0.6
    conf = max(0.0, min(1.0, conf))

    if not isinstance(flags, list):
        flags = []
    if not isinstance(rationale, str):
        rationale = ""

    # If confidence is low, still default to legal (policy)
    if conf < 0.55:
        cat = "legal"
        flags = list(set(flags + ["low_confidence"]))
        rationale = "Low confidence; defaulting to legal."

    return ClassifyResponse(category=cat, confidence=conf, flags=flags, rationale=rationale)

def ollama_chat(system_prompt: str, user_message: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "stream": False
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data["message"]["content"]


@app.get("/chat")
def chat():
    return "Hello world"

@app.post("/bot")
def bot(req: ChatRequest):
    # Step 1: classify (rules first, then LLM)
    classification = rule_based_classify(req.message) or llm_classify(req.message)

    # Step 2: choose responder behavior
    if classification.category == "legal":
        reply = ollama_chat(LEGAL_REFUSAL_PROMPT, req.message)
    else:
        reply = ollama_chat(BUSINESS_ASSISTANT_PROMPT, req.message)

    return {
        "reply": reply,
        "classification": classification.model_dump(),  # shows what happened (great for debugging)
    }

@app.post("/classify", response_model=ClassifyResponse)
def classify(req: ClassifyRequest):
    # 1) rules
    ruled = rule_based_classify(req.text)
    if ruled:
        return ruled
    # 2) LLM fallback
    return llm_classify(req.text)