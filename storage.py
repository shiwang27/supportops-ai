import json
from dataclasses import asdict
from pathlib import Path

from ticket import SupportTicket


DATA_FILE = Path(__file__).parent / "tickets.json"


def load_tickets():
    if not DATA_FILE.exists():
        return []

    try:
        ticket_data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("Could not read tickets.json. Starting with an empty list.")
        return []

    return [SupportTicket(**data) for data in ticket_data]


def save_tickets(tickets):
    ticket_data = [asdict(ticket) for ticket in tickets]
    DATA_FILE.write_text(
        json.dumps(ticket_data, indent=2),
        encoding="utf-8",
    )
