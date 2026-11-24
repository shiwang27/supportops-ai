from ticket import SupportTicket
from storage import load_tickets, save_tickets


def create_ticket(tickets):
    print("\nCreate a support ticket")

    title = input("Title: ").strip()
    description = input("Description: ").strip()

    priority = input("Priority (low/medium/high): ").strip().lower()
    while priority not in {"low", "medium", "high"}:
        print("Please choose low, medium, or high.")
        priority = input("Priority (low/medium/high): ").strip().lower()

    ticket = SupportTicket(
        ticket_id=len(tickets) + 1,
        title=title,
        description=description,
        priority=priority,
    )
    tickets.append(ticket)
    save_tickets(tickets)

    print(f"Ticket #{ticket.ticket_id} created.\n")


def list_tickets(tickets):
    if not tickets:
        print("\nNo tickets have been created yet.\n")
        return

    print("\nSupport tickets")
    for ticket in tickets:
        print(f"#{ticket.ticket_id} - {ticket.title}")
        print(f"  Priority: {ticket.priority}")
        print(f"  Status: {ticket.status}")
        print(f"  Description: {ticket.description}\n")


def main():
    print("SupportOps AI")

    tickets = load_tickets()

    if tickets:
        print(f"Loaded {len(tickets)} saved ticket(s).\n")

    while True:
        print("1. Create a ticket")
        print("2. List tickets")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_ticket(tickets)
        elif choice == "2":
            list_tickets(tickets)
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Please choose 1, 2, or 3.\n")


if __name__ == "__main__":
    main()
