import typer

from ciopen.git import get_remote_url
from ciopen.providers.azure_devops import AzureDevOpsProvider
from ciopen.providers.bitbucket import BitbucketProvider
from ciopen.providers.github import GitHubProvider
from ciopen.providers.gitlab import GitLabProvider


def detect_provider():
    # -- 1. Get remote URL
    try:
        remote_url = get_remote_url()
    except Exception:
        typer.echo("Unable to detect git repository!")
        raise typer.Exit(code=1)

    # -- 2. Map to provider
    provider_registry = (
        ("github.com", GitHubProvider),
        ("bitbucket.org", BitbucketProvider),
        ("dev.azure.com", AzureDevOpsProvider),
        ("gitlab.com", GitLabProvider),
    )

    for domain, provider_cls in provider_registry:
        if domain in remote_url:
            return provider_cls(remote_url=remote_url)

    typer.echo(f"Unsupported git provider: {remote_url}")
    raise typer.Exit(code=1)
