import typer

from ciopen import __author__, __version__


def info_command() -> None:
    typer.echo(f"ciopen {__version__}")
    typer.echo(f"Author: {__author__}")
    # Make this not hard coded in the future
    typer.echo("Homepage: https://github.com/mel-cdn/ciopen")
