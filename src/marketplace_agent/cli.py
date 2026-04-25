from __future__ import annotations

import json
import tomllib
from datetime import datetime, timezone
from pathlib import Path

import typer
from rich.console import Console

from marketplace_agent.config import MarketplaceConfig
from marketplace_agent.models import Item
from marketplace_agent.vendors.base import Vendor
from marketplace_agent.vendors.builtins.amazon import AmazonVendor
from marketplace_agent.vendors.builtins.ebay import EBayVendor
from marketplace_agent.vendors.builtins.blocket import BlocketVendor

app = typer.Typer(help="Marketplace automation: find deals now, draft listings later.")
hermes_app = typer.Typer(help="Generate Hermes-friendly context and task prompts.")
hermes_prompt_app = typer.Typer(help="Generate copy-paste prompts for Hermes workflows.")
hermes_app.add_typer(hermes_prompt_app, name="prompt")
app.add_typer(hermes_app, name="hermes")
console = Console()

BUILTIN_VENDORS: dict[str, type[Vendor]] = {
    "amazon": AmazonVendor,
    "ebay": EBayVendor,
    "blocket": BlocketVendor,
}


def _config_text(name: str, country: str, currency: str) -> str:
    return f'''# marketplace-agent workspace config
# This file belongs in a user workspace, not in the engine repository.

name = "{name}"

[user]
country = "{country}"
currency = "{currency}"
language = "en"

[schedule]
cron = ""
timezone = "Europe/Stockholm"

[find]
enabled = true

# Amazon and eBay are the default real providers.
[[vendors]]
name = "amazon"
type = "amazon"
enabled = true

[[vendors]]
name = "ebay"
type = "ebay"
enabled = true

# Products/categories to search for. Add your own queries here.
[[categories]]
name = "tech"
queries = ["rtx 3060", "steam deck", "sony wh-1000xm4"]

[sell]
enabled = true
# Safety default: generate drafts only. Do not post without explicit approval.
auto_post = false
'''


def _workspace_readme(name: str) -> str:
    return f"""# {name}

Local marketplace-agent workspace.

This folder is your personal config/data area. Keep it separate from the
`marketplace-agent` engine repository so tool updates do not conflict with your
vendors, templates, diagnostics, or generated output.

Useful commands:

```bash
marketplace-agent doctor .
marketplace-agent find .
marketplace-agent hermes context .
```

Edit `marketplace.toml` to change vendors and product queries.
"""


def _load_config(project: Path) -> MarketplaceConfig:
    config_path = project / "marketplace.toml"
    if not config_path.exists():
        raise typer.BadParameter(f"missing marketplace.toml in {project}")
    raw = tomllib.loads(config_path.read_text(encoding="utf-8"))
    return MarketplaceConfig.model_validate(raw)


def _enabled_vendors(config: MarketplaceConfig) -> list[Vendor]:
    vendors: list[Vendor] = []
    for vendor_config in config.vendors:
        if not vendor_config.enabled:
            continue
        vendor_cls = BUILTIN_VENDORS.get(vendor_config.type)
        if vendor_cls is None:
            raise typer.BadParameter(
                f"unknown vendor type '{vendor_config.type}' for vendor '{vendor_config.name}'. "
                f"Available built-ins: {', '.join(sorted(BUILTIN_VENDORS))}"
            )
        vendors.append(vendor_cls())
    return vendors


def _item_to_json(item: Item) -> dict:
    return item.model_dump(mode="json")


def _find_prompt(workspace: Path, goal: str, country: str, vendors: str, repo: Path) -> str:
    vendor_list = [v.strip() for v in vendors.split(",") if v.strip()]
    vendor_text = ", ".join(vendor_list) if vendor_list else "choose suitable vendors"
    repo = repo.resolve()
    return f"""You are configuring marketplace-agent for me.

Goal:
{goal}

Workspace:
{workspace.resolve()}

Country/market:
{country}

Requested vendors:
{vendor_text}

Marketplace-agent repo:
{repo}

Read these local repo skill files first, then follow them:
- {repo / 'hermes' / 'skills' / 'marketplace-agent-workspace.md'}
- {repo / 'hermes' / 'skills' / 'marketplace-agent-vendor-builder.md'}
- {repo / 'hermes' / 'skills' / 'marketplace-agent-browser-harness.md'}
- {repo / 'hermes' / 'skills' / 'marketplace-agent-sell-draft.md'}

Use the full browser-harness submodule for vendor discovery:
- {repo / 'third_party' / 'browser-harness' / 'SKILL.md'}
- {repo / 'third_party' / 'browser-harness' / 'install.md'}
- {repo / 'third_party' / 'browser-harness' / 'domain-skills' / 'amazon' / 'product-search.md'}
- {repo / 'third_party' / 'browser-harness' / 'domain-skills' / 'ebay' / 'scraping.md'}

If those files are missing, clone/update the repo with submodules enabled from https://github.com/Matars/marketplace-agent and continue with the closest available workflow.

Default workflow:
1. Clone or update marketplace-agent with submodules enabled from https://github.com/Matars/marketplace-agent using uv where applicable.
2. Create or update the workspace above. Keep it separate from the engine repo.
3. Convert my goal into concrete marketplace categories and product queries.
4. Configure the workspace marketplace.toml.
5. Use real requested vendors only. Do not configure demo vendors unless I explicitly ask for a dry-run placeholder.
6. For each requested real vendor that is missing, use browser/browser-harness analysis to build or repair a vendor plugin.
7. Run: marketplace-agent doctor {workspace.resolve()}
8. Run: marketplace-agent find {workspace.resolve()}
9. Inspect: {workspace.resolve() / 'output' / 'latest.json'}
10. Summarize what was configured, what worked, what failed, and the next exact command.

Safety:
- Do not auto-post listings.
- Do not message sellers/buyers unless I explicitly ask.
- Do not bypass captcha/login protections without asking.
- Keep personal config and output outside the engine repo to avoid git conflicts.
"""


