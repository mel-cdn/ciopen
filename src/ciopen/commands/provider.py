import typer

from ciopen.detector import detect_provider


def provider_command() -> None:
    provider = detect_provider()
    typer.echo(provider.name)
