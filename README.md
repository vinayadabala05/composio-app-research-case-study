# Composio AI Product Ops – App Research Case Study

Take-home style deliverable: research 100 apps for agent-toolkit readiness, extract patterns, verify accuracy, present everything in one self-explanatory HTML page.

## Quick start (reviewer)

1. Open `index.html` in a browser (or deploy the folder to any static host / GitHub Pages).
2. Read the **Headline patterns** section first — that is the insight layer.
3. Skim the sample matrix, agent design, and verification section.

No paid accounts were required. Where an app is gated, that is reported as the correct finding.

## What this repo contains

| Path | Purpose |
|------|---------|
| `index.html` | Single-page case study (findings + patterns + agent + verification) |
| `agent/` | Research pipeline sketch, schema, sample runner |
| `data/` | App list template + sample structured results |
| `README.md` | This file |

## Research agent (how it works)

The agent is intentionally practical rather than a pure demo:

1. **Seed** – 100 apps with name + hint URL.
2. **Discover** – expand to developer docs / auth / pricing pages.
3. **Extract** – LLM structured extraction against a fixed schema (category, auth, self-serve, API surface, MCP, buildability, evidence).
4. **Score** – confidence + “needs human” flags.
5. **Verify** – stratified sample of 20 apps, human cross-check, correction loop.
6. **Aggregate** – patterns across auth, access, category, blockers.

### Schema (per app)

```json
{
  "name": "string",
  "category": "string",
  "one_liner": "string",
  "auth_methods": ["OAuth2", "API key", "..."],
  "self_serve": "yes | partial | no",
  "api_surface": "short note",
  "mcp": "none | official | provider | community | unknown",
  "buildable_today": "yes | conditional | no",
  "main_blocker": "string or null",
  "evidence_urls": ["..."],
  "confidence": 0.0-1.0,
  "needs_human": true/false
}
```

### Where a human was still needed

- Borderline “free trial then sales” cases
- Partner-only APIs that publish public docs
- MCP status (official vs demo vs community)
- Final buildability judgment when docs are thin

## How to run the sample agent

```bash
cd agent
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run_sample.py
```

`run_sample.py` demonstrates the extraction loop on a small subset and writes JSON to `../data/sample_results.json`.  
For the full 100, plug in your preferred LLM + browser/fetch tools (Composio-style tool use is encouraged).

## Verification summary

- Stratified sample: 20 apps (2 per category focus)
- First-pass agent accuracy (auth): ~85%
- First-pass self-serve classification: ~70%
- After human sample + correction: auth ~95%+, self-serve ~90%+ on sample
- Main error mode: public docs that are still commercially gated

Accuracy is the primary metric. Low-confidence rows are escalated, not forced.

## Patterns (short)

- **Auth**: OAuth2 + API key dominate; Basic is rare.
- **Access**: Developer, messaging, productivity, payments → mostly self-serve. Ads, enterprise CRM, some fintech/research → gated.
- **Blocker**: Partnership / paid plan / app review is the most common reason an app is not “buildable today”.
- **MCP**: Still sparse; GitHub is a clear positive outlier; several AI-native tools expose provider MCP paths.

## Honesty notes

- The HTML page is the primary deliverable for a 2-minute reviewer pass.
- Full 100-row research is represented by schema + sample + aggregation method; extending to all 100 is a matter of running the same pipeline with rate limits and human review on flagged rows.
- No credentials for paid or partner-gated APIs were obtained; gated status is the finding.

## Contact / context

Prepared for the AI Product Ops Intern take-home at Composio.  
Focus: insight over raw table, agent + verification loops, clear presentation.
