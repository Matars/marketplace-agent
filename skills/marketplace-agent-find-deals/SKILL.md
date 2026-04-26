---
name: marketplace-agent-find-deals
description: Day-to-day marketplace-agent run. Validate an existing workspace, run the find workflow, inspect output/latest.json, and summarize best results and provider failures.
version: 0.0.2
metadata:
  hermes:
    tags: [marketplace-agent, deals, marketplace, daily]
---

# marketplace-agent find deals

Use this skill when marketplace-agent is already installed/configured and the user wants to run the normal find workflow.

## Inputs to infer or ask once

- repo path: user-provided path if given; otherwise locate the clone before assuming the current directory is the repo root
- workspace path: default `workspaces/default` relative to the repo

Do not redo first-time onboarding unless required config is missing. If the repo/workspace cannot be located, ask one concise question for the missing path instead of guessing.

## Steps

1. Locate the repo and workspace. Do not assume Hermes was started from the repo root.
2. Read repo docs only as needed for operating rules:
   - `prompts/hermes-installation-guide.md`
   - `skills/marketplace-agent-workspace/SKILL.md` or `hermes/skills/marketplace-agent-workspace.md`
3. Validate the workspace:
   - prefer `uv run marketplace-agent doctor <workspace>` from the repo when working from source
   - otherwise use `marketplace-agent doctor <workspace>`
4. Run the find workflow:
   - prefer `uv run marketplace-agent find <workspace>` from the repo
   - otherwise use `marketplace-agent find <workspace>`
5. Inspect `<workspace>/output/latest.json`.
6. Normalize latest output for frontend rendering:
   - `python3 frontend/scripts/normalize_latest_json.py --input <workspace>/output/latest.json --output frontend/data/items-normalized.json`
7. Summarize:
   - strongest results first
   - prices/currency/location when available
   - source/vendor and URL
   - provider failures or zero-result categories
   - output path and frontend path (`frontend/data/items-normalized.json`)
   - exact next command to rerun or adjust the search brief

## Safety / quality

- Do not modify workspace config unless the user asks.
- Do not commit workspace output.
- If a provider is broken, recommend the vendor repair skill instead of silently ignoring it.
