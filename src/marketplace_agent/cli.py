from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Marketplace automation: find deals now, draft listings later.")
hermes_app = typer.Typer(help="Generate Hermes-friendly context and task prompts.")
app.add_typer(hermes_app, name="hermes")
console = Console()


def _config_text(name: str, country: str, currency: str) -> str:
    return f'''# marketplace-agent project config

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


@app.command()
def init(
    path: Path = typer.Argument(..., help="Project directory to initialize."),
    name: str = typer.Option("My Marketplace Agent", "--name", help="Human-friendly project name."),
    country: str = typer.Option("SE", "--country", help="Country code, e.g. SE, DE, US."),
    currency: str = typer.Option("SEK", "--currency", help="Currency code, e.g. SEK, EUR, USD."),
) -> None:
    """Create a local marketplace-agent project folder."""
    path.mkdir(parents=True, exist_ok=True)
    for dirname in ("vendors", "templates", "output", ".marketplace-agent/diagnostics"):
        (path / dirname).mkdir(parents=True, exist_ok=True)

    config_path = path / "marketplace.toml"
    if not config_path.exists():
        config_path.write_text(_config_text(name, country, currency), encoding="utf-8")

    readme = path / "README.md"
    if not readme.exists():
        readme.write_text(
            f"# {name}\n\nLocal marketplace-agent project.\n\nRun: `marketplace-agent hermes context .`\n",
            encoding="utf-8",
        )

    console.print(f"initialized marketplace project at {path}")


@hermes_app.command("context")
def hermes_context(path: Path = typer.Argument(Path("."), help="Project path.")) -> None:
    """Print compact context Hermes can use without re-asking basics."""
    project = path.resolve()
    config_path = project / "marketplace.toml"
    typer.echo("Marketplace-agent Hermes context")
    typer.echo(f"Project path: {project}")
    typer.echo(f"Config: {config_path}")
    typer.echo("Vendor plugins: ./vendors/ supports Python plugins and future declarative configs")
    typer.echo("Outputs: ./output/")
    typer.echo("Diagnostics: ./.marketplace-agent/diagnostics/")
    typer.echo("Safety: Do not auto-post listings. Generate drafts and require explicit user approval.")


def main() -> None:
    app()
