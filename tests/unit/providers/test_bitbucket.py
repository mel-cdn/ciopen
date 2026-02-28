import pytest

from ciopen.providers.bitbucket import BitbucketProvider


@pytest.mark.parametrize(
    argnames=["remote_url", "expected_repo_path"],
    argvalues=[
        ("git@bitbucket.org:workspace/repo.git", "workspace/repo"),
        ("git@bitbucket.org:workspace/repo", "workspace/repo"),
        ("https://bitbucket.org/workspace/repo.git", "workspace/repo"),
        ("https://bitbucket.org/workspace/repo", "workspace/repo"),
    ],
    ids=["SSH with .git", "SSH wo .git", "HTTPS with .git", "HTTPS wo .git"],
)
def test_bitbucket_provider_extracts_repo_path(remote_url, expected_repo_path):
    provider = BitbucketProvider(remote_url=remote_url)
    assert provider.repo_path == expected_repo_path


def test_bitbucket_provider_properties():
    provider = BitbucketProvider(remote_url="https://bitbucket.org/workspace/repo.git")
    assert provider.name == "Bitbucket"
    assert provider.repository_url == "https://bitbucket.org/workspace/repo"
    assert provider.pipeline_url == "https://bitbucket.org/workspace/repo/pipelines"
    assert provider.pull_request_url == "https://bitbucket.org/workspace/repo/pull-requests"
