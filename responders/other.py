import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

OTHER_ASSISTANT_PROMPT = """You are the Ciocca Center Assistant.

The user is asking informational questions about the Ciocca Center and/or its website.
Provide a short, clear overview of what the Ciocca Center is and what it can help with,
and then ask up to 3 clarifying questions to direct them to the right resources.

Rules:
- Do not give legal advice.
- Keep it practical and oriented around how to use the center/website.
- If the user asks something legal, remind them you can't provide legal advice.

Output format:
1) 2–4 sentences overview.
2) 1 short bullet list of common things the Ciocca Center can help with.
3) Up to 3 clarifying questions.
"""

def respond(message: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": OTHER_ASSISTANT_PROMPT},
            {"role": "user", "content": message},
        ],
        "stream": False,
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=60)
    r.raise_for_status()
    return r.json()["message"]["content"]