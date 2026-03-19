# JC-OS v3 Unified Dashboard

A practical personal operating system that merges Jira work, Gmail action items, family/admin tasks, projects, and quick-capture notes into one daily command center.

## What this repo includes
- Jira ingestion starter scripts
- Gmail action item CSV intake
- Manual capture intake
- Master task normalization into a shared JSON schema
- Daily summary generator
- Simple HTML dashboard renderer
- Prompt library for ChatGPT-assisted prioritization and updates

## Repo layout
- `data/` raw inputs
- `outputs/` generated artifacts
- `scripts/` Python utilities and pipelines
- `dashboard/` static HTML dashboard
- `prompts/` reusable ChatGPT prompts
- `templates/` starter templates
- `automation/` placeholders for schedulers and future integrations

## Quick start
1. Create a Python virtual environment.
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Populate sample or real data:
   - `data/jira/issues.json`
   - `data/gmail/action_items.csv`
   - `data/capture/inbox.txt`
4. Build the unified task list:
   ```bash
   python scripts/dashboard/build_master_tasks.py
   ```
5. Generate today's summary:
   ```bash
   python scripts/dashboard/generate_today.py
   ```
6. Render the dashboard:
   ```bash
   python scripts/dashboard/render_dashboard.py
   ```
7. Open `dashboard/index.html` in your browser.

## Optional Jira setup
Set these environment variables before using Jira scripts:
- `JIRA_URL`
- `JIRA_EMAIL`
- `JIRA_API_TOKEN`
- `JIRA_JQL` (optional)
- `JIRA_PROJECT_KEY` (for ticket creation)

## Unified task schema
All sources normalize into this structure:
```json
{
  "id": "unique-id",
  "source": "jira|gmail|manual|legal|school|project",
  "category": "work|personal|family|legal|project",
  "title": "Short title",
  "details": "Longer description",
  "status": "new|active|blocked|waiting|done",
  "priority": "critical|high|medium|low",
  "due_date": "2026-03-18",
  "next_action": "Specific next step",
  "owner": "Jeremiah",
  "tags": ["jira", "vmware", "school"],
  "linked_item": "TM-1234",
  "notes": "Extra context"
}
```

## Notes
This starter repo is designed to be practical first: Python + JSON/CSV + static HTML. You can later evolve it into Flask, React, or a SQLite-backed app.
