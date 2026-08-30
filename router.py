from __future__ import annotations

import re

from responders.legalPrompt import respond as legal_redirect_respond
from responders.legal_intake import respond as legal_intake_respond
from responders.business_llm import respond as business_respond
from responders.other import respond as other_respond

FIELDS_BY_CATEGORY = {
    "business": ["problem", "stage", "urgency", "funding_status", "team_size", "name"],
    "legal": ["problem", "legal_topic", "stage", "urgency", "name"],
}

# Topics BEACH does NOT advise on directly — redirect to a professional instead.
# Matches the three items in the gate question (Taxes, Rental/Property Issues/Evictions, Litigations).
DISALLOWED_LEGAL_PATTERNS = [
    r"\btax\b", r"\btaxes\b", r"\b1099\b", r"\bw-2\b", r"\bsales tax\b", r"\bfiling taxes\b",
    r"\beviction\b", r"\blandlord\b", r"\btenant\b", r"\brental agreement\b", r"\blease\b",
    r"\blitigation\b", r"\blawsuit\b", r"\bsue\b", r"\bsuing\b", r"\bsued\b", r"\bcourt case\b",
]


def _is_disallowed_legal_topic(message: str) -> bool:
    t = message.lower()
    return any(re.search(pat, t) for pat in DISALLOWED_LEGAL_PATTERNS)


def route(message: str, classification: dict, history: list[dict], collected: dict):
    category = (classification.get("category") or "other").lower()
    if category not in ("business", "legal", "other"):
        category = "other"

    if category == "business":
        reply, updated, done = business_respond(message, history, collected)
        fields = FIELDS_BY_CATEGORY["business"]
        answered = sum(1 for f in fields if updated.get(f))
        progress = {
            "answered": answered,
            "total": len(fields),
            "remaining": len(fields) - answered,
            "done": done,
            "tracked": True,
            "is_summary": done,
        }
        return reply, updated, progress, category

    if category == "legal":
        legal_path = collected.get("_legal_path")
        if legal_path is None:
            legal_path = "redirect" if _is_disallowed_legal_topic(message) else "intake"

        if legal_path == "redirect":
            reply = legal_redirect_respond(message)
            updated = dict(collected)
            updated["_legal_path"] = "redirect"
            progress = {"answered": 1, "total": 1, "remaining": 0, "done": True, "tracked": True, "is_summary": False}
            return reply, updated, progress, category

        working_collected = dict(collected)
        working_collected["_legal_path"] = "intake"
        reply, updated, done = legal_intake_respond(message, history, working_collected)
        fields = FIELDS_BY_CATEGORY["legal"]
        answered = sum(1 for f in fields if updated.get(f))
        progress = {
            "answered": answered,
            "total": len(fields),
            "remaining": len(fields) - answered,
            "done": done,
            "tracked": True,
            "is_summary": done,
        }
        return reply, updated, progress, category

    reply = other_respond(message, history)
    category = "other"
    progress = {"answered": 1, "total": 1, "remaining": 0, "done": True, "tracked": True, "is_summary": False}
    return reply, collected, progress, category