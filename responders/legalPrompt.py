import requests
import pandas as pd
from datetime import datetime
import os
import re

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

LEGAL_REFUSAL_PROMPT = """You are the BEACH Startup Strategy Assistant. 
The user asked a legal question, but you cannot provide legal advice. Instead, you will try to orient the user towards business strategy questions that can help them clarify their needs and prepare for a conversation with a legal professional.

Do the following:
1. CLEARLY STATE: Acknowledge the topic and briefly state that as an AI, you provide business strategy guidance, not legal advice or document drafting.
2. THE BUSINESS FOLLOW-UP: Ask 2-3 deep questions about their business model related to that legal topic. (e.g., If they ask about IP, ask about their unique value proposition or trade secrets).
3. THE LEGAL LOG: List 1-2 specific questions they should save for a qualified legal professional or BEACH coordinator and note on the form this bot lives on in the questions box.

TONE: Encouraging, professional, and analytical. No emojis.

REQUIRED STRUCTURE:
[Your friendly response and Business Follow-ups]

PROJECT NAME: [Extract the project name from the user's prompt. If they did not provide one, write exactly 'NONE']
SUMMARY: [1-sentence summary of the startup's initial legal concern for the Excel log]
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

def _save_to_excel(project_name, user_query, ai_summary):
    file_name = "Legal_Log.xlsx"
    new_data = {
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M")],
        "Project Name": [project_name],
        "User Query": [user_query],
        "Simplified Summary": [ai_summary]
    }
    df_new = pd.DataFrame(new_data)

    try:
        if os.path.exists(file_name):
            df_old = pd.read_excel(file_name)
            df_final = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_final = df_new

        df_final.to_excel(file_name, index=False)
        print(f"[SERVER LOG] Excel updated for {project_name}")
    except PermissionError:
        print(f"[SERVER ERROR] Could not save to {file_name} - File is open elsewhere.")
    except Exception as e:
        print(f"[SERVER ERROR] Excel save failed: {e}")

# --- THE WEB ROUTER ENTRY POINT ---
def respond(message: str) -> str:
    full_response = _get_ai_response(message)

    # 1. Use Regex to extract the data tags from the AI's response
    project_match = re.search(r'PROJECT NAME:\s*(.*)', full_response, re.IGNORECASE)
    summary_match = re.search(r'SUMMARY:\s*(.*)', full_response, re.IGNORECASE)

    project_name = project_match.group(1).strip() if project_match else "NONE"
    summary = summary_match.group(1).strip() if summary_match else "No summary provided."

    # 2. Clean the tags out of the message so the user on the website doesn't see them
    user_message = re.sub(r'PROJECT NAME:.*', '', full_response, flags=re.IGNORECASE)
    user_message = re.sub(r'SUMMARY:.*', '', user_message, flags=re.IGNORECASE).strip()

    # 3. Logic: Only save if the AI found a project name
    if project_name.upper() == "NONE" or not project_name:
        # If no name, add a gentle prompt to the end of the web response
        user_message += "\n\nCould you please let me know the name of your project? I'd like to log these strategy questions so a BEACH coordinator can review them with you."
    else:
        # If the name exists, execute the save silently on the server
        _save_to_excel(project_name, message, summary)

    # 4. Return strictly the text for the website frontend to display
    return user_message