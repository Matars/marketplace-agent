from pathlib import Path

from typer.testing import CliRunner

from marketplace_agent.cli import app


runner = CliRunner()


def test_hermes_prompt_find_generates_single_copy_paste_prompt(tmp_path: Path):
    workspace = tmp_path / "my-marketplace"
    runner.invoke(app, ["init", str(workspace), "--name", "Home Deals"])

    result = runner.invoke(
        app,
        [
            "hermes",
            "prompt",
            "find",
            "--workspace",
            str(workspace),
            "--goal",
            "GPUs that can run Qwen locally",
            "--country",
            "SE",
            "--vendors",
            "blocket,tradera",
        ],
    )

    assert result.exit_code == 0
    assert "You are configuring marketplace-agent" in result.output
    assert "GPUs that can run Qwen locally" in result.output
    assert str(workspace) in result.output
    assert "Read these local repo skill files first" in result.output
    assert "hermes/skills/marketplace-agent-workspace.md" in result.output
    assert "hermes/skills/marketplace-agent-vendor-builder.md" in result.output
    assert "hermes/skills/marketplace-agent-sell-draft.md" in result.output
    assert "blocket" in result.output
    assert "tradera" in result.output
    assert "Do not auto-post" in result.output
    assert "marketplace-agent find" in result.output


def test_hermes_prompt_find_can_write_to_file(tmp_path: Path):
    workspace = tmp_path / "my-marketplace"
    output = tmp_path / "prompt.md"
    runner.invoke(app, ["init", str(workspace), "--name", "Home Deals"])

    result = runner.invoke(
        app,
        [
            "hermes",
            "prompt",
            "find",
            "--workspace",
            str(workspace),
            "--goal",
            "cheap e-bikes",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0
    assert output.exists()
    assert "wrote" in result.output.lower()
    assert "cheap e-bikes" in output.read_text(encoding="utf-8")
