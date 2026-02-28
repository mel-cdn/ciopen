import pytest

from ciopen.providers.gitlab import GitLabProvider


@pytest.mark.parametrize(
    argnames=["remote_url", "expected_repo_path"],
    argvalues=[
        ("git@gitlab.com:group/subgroup/repo.git", "group/subgroup/repo"),
        ("git@gitlab.com:group/subgroup/repo", "group/subgroup/repo"),
        ("https://gitlab.com/group/subgroup/repo.git", "group/subgroup/repo"),
        ("https://gitlab.com/group/subgroup/repo", "group/subgroup/repo"),
    ],
    ids=["SSH with .git", "SSH wo .git", "HTTPS with .git", "HTTPS wo .git"],
)
def test_gitlab_provider_extracts_repo_path(remote_url, expected_repo_path):
    provider = GitLabProvider(remote_url=remote_url)
    assert provider.repo_path == expected_repo_path


def test_gitlab_provider_properties():
    provider = GitLabProvider(remote_url="https://gitlab.com/group/subgroup/repo.git")
    assert provider.name == "GitLab"
    assert provider.repository_url == "https://gitlab.com/group/subgroup/repo"
    assert provider.pipeline_url == "https://gitlab.com/group/subgroup/repo/-/pipelines"
    assert provider.pull_request_url == "https://gitlab.com/group/subgroup/repo/-/merge_requests"
