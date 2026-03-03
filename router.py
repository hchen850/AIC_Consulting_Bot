from responders.legalPrompt import respond as legal_respond
from responders.business_llm import respond as business_respond
from responders.other import respond as other_respond

def route(message: str, classification: dict) -> str:
    category = (classification.get("category") or "").lower()

    if category == "legal":
        return legal_respond(message)
    elif category == "business":
        return business_respond(message)
    else:
        return other_respond(message)