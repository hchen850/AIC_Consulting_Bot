"""
test_ciocca.py
Mini test set for the Ciocca / BEACH chatbot.
Run: python test_ciocca.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from knowledge_base.ciocca_kb import retrieve_chunks

# ── Inline classifier (mirrors ciocca_module.py) ───────────────────────────
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
    msg_lower = message.lower()
    return any(kw in msg_lower for kw in CIOCCA_KEYWORDS)

# ── Test Cases ────────────────────────────────────────────────────────────────
# Format: (question, expected_behavior, expected_category_hint)
# expected_behavior: "answer" | "escalate"
TEST_CASES = [
    # SCOPE
    ("What is BEACH?", "answer", "scope"),
    ("What does BEACH stand for?", "answer", "scope"),
    ("What is the Ciocca Center?", "answer", "scope"),
    ("What can BEACH help me with?", "answer", "scope"),
    ("Is BEACH like hiring a lawyer?", "answer", "scope"),
    ("Can BEACH give me legal advice?", "answer", "scope"),
    ("What topics does BEACH cover?", "answer", "scope"),
    ("Is BEACH really free?", "answer", "scope"),
    ("How many clients does BEACH serve per year?", "answer", "scope"),

    # INTAKE / PROCESS
    ("How do I apply to BEACH as a client?", "answer", "intake"),
    ("What is the Discovery Meeting?", "answer", "intake"),
    ("How does a BEACH session work?", "answer", "intake"),
    ("How do I apply as a BEACH student?", "answer", "intake"),
    ("How do I apply as a BEACH mentor?", "answer", "intake"),

    # ELIGIBILITY
    ("Who can be a BEACH client?", "answer", "eligibility"),
    ("Do I have to be an SCU student to use BEACH?", "answer", "eligibility"),
    ("Who can be a BEACH mentor?", "answer", "eligibility"),
    ("What stage does my startup need to be at?", "answer", "eligibility"),

    # RESOURCES
    ("What other programs does the Ciocca Center offer?", "answer", "resources"),
    ("What is the Bronco Ventures Accelerator?", "answer", "resources"),
    ("Are there other resources for small businesses besides BEACH?", "answer", "resources"),

    # CONTACT
    ("How do I contact the Ciocca Center?", "answer", "contact"),
    ("When does the next BEACH session start?", "answer", "contact"),

    # PRIVACY
    ("Is my business information kept confidential?", "answer", "privacy"),
    ("Will BEACH sign an NDA?", "answer", "privacy"),

    # ESCALATION (should trigger fallback)
    ("What is the stock price of Apple?", "escalate", None),
    ("Write me a Python script", "escalate", None),
]


def run_tests():
    passed = 0
    failed = 0
    escalated_correctly = 0

    print("=" * 65)
    print("CIOCCA / BEACH CHATBOT — MINI TEST SET")
    print("=" * 65)

    for question, expected, category_hint in TEST_CASES:
        is_ciocca = is_ciocca_question(question)
        chunks = retrieve_chunks(question, top_k=3)
        has_chunks = len(chunks) > 0

        if expected == "answer":
            if has_chunks:
                status = "✅ PASS"
                passed += 1
            else:
                status = "❌ FAIL (no chunks found — would escalate)"
                failed += 1
        elif expected == "escalate":
            if not has_chunks or not is_ciocca:
                status = "✅ PASS (correctly escalated)"
                escalated_correctly += 1
                passed += 1
            else:
                status = "⚠️  WARN (has chunks but shouldn't)"
                failed += 1

        top_chunk = chunks[0]["title"] if chunks else "—"
        print(f"\n{status}")
        print(f"  Q: {question}")
        print(f"  Expected: {expected} | Is Ciocca: {is_ciocca} | Chunks: {len(chunks)}")
        print(f"  Top match: {top_chunk}")

    print("\n" + "=" * 65)
    print(f"RESULTS: {passed}/{len(TEST_CASES)} passed | {failed} failed")
    print("=" * 65)

    return passed, failed


if __name__ == "__main__":
    run_tests()
