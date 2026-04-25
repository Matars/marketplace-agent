---
name: marketplace-agent-workspace
category: marketplace-agent
description: Configure marketplace-agent user workspaces from natural-language shopping goals. Install/update the CLI, create workspace config, translate intent into categories/queries, run find, and inspect output.
---

# marketplace-agent workspace

Use this skill when a user wants Hermes to set up or configure marketplace-agent.

## Core rule

Keep the engine package and the user workspace separate.

- Engine: local clone of `https://github.com/Matars/marketplace-agent`
- Workspace: user config/data folder outside the engine repo

Do not ask the user to edit the engine repo for personal vendors/products.

## Install/update

Use `uv` for Python/project commands. Do not use pip directly.

If working from a local clone during development:

```bash
uv sync
uv run pytest -q
```

## Create workspace

Create a user workspace outside the engine repo. If the workspace exists, edit `marketplace.toml` instead of overwriting unless the user explicitly asks.

## Convert user intent to categories

Turn the user's own goal into concrete product/category queries.

Guidelines:

- Prefer concrete product names/models over vague terms.
- Include important constraints from the user: size, location, compatibility, budget, condition, brand, platform, etc.
- If the user's request is broad, create multiple focused categories.
- Do not copy examples into the config unless they match the user's actual goal.

Example only:

```toml
[[categories]]
name = "example_category"
queries = ["specific product 1", "specific product 2"]
```

## Vendors

Use the vendors requested by the user. If the user asks Hermes to choose, pick sensible real providers for the user's country and goal.

Do not configure demo vendors unless the user explicitly asks for a dry-run placeholder. If a requested vendor plugin does not exist, use marketplace-agent-vendor-builder to create it.

## Run and verify

After configuration:

```bash
marketplace-agent doctor <workspace>
marketplace-agent find <workspace>
python3 -m json.tool <workspace>/output/latest.json
```

Success means:

- command exits 0
- `output/latest.json` exists
- JSON includes title, url, source, category, price/currency when available

## Hermes context

```bash
marketplace-agent hermes context <workspace>
```

Use that output in summaries and future tasks so Hermes does not re-ask basic setup questions.
