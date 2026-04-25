from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from marketplace_agent.cli import app


runner = CliRunner()


def test_init_writes_real_vendor_config(tmp_path: Path):
    workspace = tmp_path / "my-marketplace"

    result = runner.invoke(app, ["init", str(workspace), "--name", "Home Deals"])

    assert result.exit_code == 0
    config = (workspace / "marketplace.toml").read_text(encoding="utf-8")
    assert '[[categories]]' in config
    assert '[[vendors]]' in config
    assert 'name = "amazon"' in config
    assert 'name = "ebay"' in config


def test_find_runs_and_writes_latest_json(tmp_path: Path):
    workspace = tmp_path / "my-marketplace"
    runner.invoke(app, ["init", str(workspace), "--name", "Home Deals"])

    result = runner.invoke(app, ["find", str(workspace)])

    assert result.exit_code == 0
    assert "found" in result.output.lower()
    assert "items" in result.output.lower()
    latest = workspace / "output" / "latest.json"
    assert latest.exists()
    payload = json.loads(latest.read_text(encoding="utf-8"))
    assert payload["workspace"] == "Home Deals"
    assert "items" in payload


def test_find_fails_clearly_when_no_categories_configured(tmp_path: Path):
    workspace = tmp_path / "my-marketplace"
    runner.invoke(app, ["init", str(workspace), "--name", "Home Deals"])
    (workspace / "marketplace.toml").write_text(
        'name = "Home Deals"\n\n[[vendors]]\nname = "amazon"\ntype = "amazon"\nenabled = true\n',
        encoding="utf-8",
    )

    result = runner.invoke(app, ["find", str(workspace)])

    assert result.exit_code != 0
    assert "no categories configured" in result.output.lower()
