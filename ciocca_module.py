"""
ciocca_module.py
FastAPI router for Ciocca Center / BEACH chatbot.

Flow:
1. Receive message classified as category="ciocca"
2. Retrieve relevant chunks from knowledge base
3. Call Ollama/Mistral with context (RAG)
4. If nothing relevant found → hard fallback
5. Return: { reply, sources, category }
"""

from fastapi import APIRouter
import requests

from knowledge_base.ciocca_kb import retrieve_chunks
from response_templates import apply_template, TEMPLATES

# ── Config ──────────────────────────────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

router = APIRouter()

# ── Classifier keywords ──────────────────────────────────────────────────────
CIOCCA_KEYWORDS = [
    "ciocca", "beach", "bronco entrepreneur", "scu", "santa clara university",
    "legal advice", "business advice", "startup advising", "small business help",
    "free advising", "student advisor", "law student", "business student",
    "bronco ventures", "accelerator", "pitch competition", "venture capital competition",
    "mindset scholar", "innovation fellow", "venture virtuoso",
    "discovery meeting", "advising meeting", "mentor", "client application",
    "llc", "business formation", "intellectual property", "trademark", "patent",
    "fundraising resources", "investor readiness",
]


def is_ciocca_question(message: str) -> bool:
    """Return True if message is likely a Ciocca/BEACH question."""
    msg_lower = message.lower()
    return any(kw in msg_lower for kw in CIOCCA_KEYWORDS)


def build_system_prompt(chunks: list[dict]) -> str:
    """Build RAG system prompt with retrieved knowledge chunks."""
    if not chunks:
        return ""

    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(
            f"[Source {i}: {chunk['title']}]\n{chunk['content']}"
        )

    context = "\n\n".join(context_parts)

    return f"""You are the Ciocca Center / BEACH assistant for Santa Clara University.
You answer questions about the BEACH program (Bronco Entrepreneurs' Applied Collaboration Hub),
the Ciocca Center for Innovation and Entrepreneurship, and related SCU programs.

IMPORTANT RULES:
- Answer ONLY using the provided knowledge base context below.
- Do NOT make up information not in the context.
- If the context does not contain the answer, say you cannot confirm from policy.
- Keep answers concise and helpful (3-5 sentences max unless more detail is needed).
- Never claim to provide legal advice — always note BEACH provides information only.
- Always suggest the official website or contact for further details when appropriate.

KNOWLEDGE BASE CONTEXT:
{context}

Answer the user's question based strictly on the above context."""


def call_ollama(system_prompt: str, user_message: str) -> str:
    """Call Ollama Mistral with system prompt and user message."""
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]


def format_sources(chunks: list[dict]) -> list[dict]:
    """Format chunks as a sources list for the frontend."""
    sources = []
    seen = set()
    for chunk in chunks:
        if chunk["source"] not in seen:
            sources.append({
                "title": chunk["title"],
                "url": chunk["source"],
                "category": chunk["category"],
                "snippet": chunk["content"][:200] + "...",
            })
            seen.add(chunk["source"])
    return sources


def handle_ciocca_query(message: str) -> dict:
    """
    Main handler for Ciocca/BEACH queries.
    Returns: { reply: str, sources: list, category: str, used_fallback: bool }
    """
    # Step 1: Retrieve relevant chunks
    chunks = retrieve_chunks(message, top_k=3)

    # Step 2: Hard fallback if nothing relevant found
    if not chunks:
        return {
            "reply": TEMPLATES["fallback"],
            "sources": [],
            "category": "ciocca",
            "used_fallback": True,
        }

    # Step 3: Determine primary category for templating
    primary_category = chunks[0]["category"] if chunks else "scope"

    # Step 4: Build RAG prompt and call LLM
    system_prompt = build_system_prompt(chunks)
    try:
        raw_answer = call_ollama(system_prompt, message)
    except Exception as e:
        # If Ollama unavailable, use best chunk content directly
        raw_answer = chunks[0]["content"]

    # Step 5: Apply response template
    formatted_reply = apply_template(primary_category, raw_answer)

    # Step 6: Format sources
    sources = format_sources(chunks)

    return {
        "reply": formatted_reply,
        "sources": sources,
        "category": "ciocca",
        "used_fallback": False,
    }
