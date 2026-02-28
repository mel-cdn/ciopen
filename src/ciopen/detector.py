import typer

from ciopen.git import get_remote_url
from ciopen.providers.github import GitHubProvider


def detect_provider():
    try:
        remote_url = get_remote_url()
    except Exception:
        typer.echo("Unable to detect git repository!")
        raise typer.Exit(code=1)

    if "github.com" in remote_url:
        return GitHubProvider(remote_url=remote_url)

    typer.echo(f"Unsupported git provider: {remote_url}")
    raise typer.Exit(code=1)
