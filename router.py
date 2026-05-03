from responders.intake_responder import respond as intake_respond

def route(message: str, classification: dict) -> str:
    return intake_respond(message, classification)
