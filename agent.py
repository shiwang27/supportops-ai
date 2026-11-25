from dataclasses import asdict

from rag import answer_question
from safety import check_request
from storage import load_tickets


def handle_request(question: str):
    safety_result = check_request(question)
    if not safety_result["allowed"]:
        return {
            "route": "blocked",
            "answer": safety_result["reason"],
            "sources": [],
        }

    normalized_question = question.lower()
    if "ticket" in normalized_question and any(
        word in normalized_question for word in ("list", "show", "open")
    ):
        tickets = load_tickets()
        return {
            "route": "ticket_lookup",
            "answer": f"Found {len(tickets)} ticket(s).",
            "tickets": [asdict(ticket) for ticket in tickets],
            "sources": [],
        }

    grounded_answer = answer_question(question)
    return {
        "route": "document_search",
        "answer": grounded_answer.answer,
        "sources": grounded_answer.sources,
        "matches": [asdict(match) for match in grounded_answer.matches],
    }
