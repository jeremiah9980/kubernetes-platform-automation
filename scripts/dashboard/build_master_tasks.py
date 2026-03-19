from __future__ import annotations

import csv
import uuid
from pathlib import Path

from scripts.utils.common import DATA_DIR, OUTPUTS_DIR, read_json, write_json

JIRA_INPUT = DATA_DIR / "jira" / "issues.json"
GMAIL_INPUT = DATA_DIR / "gmail" / "action_items.csv"
CAPTURE_OUTPUT = OUTPUTS_DIR / "dashboard" / "capture_tasks.json"
MASTER_OUTPUT = OUTPUTS_DIR / "dashboard" / "master_tasks.json"

PRIORITY_MAP = {
    "highest": "critical",
    "high": "high",
    "medium": "medium",
    "low": "low",
    "lowest": "low",
}


def normalize_jira() -> list[dict]:
    data = read_json(JIRA_INPUT, default={"issues": []})
    tasks = []
    for issue in data.get("issues", []):
        fields = issue.get("fields", {})
        status_name = fields.get("status", {}).get("name", "To Do")
        status_norm = "blocked" if "block" in status_name.lower() else ("active" if status_name.lower() in {"in progress", "doing"} else "new")
        priority_name = fields.get("priority", {}).get("name", "medium").lower()
        tasks.append({
            "id": issue.get("key", f"JIRA-{uuid.uuid4().hex[:8]}"),
            "source": "jira",
            "category": "work",
            "title": fields.get("summary", "Untitled Jira issue"),
            "details": fields.get("description", ""),
            "status": status_norm,
            "priority": PRIORITY_MAP.get(priority_name, "medium"),
            "due_date": fields.get("duedate", ""),
            "next_action": f"Review and advance {issue.get('key', 'ticket')}",
            "owner": "Jeremiah",
            "tags": fields.get("labels", []),
            "linked_item": issue.get("key", ""),
            "notes": status_name,
        })
    return tasks


def normalize_gmail() -> list[dict]:
    if not GMAIL_INPUT.exists():
        return []
    tasks = []
    with GMAIL_INPUT.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tags = [t.strip() for t in row.get("tags", "").split(";") if t.strip()]
            tasks.append({
                "id": row.get("id") or f"GMAIL-{uuid.uuid4().hex[:8]}",
                "source": row.get("source", "gmail"),
                "category": row.get("category", "personal"),
                "title": row.get("title", "Untitled Gmail task"),
                "details": row.get("details", ""),
                "status": row.get("status", "new"),
                "priority": row.get("priority", "medium"),
                "due_date": row.get("due_date", ""),
                "next_action": row.get("next_action", "Review and act"),
                "owner": row.get("owner", "Jeremiah"),
                "tags": tags,
                "linked_item": row.get("linked_item", ""),
                "notes": row.get("notes", ""),
            })
    return tasks


def normalize_capture() -> list[dict]:
    return read_json(CAPTURE_OUTPUT, default=[])


def score(task: dict) -> int:
    score_value = 0
    priority = task.get("priority", "medium")
    if priority == "critical":
        score_value += 10
    elif priority == "high":
        score_value += 7
    elif priority == "medium":
        score_value += 4
    else:
        score_value += 1

    category = task.get("category", "")
    if category == "legal":
        score_value += 8
    if category == "family":
        score_value += 8
    if task.get("source") == "jira":
        score_value += 3
    if task.get("status") == "blocked":
        score_value += 2
    if task.get("next_action"):
        score_value += 1
    return score_value


def main() -> None:
    tasks = normalize_jira() + normalize_gmail() + normalize_capture()
    for task in tasks:
        task["score"] = score(task)

    tasks.sort(key=lambda x: x.get("score", 0), reverse=True)
    write_json(MASTER_OUTPUT, tasks)
    print(f"Wrote {len(tasks)} normalized tasks to {MASTER_OUTPUT}")


if __name__ == "__main__":
    main()
