from pydantic import BaseModel, Field
import requests
from typing import List, Literal, Optional
import re
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"


class ClassifyResponse(BaseModel):
    category: Literal["legal", "business", "other"]
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

    # 1) legal first
    legal_hits = []
    for pat, flag in LEGAL_PATTERNS:
        if re.search(pat, t):
            legal_hits.append(flag)

    if legal_hits:
        return ClassifyResponse(
            category="legal",
            confidence=0.95,
            flags=sorted(list(set(legal_hits))),
            rationale="Detected legal-related topic keywords."
        )

    # 2) business next
    business_hits = []
    for pat, flag in BUSINESS_HINTS:
        if re.search(pat, t):
            business_hits.append(flag)

    if business_hits:
        return ClassifyResponse(
            category="business",
            confidence=0.75,
            flags=sorted(list(set(business_hits))),
            rationale="Detected business-related topic keywords."
        )

    # 3) other (Ciocca Center informational/website) last
    # Logic: must mention ciocca AND show some informational/website intent
    mentions_ciocca = re.search(r"\bciocca\b|\bciocca center\b", t) is not None
    info_or_website_intent = re.search(
        r"\bwhat is\b|\bwhat does\b|\bwhat can\b|\bservices?\b|\bhelp with\b|\boffer(s|ed)?\b|\babout\b|\bwebsite\b|\bsite\b|\bpage\b|\blink\b|\bwhere can i find\b|\bcontact\b",
        t
    ) is not None

    if mentions_ciocca and info_or_website_intent:
        return ClassifyResponse(
            category="other",
            confidence=0.85,
            flags=["ciocca_center"],
            rationale="Detected Ciocca Center informational inquiry."
        )

    return None


CLASSIFIER_SYSTEM_PROMPT = """You are a strict classifier for a university consulting chatbot.

Classify the user's message into exactly one category:
- "legal": trademarks/IP, contracts, incorporation/entity formation, employment law, compliance/regulatory, liability, taxes
- "business": product, customers, marketing, pricing, operations, strategy, fundraising (non-legal framing)
- "other": informational questions about the Ciocca Center or its website (what it is, what it offers, how it works)

Rules:
- If you are unsure, choose "legal".
- Do not provide advice.
- Output JSON only, exactly matching this schema:
{"category":"legal"|"business"|"other","confidence":0.0-1.0,"flags":["..."],"rationale":"..."}
- rationale must be one short sentence, no more than 12 words.
"""


def llm_classify(text: str) -> ClassifyResponse:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": CLASSIFIER_SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    content = data["message"]["content"].strip()

    try:
        obj = json.loads(content)
    except json.JSONDecodeError:
        return ClassifyResponse(
            category="legal",
            confidence=0.6,
            flags=["parse_error"],
            rationale="Unclear classification; defaulting to legal."
        )

    cat = obj.get("category", "legal")
    conf = obj.get("confidence", 0.6)
    flags = obj.get("flags", [])
    rationale = obj.get("rationale", "")

    if cat not in ("legal", "business", "other"):
        cat = "legal"

    try:
        conf = float(conf)
    except Exception:
        conf = 0.6
    conf = max(0.0, min(1.0, conf))

    if not isinstance(flags, list):
        flags = []
    if not isinstance(rationale, str):
        rationale = ""

    if conf < 0.55:
        cat = "legal"
        flags = list(set(flags + ["low_confidence"]))
        rationale = "Low confidence; defaulting to legal."

    return ClassifyResponse(category=cat, confidence=conf, flags=flags, rationale=rationale)


def classify_text(text: str) -> dict:
    """
    Returns a plain dict suitable for routing.
    Example:
    {"category":"business","confidence":0.75,"flags":[...],"rationale":"..."}
    """
    classification = rule_based_classify(text) or llm_classify(text)
    return classification.model_dump()