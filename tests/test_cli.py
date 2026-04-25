from pathlib import Path

from typer.testing import CliRunner

from marketplace_agent.cli import app


runner = CliRunner()


def test_init_creates_project_config_and_directories(tmp_path: Path):
    result = runner.invoke(app, ["init", str(tmp_path), "--name", "Home Deals", "--country", "SE", "--currency", "SEK"])

    assert result.exit_code == 0
    assert (tmp_path / "marketplace.toml").exists()
    assert (tmp_path / "vendors").is_dir()
    assert (tmp_path / "templates").is_dir()
    assert (tmp_path / "output").is_dir()
    assert "initialized marketplace project" in result.output.lower()


def test_hermes_context_prints_project_summary(tmp_path: Path):
    runner.invoke(app, ["init", str(tmp_path), "--name", "Home Deals", "--country", "SE", "--currency", "SEK"])

    result = runner.invoke(app, ["hermes", "context", str(tmp_path)])

    assert result.exit_code == 0
    assert "Project path:" in result.output
    assert "marketplace.toml" in result.output
    assert "Do not auto-post listings" in result.output
