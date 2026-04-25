# Hermes installation guide for marketplace-agent

You are setting up marketplace-agent for the user. Follow this guide before improvising.

## Goal

Turn a natural-language marketplace goal into a working marketplace-agent workspace.

Example goal:

> I want to find GPUs that can run Qwen locally.

The default real providers should be Amazon and eBay. Do not configure demo vendors unless the user explicitly asks for a dry-run placeholder.

## Repos and folders

Use these roles, not hardcoded personal paths:

- engine repo: local clone of `https://github.com/Matars/marketplace-agent`
- browser-harness: full upstream submodule at `<engine repo>/third_party/browser-harness`
- user workspace: a separate folder outside the engine repo for personal config/output

Keep engine/workspace separate. The engine repo is source code. The workspace is personal config/output.

## Setup steps

1. Clone or update the engine repo with submodules enabled.
2. Use `uv` for all Python/project commands. Do not use pip directly.
3. Ensure the full browser-harness submodule exists at `third_party/browser-harness`. If missing, initialize submodules.
4. Read these repo skill files:
   - `hermes/skills/marketplace-agent-workspace.md`
   - `hermes/skills/marketplace-agent-vendor-builder.md`
   - `hermes/skills/marketplace-agent-browser-harness.md`
   - `hermes/skills/marketplace-agent-sell-draft.md`
5. Read browser-harness files from the full submodule when vendor discovery/scraper repair is needed:
   - `third_party/browser-harness/SKILL.md`
   - `third_party/browser-harness/install.md`
   - `third_party/browser-harness/domain-skills/amazon/product-search.md`
   - `third_party/browser-harness/domain-skills/ebay/scraping.md`
6. Install or run the marketplace-agent CLI from the engine repo.
7. Create or update the user workspace outside the engine repo.
8. Configure `marketplace.toml` using real providers only.

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

If Amazon/eBay plugins do not exist or fail, implement or repair them using the vendor-builder skill plus the full browser-harness submodule. Use:

- Amazon reference: `third_party/browser-harness/domain-skills/amazon/product-search.md`
- eBay reference: `third_party/browser-harness/domain-skills/ebay/scraping.md`

If a vendor is blocked by login, captcha, anti-bot, or terms-sensitive behavior, stop and explain the issue before trying to bypass it.

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
3. inspect `<workspace>/output/latest.json`
4. summarize:
   - engine repo path
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
