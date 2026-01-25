import json
import requests
import sys
from pathlib import Path

TEST_FILE = Path("tests/classification_cases.json")
TEST_FILE.parent.mkdir(exist_ok=True)

text = sys.argv[1]
expected = sys.argv[2]

resp = requests.post(
    "http://127.0.0.1:8000/classify",
    json={"text": text},
    timeout=10
).json()

entry = {
    "input": text,
    "expected": expected,
    "actual": resp
}

if TEST_FILE.exists():
    data = json.loads(TEST_FILE.read_text())
else:
    data = []

data.append(entry)
TEST_FILE.write_text(json.dumps(data, indent=2))
print("Saved test case.")
