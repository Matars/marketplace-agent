from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Marketplace automation: find deals now, draft listings later.")
hermes_app = typer.Typer(help="Generate Hermes-friendly context and task prompts.")
app.add_typer(hermes_app, name="hermes")
console = Console()


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
marketplace-agent hermes context .
```
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


@app.command()
def doctor(path: Path = typer.Argument(Path("."), help="User workspace path.")) -> None:
    """Validate that a user workspace has the expected shape."""
    project = path.resolve()
    config_path = project / "marketplace.toml"
    if not config_path.exists():
        raise typer.BadParameter(f"missing marketplace.toml in {project}")

    missing_dirs = [
        dirname
        for dirname in ("vendors", "templates", "output", ".marketplace-agent/diagnostics")
        if not (project / dirname).is_dir()
    ]
    if missing_dirs:
        raise typer.BadParameter(f"missing workspace directories: {', '.join(missing_dirs)}")

    typer.echo(f"workspace looks valid: {project}")


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
