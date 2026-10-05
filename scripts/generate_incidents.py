from pathlib import Path
import csv
import math
import random
from datetime import datetime, timedelta

SEED = 2026
ROWS = 1200
OUTPUT = Path(__file__).resolve().parents[1] / "data" / "incidents.csv"

random.seed(SEED)

categories = {
    "Access Management": ["Password Reset", "Account Lockout", "Permission", "MFA"],
    "Hardware": ["Laptop", "Desktop", "Printer", "Peripheral"],
    "Network": ["LAN", "Wi-Fi", "DNS", "VPN"],
    "Software": ["Application Error", "Installation", "Configuration", "Licensing"],
    "Email & Collaboration": ["Mailbox", "Calendar", "Teams", "Distribution List"],
    "Server & Infrastructure": ["Server Availability", "Storage", "Virtual Machine", "Backup"],
    "Security": ["Suspicious Activity", "Endpoint Protection", "Policy", "Phishing"],
}

services = [
    "Active Directory", "Corporate Network", "ERP", "Email & Collaboration",
    "File Services", "Service Desk", "Virtual Infrastructure",
    "Printing", "Endpoint Management", "Business Applications"
]
groups = ["Service Desk", "Infrastructure", "Network Team", "Systems Administration", "Application Support", "Cybersecurity"]
departments = ["Finance", "HR", "Procurement", "Engineering", "Operations", "Administration", "Project Management", "IT"]
locations = ["Head Office", "Site A", "Site B", "Remote", "Regional Office"]
priorities = ["P1", "P2", "P3", "P4"]
statuses = ["Closed", "Resolved", "In Progress", "Open"]
sla_targets = {"P1": 4, "P2": 8, "P3": 24, "P4": 48}
impact = {"P1": "Critical", "P2": "High", "P3": "Medium", "P4": "Low"}
root_causes = ["User Error", "Configuration", "Hardware Failure", "Network Issue", "Application Defect", "Access Control", "Capacity", "Unknown"]

start = datetime(2025, 1, 1, 8, 0)
rows = []

for i in range(1, ROWS + 1):
    created = start + timedelta(
        days=random.randint(0, 364),
        hours=random.randint(0, 10),
        minutes=random.randint(0, 59)
    )
    priority = random.choices(priorities, weights=[3, 12, 50, 35])[0]
    category = random.choice(list(categories))
    status = random.choices(statuses, weights=[52, 28, 13, 7])[0]
    base_hours = {"P1": 3.5, "P2": 5.5, "P3": 11, "P4": 18}[priority]
    resolution_hours = round(max(0.5, random.lognormvariate(math.log(base_hours), 0.65)), 1)
    if status in {"Open", "In Progress"}:
        resolution_hours = round(random.uniform(0.5, 18), 1)

    fcr = "Yes" if random.random() < {"P1": 0.15, "P2": 0.30, "P3": 0.62, "P4": 0.75}[priority] else "No"
    reopened = "Yes" if random.random() < (0.04 if fcr == "Yes" else 0.10) else "No"

    rows.append({
        "Incident ID": f"INC-{i:05d}",
        "Created Date": created.strftime("%Y-%m-%d"),
        "Created Time": created.strftime("%H:%M"),
        "Priority": priority,
        "Category": category,
        "Subcategory": random.choice(categories[category]),
        "Service": random.choice(services),
        "Assignment Group": random.choice(groups),
        "Department": random.choice(departments),
        "Location": random.choice(locations),
        "Status": status,
        "Resolution Hours": resolution_hours,
        "SLA Target Hours": sla_targets[priority],
        "SLA Met": "Yes" if resolution_hours <= sla_targets[priority] else "No",
        "First Contact Resolution": fcr,
        "Reopened": reopened,
        "Business Impact": impact[priority],
        "Root Cause Type": random.choice(root_causes),
    })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Created {ROWS} synthetic incidents at {OUTPUT}")