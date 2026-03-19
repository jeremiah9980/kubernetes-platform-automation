from __future__ import annotations

import csv
from pathlib import Path

from scripts.utils.common import DATA_DIR, OUTPUTS_DIR, read_json

INPUT = DATA_DIR / "jira" / "issues.json"
OUTPUT = OUTPUTS_DIR / "jira" / "jira_summary.csv"


def main() -> None:
    data = read_json(INPUT, default={"issues": []})
    issues = data.get("issues", [])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Key", "Summary", "Status", "Priority", "Due Date"])
        for issue in issues:
            fields = issue.get("fields", {})
            writer.writerow([
                issue.get("key", ""),
                fields.get("summary", ""),
                fields.get("status", {}).get("name", ""),
                fields.get("priority", {}).get("name", ""),
                fields.get("duedate", ""),
            ])

    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
