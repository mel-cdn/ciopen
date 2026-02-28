import pytest

from ciopen.providers.github import GitHubProvider


@pytest.mark.parametrize(
    argnames=["remote_url", "expected_repo_path"],
    argvalues=[
        ("git@github.com:org/repo.git", "org/repo"),
        ("git@github.com:org/repo", "org/repo"),
        ("https://github.com/org/repo.git", "org/repo"),
        ("https://github.com/org/repo", "org/repo"),
    ],
    ids=["SSH with .git", "SSH wo .git", "HTTPS with .git", "HTTPS wo .git"],
)
def test_github_provider_extracts_repo_path(remote_url, expected_repo_path):
    provider = GitHubProvider(remote_url=remote_url)
    assert provider.repo_path == expected_repo_path


def test_github_provider_properties():
    provider = GitHubProvider(remote_url="https://github.com/org/repo.git")
    assert provider.name == "GitHub"
    assert provider.repository_url == "https://github.com/org/repo"
    assert provider.pipeline_url == "https://github.com/org/repo/actions"
    assert provider.pull_request_url == "https://github.com/org/repo/pulls"
