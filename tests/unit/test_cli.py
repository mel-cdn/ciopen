from typer.testing import CliRunner

from ciopen import cli


def test_cli_help_lists_commands():
    runner = CliRunner()
    result = runner.invoke(cli.app, ["--help"])
    assert result.exit_code == 0

    # Ensure commands are registered (don’t overfit exact help formatting)
    assert "version" in result.stdout
    assert "info" in result.stdout
    assert "doctor" in result.stdout
    assert "provider" in result.stdout
    assert "repo" in result.stdout
    assert "pr" in result.stdout
