---
name: marketplace-agent-workspace
category: marketplace-agent
description: Configure marketplace-agent user workspaces from natural-language shopping goals. Install/update the CLI, create workspace config, translate intent into categories/queries, run find, and inspect output.
---

# marketplace-agent workspace

Use this skill when a user wants Hermes to set up or configure marketplace-agent.

## Core rule

Keep the engine package and the user workspace separate.

- Engine: installed from `git+https://github.com/Matars/marketplace-agent.git`
- Workspace: user config/data folder such as `~/my-marketplace`

Do not ask the user to edit the engine repo for personal vendors/products.

## Install/update

```bash
uv tool install --force git+https://github.com/Matars/marketplace-agent.git
```

If working from a local clone during development:

```bash
cd ~/fafo/marketplace-agent
uv sync
uv run pytest -q
```

## Create workspace

```bash
marketplace-agent init ~/my-marketplace --name "Home Deals" --country SE --currency SEK
marketplace-agent doctor ~/my-marketplace
```

If the workspace exists, edit `marketplace.toml` instead of overwriting unless the user explicitly asks.

## Convert user intent to categories

Take goals like "GPUs that can run Qwen locally" and turn them into concrete product queries.

Example for local LLM GPUs:

```toml
[[categories]]
name = "local_ai_gpu"
queries = [
  "rtx 3090",
  "rtx 4090",
  "rtx 4080 super",
  "rtx 4070 ti super",
  "rtx a4000",
  "rtx a5000",
  "rtx a6000",
  "tesla p40",
  "nvidia 24gb"
]
```

Prefer concrete model names over vague terms. Add comments or notes when a recommendation is capability-based, e.g. 24GB VRAM preferred for larger local models.

## Vendors

Default real vendors are Amazon and eBay:

```toml
[[vendors]]
name = "amazon"
type = "amazon"
enabled = true

[[vendors]]
name = "ebay"
type = "ebay"
enabled = true
```

Do not configure demo vendors unless the user explicitly asks for a dry-run placeholder. If a requested vendor plugin does not exist, use marketplace-agent-vendor-builder to create it.

## Run and verify

```bash
marketplace-agent doctor ~/my-marketplace
marketplace-agent find ~/my-marketplace
python3 -m json.tool ~/my-marketplace/output/latest.json
```

Success means:

- command exits 0
- `output/latest.json` exists
- item count matches configured vendor/query behavior
- JSON includes title, url, source, category, price/currency when available

## Hermes context

```bash
marketplace-agent hermes context ~/my-marketplace
```

Use that output in summaries and future tasks so Hermes does not re-ask basic setup questions.
