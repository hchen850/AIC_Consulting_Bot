import gspread
from google.oauth2.service_account import Credentials
import re
import json
import os
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from openai import OpenAI

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
MODEL_NAME = "deepseek-chat"

class ClassifyResponse(BaseModel):
    category: Literal["legal", "business", "other"]
    project_name: str = "Unknown"  # Added to capture project identity
    confidence: float = Field(..., ge=0.0, le=1.0)
    flags: List[str] = []
    rationale: str = ""

LEGAL_PATTERNS = [
    (r"\btrademark\b|\btm\b|\b®\b|\bbrand name\b", "trademark"),
    (r"\bpatent\b|\bprovisional patent\b|\bprior art\b", "patent"),
    (r"\bcopyright\b|\bdmca\b", "copyright"),
    (r"\bnda\b|\bnon[- ]disclosure\b|\bconfidentiality\b", "nda"),
    (r"\bcontract\b|\bterms\b|\bagreement\b|\bmsa\b|\bsow\b", "contract"),
    (r"\bllc\b|\binc\b|\bcorporation\b|\bincorporat(e|ion)\b|\bentity\b", "incorporation"),
    (r"\bcompliance\b|\bregulatory\b|\bregulation\b|\bgdpr\b|\bhipaa\b|\bfda\b", "compliance"),
    (r"\btax\b|\b1099\b|\bw-2\b|\bsales tax\b", "tax"),
    (r"\bliability\b|\bindemnif(y|ication)\b|\bhold harmless\b", "liability"),
    (r"\bemployment law\b|\bmisclassification\b|\bcontractor\b", "employment_law"),
]

BUSINESS_HINTS = [
    (r"\bmarketing\b|\bgo-to-market\b|\bgtm\b", "marketing"),
    (r"\bpricing\b|\brevenue\b|\bbusiness model\b", "pricing"),
    (r"\bcustomer\b|\busers?\b|\bmarket\b|\bpersona\b", "customer_market"),
    (r"\bproduct\b|\bmvp\b|\bprototype\b|\bfeature\b", "product"),
    (r"\boperations\b|\bprocess\b|\bhiring\b|\bteam\b", "operations"),
]

def rule_based_classify(text: str) -> Optional[ClassifyResponse]:
    t = text.lower()

    legal_hits = []
    for pat, flag in LEGAL_PATTERNS:
        if re.search(pat, t):
            legal_hits.append(flag)

    if legal_hits:
        return ClassifyResponse(
            category="legal",
            project_name="Unknown",
            confidence=0.95,
            flags=sorted(list(set(legal_hits))),
            rationale="Detected legal-related topic keywords."
        )

    business_hits = []
    for pat, flag in BUSINESS_HINTS:
        if re.search(pat, t):
            business_hits.append(flag)

    if business_hits:
        return ClassifyResponse(
            category="business",
            project_name="Unknown",
            confidence=0.75,
            flags=sorted(list(set(business_hits))),
            rationale="Detected business-related topic keywords."
        )

    mentions_ciocca = re.search(r"\bciocca\b|\bciocca center\b", t) is not None
    info_or_website_intent = re.search(
        r"\bwhat is\b|\bwhat does\b|\bwhat can\b|\bservices?\b|\bhelp with\b|\boffer(s|ed)?\b|\babout\b|\bwebsite\b|\bsite\b|\bpage\b|\blink\b|\bwhere can i find\b|\bcontact\b",
        t
    ) is not None

    if mentions_ciocca and info_or_website_intent:
        return ClassifyResponse(
            category="other",
            project_name="Unknown",
            confidence=0.85,
            flags=["ciocca_center"],
            rationale="Detected Ciocca Center informational inquiry."
        )

    return None

CLASSIFIER_SYSTEM_PROMPT = """You are a strict classifier for a university consulting chatbot.

Analyze the user's message and extract two things:
1. CATEGORY: "legal" (IP, contracts), "business" (MVP, marketing, pricing), or "other" (Ciocca Center info).
2. PROJECT NAME: Extract the startup name if mentioned. If not found, write "Unknown".

Rules:
- If you are unsure, choose "legal".
- Do not provide advice.
- Output JSON only, exactly matching this schema:
{"category":"legal"|"business"|"other", "project_name":"...", "confidence":0.0-1.0, "flags":["..."], "rationale":"..."}
- rationale must be one short sentence, no more than 12 words.
"""

def llm_classify(text: str) -> ClassifyResponse:
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": CLASSIFIER_SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            stream=False,
        )
        obj = response.choices[0].message.content.strip()
        parsed = json.loads(obj)

        return ClassifyResponse(
            category=parsed.get("category", "legal"),
            project_name=parsed.get("project_name", "Unknown"),
            confidence=parsed.get("confidence", 0.6),
            flags=parsed.get("flags", []),
            rationale=parsed.get("rationale", "AI classification")
        )
    except Exception:
        return ClassifyResponse(category="legal", project_name="Unknown", confidence=0.5, rationale="Error parsing AI response.")

def _log_interaction_globally(data: ClassifyResponse, raw_text: str):
    """Logs EVERY prompt to a single shared Google Sheet for BEACH employees."""
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        client_sheets = gspread.authorize(creds)

        sheet = client_sheets.open("BEACH_Global_Activity_Log").sheet1

        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            data.project_name,
            data.category,
            raw_text,
            data.rationale,
            f"{int(data.confidence * 100)}%"
        ]

        sheet.append_row(row)
    except Exception as e:
        print(f"[INTERNAL LOG ERROR] Failed to update global sheet: {e}")

def classify_text(text: str) -> dict:
    """
    Returns a plain dict suitable for routing.
    """
    classification = rule_based_classify(text) or llm_classify(text)
    _log_interaction_globally(classification, text)
    return classification.model_dump()