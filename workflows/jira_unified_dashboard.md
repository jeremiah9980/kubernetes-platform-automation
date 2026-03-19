# Jira + Command Center Unified Flow

1. Pull Jira tickets into `data/jira/issues.json`
2. Maintain or import Gmail actions into `data/gmail/action_items.csv`
3. Capture raw notes into `data/capture/inbox.txt`
4. Build normalized master tasks with `scripts/dashboard/build_master_tasks.py`
5. Generate today's prioritized board with `scripts/dashboard/generate_today.py`
6. Render `dashboard/index.html` with `scripts/dashboard/render_dashboard.py`
7. Use prompt files in `prompts/` to get ChatGPT prioritization, Jira comment drafts, and end-of-day wrap-ups
