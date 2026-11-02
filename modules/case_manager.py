
from datetime import datetime
import uuid
import pandas as pd


def create_case(title, investigator, description=""):
    """Create a new investigation case."""

    case = {
        "case_id": f"FRQ-{uuid.uuid4().hex[:8].upper()}",
        "title": title,
        "investigator": investigator,
        "description": description,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Open"
    }

    return case


def get_case_summary(case):
    """Return a formatted case summary."""

    return {
        "Case ID": case["case_id"],
        "Case Title": case["title"],
        "Investigator": case["investigator"],
        "Description": case["description"],
        "Created At": case["created_at"],
        "Status": case["status"]
    }


def update_case_status(case, new_status):
    """Update the investigation status."""

    allowed_statuses = ["Open", "Under Review", "Closed"]

    if new_status not in allowed_statuses:
        raise ValueError("Invalid case status.")

    case["status"] = new_status
    return case


def export_case_details(case):
    """Convert case details into a downloadable CSV."""

    summary = get_case_summary(case)
    return pd.DataFrame([summary]).to_csv(index=False).encode("utf-8")
