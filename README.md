# marketplace-agent

Marketplace automation toolkit for finding marketplace deals and drafting sell listings.

The intended UX is simple: audit the repo, install the native Hermes skills once, then use `/skill marketplace-agent-...` for setup and day-to-day workflows.

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

## Install native Hermes skills

The repo includes native Hermes skills under `skills/`. Install them once so they are available through `/skill ...` in day-to-day Hermes sessions.

```bash
hermes skills tap add Matars/marketplace-agent
hermes skills install Matars/marketplace-agent/skills/marketplace-agent-setup --yes
hermes skills install Matars/marketplace-agent/skills/marketplace-agent-workspace --yes
hermes skills install Matars/marketplace-agent/skills/marketplace-agent-find-deals --yes
hermes skills install Matars/marketplace-agent/skills/marketplace-agent-update-search --yes
hermes skills install Matars/marketplace-agent/skills/marketplace-agent-vendor-repair --yes
hermes skills install Matars/marketplace-agent/skills/marketplace-agent-sell-draft --yes
```

After that, keep skills updated with:

```bash
hermes skills update
```

Do not manually copy these skills into `~/.hermes/skills`; installing from the GitHub repo preserves update metadata.

### What about browser-harness?

You do not need to install a separate third-party Hermes skill for normal marketplace-agent use.

`browser-harness` is included as a git submodule at `third_party/browser-harness/`, and the marketplace-agent skills read/use that local submodule when vendor discovery or scraper repair is needed.

The important part is cloning/updating with submodules enabled:

```bash
git clone --recurse-submodules https://github.com/Matars/marketplace-agent
# or, in an existing clone:
git submodule update --init --recursive
```

Only install a separate upstream browser-harness skill if you want to use browser-harness directly outside marketplace-agent.

## First-time setup

In Hermes, load the setup skill and describe what you want to find or sell:

```text
/skill marketplace-agent-setup

Set up marketplace-agent for me.

Search/selling brief:
<what you want to find or sell, what counts as a good result, and any deal-breakers>
```

The setup skill clones/updates the repo, initializes `workspaces/default`, configures vendors/searches, validates the workspace, and runs the first workflow.

## Day-to-day skills

Use these after marketplace-agent is already installed/configured. Replace `<path-to-marketplace-agent>` with the actual clone path if Hermes was not started from the repo root.

### Find new deals

```text
/skill marketplace-agent-find-deals

Use repo <path-to-marketplace-agent> and workspace workspaces/default.
Run the normal find workflow and summarize the best results.
```

### Change what I am looking for

```text
/skill marketplace-agent-update-search

Use repo <path-to-marketplace-agent> and workspace workspaces/default.

New search brief:
<what you want to find now, what counts as a good result, and any deal-breakers>
```

### Add or repair a marketplace/vendor

```text
/skill marketplace-agent-vendor-repair

Use repo <path-to-marketplace-agent> and workspace workspaces/default.
Vendor/site: <marketplace name or URL>
```

### Draft a sell listing

```text
/skill marketplace-agent-sell-draft

Use repo <path-to-marketplace-agent> and workspace workspaces/default.
Item to sell: <item, condition, price idea, photos/info available>
```

## What Hermes should read

The full onboarding/installation/orchestration guide is here:

```text
prompts/hermes-installation-guide.md
```

Native Hermes skills live here and can be installed with `hermes skills install`:

```text
skills/marketplace-agent-setup/SKILL.md
skills/marketplace-agent-workspace/SKILL.md
skills/marketplace-agent-find-deals/SKILL.md
skills/marketplace-agent-update-search/SKILL.md
skills/marketplace-agent-vendor-repair/SKILL.md
skills/marketplace-agent-sell-draft/SKILL.md
```

Legacy repo prompt support files are also kept here:

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

## Current status

Prototype.

The project has the CLI/workspace foundation and Hermes prompt/skill workflow. Amazon and eBay vendor plugins are implemented and work out of the box.
