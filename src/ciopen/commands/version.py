import typer

from ciopen import __version__


def version_command() -> None:
    typer.echo(f"ciopen {__version__}")
