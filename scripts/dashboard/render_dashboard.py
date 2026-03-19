from __future__ import annotations

from html import escape

from scripts.utils.common import DASHBOARD_DIR, OUTPUTS_DIR, read_json

TODAY_INPUT = OUTPUTS_DIR / "dashboard" / "today.json"
MASTER_INPUT = OUTPUTS_DIR / "dashboard" / "master_tasks.json"
HTML_OUTPUT = DASHBOARD_DIR / "index.html"


def render_items(items: list[dict]) -> str:
    if not items:
        return "<p>No items.</p>"
    rows = []
    for item in items:
        rows.append(
            f"<div class='card'>"
            f"<h3>{escape(item.get('title', 'Untitled'))}</h3>"
            f"<p><strong>Source:</strong> {escape(item.get('source', ''))} | <strong>Priority:</strong> {escape(item.get('priority', ''))} | <strong>Status:</strong> {escape(item.get('status', ''))}</p>"
            f"<p><strong>Next:</strong> {escape(item.get('next_action', ''))}</p>"
            f"<p><strong>Linked:</strong> {escape(item.get('linked_item', ''))}</p>"
            f"</div>"
        )
    return "\n".join(rows)


def main() -> None:
    today = read_json(TODAY_INPUT, default={})
    master = read_json(MASTER_INPUT, default=[])

    html = f"""<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>JC-OS Unified Dashboard</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; background: #f5f7fb; color: #222; }}
    h1, h2 {{ margin-bottom: 8px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; }}
    .panel {{ background: white; padding: 16px; border-radius: 14px; box-shadow: 0 2px 10px rgba(0,0,0,.08); }}
    .card {{ border: 1px solid #e5e7eb; padding: 12px; border-radius: 10px; margin: 10px 0; background: #fff; }}
    .muted {{ color: #666; font-size: 0.95rem; }}
  </style>
</head>
<body>
  <h1>JC-OS Unified Dashboard</h1>
  <p class='muted'>One view for Jira, Gmail action items, manual capture, and project execution.</p>
  <div class='grid'>
    <section class='panel'>
      <h2>Today's Top 5</h2>
      {render_items(today.get('top5', []))}
    </section>
    <section class='panel'>
      <h2>Quick Wins</h2>
      {render_items(today.get('quick_wins', []))}
    </section>
    <section class='panel'>
      <h2>Deep Work</h2>
      {render_items(today.get('deep_work', []))}
    </section>
    <section class='panel'>
      <h2>Blocked</h2>
      {render_items(today.get('blocked', []))}
    </section>
    <section class='panel'>
      <h2>Waiting</h2>
      {render_items(today.get('waiting', []))}
    </section>
    <section class='panel'>
      <h2>All Tasks</h2>
      {render_items(master)}
    </section>
  </div>
</body>
</html>
"""
    HTML_OUTPUT.write_text(html, encoding="utf-8")
    print(f"Wrote dashboard to {HTML_OUTPUT}")


if __name__ == "__main__":
    main()
