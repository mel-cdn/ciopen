from contextlib import chdir

from ciopen import cli
from tests.integration.conftest import _git


def test_doctor_command_detects_git_repo_without_origin(fx_git_repo, fx_cli_runner):
    with chdir(fx_git_repo):
        result = fx_cli_runner.invoke(cli.app, ["doctor"])

    assert result.exit_code == 0
    assert "✅ Git installed" in result.output
    assert "✅ Inside a Git repository" in result.output
    assert "❌ Remote origin found" in result.output


def test_doctor_command_failed_to_detect_unsupported_provider(fx_git_repo, fx_cli_runner):
    with chdir(fx_git_repo):
        # Add an unsupported provider
        _git(fx_git_repo, "remote", "add", "origin", "https://unsupported-git.com/org/repo.git")
        result = fx_cli_runner.invoke(cli.app, ["doctor"])

    assert result.exit_code == 0
    assert "✅ Git installed" in result.output
    assert "✅ Inside a Git repository" in result.output
    assert "✅ Remote origin found" in result.output
    assert "❌ CI Provider detection failed" in result.output

    # Details section should not appear
    assert "Environment details" not in result.output
