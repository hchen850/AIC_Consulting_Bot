import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

LEGAL_REFUSAL_PROMPT = """You are the BEACH Consulting Assistant.

The user asked a legal question. You must:
- Refuse to provide legal advice.
- Encourage them to consult a qualified legal professional or a BEACH coordinator.
- Offer a safe alternative: you can help them clarify business priorities or prepare a summary for consultants.

Do NOT ask follow-up questions about legal details.
Do NOT provide legal steps, definitions, or recommendations.

Write 4–8 sentences. Professional, calm, no emojis.
"""

def respond(message: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": LEGAL_REFUSAL_PROMPT},
            {"role": "user", "content": message},
        ],
        "stream": False,
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=60)
    r.raise_for_status()
    return r.json()["message"]["content"]