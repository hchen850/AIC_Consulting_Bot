import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from intake_bot import process_intake_message


def test_clarifies_vague_needs_response():
    session_id = "clarify-test"
    first = process_intake_message(session_id, "Hi")
    assert "first name" in first.lower()

    second = process_intake_message(session_id, "Alex")
    assert "last name" in second.lower()

    third = process_intake_message(session_id, "Smith")
    assert "email" in third.lower()

    fourth = process_intake_message(session_id, "alex@example.com")
    assert "phone" in fourth.lower()

    fifth = process_intake_message(session_id, "555-1234")
    assert "student" in fifth.lower()

    sixth = process_intake_message(session_id, "ACME")
    assert "business" in sixth.lower()

    seventh = process_intake_message(session_id, "Consulting")
    assert "business address" in seventh.lower()

    eighth = process_intake_message(session_id, "123 Main St")
    assert "How long" in eighth or "operating" in eighth.lower()

    ninth = process_intake_message(session_id, "2 years")
    assert "Generally, what type of advice" in ninth or "business or strategy" in ninth.lower()

    tenth = process_intake_message(session_id, "marketing")
    assert "more detail" in tenth.lower() or "specific" in tenth.lower()
