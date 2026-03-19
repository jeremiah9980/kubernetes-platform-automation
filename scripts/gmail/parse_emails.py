from __future__ import annotations

import csv
from pathlib import Path

from scripts.utils.common import DATA_DIR, OUTPUTS_DIR

INPUT = DATA_DIR / "gmail" / "emails.txt"
OUTPUT = OUTPUTS_DIR / "csv" / "action_items_extracted.csv"
KEYWORDS = ("due", "action", "deadline", "respond", "reply", "school", "legal", "payment")


def main() -> None:
    if not INPUT.exists():
        raise SystemExit(f"Input file not found: {INPUT}")

    lines = INPUT.read_text(encoding="utf-8").splitlines()
    actions = []
    for line in lines:
        lower = line.lower()
        if any(k in lower for k in KEYWORDS):
            actions.append([line.strip()])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Action Items"])
        writer.writerows(actions)

    print(f"Extracted {len(actions)} action items to {OUTPUT}")


if __name__ == "__main__":
    main()
