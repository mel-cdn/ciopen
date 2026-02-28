import typer

from ciopen.commands.doctor import doctor_command
from ciopen.commands.open import open_command
from ciopen.commands.provider import provider_command
from ciopen.commands.version import version_command

app = typer.Typer(help="Quickly open CI pipelines from your Git repository.")

app.callback(invoke_without_command=True)(open_command)

app.command(name="version", help="Show ciopen version")(version_command)
app.command(name="doctor", help="Check if everything is set up right")(doctor_command)
app.command(name="provider", help="Show which CI provider is detected")(provider_command)
