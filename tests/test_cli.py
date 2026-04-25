from pathlib import Path

from typer.testing import CliRunner

from marketplace_agent.cli import app


runner = CliRunner()


def test_init_creates_external_project_config_and_directories(tmp_path: Path):
    workspace = tmp_path / "my-marketplace"

    result = runner.invoke(app, ["init", str(workspace), "--name", "Home Deals", "--country", "SE", "--currency", "SEK"])

    assert result.exit_code == 0
    assert (workspace / "marketplace.toml").exists()
    assert (workspace / "vendors").is_dir()
    assert (workspace / "templates").is_dir()
    assert (workspace / "output").is_dir()
    assert (workspace / ".marketplace-agent" / "diagnostics").is_dir()
    assert "initialized marketplace project" in result.output.lower()
    assert "outside the engine repo" in result.output.lower()


def test_init_refuses_to_overwrite_existing_config_without_force(tmp_path: Path):
    workspace = tmp_path / "my-marketplace"
    runner.invoke(app, ["init", str(workspace), "--name", "First"])

    result = runner.invoke(app, ["init", str(workspace), "--name", "Second"])

    assert result.exit_code != 0
    assert "already exists" in result.output.lower()
    assert 'name = "First"' in (workspace / "marketplace.toml").read_text(encoding="utf-8")


def test_init_can_force_rewrite_existing_config(tmp_path: Path):
    workspace = tmp_path / "my-marketplace"
    runner.invoke(app, ["init", str(workspace), "--name", "First"])

    result = runner.invoke(app, ["init", str(workspace), "--name", "Second", "--force"])

    assert result.exit_code == 0
    assert 'name = "Second"' in (workspace / "marketplace.toml").read_text(encoding="utf-8")


def test_hermes_context_prints_project_summary(tmp_path: Path):
    workspace = tmp_path / "my-marketplace"
    runner.invoke(app, ["init", str(workspace), "--name", "Home Deals", "--country", "SE", "--currency", "SEK"])

    result = runner.invoke(app, ["hermes", "context", str(workspace)])

    assert result.exit_code == 0
    assert "Project path:" in result.output
    assert "marketplace.toml" in result.output
    assert "Do not auto-post listings" in result.output
    assert "Engine updates should not modify this project folder" in result.output


def test_doctor_validates_workspace_shape(tmp_path: Path):
    workspace = tmp_path / "my-marketplace"
    runner.invoke(app, ["init", str(workspace), "--name", "Home Deals"])

    result = runner.invoke(app, ["doctor", str(workspace)])

    assert result.exit_code == 0
    assert "workspace looks valid" in result.output.lower()


def test_doctor_fails_when_config_is_missing(tmp_path: Path):
    workspace = tmp_path / "empty"
    workspace.mkdir()

    result = runner.invoke(app, ["doctor", str(workspace)])

    assert result.exit_code != 0
    assert "missing marketplace.toml" in result.output.lower()
