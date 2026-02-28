import typer

from ciopen.commands.open import open_command
from ciopen.commands.version import version_command

app = typer.Typer(help="Quickly open CI pipelines from your Git repository.")

app.callback(invoke_without_command=True)(open_command)

app.command(name="version", help="Show ciopen version")(version_command)
