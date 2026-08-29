"""
Generate synthetic Shop Drawings Log data for the "Ahmed Mostafa" portfolio demo project.
All data (building names, drawing numbers, titles) is randomly generated and does NOT
reflect any real project data. Structure (columns) mirrors a typical Shop Drawings Log
used in construction document control.
"""

import json
import random
from datetime import datetime, timedelta

random.seed(42)  # reproducible output

# ---------------------------------------------------------------------------
# Config - generic, non-identifying project name
# ---------------------------------------------------------------------------
PROJECT_NAME = "Ahmed Mostafa"

TRADES = [
    "Civil",
    "Architectural",
    "Structural",
    "Electrical",
    "Mechanical",
    "Survey",
]

# Generic building naming (no real facility names)
BUILDING_TYPES = [
    "Administration Building", "Pump Station", "Control Room", "Warehouse",
    "Workshop", "Guard House", "Substation", "Storage Tank Area",
    "Process Building", "Utility Building", "Laboratory", "Gate House",
]

def generate_building_names(n=48):
    names = []
    counters = {}
    for i in range(n):
        btype = BUILDING_TYPES[i % len(BUILDING_TYPES)]
        counters[btype] = counters.get(btype, 0) + 1
        suffix = f" {counters[btype]}" if counters[btype] > 1 else ""
        names.append(f"{btype}{suffix}")
    return names

BUILDINGS = generate_building_names(48)

TRADE_CODE = {
    "Civil": "CIV",
    "Architectural": "ARC",
    "Structural": "STR",
    "Electrical": "ELE",
    "Mechanical": "MEC",
    "Survey": "SUR",
}

TITLE_TEMPLATES = {
    "Civil": ["Site Grading Plan", "Foundation Layout", "Drainage Plan", "Road Layout Plan", "Earthworks Section"],
    "Architectural": ["Floor Plan", "Roof Plan", "Elevation - North", "Elevation - South", "Door & Window Schedule"],
    "Structural": ["Column Layout", "Beam Reinforcement Detail", "Slab Reinforcement Plan", "Foundation Detail", "Steel Connection Detail"],
    "Electrical": ["Lighting Layout", "Power Distribution Layout", "Cable Routing Plan", "Single Line Diagram", "Earthing Layout"],
    "Mechanical": ["HVAC Layout", "Piping Layout", "Equipment Layout", "Ventilation Plan", "Pump Installation Detail"],
    "Survey": ["Topographic Survey", "As-Built Survey", "Setting Out Plan", "Benchmark Location Plan", "Levels Survey"],
}

# Approval codes used in typical shop drawing workflows
# Code C (Rejected / Revise & Resubmit) is EXCLUDED from the demo dataset,
# matching the real project's filtering logic.
APPROVAL_CODES = {
    "A": "Approved",
    "B": "Approved as Noted",
    # "C": "Rejected"  -> excluded intentionally
}

STATUS_OPTIONS = ["Approved", "Closed", "Approved as Noted"]

def random_date(start_year=2023, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def generate_drawings(target_total=3400, target_approved=2400):
    rows = []
    seq_counter = {}

    # First generate the "approved/closed" portion
    for i in range(target_approved):
        building = random.choice(BUILDINGS)
        trade = random.choice(TRADES)
        code = TRADE_CODE[trade]
        key = f"{building}-{code}"
        seq_counter[key] = seq_counter.get(key, 0) + 1
        seq = seq_counter[key]

        drawing_number = f"{PROJECT_NAME.replace(' ', '')}-{code}-{seq:04d}"
        title = f"{random.choice(TITLE_TEMPLATES[trade])} - {building}"
        approval_code = random.choice(list(APPROVAL_CODES.keys()))
        status = "Closed" if random.random() < 0.4 else APPROVAL_CODES[approval_code]

        rows.append({
            "Building": building,
            "Trade": trade,
            "Drawing Number": drawing_number,
            "Title": title,
            "Approval Code": approval_code,
            "Status": status,
            "Submission Date": random_date().strftime("%Y-%m-%d"),
        })

    # Remaining drawings: mix of statuses OTHER than the excluded "C" (rejected)
    remaining = target_total - target_approved
    other_statuses = ["Under Review", "Pending Submission", "Submitted"]
    for i in range(remaining):
        building = random.choice(BUILDINGS)
        trade = random.choice(TRADES)
        code = TRADE_CODE[trade]
        key = f"{building}-{code}"
        seq_counter[key] = seq_counter.get(key, 0) + 1
        seq = seq_counter[key]

        drawing_number = f"{PROJECT_NAME.replace(' ', '')}-{code}-{seq:04d}"
        title = f"{random.choice(TITLE_TEMPLATES[trade])} - {building}"

        rows.append({
            "Building": building,
            "Trade": trade,
            "Drawing Number": drawing_number,
            "Title": title,
            "Approval Code": "-",
            "Status": random.choice(other_statuses),
            "Submission Date": random_date().strftime("%Y-%m-%d"),
        })

    random.shuffle(rows)
    return rows

if __name__ == "__main__":
    data = generate_drawings()
    print(f"Generated {len(data)} synthetic drawing records.")
    print(f"Approved/Closed: {sum(1 for r in data if r['Status'] in ('Approved', 'Closed', 'Approved as Noted'))}")

    with open("demo_drawings_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Saved: demo_drawings_data.json")
