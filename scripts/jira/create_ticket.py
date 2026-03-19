from __future__ import annotations

import json
import sys
import requests

from scripts.utils.common import env

JIRA_URL = env("JIRA_URL")
EMAIL = env("JIRA_EMAIL")
API_TOKEN = env("JIRA_API_TOKEN")
PROJECT_KEY = env("JIRA_PROJECT_KEY")


def create_ticket(summary: str, description: str, issue_type: str = "Task") -> dict:
    if not (JIRA_URL and EMAIL and API_TOKEN and PROJECT_KEY):
        raise SystemExit("Set JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN, and JIRA_PROJECT_KEY first.")

    url = f"{JIRA_URL.rstrip('/')}/rest/api/3/issue"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    auth = (EMAIL, API_TOKEN)
    payload = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
        }
    }
    response = requests.post(url, headers=headers, auth=auth, data=json.dumps(payload), timeout=30)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit("Usage: python scripts/jira/create_ticket.py \"Summary\" \"Description\"")
    result = create_ticket(sys.argv[1], sys.argv[2])
    print(json.dumps(result, indent=2))
