---
name: marketplace-agent-setup
description: First-time setup for marketplace-agent. Clone/update the repo, initialize the gitignored workspace, configure vendors/searches from the user's brief, validate, and run the first workflow.
version: 0.0.2
metadata:
  hermes:
    tags: [marketplace-agent, setup, onboarding, marketplace]
---

# marketplace-agent setup

Use this skill for first-time marketplace-agent setup or when the workspace is missing required configuration.

## Default paths

- repo: user-provided path if given; otherwise locate the clone before assuming the current directory is the repo root
- workspace: `workspaces/default` inside the repo unless the user gives another path
- browser-harness: `third_party/browser-harness/`

Keep user config, generated vendors, diagnostics, and output inside the gitignored workspace. Do not commit personal workspace data.

## Steps

1. Locate the repo path. Do not assume Hermes was started from the repo root. If no repo path is provided, check whether the current directory is the repo; otherwise look for a local clone or ask one concise question.
2. Clone or update `https://github.com/Matars/marketplace-agent` with submodules enabled if the repo is not present.
3. Read repo operating docs if present:
   - `prompts/hermes-installation-guide.md`
   - `skills/marketplace-agent-workspace/SKILL.md` or `hermes/skills/marketplace-agent-workspace.md`
   - `skills/marketplace-agent-vendor-repair/SKILL.md` or `hermes/skills/marketplace-agent-vendor-builder.md`
   - `skills/marketplace-agent-sell-draft/SKILL.md` or `hermes/skills/marketplace-agent-sell-draft.md`
4. Ask compact onboarding questions before final config. Do not require the user to include these in the copied prompt:
   - find, sell, or both?
   - what should be found or sold?
   - what counts as a good result?
   - deal-breakers: budget, condition, location, shipping/pickup, brands/models, exclusions?
   - country/region?
   - preferred marketplaces/vendors, or should Hermes choose sensible real providers?
5. Create/update the workspace at `workspaces/default` unless the user asks otherwise.
6. Configure `marketplace.toml` from the user's search/selling brief.
7. Use real providers only. Do not configure demo vendors unless explicitly requested.
8. If a requested vendor is missing or broken, use the marketplace-agent vendor repair skill.
9. Run validation, then the requested workflow.
10. Inspect output (`output/latest.json` for find workflows, draft JSON for sell workflows).
11. Summarize repo path, workspace path, vendors, categories/queries, output path, what worked, and what failed.

## Safety

- Do not auto-post listings.
- Do not message sellers or buyers.
- Do not bypass login/captcha/anti-bot protections without explicit approval.
