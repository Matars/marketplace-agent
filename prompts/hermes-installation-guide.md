# Hermes installation guide for marketplace-agent

You are setting up marketplace-agent for the user. Follow this guide before improvising.

## Goal

Onboard the user, then turn their answers into a working marketplace-agent workspace.

Do not assume the user's marketplace goal, products, vendors, country, schedule, or output preference from this guide. Ask first.

## Repos and folders

Use these roles, not hardcoded personal paths:

- engine repo: local clone of `https://github.com/Matars/marketplace-agent`
- browser-harness: full upstream submodule at `<engine repo>/third_party/browser-harness`
- user workspace: gitignored folder inside the engine repo, defaulting to `<engine repo>/workspaces/default`, for personal config/output

Keep engine source and workspace data separate by path and gitignore. The engine repo is source code; the workspace is personal config/output and must not be committed.

## Setup steps before onboarding

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

## Onboarding questions

Ask these questions before creating the final config. Keep it compact; ask in one message when possible.

Required:

1. Are you using marketplace-agent to find things, sell things, or both?
2. What are you looking for or selling? Describe it naturally.
3. What country/region should marketplaces target?
4. Which marketplaces/vendors do you want to use? If unsure, ask whether Hermes should choose sensible real providers for the region.
5. Where should the workspace live? Offer `<engine repo>/workspaces/default` as the safe default unless the user asks for a different location.

Optional, ask if relevant:

6. Budget or price range?
7. New/used/refurbished preferences?
8. Location radius, shipping, or pickup preferences?
9. How often should this run, if recurring?
10. Desired output: local JSON/site, GitHub Pages, Discord summary, or just terminal summary?
11. For sell workflows: should Hermes only create listing drafts? Default is yes.

After the user answers, summarize the intended config briefly and proceed unless something is unclear.

## Provider selection

Use the vendors from onboarding. If the user asks Hermes to choose defaults, choose reasonable real marketplaces for the user's country and goal.

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

## Workspace creation and config

After onboarding:

1. Create or update the user workspace at `<engine repo>/workspaces/default` unless the user chose another location.
2. Configure `marketplace.toml` using real providers only.
3. Keep personal config and generated output in the gitignored workspace, not in tracked engine paths.

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
- Do not commit personal config, generated vendors, diagnostics, or output.
