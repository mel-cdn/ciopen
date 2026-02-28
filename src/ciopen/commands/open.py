import typer

from ciopen.detector import detect_provider
from ciopen.opener import open_url


def open_command(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        provider = detect_provider()
        open_url(url=provider.pipeline_url)
