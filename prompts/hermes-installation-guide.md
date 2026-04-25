# Hermes installation guide for marketplace-agent

You are setting up marketplace-agent for the user. Follow this guide before improvising.

## Goal

Turn a natural-language marketplace goal into a working marketplace-agent workspace.

Example goal:

> I want to find GPUs that can run Qwen locally.

The default real providers should be Amazon and eBay. Do not configure demo vendors unless the user explicitly asks for a dry-run placeholder.

## Repos and folders

Use these locations by default:

- engine repo: `~/fafo/marketplace-agent`
- user workspace: `~/my-marketplace`

Keep those separate. The engine repo is source code. The workspace is personal config/output.

## Setup steps

1. Clone or update the engine repo from `https://github.com/Matars/marketplace-agent` into `~/fafo/marketplace-agent`.
2. Use `uv` for all Python/project commands. Do not use pip directly.
3. Read these repo skill files:
   - `~/fafo/marketplace-agent/hermes/skills/marketplace-agent-workspace.md`
   - `~/fafo/marketplace-agent/hermes/skills/marketplace-agent-vendor-builder.md`
   - `~/fafo/marketplace-agent/hermes/skills/marketplace-agent-sell-draft.md`
4. Install or run the CLI from the repo.
5. Create or update the user workspace at `~/my-marketplace`.
6. Configure `marketplace.toml` using real providers only.

## Default find providers

Desired defaults:

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

If Amazon/eBay plugins do not exist or fail, implement or repair them using the vendor-builder skill. If a vendor is blocked by login, captcha, anti-bot, or terms-sensitive behavior, stop and explain the issue before trying to bypass it.

## Convert user intent into product queries

For “GPUs that can run Qwen locally”, configure something like:

```toml
[[categories]]
name = "local_ai_gpu"
queries = [
  "rtx 3090 24gb",
  "rtx 4090 24gb",
  "rtx 4080 super 16gb",
  "rtx 4070 ti super 16gb",
  "rtx a4000 16gb",
  "rtx a5000 24gb",
  "rtx a6000 48gb",
  "tesla p40 24gb"
]
```

Prefer concrete models and VRAM terms. Avoid vague queries like just `gpu`.

## Validation

After setup:

1. validate the workspace
2. run the find workflow
3. inspect `~/my-marketplace/output/latest.json`
4. summarize:
   - workspace path
   - vendors configured
   - categories/queries configured
   - output path
   - item count
   - provider failures and next fix

## Safety

- Do not auto-post listings.
- Do not message sellers or buyers.
- Do not bypass captcha/login/anti-bot protections without explicit user approval.
- Do not put personal config in the engine repo.
