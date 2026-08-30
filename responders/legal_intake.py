from __future__ import annotations

FIELDS = [
    ("problem", None),  # filled automatically from their initial message
    ("legal_topic", "What specific area of legal help do you need? (e.g., trademark, contract review, incorporation, NDA)"),
    ("stage", "What is the current stage of your startup or small business? (e.g. idea, early revenue, growth)"),
    ("urgency", "How soon do you need this resolved — urgent, or can it wait a few weeks?"),
    ("name", "Lastly, what's your name, so we can note it for our records?"),
]

FIELD_QUESTIONS = dict(FIELDS)
FIELD_ORDER = [f for f, _ in FIELDS]


def build_summary(collected: dict) -> str:
    name = collected.get("name", "The client")
    problem = collected.get("problem", "")
    topic = collected.get("legal_topic", "")
    stage = collected.get("stage", "")
    urgency = collected.get("urgency", "")

    return (
        f"Summary for BEACH Consultants (Legal Intake): {name} came in needing help with {problem}. "
        f"The specific legal area is: {topic}. "
        f"Their startup is currently at the following stage: {stage}. "
        f"In terms of timeline, {urgency}."
    )


def respond(message: str, history: list[dict], collected: dict):
    updated = dict(collected)

    unanswered = [f for f in FIELD_ORDER if not updated.get(f)]
    current_field = unanswered[0]
    updated[current_field] = message.strip()

    still_unanswered = [f for f in FIELD_ORDER if not updated.get(f)]
    if still_unanswered:
        next_field = still_unanswered[0]
        return FIELD_QUESTIONS[next_field], updated, False

    return build_summary(updated), updated, True