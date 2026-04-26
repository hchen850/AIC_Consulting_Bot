import requests

OLLAMA_URL = "http://localhost:11434/api/chat"

print("🚀 Testing connection to local Ollama...")

payload = {
    "model": "mistral",
    "messages": [
        {"role": "user", "content": "Reply with exactly: Mistral connected"}
    ],
    "stream": False
}

try:
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    print("✅", response.json()["message"]["content"])
except requests.exceptions.ConnectionError:
    print("❌ ERROR: Could not connect. Is the Ollama app running on your computer?")
except Exception as e:
    print(f"❌ ERROR: {e}")