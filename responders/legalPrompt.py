import requests
import pandas as pd
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

# Updated prompt to generate both the user response AND a summary for Excel
LEGAL_REFUSAL_PROMPT = """You are the BEACH Consulting Assistant.
The user asked a legal question. 

1. Write a 4–8 sentence professional refusal. No legal advice. Calm, no emojis. Briefly explain why you can't answer.
2. After the refusal, add a line break and then write: 'SUMMARY: [Write a 1-sentence summary of the user's core concern for management]'.
"""

def get_ai_response(message: str) -> str:
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

def save_to_excel(user_query, ai_summary):
    file_name = "BEACH_Escalations.xlsx"
    new_data = {
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M")],
        "User Query": [user_query],
        "Simplified Summary": [ai_summary]
    }
    df_new = pd.DataFrame(new_data)

    try:
        # Append to existing file if it exists
        df_old = pd.read_excel(file_name)
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    except FileNotFoundError:
        df_final = df_new

    df_final.to_excel(file_name, index=False)
    print(f"Successfully logged to {file_name}")

# --- MAIN WORKFLOW ---
user_input = input("Enter your message: ")
full_response = get_ai_response(user_input)

# Split the AI's response into the "User Message" and the "Internal Summary"
if "SUMMARY:" in full_response:
    user_message, summary = full_response.split("SUMMARY:")
else:
    user_message, summary = full_response, "No summary provided."

print(f"\nASSISTANT:\n{user_message.strip()}")

# ASK FOR PERMISSION
share_choice = input("\nWould you like to share this concern with BEACH higher-ups for further review? (yes/no): ").lower()

if share_choice == 'yes':
    save_to_excel(user_input, summary.strip())
    print("Your concern has been escalated.")
else:
    print("Understood. This session will not be shared.")