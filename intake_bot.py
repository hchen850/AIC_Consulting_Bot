import json
import re
import requests
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from classifier import classify_text

# --- CONFIGURATION ---
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

# The expanded list matching the BEACH Client Interest Form
FORM_FIELDS = [
    {"key": "first_name", "question": "Welcome to the BEACH application! First, what is your first name?"},
    {"key": "last_name", "question": "And your last name?"},
    {"key": "email", "question": "What is the best email address to reach you at?"},
    {"key": "phone", "question": "What is your phone number?"},
    {"key": "scu_affiliation", "question": "Are you an SCU Student, Alumni, Faculty, or Staff member? (If none, just say 'None')."},
    {"key": "business_name", "question": "What is the name of your business or startup?"},
    {"key": "business_type", "question": "What type of business is it? (e.g., consulting, manufacturing, e-commerce, restaurant, etc.)"},
    {"key": "business_address", "question": "What is your business address? (You can use your home address if your business isn't started yet or is run from home)."},
    {"key": "operating_time", "question": "How long has your business been operating?"},
    {"key": "needs", "question": "Generally, what type of advice are you seeking? Please focus on business or strategy challenges (e.g., marketing, operations, financial modeling), as we cannot provide legal advice. (Do not share confidential information)."},
    {"key": "how_learned", "question": "How did you hear about the BEACH program?"},
    {"key": "commitment", "question": "Do you agree to the BEACH Client Commitment (attending two meetings, responding timely, providing feedback)? Please reply 'Yes' to confirm."},
    {"key": "disclaimer", "question": "Finally, do you understand the Non-Engagement Disclaimer, noting that we do not become your legal counsel or provide services beyond the consultation? Please reply 'Yes' to confirm."}
]

# Temporary storage for active conversations
user_sessions = {}

LEGAL_KEYWORDS = [
    "legal", "law", "lawsuit", "laws", "attorney", "attorneys", "contract",
    "contracts", "patent", "patents", "trademark", "trademarks", "copyright",
    "compliance", "regulation", "regulations", "liability", "lease", "employment",
    "nda", "nda", "entity formation", "incorporation", "corporation"
]

GENERIC_CATEGORY_WORDS = [
    "marketing", "finance", "strategy", "growth", "sales", "operations",
    "social media", "branding", "pricing", "product", "customer", "team"
]

# --- GOOGLE SHEETS INTEGRATION ---
def save_application_to_sheets(form_data: dict):
    """Logs a completed BEACH application to Google Sheets."""
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        client = gspread.authorize(creds)

        sheet = client.open("BEACH_Global_Activity_Log").sheet1

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = [
            timestamp,
            form_data.get("first_name", ""),
            form_data.get("last_name", ""),
            form_data.get("email", ""),
            form_data.get("phone", ""),
            form_data.get("scu_affiliation", ""),
            form_data.get("business_name", ""),
            form_data.get("business_type", ""),
            form_data.get("business_address", ""),
            form_data.get("operating_time", ""),
            form_data.get("needs", ""),
            form_data.get("how_learned", ""),
            form_data.get("commitment", ""),
            form_data.get("disclaimer", "")
        ]

        sheet.append_row(new_row)
        print(f"✅ SUCCESS: Saved {form_data.get('first_name')}'s application to Google Sheets!")
        
    except Exception as e:
        print(f"❌ ERROR: Failed to save to Google Sheets: {e}")

