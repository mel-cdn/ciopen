from contextlib import chdir

import pytest

from ciopen import cli
from tests.integration.conftest import _git


@pytest.mark.parametrize(
    argnames=["valid_remote"],
    argvalues=[
        ["https://gitlab.com/org/repo.git"],
        ["git@gitlab.com:org/repo.git"],
    ],
    ids=["HTTPS", "SSH"],
)
def test_doctor_command_detects_gitlab_repo(fx_git_repo, fx_cli_runner, valid_remote):
    with chdir(fx_git_repo):
        _git(fx_git_repo, "remote", "add", "origin", valid_remote)
        result = fx_cli_runner.invoke(cli.app, ["doctor"])

    assert result.exit_code == 0
    assert "✅ Git installed" in result.output
    assert "✅ Inside a Git repository" in result.output
    assert "✅ Remote origin found" in result.output
    assert "✅ CI Provider detected" in result.output

    # Details section should appear
    assert "Environment details" in result.output
    assert "Provider\t\t: GitLab" in result.output
    assert "Repository slug\t\t: org/repo" in result.output
    assert "Current branch\t\t: main" in result.output
    assert "Repository URL\t\t: https://gitlab.com/org/repo" in result.output
    assert "Pipeline URL\t\t: https://gitlab.com/org/repo/-/pipelines" in result.output
    assert "Pull Request URL\t: https://gitlab.com/org/repo/-/merge_requests" in result.output
