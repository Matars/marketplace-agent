# marketplace-agent

Marketplace automation toolkit: find second-hand deals now, draft sell listings next.

This is the v2 direction for the old deals-finder idea:

- `find` workflow: search vendors, normalize listings, score deals, publish dashboards/alerts.
- `sell` workflow: turn product photos/details into pricing research and listing drafts.
- vendor plugins declare capabilities instead of pretending every marketplace supports everything.
- Hermes is optional: the CLI should work standalone, while Hermes can generate/fix vendor plugins and interpret diagnostics.

## Important: engine repo vs user workspace

Do not clone this repo and edit it as your personal marketplace config.

Use this repo as the installable engine. Create your personal marketplace in a separate folder.
That keeps updates clean:

- engine updates happen in this repo/package
- your vendors, templates, config, output, and diagnostics live in your workspace
- pulling/upgrading the engine does not create conflicts with your personal config

## Normal user workflow

Install from GitHub with uv:

```bash
uv tool install git+https://github.com/Matars/marketplace-agent.git
```

Create a separate user workspace:

```bash
marketplace-agent init ~/my-marketplace --name "Home Deals" --country SE --currency SEK
cd ~/my-marketplace
marketplace-agent doctor .
marketplace-agent hermes context .
```

Upgrade later without touching your workspace:

```bash
uv tool install --force git+https://github.com/Matars/marketplace-agent.git
```

Your workspace looks like this:

```text
~/my-marketplace/
  marketplace.toml
  vendors/
  templates/
  output/
  .marketplace-agent/
    diagnostics/
```

## Contributor workflow

Clone this repo only if you want to develop the engine:

```bash
git clone https://github.com/Matars/marketplace-agent.git
cd marketplace-agent
uv sync
uv run pytest -q
```

For local testing from the repo, create a throwaway workspace outside the source tree:

```bash
uv run marketplace-agent init ~/tmp-marketplace --name "Test Market" --country SE --currency SEK
uv run marketplace-agent doctor ~/tmp-marketplace
uv run marketplace-agent hermes context ~/tmp-marketplace
```

If you accidentally initialize inside the repo, common workspace paths are gitignored.
Still prefer external folders.

## Current status

Initial scaffold only:

- Typer CLI
- Pydantic models
- vendor capability interface
- vendor registry
- `init` command for external user workspaces
- `doctor` command to validate a workspace
- `hermes context` command
- find pipeline stub
- sell draft service stub
- diagnostics bundle stub
- tests for the first behavior

## Design principles

1. Config over forks: users create small local workspaces, not modified copies of the engine.
2. Built-ins first: common vendors should ship as tested plugins.
3. Escape hatches: simple declarative vendors for easy sites, Python plugins for hard sites.
4. Safety by default: sell mode drafts listings; it does not auto-post without explicit approval.
5. Diagnostics over vibes: failed vendors should produce bundles Hermes or a human can inspect.
