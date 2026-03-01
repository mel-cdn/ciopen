from contextlib import chdir

import pytest

from ciopen import cli
from tests.integration.conftest import _git


@pytest.mark.parametrize(
    argnames=["valid_remote"],
    argvalues=[
        ["https://github.com/org/repo.git"],
        ["git@github.com:org/repo.git"],
    ],
    ids=["HTTPS", "SSH"],
)
def test_doctor_command_detects_github_repo(fx_git_repo, fx_cli_runner, valid_remote):
    with chdir(fx_git_repo):
        _git(fx_git_repo, "remote", "add", "origin", valid_remote)
        result = fx_cli_runner.invoke(cli.app, ["doctor"])

    assert result.exit_code == 0
    assert " ✅ Git installed" in result.output
    assert " ✅ Inside a Git repository" in result.output
    assert " ✅ Remote origin found" in result.output
    assert " ✅ CI Provider detected" in result.output

    # Details section should appear
    assert "Environment details" in result.output
    assert "Provider\t\t: GitHub" in result.output
    assert "Repository slug\t\t: org/repo" in result.output
    assert "Current branch\t\t: main" in result.output
    assert "Repository URL\t\t: https://github.com/org/repo" in result.output
    assert "Pipeline URL\t\t: https://github.com/org/repo/actions" in result.output
    assert "Pull Request URL\t: https://github.com/org/repo/pulls" in result.output
