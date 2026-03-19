from __future__ import annotations

from scripts.utils.common import OUTPUTS_DIR, read_json, write_json

MASTER_INPUT = OUTPUTS_DIR / "dashboard" / "master_tasks.json"
TODAY_OUTPUT = OUTPUTS_DIR / "dashboard" / "today.json"


def main() -> None:
    tasks = read_json(MASTER_INPUT, default=[])
    top5 = tasks[:5]
    quick_wins = [t for t in tasks if t.get("score", 0) >= 5][:5]
    deep_work = [t for t in tasks if t.get("category") in {"work", "project"}][:5]
    blocked = [t for t in tasks if t.get("status") == "blocked"]
    waiting = [t for t in tasks if t.get("status") == "waiting"]

    payload = {
        "top5": top5,
        "quick_wins": quick_wins,
        "deep_work": deep_work,
        "blocked": blocked,
        "waiting": waiting,
    }
    write_json(TODAY_OUTPUT, payload)
    print(f"Wrote daily summary to {TODAY_OUTPUT}")


if __name__ == "__main__":
    main()
