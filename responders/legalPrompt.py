import os
from openai import OpenAI

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
MODEL_NAME = "deepseek-chat"

LEGAL_REFUSAL_PROMPT = """You are the BEACH Startup Strategy Assistant.
The user asked a legal question, but you cannot provide legal advice. Instead, you will
orient the user towards business strategy questions that can help them clarify their
needs and prepare for a conversation with a legal professional.

Format your response using this EXACT structure. Separate each section with one empty
line — do not write the words "blank line," just leave the line actually empty:

Line 1: A short 1-2 sentence acknowledgment that you provide business strategy
guidance, not legal advice.

Then a section titled exactly "Questions to think about for your business:" followed by
1-2 bullet points, each starting with "- ".

Then a section titled exactly "Bring these to a legal professional:" followed by 1-2
bullet points, each starting with "- ".

TONE: Encouraging, professional, and analytical. No emojis. Keep each bullet to one
sentence. Do not add any extra sections beyond these three. Do not include any text
describing formatting instructions (e.g. never write the literal words "blank line") —
only include the actual content.
"""

def _get_ai_response(message: str) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": LEGAL_REFUSAL_PROMPT},
                {"role": "user", "content": message},
            ],
            stream=False,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to AI: {e}"

# --- THE WEB ROUTER ENTRY POINT ---
def respond(message: str) -> str:
    """
    Takes the classified legal message, generates the strategic business pivot,
    and returns the clean text for the website frontend.
    (Data logging is now handled upstream by the global classifier).
    """
    return _get_ai_response(message)