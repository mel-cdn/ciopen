from unittest import mock
from unittest.mock import call, patch

import pytest

from ciopen.detector import detect_provider


@pytest.mark.parametrize(
    argnames=["remote_url", "expected_provider"],
    argvalues=[
        ("https://github.com/user/repo.git", "GitHubProvider"),
        ("https://bitbucket.org/team/repo.git", "BitbucketProvider"),
        ("https://dev.azure.com/org/project/_git/repo", "AzureDevOpsProvider"),
        ("https://gitlab.com/group/repo.git", "GitLabProvider"),
    ],
    ids=["GitHub", "Bitbucket", "AzureDevOps", "GitLab"],
)
@patch(f"{detect_provider.__module__}.typer.echo", spec=True)
@patch(f"{detect_provider.__module__}.get_remote_url", spec=True)
def test_detect_provider_returns_provider(m_get_remote_url, m_echo, remote_url, expected_provider):
    m_get_remote_url.return_value = remote_url

    assert detect_provider().__class__.__name__ == expected_provider
    assert m_get_remote_url.mock_calls == [call()]
    assert m_echo.mock_calls == []


@patch(f"{detect_provider.__module__}.typer.echo", spec=True)
@patch(f"{detect_provider.__module__}.get_remote_url", spec=True)
def test_detect_provider_when_not_a_git_repo_exits_1(m_get_remote_url, m_echo):
    m_get_remote_url.side_effect = Exception("not a git repo")

    with pytest.raises(Exception) as excinfo:
        detect_provider()

    # typer.Exit derives from Click exception types; simplest is to assert code attribute.
    assert getattr(excinfo.value, "exit_code", None) == 1
    assert m_echo.mock_calls == [mock.call("Unable to detect git repository!")]


@patch(f"{detect_provider.__module__}.typer.echo", spec=True)
@patch(f"{detect_provider.__module__}.get_remote_url", spec=True)
def test_detect_provider_unsupported_domain_exits_1(m_get_remote_url, m_echo):
    remote_url = "https://example.com/user/repo.git"
    m_get_remote_url.return_value = remote_url

    with pytest.raises(Exception) as excinfo:
        detect_provider()

    assert getattr(excinfo.value, "exit_code", None) == 1
    assert m_echo.mock_calls == [mock.call(f"Unsupported git provider: {remote_url}")]
