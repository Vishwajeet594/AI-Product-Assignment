# Agent-readiness research: 100 requested apps

This is a reproducible, evidence-first research pipeline and a single-file case study.

## Quick start

```powershell
python -m pip install -r requirements.txt
python run.py --demo                   # deterministic, cited snapshot used by the page
python run.py --live                   # fetches all 100 linked public sources + critic/verifier pass
python -m http.server 8080 -d site     # open http://localhost:8080
```

`--demo` produces a carefully labeled baseline from `seed/apps.json` and maintained research rules. `--live` fetches the linked official sources, records resolved URL/status/title/excerpt, critiques field support independently, and re-fetches flagged rows. It needs no API key. A production extension can add search/LLM extraction, but must retain the captured source and the critic trace.

## Pipeline

1. **Researcher** finds an official developer/auth page and returns structured JSON with a short supporting quote.
2. **Critic** rejects claims whose evidence does not support the claimed field.
3. **Browser verifier** re-fetches low-confidence/gated rows and records a source snapshot.
4. **Manual audit** is stratified by category and outcome; `agent/audit.py` scores auth, access, API surface, and verdict separately.

The published page is a static, self-contained snapshot. It distinguishes (a) initial source-agnostic baseline, (b) cited final dataset, and (c) executed fetch/critic/verifier artifacts. Fetch status is not semantic proof: 403/JS-only pages remain in the flagged queue. No credentials or paid accounts are assumed.

## Sources and limitations

Every row links to a primary docs, developer, public API, or official product page. “No public API” means no documented API was found in the linked official source at the snapshot date—not that an internal endpoint cannot exist. MCP is conservative: only explicitly confirmed official entries are marked; community and unverified paths are excluded.

## Deployment

Deploy the `site/` directory unchanged to GitHub Pages, Netlify, or Vercel. No build step or server is required.
