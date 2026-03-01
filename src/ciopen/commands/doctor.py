import typer

from ciopen import __version__
from ciopen.detector import detect_provider
from ciopen.git import (
    extract_repository_slug,
    get_current_branch,
    get_remote_url,
    get_version,
    is_inside_git_repo,
)
from ciopen.providers.base import BaseProvider


def doctor_command() -> None:
    typer.echo(f"ciopen {__version__}")
    typer.echo("Running diagnostics...\n")

    checks: list[tuple[str, bool]] = []

    # -- 1. Git installed
    try:
        get_version()
        checks.append(("Git installed", True))
    except Exception:
        checks.append(("Git installed", False))

    # -- 2. Inside git repo
    try:
        is_inside = is_inside_git_repo()
        checks.append(("Inside a Git repository", is_inside))
    except Exception:
        checks.append(("Inside a Git repository", False))

    # -- 3. Remote origin
    try:
        remote_url = get_remote_url()
        checks.append(("Remote origin found", True))
    except Exception:
        remote_url = None
        checks.append(("Remote origin found", False))

    # -- 4. Provider detection
    if remote_url:
        try:
            provider = detect_provider()
            checks.append(("CI Provider detected", True))
        except Exception:
            provider = None
            checks.append(("CI Provider detection failed", False))
    else:
        provider = None

    # -- 5. Print diagnostics results
    for label, ok in checks:
        status = "✅" if ok else "❌"
        typer.echo(f" {status} {label}")

    # -- 6. Show detailed info only if everything important passed
    if provider:
        try:
            _show_results(provider=provider)
        except Exception:
            typer.echo("\n⚠️  Unable to compute full environment details.")


def _show_results(provider: BaseProvider) -> None:
    typer.echo("\nEnvironment details:\n")
    typer.echo(f"Provider\t\t: {provider.name}")
    typer.echo(f"Repository slug\t\t: {extract_repository_slug(remote_url=provider.remote_url)}")
    typer.echo(f"Current branch\t\t: {get_current_branch()}")
    typer.echo(f"Repository URL\t\t: {provider.repository_url}")
    typer.echo(f"Pipeline URL\t\t: {provider.pipeline_url}")
    typer.echo(f"Pull Request URL\t: {provider.pull_request_url}")
