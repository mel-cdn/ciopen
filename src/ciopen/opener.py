import webbrowser

import typer


def open_url(url: str) -> None:
    webbrowser.open(url=url)
    typer.echo(f"Opening {url}")
