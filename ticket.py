from dataclasses import dataclass


@dataclass
class SupportTicket:
    ticket_id: int
    title: str
    description: str
    priority: str = "medium"
    status: str = "open"
