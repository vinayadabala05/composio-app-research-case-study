"""
Sample research agent for Composio-style app toolkit research.

This is a practical sketch, not a full production system.
It demonstrates:
  - structured schema
  - fetch + extract loop
  - confidence / needs_human flags
  - writing results for the case study

For the full 100 apps, plug in a stronger LLM + better page discovery
and keep the same schema + verification loop.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Install deps: pip install -r requirements.txt")
    raise

SAMPLE_APPS = [
    {"name": "Stripe", "hint": "https://docs.stripe.com/api", "category": "Finance and Fintech"},
    {"name": "GitHub", "hint": "https://docs.github.com/rest", "category": "Developer, Infra and Data platforms"},
    {"name": "HubSpot", "hint": "https://developers.hubspot.com/docs/api/intro-to-auth", "category": "CRM and Sales"},
    {"name": "Slack", "hint": "https://api.slack.com/", "category": "Communications and Messaging"},
    {"name": "Notion", "hint": "https://developers.notion.com/", "category": "Productivity and Project Management"},
]

def fetch_text(url: str, timeout: int = 15) -> str:
    try:
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "ComposioResearchAgent/0.1 (assignment)"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        text = " ".join(soup.get_text(" ").split())
        return text[:12000]
    except Exception as e:
        return f"[FETCH_ERROR] {e}"

def heuristic_extract(name: str, category: str, hint: str, page_text: str) -> dict[str, Any]:
    text_l = page_text.lower()
    auth = []
    if "oauth" in text_l:
        auth.append("OAuth2")
    if "api key" in text_l or "api_key" in text_l or "secret key" in text_l:
        auth.append("API key")
    if "bearer" in text_l and "API key" not in auth:
        auth.append("Bearer token")
    if not auth:
        auth = ["unknown"]

    gated_signals = ["contact sales", "partner", "apply for access", "enterprise only", "request access"]
    self_serve_signals = ["get your api key", "create an app", "developer account", "sign up free", "dashboard"]
    gated_hits = sum(1 for s in gated_signals if s in text_l)
    self_hits = sum(1 for s in self_serve_signals if s in text_l)

    if gated_hits > self_hits and gated_hits > 0:
        self_serve, confidence = "no", 0.6
    elif self_hits > 0:
        self_serve, confidence = "yes", 0.75
    else:
        self_serve, confidence = "partial", 0.45

    mcp = "unknown"
    if "mcp" in text_l and ("server" in text_l or "model context" in text_l):
        mcp = "possible"
    if name.lower() == "github":
        mcp = "official"

    buildable = "yes" if self_serve == "yes" else ("conditional" if self_serve == "partial" else "no")
    blocker = None if self_serve == "yes" else "Access may require paid plan, review, or partnership — verify on official docs"
    needs_human = confidence < 0.7 or self_serve != "yes"

    return {
        "name": name,
        "category": category,
        "one_liner": f"{name} – see official docs for product description",
        "auth_methods": auth,
        "self_serve": self_serve,
        "api_surface": "Public developer docs present" if "FETCH_ERROR" not in page_text else "Docs fetch failed",
        "mcp": mcp,
        "buildable_today": buildable,
        "main_blocker": blocker,
        "evidence_urls": [hint],
        "confidence": confidence,
        "needs_human": needs_human,
        "raw_note": "Heuristic sample extractor — replace with LLM for production research",
    }

def main() -> None:
    results = []
    for app in SAMPLE_APPS:
        print(f"Researching {app['name']} ...")
        text = fetch_text(app["hint"])
        row = heuristic_extract(app["name"], app["category"], app["hint"], text)
        results.append(row)
        print(f"  → self_serve={row['self_serve']}  conf={row['confidence']}  needs_human={row['needs_human']}")

    out = Path(__file__).resolve().parent.parent / "data" / "sample_results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nWrote {len(results)} rows → {out}")

if __name__ == "__main__":
    main()
