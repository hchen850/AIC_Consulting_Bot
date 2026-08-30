from __future__ import annotations

from .llm_common import collect_fields
from .sheets_log import log_business_summary

PERSONA = """You are the BEACH Consulting Assistant, used to support BEACH clients
(startups and small businesses) before they meet with student consultants.
Your purpose is NOT to give advice — only to clarify their situation and collect
concise, relevant information for BEACH consultants. Use neutral frameworks and
plain language. Avoid prescriptive advice (avoid "you should"). Do not provide
legal, tax, or regulatory advice.

Tailor your follow-up questions to what the client actually said they need help
with — don't ask generic questions unrelated to their situation."""

FIELDS = ["problem", "stage", "urgency", "funding_status", "team_size", "name"]


def respond(message: str, history: list[dict], collected: dict):
    reply, updated, done = collect_fields(PERSONA, FIELDS, message, history, collected)

    if done:
        log_business_summary(updated)

    return reply, updated, done