# marketplace-agent

Marketplace automation toolkit for finding marketplace deals and drafting sell listings.

The intended UX is simple: audit the repo, install the native Hermes skills once, then use `/marketplace-agent-...` for setup and day-to-day workflows.

## Security: audit with AI before installing

Before running or installing this project, audit it.

This repo is open source, including the Hermes prompts, skills, and bundled browser-harness submodule, so you can inspect everything before trusting it.

Recommended process:

1. Clone this repo with submodules.
2. Point Hermes or your AI coding tool at the full source tree (Hermes, Claude Code, Codex, etc.).
3. Ask it:

```text
Analyze this repository for security vulnerabilities, malware, spyware, data exfiltration risks, prompt/skill abuse paths, and any suspicious behavior. Review all code, prompts, skills, scripts, and submodules.
```

4. Read the report and review flagged files yourself before use.

You should do this for every extension/tool you install.

## Install native Hermes skills

The repo includes native Hermes skills under `skills/`. Install them once so they are available through `/<skill-name>` in day-to-day Hermes sessions.

```bash
hermes skills tap add Matars/marketplace-agent
hermes skills install Matars/marketplace-agent/skills/marketplace-agent-setup --yes
hermes skills install Matars/marketplace-agent/skills/marketplace-agent-workspace --yes --force
hermes skills install Matars/marketplace-agent/skills/marketplace-agent-find-deals --yes --force
hermes skills install Matars/marketplace-agent/skills/marketplace-agent-update-search --yes
hermes skills install Matars/marketplace-agent/skills/marketplace-agent-vendor-repair --yes
hermes skills install Matars/marketplace-agent/skills/marketplace-agent-sell-draft --yes
hermes skills install Matars/marketplace-agent/skills/marketplace-agent-frontend-view --yes --force
```

Why `--force` for some skills?

`marketplace-agent-workspace`, `marketplace-agent-find-deals`, and `marketplace-agent-frontend-view` include runnable command examples like `uv run ...` / `python3 ...`. Hermes Hub can flag those as `supply_chain` CAUTION for community skills and block by default. In this repo those commands are intentional and required for normal operation, so `--force` is used to explicitly trust and install them.


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

Copy this into Hermes. Hermes will ask the setup questions it needs; you do not need to edit the prompt first.

```text
/marketplace-agent-setup

Set up marketplace-agent for me.
```

The setup skill clones/updates the repo, initializes `workspaces/default`, configures vendors/searches, validates the workspace, and runs the first workflow.

## Day-to-day skills

Use these after marketplace-agent is already installed/configured. Copy them as-is. If Hermes needs the repo path, workspace path, vendor name, search brief, or item details, it will ask.

### Find new deals

```text
/marketplace-agent-find-deals

Run the normal find workflow and summarize the best results.
```

### Change what I am looking for

```text
/marketplace-agent-update-search

Update what marketplace-agent searches for.
```

### Add or repair a marketplace/vendor

```text
/marketplace-agent-vendor-repair

Add or repair a marketplace/vendor.
```

### Draft a sell listing

```text
/marketplace-agent-sell-draft

Create a sell-listing draft.
```

### Refresh frontend data

```text
/marketplace-agent-frontend-view

Refresh frontend data from latest.json and verify frontend files.
```

## Frontend viewer (universal latest.json parser)

This repo now includes a static frontend in `frontend/` that can always render deal results from `latest.json`.

Flow:

1. Run the find workflow to generate/update `workspaces/default/output/latest.json`.
2. Normalize that file for UI rendering.
3. Open or publish the static frontend.

Normalize command:

```bash
python3 frontend/scripts/normalize_latest_json.py \
  --input workspaces/default/output/latest.json \
  --output frontend/data/items-normalized.json
```

Then view:

- local: open `frontend/index.html` (or serve the repo with any static server)
- GitHub Pages: publish the `frontend/` folder

Frontend files:

```text
frontend/index.html
frontend/styles.css
frontend/app.js
frontend/data/items-normalized.json
frontend/scripts/normalize_latest_json.py
frontend/README.md
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
skills/marketplace-agent-frontend-view/SKILL.md
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
