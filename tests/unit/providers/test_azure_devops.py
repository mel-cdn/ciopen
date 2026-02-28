import pytest

from ciopen.providers.azure_devops import AzureDevOpsProvider


@pytest.mark.parametrize(
    argnames=["remote_url", "expected_repo_path"],
    argvalues=[
        ("https://dev.azure.com/org/project/_git/repo", "org/project/_git/repo"),
        ("https://dev.azure.com/org/project/_git/repo.git", "org/project/_git/repo"),
        ("https://org@dev.azure.com/org/project/_git/repo", "org/project/_git/repo"),
        ("git@ssh.dev.azure.com:v3/org/project/repo", "org/project/repo"),
    ],
    ids=["HTTPS", "HTTPS with .git", "HTTPS with user@", "SSH"],
)
def test_azure_devops_provider_extracts_repo_path(remote_url, expected_repo_path):
    provider = AzureDevOpsProvider(remote_url=remote_url)
    assert provider.repo_path == expected_repo_path


def test_azure_devops_provider_properties_https_repo_path():
    provider = AzureDevOpsProvider(remote_url="https://dev.azure.com/org/project/_git/repo")

    assert provider.name == "Azure DevOps"
    assert provider.repository_url == "https://dev.azure.com/org/project/_git/repo"
    assert provider.pipeline_url == "https://dev.azure.com/org/project/_build"
    assert provider.pull_request_url == "https://dev.azure.com/org/project/_git/repo/pullrequests"


def test_azure_devops_provider_properties_ssh_repo_path_normalizes_to_https():
    provider = AzureDevOpsProvider(remote_url="git@ssh.dev.azure.com:v3/org/project/repo")

    assert provider.name == "Azure DevOps"
    assert provider.repository_url == "https://dev.azure.com/org/project/_git/repo"
    assert provider.pipeline_url == "https://dev.azure.com/org/project/_build"
    assert provider.pull_request_url == "https://dev.azure.com/org/project/_git/repo/pullrequests"
