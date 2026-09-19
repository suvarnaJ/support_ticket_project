import csv
from collections import Counter, defaultdict

FILE = "support_tickets.csv"

with open(FILE, newline="", encoding="utf-8") as f:
    tickets = list(csv.DictReader(f))

for t in tickets:
    t["ticket_id"] = int(t["ticket_id"])
    t["resolution_time"] = float(t["resolution_time"])

print("TOTAL TICKETS:", len(tickets))

def print_counts(title, field):
    counts = Counter(t[field] for t in tickets)
    print(f"\n{title}")
    for key, value in sorted(counts.items()):
        print(f"{key}: {value}")
    return counts

print_counts("TICKETS BY CATEGORY", "category")
print_counts("TICKETS BY PRIORITY", "priority")
print_counts("TICKETS BY STATUS", "status")

def print_tickets(title, rows):
    print(f"\n{title}")
    for t in rows:
        print(
            f"#{t['ticket_id']} | {t['customer_name']} | "
            f"{t['category']} | {t['priority']} | {t['status']} | "
            f"{t['assigned_agent']} | {t['resolution_time']} min"
        )

open_tickets = [t for t in tickets if t["status"] == "Open"]
critical_tickets = [t for t in tickets if t["priority"] == "Critical"]
resolved_tickets = [t for t in tickets if t["status"] == "Resolved"]

print_tickets("OPEN TICKETS", open_tickets)
print_tickets("CRITICAL TICKETS", critical_tickets)
print_tickets("RESOLVED TICKETS", resolved_tickets)

avg = sum(t["resolution_time"] for t in tickets) / len(tickets)
print(f"\nAVERAGE RESOLUTION TIME: {avg:.2f} minutes")

category_times = defaultdict(list)
for t in tickets:
    category_times[t["category"]].append(t["resolution_time"])

print("\nAVERAGE RESOLUTION TIME PER CATEGORY")
for category in sorted(category_times):
    avg_category = sum(category_times[category]) / len(category_times[category])
    print(f"{category}: {avg_category:.2f} minutes")

agent_counts = Counter(t["assigned_agent"] for t in tickets)
print("\nTICKETS HANDLED BY EACH AGENT")
for agent, count in sorted(agent_counts.items()):
    print(f"{agent}: {count}")

sorted_tickets = sorted(tickets, key=lambda t: t["resolution_time"])
print_tickets("TICKETS SORTED BY RESOLUTION TIME", sorted_tickets)

max_time = max(t["resolution_time"] for t in tickets)
max_tickets = [t for t in tickets if t["resolution_time"] == max_time]
print_tickets("MAXIMUM RESOLUTION TIME TICKETS", max_tickets)

# Export summary report
with open("summary_report.txt", "w", encoding="utf-8") as out:
    out.write(f"Total tickets: {len(tickets)}\n\n")

    for title, field in [
        ("Tickets by category", "category"),
        ("Tickets by priority", "priority"),
        ("Tickets by status", "status"),
    ]:
        out.write(title + ":\n")
        for key, value in sorted(Counter(t[field] for t in tickets).items()):
            out.write(f"  {key}: {value}\n")
        out.write("\n")

    out.write(f"Average resolution time: {avg:.2f} minutes\n\n")
    out.write("Average resolution time per category:\n")
    for category in sorted(category_times):
        value = sum(category_times[category]) / len(category_times[category])
        out.write(f"  {category}: {value:.2f} minutes\n")

    out.write("\nTickets handled by each agent:\n")
    for agent, count in sorted(agent_counts.items()):
        out.write(f"  {agent}: {count}\n")

    out.write("\nTickets taking maximum resolution time:\n")
    for t in max_tickets:
        out.write(f"  Ticket #{t['ticket_id']} - {t['customer_name']} - {t['resolution_time']} minutes\n")
