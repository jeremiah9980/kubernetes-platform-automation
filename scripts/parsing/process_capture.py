from __future__ import annotations

import uuid
from pathlib import Path

from scripts.utils.common import DATA_DIR, OUTPUTS_DIR, read_json, write_json

INPUT = DATA_DIR / "capture" / "inbox.txt"
OUTPUT = OUTPUTS_DIR / "dashboard" / "capture_tasks.json"


def infer_category(text: str) -> str:
    lower = text.lower()
    if "coach" in lower or "school" in lower or "kid" in lower:
        return "family"
    if "legal" in lower or "court" in lower:
        return "legal"
    if "jira" in lower or "ticket" in lower:
        return "work"
    return "project"


def main() -> None:
    if not INPUT.exists():
        raise SystemExit(f"Input file not found: {INPUT}")

    tasks = []
    for raw in INPUT.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        tasks.append({
            "id": f"MANUAL-{uuid.uuid4().hex[:8]}",
            "source": "manual",
            "category": infer_category(line),
            "title": line[:80],
            "details": line,
            "status": "new",
            "priority": "medium",
            "due_date": "",
            "next_action": line,
            "owner": "Jeremiah",
            "tags": ["capture"],
            "linked_item": "",
            "notes": "Generated from capture inbox",
        })

    write_json(OUTPUT, tasks)
    print(f"Wrote {len(tasks)} capture tasks to {OUTPUT}")


if __name__ == "__main__":
    main()
