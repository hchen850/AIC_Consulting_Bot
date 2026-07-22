from __future__ import annotations

from .llm_common import collect_fields

# FIELDS list for better API implementation
# FIELDS = ["problem", "stage", "urgency", "funding_status", "team_size"]

PERSONA = """You are the BEACH Consulting Assistant, used to support BEACH clients
(startups and small businesses) before they meet with student consultants.
Your purpose is NOT to give advice — only to clarify their situation and collect
concise, relevant information for BEACH consultants. Use neutral frameworks and
plain language. Avoid prescriptive advice (avoid "you should"). Do not provide
legal, tax, or regulatory advice."""

# Use with better API
"""def respond(message: str, history: list[dict], collected: dict):
    return collect_fields(PERSONA, FIELDS, message, history, collected)"""

FIELDS = [
    ("problem", None),  # filled automatically from their initial "what do you need help with" answer
    ("stage", "What is the current stage of your startup or small business? (e.g. idea, early revenue, growth)"),
    ("urgency", "How soon do you need this resolved — urgent, or can it wait a few weeks?"),
    ("funding_status", "What's your current funding status? (e.g. bootstrapped, seed round, Series A)"),
    ("team_size", "How many people are currently on your team?"),
    ("name", "Lastly, what's your name, so we can note it for our records?"),
]

# ---- REQUIRED: derived from FIELDS above, respond() depends on both of these ----
FIELD_QUESTIONS = dict(FIELDS)
FIELD_ORDER = [f for f, _ in FIELDS]

def build_summary(collected: dict) -> str:
    lines = ["Summary for BEACH Consultants:"]
    if collected.get("name"):
        lines.append(f"- Name: {collected['name']}")
    lines.append(f"- What they need help with: {collected.get('problem', '')}")
    lines.append(f"- Stage: {collected.get('stage', '')}")
    lines.append(f"- Urgency: {collected.get('urgency', '')}")
    lines.append(f"- Funding status: {collected.get('funding_status', '')}")
    lines.append(f"- Team size: {collected.get('team_size', '')}")
    return "\n".join(lines)

# ---- CURRENT (HARDCODED) IMPLEMENTATION — replace this function when upgrading ----
def respond(message: str, history: list[dict], collected: dict):
    updated = dict(collected)

    unanswered = [f for f in FIELD_ORDER if not updated.get(f)]
    # Whatever field is currently unanswered gets this message as its answer.
    current_field = unanswered[0]
    updated[current_field] = message.strip()

    still_unanswered = [f for f in FIELD_ORDER if not updated.get(f)]
    if still_unanswered:
        next_field = still_unanswered[0]
        return FIELD_QUESTIONS[next_field], updated, False

    return build_summary(updated), updated, True