# --- AI VALIDATION LOGIC ---
def validate_answer(field_key: str, question: str, user_message: str) -> dict:
    """Checks whether the user's reply is clear enough and prompts for clarification when needed."""
    cleaned = (user_message or "").strip()

    if not cleaned:
        return {
            "is_valid": False,
            "extracted_value": None,
            "reask_message": "Could you answer that a little more clearly?"
        }

    if field_key in {"commitment", "disclaimer"}:
        if re.search(r"\b(yes|yep|yeah|i agree|i confirm|confirmed|absolutely|certainly)\b", cleaned, re.IGNORECASE):
            return {"is_valid": True, "extracted_value": "Yes", "reask_message": None}
        return {
            "is_valid": False,
            "extracted_value": None,
            "reask_message": "Please reply with a clear 'Yes' to confirm."
        }

    if field_key == "needs":
        lower = cleaned.lower()
        word_count = len(re.findall(r"\b[\w']+\b", lower))
        if word_count < 4 or lower in {"none", "n/a", "na", "idk", "not sure", "unknown"}:
            return {
                "is_valid": False,
                "extracted_value": None,
                "reask_message": "Thanks — could you tell us a bit more about the business challenge you want help with? For example, what area of growth, marketing, operations, or finance you want support in."
            }

        if any(keyword in lower for keyword in LEGAL_KEYWORDS):
            return {
                "is_valid": False,
                "extracted_value": None,
                "reask_message": "We can help with business strategy and planning, not legal advice. Could you rephrase that as a business challenge, such as growth, marketing, operations, or financial planning?"
            }

        if lower in {"marketing", "finance", "strategy", "growth", "sales", "operations", "social media"}:
            return {
                "is_valid": False,
                "extracted_value": None,
                "reask_message": "That helps a little, but could you share a bit more detail about the specific business problem or goal you want help with?"
            }

        classification = classify_text(cleaned)
        if classification.category == "legal":
            return {
                "is_valid": False,
                "extracted_value": None,
                "reask_message": "We focus on business strategy rather than legal advice. Could you frame this as a business need, such as improving operations, growing sales, or planning a new initiative?"
            }

        if classification.category == "other" and not any(word in lower for word in GENERIC_CATEGORY_WORDS):
            return {
                "is_valid": False,
                "extracted_value": None,
                "reask_message": "Could you tell us more about the business issue you want help with so we can route this properly?"
            }

        return {"is_valid": True, "extracted_value": cleaned, "reask_message": None}

    if field_key in {"first_name", "last_name", "business_name", "business_type", "business_address", "operating_time", "email", "phone", "scu_affiliation", "how_learned"}:
        if re.fullmatch(r"[\W_]+", cleaned):
            return {
                "is_valid": False,
                "extracted_value": None,
                "reask_message": "Could you answer that a bit more clearly?"
            }
        return {"is_valid": True, "extracted_value": cleaned, "reask_message": None}

    prompt = f"""You are a strict intake coordinator for a premium business consulting program.
    Your absolute priority is to ensure data is detailed and accurate. Do not let the user pass with lazy or short responses.

    Current Field: {field_key}
    Question Asked: {question}
    User's Message: {user_message}

    STRICT FIELD-SPECIFIC RULES:
    - For 'needs':
        1. If the answer is extremely brief, generic, or just lists a category (e.g., "marketing", "finance", "strategy", "growth", "sales", "social media"), you MUST set "is_valid" to false. It is completely invalid unless they give context or a short sentence explaining what about it they need help with.
        2. If they ask for legal advice (e.g., trademarks, contracts, patents, legal structures), set "is_valid" to false. Explain that we only handle business strategy.
        3. If rejected for being too short or legal, write a conversational, helpful request in "reask_message" asking them to elaborate or reframe.
    - For 'commitment' and 'disclaimer':
        They MUST give an explicit confirmation (e.g., "Yes", "I agree"). If they say "sure", "ok", or anything ambiguous, set "is_valid" to false and politely demand a clear "Yes".
    - For all other fields (names, email, business name):
        Ensure the answer makes logical sense for that field. If it looks like nonsense, gibberish, or a typo, set "is_valid" to false.

    OUTPUT EXPECTATIONS:
    - If the answer is fully detailed, clear, and perfectly answers the question, set "is_valid": true.
    - If it fails ANY rule above, set "is_valid": false and provide a custom follow-up in "reask_message".
    - Output ONLY raw JSON. No markdown backticks.

    Format:
    {{
        "is_valid": false,
        "extracted_value": null,
        "reask_message": "That sounds interesting, but could you give us a little more detail? What specific marketing challenges are you facing so our business advisors can fully prepare?"
    }}
    """
    
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "system", "content": prompt}],
        "stream": False,
        "options": {
            "temperature": 0.1
        }
    }
    
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        r.raise_for_status()
        raw_text = r.json()["message"]["content"].strip()
        
        if raw_text.startswith("```json"):
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text.replace("```", "").strip()
            
        return json.loads(raw_text)
    except Exception as e:
        print(f"❌ Validation Error: {e}")
        return {"is_valid": True, "extracted_value": cleaned, "reask_message": None}

# --- MAIN CHATBOT FLOW ---
def process_intake_message(session_id: str, user_message: str):
    if session_id not in user_sessions:
        user_sessions[session_id] = {
            "step": 0,
            "data": {field["key"]: None for field in FORM_FIELDS},
            "clarification_attempts": {}
        }
        return FORM_FIELDS[0]["question"]

    session = user_sessions[session_id]
    current_step = session["step"]
    current_field = FORM_FIELDS[current_step]

    print(f"🧠 Checking if '{user_message}' answers '{current_field['key']}'...")
    validation = validate_answer(current_field["key"], current_field["question"], user_message)

    if not validation.get("is_valid"):
        attempts = session.setdefault("clarification_attempts", {})
        field_attempts = attempts.get(current_field["key"], 0) + 1
        attempts[current_field["key"]] = field_attempts

        if field_attempts >= 2:
            print("⚠️ Repeated weak answer; proceeding with best effort.")
            session["data"][current_field["key"]] = user_message
            session["step"] += 1
            next_step = session["step"]
            if next_step < len(FORM_FIELDS):
                return (
                    f"I’m going to move forward with your answer for now. "
                    f"{FORM_FIELDS[next_step]['question']}"
                )
            final_data = session["data"]
            save_application_to_sheets(final_data)
            del user_sessions[session_id]
            return f"Thank you, {final_data.get('first_name')}! Your application for {final_data.get('business_name')} has been submitted to the BEACH team. A coordinator will reach out soon."

        print("❌ Answer needs clarification. Re-asking.")
        return validation.get("reask_message", f"Could you clarify that? {current_field['question']}")

    print(f"✅ Valid! Extracted: {validation.get('extracted_value')}")
    session["data"][current_field["key"]] = validation.get("extracted_value", user_message)
    session["clarification_attempts"].pop(current_field["key"], None)
    
    session["step"] += 1
    next_step = session["step"]

    if next_step < len(FORM_FIELDS):
        return FORM_FIELDS[next_step]["question"]
    else:
        final_data = session["data"]
        save_application_to_sheets(final_data)
        del user_sessions[session_id]
        
        return f"Thank you, {final_data.get('first_name')}! Your application for {final_data.get('business_name')} has been submitted to the BEACH team. A coordinator will reach out soon."