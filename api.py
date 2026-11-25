from dataclasses import asdict
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent import handle_request
from evaluation import run_evaluation
from ingestion import ingest_documents
from storage import load_tickets, save_tickets
from ticket import SupportTicket


app = FastAPI(title="SupportOps AI")


class TicketRequest(BaseModel):
    title: str
    description: str
    priority: Literal["low", "medium", "high"] = "medium"


class AssistantRequest(BaseModel):
    question: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tickets")
def get_tickets():
    tickets = load_tickets()
    return [asdict(ticket) for ticket in tickets]


@app.post("/tickets")
def create_ticket(ticket_request: TicketRequest):
    tickets = load_tickets()
    next_id = max((ticket.ticket_id for ticket in tickets), default=0) + 1

    ticket = SupportTicket(
        ticket_id=next_id,
        title=ticket_request.title,
        description=ticket_request.description,
        priority=ticket_request.priority,
    )
    tickets.append(ticket)
    save_tickets(tickets)

    return asdict(ticket)


@app.get("/documents/chunks")
def get_document_chunks():
    chunks = ingest_documents()
    return [asdict(chunk) for chunk in chunks]


@app.post("/assistant/ask")
def ask_assistant(request: AssistantRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    return handle_request(request.question)


@app.get("/evaluation")
def get_evaluation():
    return run_evaluation()
