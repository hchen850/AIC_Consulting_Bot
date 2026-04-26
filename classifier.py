import requests
import json
import re
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

class ClassifyResponse(BaseModel):
    category: Literal["legal", "business", "other"]
    confidence: float
    rationale: str

CLASSIFIER_SYSTEM_PROMPT = """You are a strict classifier for a consulting chatbot.
You must respond ONLY with a raw JSON object. Do not use markdown formatting.

Analyze the user's business needs and categorize them into exactly one of these: "legal", "business", or "other".

Format your response exactly like this:
{
  "category": "legal",
  "confidence": 0.9,
  "rationale": "Brief reason"
}
"""

def classify_text(text: str) -> ClassifyResponse:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": CLASSIFIER_SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        "stream": False
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        r.raise_for_status()
        raw_text = r.json()["message"]["content"].strip()
        
        # Strip markdown if Mistral disobeys the prompt
        if raw_text.startswith("```json"):
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text.replace("```", "").strip()

        parsed = json.loads(raw_text)
        
        return ClassifyResponse(
            category=parsed.get("category", "legal"),
            confidence=float(parsed.get("confidence", 0.6)),
            rationale=parsed.get("rationale", "AI classification")
        )
    except Exception as e:
        print(f"❌ Classifier Error: {e}")
        # Bulletproof fallback so the server never crashes
        return ClassifyResponse(category="business", confidence=0.5, rationale="Default due to parsing error.")