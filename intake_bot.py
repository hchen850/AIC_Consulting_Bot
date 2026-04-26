import requests
import json
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
# IMPORT YOUR GOOGLE SHEETS FUNCTION HERE
# from sheets_manager import save_application_to_sheets 

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

FORM_FIELDS = [
    {"key": "name", "question": "Welcome to the BEACH application! First, what is your full name?"},
    {"key": "company", "question": "Great to meet you! What is the name of your startup or project?"},
    {"key": "needs", "question": "Thanks! Finally, briefly describe the business or strategy challenges you need help with."}
]

user_sessions = {}
def save_application_to_sheets(name: str, company: str, needs: str):
    """Logs a completed BEACH application to Google Sheets."""
    try:
        # 1. Load the Credentials
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        client = gspread.authorize(creds)

        # 2. Open the Spreadsheet
        # Note: You might want to create a new tab in your sheet called 'Applications'
        # and use .worksheet("Applications") instead of .sheet1
        sheet = client.open("BEACH_Global_Activity_Log").sheet1

        # 3. Format the row of data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = [timestamp, name, company, needs]

        # 4. Push it to the cloud
        sheet.append_row(new_row)
        print(f"✅ SUCCESS: Saved {name}'s application to Google Sheets!")
        
    except Exception as e:
        print(f"❌ ERROR: Failed to save to Google Sheets: {e}")

def validate_answer(field_key: str, question: str, user_message: str) -> dict:
    """Uses Mistral to check if the user actually answered the question."""
    
    prompt = f"""You are a strict data validation assistant for a consulting intake form.
    Your job is to determine if the user's message appropriately answers the current question.

    Current Field: {field_key}
    Question Asked: {question}
    User's Message: {user_message}

    Rules:
    1. If the user answered the question (even casually), set "is_valid" to true and extract the core answer into "extracted_value".
    2. If the user asked a completely unrelated question, gave a nonsense answer, or refused, set "is_valid" to false.
    3. If invalid, write a polite follow-up question in "reask_message" guiding them to answer the actual question.
    4. Output ONLY raw JSON, no markdown formatting.

    Format:
    {{
        "is_valid": true,
        "extracted_value": "clean answer or null",
        "reask_message": "polite follow-up or null"
    }}
    """
    
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "system", "content": prompt}],
        "stream": False
    }
    
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        r.raise_for_status()
        raw_text = r.json()["message"]["content"].strip()
        
        # Clean markdown if Mistral accidentally adds it
        if raw_text.startswith("```json"):
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text.replace("```", "").strip()
            
        return json.loads(raw_text)
    except Exception as e:
        print(f"❌ Validation Error: {e}")
        # If the AI crashes, default to accepting the answer so the user doesn't get stuck
        return {"is_valid": True, "extracted_value": user_message, "reask_message": None}


def process_intake_message(session_id: str, user_message: str):
    # 1. NEW USER: Start the form
    if session_id not in user_sessions:
        user_sessions[session_id] = {
            "step": 0,
            "data": {field["key"]: None for field in FORM_FIELDS}
        }
        return FORM_FIELDS[0]["question"]

    # 2. EXISTING USER: Check their current step
    session = user_sessions[session_id]
    current_step = session["step"]
    current_field = FORM_FIELDS[current_step]

    # 3. RUN THE LLM GATEKEEPER
    print(f"🧠 Checking if '{user_message}' answers '{current_field['key']}'...")
    validation = validate_answer(current_field["key"], current_field["question"], user_message)

    if not validation.get("is_valid"):
        # The user didn't answer properly. Push back!
        print("❌ Invalid answer. Re-asking.")
        return validation.get("reask_message", f"I didn't quite get that. {current_field['question']}")

    # 4. VALID ANSWER: Save it to short-term memory
    print(f"✅ Valid! Extracted: {validation.get('extracted_value')}")
    session["data"][current_field["key"]] = validation.get("extracted_value", user_message)
    
    # 5. MOVE TO NEXT STEP
    session["step"] += 1
    next_step = session["step"]

    # 6. CHECK IF WE ARE DONE
    if next_step < len(FORM_FIELDS):
        # Ask the next question
        return FORM_FIELDS[next_step]["question"]
    else:
        # ALL SLOTS FULL! 
        final_data = session["data"]
        
        # ---> PUSH TO GOOGLE SHEETS <---
        # save_application_to_sheets(final_data["name"], final_data["company"], final_data["needs"])
        

        
        # ---> THIS IS WHERE YOU CALL YOUR GOOGLE SHEETS FUNCTION <---
        # save_to_sheets(final_data["name"], final_data["company"], final_data["needs"])
        save_application_to_sheets(
            name=final_data["name"], 
            company=final_data["company"], 
            needs=final_data["needs"]
        )
        # Clear their session so they can start over if they want
        del user_sessions[session_id]
        
        return f"Thank you, {final_data['name']}! Your application for {final_data['company']} has been submitted to the BEACH team. A coordinator will reach out soon."