@app.command()
def init(
    path: Path = typer.Argument(..., help="User workspace directory to initialize. Prefer a folder outside the engine repo."),
    name: str = typer.Option("My Marketplace Agent", "--name", help="Human-friendly project name."),
    country: str = typer.Option("SE", "--country", help="Country code, e.g. SE, DE, US."),
    currency: str = typer.Option("SEK", "--currency", help="Currency code, e.g. SEK, EUR, USD."),
    force: bool = typer.Option(False, "--force", help="Overwrite an existing marketplace.toml."),
) -> None:
    """Create a local user workspace outside the engine repo."""
    path.mkdir(parents=True, exist_ok=True)
    for dirname in ("vendors", "templates", "output", ".marketplace-agent/diagnostics"):
        (path / dirname).mkdir(parents=True, exist_ok=True)

    config_path = path / "marketplace.toml"
    if config_path.exists() and not force:
        raise typer.BadParameter(f"{config_path} already exists. Use --force to overwrite it.")
    config_path.write_text(_config_text(name, country, currency), encoding="utf-8")

    readme = path / "README.md"
    if not readme.exists() or force:
        readme.write_text(_workspace_readme(name), encoding="utf-8")

    typer.echo(f"initialized marketplace project at {path}")
    typer.echo("Keep this workspace outside the engine repo to avoid pull/update conflicts.")
    typer.echo("Try: marketplace-agent find <that-folder>")


@app.command()
def doctor(path: Path = typer.Argument(Path("."), help="User workspace path.")) -> None:
    """Validate that a user workspace has the expected shape."""
    project = path.resolve()
    _load_config(project)

    missing_dirs = [
        dirname
        for dirname in ("vendors", "templates", "output", ".marketplace-agent/diagnostics")
        if not (project / dirname).is_dir()
    ]
    if missing_dirs:
        raise typer.BadParameter(f"missing workspace directories: {', '.join(missing_dirs)}")

    typer.echo(f"workspace looks valid: {project}")


@app.command("find")
def find_command(path: Path = typer.Argument(Path("."), help="User workspace path.")) -> None:
    """Run the find workflow for configured categories and vendors."""
    project = path.resolve()
    config = _load_config(project)
    vendors = _enabled_vendors(config)
    if not vendors:
        raise typer.BadParameter("no enabled vendors configured in marketplace.toml")
    if not config.categories:
        raise typer.BadParameter("no categories configured in marketplace.toml")

    items: list[Item] = []
    for category in config.categories:
        if not category.queries:
            continue
        for query in category.queries:
            for vendor in vendors:
                items.extend(vendor.search(query, category=category.name))

    output_dir = project / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "workspace": config.name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "items": [_item_to_json(item) for item in items],
    }
    (output_dir / "latest.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    typer.echo(f"found {len(items)} items")
    typer.echo(f"wrote {output_dir / 'latest.json'}")


@hermes_prompt_app.command("find")
def hermes_prompt_find(
    workspace: Path = typer.Option(Path("~/my-marketplace"), "--workspace", help="User workspace path."),
    goal: str = typer.Option(..., "--goal", help="Natural-language find goal."),
    country: str = typer.Option("SE", "--country", help="Country/market to configure for."),
    vendors: str = typer.Option("amazon,ebay", "--vendors", help="Comma-separated requested vendors."),
    repo: Path = typer.Option(Path.cwd(), "--repo", help="Local marketplace-agent repo path containing hermes/skills."),
    output: Path | None = typer.Option(None, "--output", help="Optional file to write the prompt to."),
) -> None:
    """Generate a single copy-paste prompt for Hermes to configure a find workflow."""
    prompt = _find_prompt(workspace.expanduser(), goal=goal, country=country, vendors=vendors, repo=repo.expanduser())
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(prompt, encoding="utf-8")
        typer.echo(f"wrote {output}")
        return
    typer.echo(prompt)


@hermes_app.command("context")
def hermes_context(path: Path = typer.Argument(Path("."), help="User workspace path.")) -> None:
    """Print compact context Hermes can use without re-asking basics."""
    project = path.resolve()
    config_path = project / "marketplace.toml"
    typer.echo("Marketplace-agent Hermes context")
    typer.echo(f"Project path: {project}")
    typer.echo(f"Config: {config_path}")
    typer.echo("Workspace model: this is user config/data, separate from the installed engine package.")
    typer.echo("Engine updates should not modify this project folder.")
    typer.echo("Vendor plugins: ./vendors/ supports Python plugins and future declarative configs")
    typer.echo("Outputs: ./output/")
    typer.echo("Diagnostics: ./.marketplace-agent/diagnostics/")
    typer.echo("Safety: Do not auto-post listings. Generate drafts and require explicit user approval.")


def main() -> None:
    app()
