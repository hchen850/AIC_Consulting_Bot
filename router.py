from __future__ import annotations

from responders.legalPrompt import respond as legal_respond
from responders.business_llm import respond as business_respond
from responders.other import respond as other_respond

FIELDS_BY_CATEGORY = {
    "business": ["problem", "stage", "urgency", "funding_status", "team_size", "name"],
}

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
        }
        return reply, updated, progress, category

    elif category == "legal":
        reply = legal_respond(message)
    else:
        reply = other_respond(message, history)
        category = "other"

    progress = {"answered": 1, "total": 1, "remaining": 0, "done": True, "tracked": True}
    return reply, collected, progress, category