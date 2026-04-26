# marketplace-agent

Marketplace automation toolkit for finding marketplace deals and drafting sell listings.

The intended UX is simple: copy the prompt below into Hermes. Hermes handles setup, asks you onboarding questions, creates your workspace, configures vendors/products, and runs the first workflow.

## First-time setup prompt

```text
Set up marketplace-agent for me.

Do this:
1. Clone or update https://github.com/Matars/marketplace-agent with submodules enabled.
2. Read the repo file prompts/hermes-installation-guide.md first.
3. Follow that guide exactly.
4. Start onboarding by asking me the required setup questions from the guide.
5. After I answer, create or update a gitignored workspace inside this repo at workspaces/default unless I ask for a different location.
6. Configure marketplace-agent from my answers.
7. Keep user-specific config, generated vendors, diagnostics, and output inside the gitignored workspace.
8. Use the bundled browser-harness submodule at third_party/browser-harness for vendor discovery/scraper repair.
9. If a provider plugin is missing or broken, use the repo vendor-builder and browser-harness skills to implement or repair it.
10. Run validation and the requested workflow from the guide.
11. Show me where the output JSON or draft JSON is and summarize what worked.
```

That is the first-time setup prompt. After marketplace-agent is already installed/configured, use the day-to-day prompts below.

## Day-to-day prompts

Copy one of these into Hermes when you already have a local clone and workspace.

### Find new deals

```text
Run marketplace-agent for me.

Use this repo and workspace:
- repo: ./
- workspace: workspaces/default

Do this:
1. Read prompts/hermes-installation-guide.md only for operating rules; do not redo first-time onboarding unless required config is missing.
2. Read the relevant repo skills under hermes/skills/.
3. Run validation for the workspace.
4. Run the find workflow.
5. Inspect workspaces/default/output/latest.json.
6. Summarize the best results, provider failures, and exact next command I should run.
```

### Change what I am looking for

```text
Update my marketplace-agent search.

Use this repo and workspace:
- repo: ./
- workspace: workspaces/default

New goal:
<describe what you want to find now>

Do this:
1. Read prompts/hermes-installation-guide.md and hermes/skills/marketplace-agent-workspace.md.
2. Update marketplace.toml in the workspace only.
3. Keep existing useful vendor config unless it conflicts with the new goal.
4. Validate the workspace.
5. Run the find workflow and inspect output/latest.json.
6. Summarize what changed and what results were found.
```

### Add or repair a marketplace/vendor

```text
Add or repair a marketplace-agent vendor.

Use this repo and workspace:
- repo: ./
- workspace: workspaces/default

Vendor/site:
<marketplace name or URL>

Do this:
1. Read hermes/skills/marketplace-agent-vendor-builder.md and hermes/skills/marketplace-agent-browser-harness.md.
2. Use third_party/browser-harness for discovery if needed.
3. Implement or repair the provider plugin.
4. Keep personal config/output inside the gitignored workspace.
5. Run tests or validation for the changed provider.
6. Run marketplace-agent against the workspace and summarize what works.
```

### Draft a sell listing

```text
Create a sell-listing draft with marketplace-agent.

Use this repo and workspace:
- repo: ./
- workspace: workspaces/default

Item to sell:
<describe the item, condition, price idea, photos/info available>

Do this:
1. Read hermes/skills/marketplace-agent-sell-draft.md.
2. Create draft JSON only; do not post, message buyers, or bypass login/captcha.
3. Put outputs inside the gitignored workspace.
4. Show me the draft path and summarize what still needs my approval.
```

## What Hermes should read

The full onboarding/installation/orchestration guide is here:

```text
prompts/hermes-installation-guide.md
```

Supporting repo skills:

```text
hermes/skills/marketplace-agent-workspace.md
hermes/skills/marketplace-agent-vendor-builder.md
hermes/skills/marketplace-agent-browser-harness.md
hermes/skills/marketplace-agent-sell-draft.md
```

Browser-harness is included as a full upstream submodule:

```text
third_party/browser-harness/
```

## Security: audit with AI before installing

Before running or installing this project, audit it.

This repo is open source, including the Hermes prompts, skills, and bundled browser-harness submodule, so you can inspect everything before trusting it.

Recommended process:

1. Clone this repo with submodules.
2. Point your AI coding tool at the full source tree (Cursor, Claude Code, Codex, etc.).
3. Ask it:

```text
Analyze this repository for security vulnerabilities, malware, spyware, data exfiltration risks, prompt/skill abuse paths, and any suspicious behavior. Review all code, prompts, skills, scripts, and submodules.
```

4. Read the report and review flagged files yourself before use.

You should do this for every extension/tool you install. Most are closed source and cannot be fully audited; this one can.

## Current status

Prototype.

The project has the CLI/workspace foundation and Hermes prompt/skill workflow. Amazon and eBay vendor plugins are implemented and work out of the box.
