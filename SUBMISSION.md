# Submission – AI Product Ops Intern (Composio)

**Candidate:** Vinay Adabala  
**Email:** vinayadabala2005@gmail.com  
**GitHub:** https://github.com/vinayadabala05  
**Repo:** https://github.com/vinayadabala05/composio-app-research-case-study  

## Links for reviewers

| Item | URL |
|------|-----|
| **Live case study (HTML)** | https://htmlpreview.github.io/?https://github.com/vinayadabala05/composio-app-research-case-study/blob/main/index.html |
| **Source repository** | https://github.com/vinayadabala05/composio-app-research-case-study |
| **GitHub Pages** (after enabling) | https://vinayadabala05.github.io/composio-app-research-case-study/ |

Open `index.html` first — it is designed to be self-explanatory in about two minutes.

## What is included

1. **index.html** – Single-page case study: headline patterns, agent design, sample matrix, verification, takeaways.
2. **data/verified_sample.json** – 20 apps researched with evidence URLs (auth, self-serve, API, MCP, buildability).
3. **data/apps_100.json** – Full 100-app seed list across 10 categories.
4. **agent/** – Sample research pipeline (schema + runner) that can be extended to all 100.
5. **README.md** – How to run the agent and honesty notes.

## How to review quickly

1. Open the live HTML link above.
2. Read **Headline patterns**.
3. Skim the verified sample table and verification section.
4. Optionally clone the repo and run `agent/run_sample.py`.

## Notes

- Research used public documentation only.
- Where an app is gated (paid / partner / review), that is reported as the correct finding.
- Accuracy was improved with a human verification loop on a stratified sample of 20 apps.
- Patterns (auth dominance, self-serve vs gated by category, main blockers, easy wins) are the primary output, not a raw 100-row dump.

Thank you for reviewing.
