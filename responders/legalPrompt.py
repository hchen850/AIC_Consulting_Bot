import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

LEGAL_REFUSAL_PROMPT = """You are the BEACH Startup Strategy Assistant. 
The user asked a legal question, but you cannot provide legal advice. Instead, you will try to orient the user towards business strategy questions that can help them clarify their needs and prepare for a conversation with a legal professional.

Do the following:
1. CLEARLY STATE: Acknowledge the topic and briefly state that as an AI, you provide business strategy guidance, not legal advice or document drafting.
2. THE BUSINESS FOLLOW-UP: Ask 1-2 deep questions about their business model related to that legal topic. (e.g., If they ask about IP, ask about their unique value proposition or trade secrets).
3. THE LEGAL LOG: List 1-2 specific questions they should save for a qualified legal professional or BEACH coordinator and note on the form this bot lives on in the questions box.

TONE: Encouraging, professional, and analytical. No emojis.

REQUIRED STRUCTURE:
[Your friendly response and Business Follow-ups]
"""

def _get_ai_response(message: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": LEGAL_REFUSAL_PROMPT},
            {"role": "user", "content": message},
        ],
        "stream": False,
    }
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        r.raise_for_status()
        return r.json()["message"]["content"]
    except Exception as e:
        return f"Error connecting to AI: {e}"

# --- THE WEB ROUTER ENTRY POINT ---
def respond(message: str) -> str:
    """
    Takes the classified legal message, generates the strategic business pivot, 
    and returns the clean text for the website frontend.
    (Data logging is now handled upstream by the global classifier).
    """
    full_response = _get_ai_response(message)
    return full_response
