---
name: marketplace-agent-frontend-view
description: Build/update the static frontend viewer from latest.json by normalizing output into frontend/data/items-normalized.json and verifying frontend files for GitHub Pages.
version: 0.0.2
metadata:
  hermes:
    tags: [marketplace-agent, frontend, github-pages, ui]
---

# marketplace-agent frontend view

Use this skill to keep `frontend/` synced with the latest marketplace-agent results.

## Paths

- repo: user-provided path if given; otherwise locate clone first
- workspace: default `workspaces/default`
- latest output: `<workspace>/output/latest.json`
- frontend data: `frontend/data/items-normalized.json`

## Steps

1. Locate repo/workspace paths. Do not assume Hermes started from repo root.
2. Ensure `<workspace>/output/latest.json` exists. If missing, run:
   - `uv run marketplace-agent find <workspace>` (or `marketplace-agent find <workspace>`)
3. Normalize output:
   - `python3 frontend/scripts/normalize_latest_json.py --input <workspace>/output/latest.json --output frontend/data/items-normalized.json`
4. Verify frontend files exist:
   - `frontend/index.html`
   - `frontend/styles.css`
   - `frontend/app.js`
   - `frontend/data/items-normalized.json`
5. Summarize item count, output path, and frontend path.

## GitHub Pages

For static deploys, publish `frontend/` on GitHub Pages.

## Safety

- Do not auto-post listings.
- Do not commit private workspace data under `workspaces/`.
