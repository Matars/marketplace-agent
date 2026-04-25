from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from marketplace_agent.cli import app


runner = CliRunner()


def test_init_writes_runnable_demo_find_config(tmp_path: Path):
    workspace = tmp_path / "my-marketplace"

    result = runner.invoke(app, ["init", str(workspace), "--name", "Home Deals"])

    assert result.exit_code == 0
    config = (workspace / "marketplace.toml").read_text(encoding="utf-8")
    assert '[[categories]]' in config
    assert '[[vendors]]' in config
    assert 'type = "demo"' in config


def test_find_runs_demo_vendor_and_writes_latest_json(tmp_path: Path):
    workspace = tmp_path / "my-marketplace"
    runner.invoke(app, ["init", str(workspace), "--name", "Home Deals"])

    result = runner.invoke(app, ["find", str(workspace)])

    assert result.exit_code == 0
    assert "found 3 items" in result.output.lower()
    latest = workspace / "output" / "latest.json"
    assert latest.exists()
    payload = json.loads(latest.read_text(encoding="utf-8"))
    assert payload["workspace"] == "Home Deals"
    assert len(payload["items"]) == 3
    assert payload["items"][0]["source"] == "demo"


def test_find_fails_clearly_when_no_categories_configured(tmp_path: Path):
    workspace = tmp_path / "my-marketplace"
    runner.invoke(app, ["init", str(workspace), "--name", "Home Deals"])
    (workspace / "marketplace.toml").write_text(
        'name = "Home Deals"\n\n[[vendors]]\nname = "demo"\ntype = "demo"\nenabled = true\n',
        encoding="utf-8",
    )

    result = runner.invoke(app, ["find", str(workspace)])

    assert result.exit_code != 0
    assert "no categories configured" in result.output.lower()
