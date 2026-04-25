# marketplace-agent

Marketplace automation toolkit: find second-hand deals now, draft sell listings next.

This is the fresh v2 direction for the old deals-finder idea:

- `find` workflow: search vendors, normalize listings, score deals, publish dashboards/alerts.
- `sell` workflow: turn product photos/details into pricing research and listing drafts.
- vendor plugins declare capabilities instead of pretending every marketplace supports everything.
- Hermes is optional: the CLI should work standalone, while Hermes can generate/fix vendor plugins and interpret diagnostics.

## Quick start

```bash
uv sync
uv run marketplace-agent init ./my-marketplace --name "Home Deals" --country SE --currency SEK
uv run marketplace-agent hermes context ./my-marketplace
uv run pytest -q
```

## Current status

Initial scaffold only:

- Typer CLI
- Pydantic models
- vendor capability interface
- vendor registry
- `init` command
- `hermes context` command
- tests for the first behavior

## Design principles

1. Config over forks: users create small local projects, not modified copies of the engine.
2. Built-ins first: common vendors should ship as tested plugins.
3. Escape hatches: simple declarative vendors for easy sites, Python plugins for hard sites.
4. Safety by default: sell mode drafts listings; it does not auto-post without explicit approval.
5. Diagnostics over vibes: failed vendors should produce bundles Hermes or a human can inspect.
