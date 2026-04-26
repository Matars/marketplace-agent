---
name: marketplace-agent-update-search
description: Update an existing marketplace-agent workspace from a new search brief, preserving useful vendor config, validating, running find, and summarizing changes/results.
version: 0.0.2
metadata:
  hermes:
    tags: [marketplace-agent, search, config, marketplace]
---

# marketplace-agent update search

Use this skill when the user wants to change what marketplace-agent searches for.

## Default paths

- repo: user-provided path if given; otherwise locate the clone before assuming the current directory is the repo root
- workspace: `workspaces/default` relative to the repo
- config: `<workspace>/marketplace.toml`

## Ask for a search brief if missing

If the new search brief is missing, ask the user for it instead of requiring them to edit the copied prompt. Ask for:

- what they want to find now
- what counts as a good result
- deal-breakers: budget, condition, location, shipping/pickup, brands/models, exclusions
- country/region if it changed
- vendors/marketplaces if they changed

## Steps

1. Locate the repo and workspace. Do not assume Hermes was started from the repo root.
2. Read the current workspace config.
3. Convert the new search brief into concrete categories and queries.
4. Update `marketplace.toml` in the workspace only.
5. Preserve existing useful vendor config unless it conflicts with the new brief.
6. Do not edit tracked source files unless the user asks for new built-in provider code.
7. Validate the workspace.
8. Run the find workflow.
9. Inspect `<workspace>/output/latest.json`.
10. Normalize latest output for frontend rendering:
   - `python3 frontend/scripts/normalize_latest_json.py --input <workspace>/output/latest.json --output frontend/data/items-normalized.json`
11. Summarize:
   - what changed in config
   - configured vendors
   - categories/queries
   - best results
   - provider failures or missing provider work
   - frontend output path (`frontend/data/items-normalized.json`)

## Quality rules

- Prefer specific product/model queries over broad vague keywords.
- Include constraints and deal-breakers explicitly.
- Do not invent the user's preferences.
