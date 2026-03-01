from contextlib import chdir
from unittest.mock import call, patch

import pytest

from ciopen import cli
from tests.integration.conftest import _git

CASES = [
    # test id, remote_url, cli_args, expected_url
    # --- GitHub (HTTPS + SSH)
    (
        "GitHub HTTPS: pipeline (default)",
        [],
        "https://github.com/org/repo.git",
        "https://github.com/org/repo/actions",
    ),
    (
        "GitHub HTTPS: repo",
        ["repo"],
        "https://github.com/org/repo.git",
        "https://github.com/org/repo",
    ),
    (
        "GitHub HTTPS: pr",
        ["pr"],
        "https://github.com/org/repo.git",
        "https://github.com/org/repo/pulls",
    ),
    (
        "GitHub SSH: pipeline (default)",
        [],
        "git@github.com:org/repo.git",
        "https://github.com/org/repo/actions",
    ),
    (
        "GitHub SSH: repo",
        ["repo"],
        "git@github.com:org/repo.git",
        "https://github.com/org/repo",
    ),
    (
        "GitHub SSH: pr",
        ["pr"],
        "git@github.com:org/repo.git",
        "https://github.com/org/repo/pulls",
    ),
    # --- Bitbucket (HTTPS + SSH)
    (
        "Bitbucket HTTPS: pipeline (default)",
        [],
        "https://bitbucket.org/workspace/repo.git",
        "https://bitbucket.org/workspace/repo/pipelines",
    ),
    (
        "Bitbucket HTTPS: repo",
        ["repo"],
        "https://bitbucket.org/workspace/repo.git",
        "https://bitbucket.org/workspace/repo",
    ),
    (
        "Bitbucket HTTPS: pr",
        ["pr"],
        "https://bitbucket.org/workspace/repo.git",
        "https://bitbucket.org/workspace/repo/pull-requests",
    ),
    (
        "Bitbucket SSH: pipeline (default)",
        [],
        "git@bitbucket.org:workspace/repo.git",
        "https://bitbucket.org/workspace/repo/pipelines",
    ),
    (
        "Bitbucket SSH: repo",
        ["repo"],
        "git@bitbucket.org:workspace/repo.git",
        "https://bitbucket.org/workspace/repo",
    ),
    (
        "Bitbucket SSH: pr",
        ["pr"],
        "git@bitbucket.org:workspace/repo.git",
        "https://bitbucket.org/workspace/repo/pull-requests",
    ),
    # --- GitLab (HTTPS + SSH)
    (
        "GitLab HTTPS: pipeline (default)",
        [],
        "https://gitlab.com/group/subgroup/repo.git",
        "https://gitlab.com/group/subgroup/repo/-/pipelines",
    ),
    (
        "GitLab HTTPS: repo",
        ["repo"],
        "https://gitlab.com/group/subgroup/repo.git",
        "https://gitlab.com/group/subgroup/repo",
    ),
    (
        "GitLab HTTPS: pr",
        ["pr"],
        "https://gitlab.com/group/subgroup/repo.git",
        "https://gitlab.com/group/subgroup/repo/-/merge_requests",
    ),
    (
        "GitLab SSH: pipeline (default)",
        [],
        "git@gitlab.com:group/subgroup/repo.git",
        "https://gitlab.com/group/subgroup/repo/-/pipelines",
    ),
    (
        "GitLab SSH: repo",
        ["repo"],
        "git@gitlab.com:group/subgroup/repo.git",
        "https://gitlab.com/group/subgroup/repo",
    ),
    (
        "GitLab SSH: pr",
        ["pr"],
        "git@gitlab.com:group/subgroup/repo.git",
        "https://gitlab.com/group/subgroup/repo/-/merge_requests",
    ),
    # --- Azure DevOps (HTTPS + SSH)
    (
        "AzureDevOps HTTPS: pipeline (default)",
        [],
        "https://dev.azure.com/org/project/_git/repo",
        "https://dev.azure.com/org/project/_build",
    ),
    (
        "AzureDevOps HTTPS: repo",
        ["repo"],
        "https://dev.azure.com/org/project/_git/repo",
        "https://dev.azure.com/org/project/_git/repo",
    ),
    (
        "AzureDevOps HTTPS: pr",
        ["pr"],
        "https://dev.azure.com/org/project/_git/repo",
        "https://dev.azure.com/org/project/_git/repo/pullrequests",
    ),
    (
        "AzureDevOps SSH: pipeline (default)",
        [],
        "git@ssh.dev.azure.com:v3/org/project/repo",
        "https://dev.azure.com/org/project/_build",
    ),
    (
        "AzureDevOps SSH: repo",
        ["repo"],
        "git@ssh.dev.azure.com:v3/org/project/repo",
        "https://dev.azure.com/org/project/_git/repo",
    ),
    (
        "AzureDevOps SSH: pr",
        ["pr"],
        "git@ssh.dev.azure.com:v3/org/project/repo",
        "https://dev.azure.com/org/project/_git/repo/pullrequests",
    ),
]


@pytest.mark.parametrize(
    argnames=["cli_args", "remote_url", "expected_url"],
    argvalues=[(c[1], c[2], c[3]) for c in CASES],
    ids=[c[0] for c in CASES],
)
@patch("ciopen.opener.typer.echo", spec=True)
@patch("ciopen.opener.webbrowser.open", spec=True)
def test_browser_opener_should_call_pipeline_url(
    m_open,
    m_echo,
    fx_git_repo,
    fx_cli_runner,
    cli_args,
    remote_url,
    expected_url,
):
    with chdir(fx_git_repo):
        _git(fx_git_repo, "remote", "add", "origin", remote_url)
        result = fx_cli_runner.invoke(cli.app, cli_args)

    assert result.exit_code == 0
    assert m_open.mock_calls == [call(url=expected_url)]
    assert m_echo.mock_calls == [call(f"Opening {expected_url}")]
