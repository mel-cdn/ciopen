from unittest.mock import Mock, call, patch

import pytest

from ciopen import git


@patch(f"{git.__name__}.subprocess.run", spec=True)
def test__run_command_invokes_git_and_strips_stdout(m_run):
    m_run.return_value = Mock(stdout="hello\n", returncode=0)

    out = git._run_command(["version"])

    assert out == "hello"
    assert m_run.mock_calls == [
        call(
            ["git", "version"],
            capture_output=True,
            text=True,
            check=True,
        )
    ]


@pytest.mark.parametrize(
    argnames=["remote_url", "expected_slug"],
    argvalues=[
        ("https://github.com/org/repo.git", "org/repo"),
        ("https://github.com/org/repo", "org/repo"),
        ("git@github.com:org/repo.git", "org/repo"),
        ("git@github.com:org/repo", "org/repo"),
        ("git@ssh.dev.azure.com:v3/org/project/repo", "org/project/repo"),
        ("https://dev.azure.com/org/project/_git/repo.git", "org/project/repo"),
    ],
)
def test_extract_repository_slug_common_urls(remote_url, expected_slug):
    assert git.extract_repository_slug(remote_url) == expected_slug


@patch(f"{git.__name__}._run_command", spec=True)
def test_get_version_calls_run_command(m_run_command):
    m_run_command.return_value = "git version 2.44.0"

    assert git.get_version() == "git version 2.44.0"
    assert m_run_command.mock_calls == [call(["version"])]


@patch(f"{git.__name__}._run_command", spec=True)
def test_get_remote_url_calls_run_command(m_run_command):
    m_run_command.return_value = "https://github.com/user/repo.git"

    assert git.get_remote_url() == "https://github.com/user/repo.git"
    assert m_run_command.mock_calls == [call(["remote", "get-url", "origin"])]


@pytest.mark.parametrize(
    argnames=["cmd_output", "expected"],
    argvalues=[
        ("true", True),
        ("false", False),
        ("TRUE", False),  # function checks exact string match
        ("", False),
    ],
)
@patch(f"{git.__name__}._run_command", spec=True)
def test_is_inside_git_repo(m_run_command, cmd_output, expected):
    m_run_command.return_value = cmd_output

    assert git.is_inside_git_repo() is expected
    assert m_run_command.mock_calls == [call(["rev-parse", "--is-inside-work-tree"])]


@patch(f"{git.__name__}._run_command", spec=True)
def test_get_current_branch_calls_run_command(m_run_command):
    m_run_command.return_value = "main"

    assert git.get_current_branch() == "main"
    assert m_run_command.mock_calls == [call(["rev-parse", "--abbrev-ref", "HEAD"])]
