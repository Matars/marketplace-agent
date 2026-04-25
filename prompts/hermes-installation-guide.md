# Hermes installation guide for marketplace-agent

You are setting up marketplace-agent for the user. Follow this guide before improvising.

## Goal

Turn the user's natural-language marketplace goal into a working marketplace-agent workspace.

The user's goal and preferred vendors must come from the user's prompt. Do not hardcode the example from this guide into their config.

Do not configure demo vendors unless the user explicitly asks for a dry-run placeholder.

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

## Provider selection

Use the vendors from the user's prompt. If the user asks Hermes to choose defaults, choose reasonable real marketplaces for the user's country and goal.

Examples only, not defaults:

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

If a provider plugin does not exist or fails, implement or repair it using the vendor-builder skill plus the full browser-harness submodule. For Amazon/eBay specifically, useful references are:

- Amazon reference: `third_party/browser-harness/domain-skills/amazon/product-search.md`
- eBay reference: `third_party/browser-harness/domain-skills/ebay/scraping.md`

If a vendor is blocked by login, captcha, anti-bot, or terms-sensitive behavior, stop and explain the issue before trying to bypass it.

## Convert user intent into product queries

Convert the user's own goal into concrete categories and queries. Prefer specific model names, brands, constraints, sizes, locations, or compatibility terms over vague keywords.

Template shape:

```toml
[[categories]]
name = "<short_category_name>"
queries = [
  "<specific product query 1>",
  "<specific product query 2>",
  "<specific product query 3>"
]
```

Fill this from the user's actual goal. Do not insert any default product preferences.

## Validation

After setup:

1. validate the workspace
2. run the requested workflow
3. inspect `<workspace>/output/latest.json` for find workflows, or the draft JSON for sell workflows
4. summarize:
   - engine repo path
   - workspace path
   - vendors configured
   - categories/queries configured
   - output path
   - item count or draft path
   - provider failures and next fix

## Safety

- Do not auto-post listings.
- Do not message sellers or buyers.
- Do not bypass captcha/login/anti-bot protections without explicit user approval.
- Do not put personal config in the engine repo.
