from __future__ import annotations

import json
from pathlib import Path
import requests

from scripts.utils.common import DATA_DIR, env

JIRA_URL = env("JIRA_URL")
EMAIL = env("JIRA_EMAIL")
API_TOKEN = env("JIRA_API_TOKEN")
JQL = env("JIRA_JQL", "assignee = currentUser() AND status != Done ORDER BY priority DESC")
OUTPUT = DATA_DIR / "jira" / "issues.json"


def main() -> None:
    if not (JIRA_URL and EMAIL and API_TOKEN):
        raise SystemExit("Set JIRA_URL, JIRA_EMAIL, and JIRA_API_TOKEN environment variables first.")

    url = f"{JIRA_URL.rstrip('/')}/rest/api/3/search"
    headers = {"Accept": "application/json"}
    auth = (EMAIL, API_TOKEN)

    response = requests.get(url, headers=headers, params={"jql": JQL}, auth=auth, timeout=30)
    response.raise_for_status()
    data = response.json()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Jira issues pulled to {OUTPUT}")


if __name__ == "__main__":
    main()
