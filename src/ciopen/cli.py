import typer

from ciopen.commands.doctor import doctor_command
from ciopen.commands.info import info_command
from ciopen.commands.open import open_command
from ciopen.commands.pr import pr_command
from ciopen.commands.provider import provider_command
from ciopen.commands.repo import repo_command
from ciopen.commands.version import version_command

app = typer.Typer(help="Quickly open CI pipelines from your Git repository.")

app.callback(invoke_without_command=True)(open_command)

app.command(name="version", help="Show ciopen version")(version_command)
app.command(name="info", help="Show ciopen information")(info_command)
app.command(name="doctor", help="Check if everything is set up right")(doctor_command)
app.command(name="provider", help="Show which CI provider is detected")(provider_command)
app.command(name="repo", help="Open the main page of this repository")(repo_command)
app.command(name="pr", help="Open the pull requests page of this repository")(pr_command)
