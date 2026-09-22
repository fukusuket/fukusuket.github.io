#!/usr/bin/env python3
"""Render index.html from the daily ioc_stats CSVs under yyyy/mm/.

Reads the last week of CSVs written by ThreatfeedCollector (--no-misp),
dedupes articles on their URL and groups them by publication date.
Standard library only.
"""

import csv
import html
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_GLOB = "[0-9][0-9][0-9][0-9]/[0-9][0-9]/ioc_stats_*.csv"
FILE_DATE = re.compile(r"ioc_stats_(\d{8})\.csv$")
WINDOW_DAYS = 7


def dated_csv_files():
    """Newest first, limited to the week ending at the newest file."""
    found = []
    for path in ROOT.glob(CSV_GLOB):
        match = FILE_DATE.search(path.name)
        if not match:
            continue
        try:
            found.append((datetime.strptime(match.group(1), "%Y%m%d").date(), path))
        except ValueError:
            continue
    if not found:
        return []
    found.sort(key=lambda item: item[0], reverse=True)
    cutoff = found[0][0] - timedelta(days=WINDOW_DAYS - 1)
    return [path for day, path in found if day >= cutoff]


def read_articles(paths):
    """Dedupe on url, newest file winning."""
    articles = {}
    for path in paths:
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                url = (row.get("blog url") or "").strip()
                title = (row.get("title") or "").strip()
                if not url or not title or url in articles:
                    continue
                articles[url] = {
                    "date": (row.get("date") or "").strip() or "unknown",
                    "vendor": (row.get("vendor") or "").strip(),
                    "title": title,
                    "url": url,
                }
    return list(articles.values())


def group_by_date(articles):
    groups = {}
    for article in articles:
        groups.setdefault(article["date"], []).append(article)
    for items in groups.values():
        items.sort(key=lambda a: (a["vendor"].lower(), a["title"].lower()))
    return sorted(groups.items(), key=lambda item: item[0], reverse=True)


STYLE = """\
:root {
  color-scheme: light dark;
  --bg: #ffffff;
  --fg: #1a1a1a;
  --muted: #6b7280;
  --rule: #e5e7eb;
  --link: #1d4ed8;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #101214;
    --fg: #e8e8e8;
    --muted: #9099a6;
    --rule: #262b31;
    --link: #7ba7ff;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  padding: 3rem clamp(1rem, 4vw, 4rem) 5rem;
  background: var(--bg);
  color: var(--fg);
  font-family: "Inter", ui-sans-serif, system-ui, -apple-system,
    "Segoe UI", Helvetica, Arial, sans-serif;
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}
main { width: 100%; margin: 0 auto; }
h1 { font-size: 1.5rem; font-weight: 650; letter-spacing: -0.01em; margin: 0; }
.meta { color: var(--muted); font-size: 0.85rem; margin: 0.35rem 0 2.75rem; }
h2 {
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-variant-numeric: tabular-nums;
  color: var(--muted);
  margin: 2.5rem 0 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--rule);
}
ul { list-style: none; margin: 0; padding: 0; }
li { padding: 0.45rem 0; }
a { color: var(--link); text-decoration: none; }
a:hover { text-decoration: underline; }
.vendor {
  display: block;
  color: var(--muted);
  font-size: 0.78rem;
  letter-spacing: 0.01em;
}
.empty { color: var(--muted); }
footer {
  margin-top: 4rem;
  padding-top: 1rem;
  border-top: 1px solid var(--rule);
  color: var(--muted);
  font-size: 0.78rem;
}
"""


def render(groups, total):
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    parts = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>neko-tanuki-furoshiki feed</title>",
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        "family=Inter:wght@400..700&amp;display=swap\">",
        f"<style>\n{STYLE}</style>",
        "</head>",
        "<body>",
        "<main>",
        "<h1>neko-tanuki-furoshiki feed</h1>",
        f'<p class="meta">Last {WINDOW_DAYS} days &middot; {total} articles '
        f"&middot; updated {generated}</p>",
    ]
    if not groups:
        parts.append('<p class="empty">No articles collected yet.</p>')
    for date, items in groups:
        parts.append("<section>")
        parts.append(f"<h2>{html.escape(date)}</h2>")
        parts.append("<ul>")
        for article in items:
            parts.append(
                "<li>"
                f'<a href="{html.escape(article["url"], quote=True)}" '
                f'target="_blank" rel="noopener noreferrer">'
                f'{html.escape(article["title"])}</a>'
                f'<span class="vendor">{html.escape(article["vendor"])}</span>'
                "</li>"
            )
        parts.append("</ul>")
        parts.append("</section>")
    parts += [
        '<footer>Collected with '
        '<a href="https://github.com/fukusuket/ThreatfeedCollector" '
        'target="_blank" rel="noopener noreferrer">ThreatfeedCollector</a>.'
        "</footer>",
        "</main>",
        "</body>",
        "</html>",
        "",
    ]
    return "\n".join(parts)


def main():
    paths = dated_csv_files()
    articles = read_articles(paths)
    groups = group_by_date(articles)
    (ROOT / "index.html").write_text(render(groups, len(articles)), encoding="utf-8")
    print(f"index.html: {len(articles)} articles from {len(paths)} CSV file(s)")


if __name__ == "__main__":
    main()
