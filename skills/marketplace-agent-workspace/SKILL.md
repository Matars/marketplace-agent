---
name: marketplace-agent-workspace
description: Configure marketplace-agent user workspaces from natural-language search/selling briefs. Create/update marketplace.toml, preserve gitignored workspace data, validate, run find, and inspect output.
version: 0.0.2
metadata:
  hermes:
    tags: [marketplace-agent, workspace, config, marketplace]
---

# marketplace-agent workspace

Use this skill when configuring or updating a marketplace-agent workspace.

## Core rule

Keep engine source and user workspace data separate by path and gitignore.

- Engine: local clone of `https://github.com/Matars/marketplace-agent`
- Workspace: gitignored user config/data folder inside the repo, defaulting to `workspaces/default`

Do not edit tracked source files for personal vendors/products unless the user explicitly asks for reusable provider code.

## Locate paths first

Do not assume Hermes was started from the repo root.

If the user gives a repo path, use it. Otherwise check whether the current directory is the marketplace-agent repo; if not, look for a local clone or ask one concise question.

## Install/update

Use `uv` for Python/project commands. Do not use pip directly.

If working from a local clone during development:

```bash
uv sync
uv run pytest -q
```

## Onboarding/config questions

Do not invent what the user wants to find/sell or which vendors to use. Ask compact questions before creating final config; do not require the user to include these details in the copied prompt:

1. Find, sell, or both?
2. What are they looking for/selling?
3. What counts as a good result?
4. Deal-breakers: budget, condition, location, shipping/pickup, brands/models, exclusions?
5. Country/region?
6. Preferred marketplaces/vendors, or should Hermes choose real providers?
7. Workspace location, with `workspaces/default` as the safe default?

## Create/update workspace

Create a gitignored user workspace at `workspaces/default` unless the user asks for a different location. If the workspace exists, edit `marketplace.toml` instead of overwriting unless explicitly asked.

## Convert search/selling brief to categories

Turn the user's brief into concrete product/category queries.

Guidelines:

- Prefer concrete product names/models over vague terms.
- Include constraints: size, location, compatibility, budget, condition, brand, platform, exclusions.
- If the request is broad, create multiple focused categories.
- Do not copy examples into config unless they match the user's actual brief.

Example only:

```toml
[[categories]]
name = "example_category"
queries = ["specific product 1", "specific product 2"]
```

## Vendors

Use requested vendors. If the user asks Hermes to choose, pick sensible real providers for the user's country and request.

If a requested vendor plugin does not exist, use `marketplace-agent-vendor-repair`.

## Run and verify

From the repo, prefer:

```bash
uv run marketplace-agent doctor <workspace>
uv run marketplace-agent find <workspace>
python3 -m json.tool <workspace>/output/latest.json
```

Success means:

- command exits 0
- `output/latest.json` exists for find workflows
- JSON includes title, url, source, category, price/currency when available

## Hermes context

If available, run:

```bash
uv run marketplace-agent hermes context <workspace>
```

Use that output in summaries and future tasks so Hermes does not re-ask basic setup questions.
