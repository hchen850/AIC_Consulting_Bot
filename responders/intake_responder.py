# responders/intake_responder.py

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "phi3:mini"

QUESTIONS = [
    "Please tell us generally what type of advice you are seeking (e.g., a business or legal problem or opportunity, things you have questions about, etc.). Please do not provide any confidential information, but be as specific as possible.",
    "What is your first name?",
    "What is your last name?",
    "What is your email address?",
    "What is your phone number?",
    "Are you an SCU undergraduate student, graduate or PhD student, faculty member, staff member, alumni, or none?",
    "What is your business name?",
    "What type of business is it, such as consulting, manufacturing, e-commerce, restaurant, or another type?",
    "What is your business address, or home address if your business has not started or is run from home?",
    "How long has your business been operating?",
]

session_answers = []

LLM_FOLLOWUP_PROMPT = """
You are the BEACH Consulting Intake Agent.

The required intake form questions have already been completed.

Your role is now to ask one thoughtful follow-up question at a time to better understand the user's situation.

Rules:
- Ask EXACTLY one question.
- Do NOT provide advice.
- Do NOT summarize.
- Do NOT use bullet points.
- Do NOT ask multiple questions.
- No extra text before or after.
"""

def ask_llm_followup(message: str, classification: dict) -> str:
    category = classification.get("category", "unknown")

    intake_context = "\n".join(
        f"{i + 1}. {item['question']} Answer: {item['answer']}"
        for i, item in enumerate(session_answers)
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": LLM_FOLLOWUP_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Detected category: {category}

Intake answers:
{intake_context}

Latest user message:
{message}

Ask the next best follow-up question.
"""
            }
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"].strip()
    except Exception as e:
        print("LLM FOLLOWUP ERROR:", e)
        return "What is the biggest challenge or goal you would like help with first?"

def respond(message: str, classification: dict) -> str:
    current_index = len(session_answers)

    if current_index < len(QUESTIONS):
        session_answers.append({
            "question": QUESTIONS[current_index],
            "answer": message,
            "classification": classification
        })

        next_index = len(session_answers)

        if next_index < len(QUESTIONS):
            return QUESTIONS[next_index]

    return ask_llm_followup(message, classification)