import typer

from ciopen.config import get_jira_base_url, set_jira_base_url, unset_jira_base_url
from ciopen.git import get_current_branch
from ciopen.jira import extract_ticket_key
from ciopen.opener import open_url

jira_app = typer.Typer(help="Open the Jira ticket linked to the current branch")


@jira_app.callback(invoke_without_command=True)
def jira_command(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is not None:
        return

    base_url = get_jira_base_url()
    if not base_url:
        typer.echo(
            "Jira base URL is not set. Run 'ciopen jira set-base-url <url>' first, e.g. https://your-org.atlassian.net"
        )
        raise typer.Exit(code=1)

    branch = get_current_branch()
    ticket_key = extract_ticket_key(branch)
    if not ticket_key:
        typer.echo(f"No Jira ticket detected in branch name: {branch}")
        raise typer.Exit(code=1)

    open_url(url=f"{base_url}/browse/{ticket_key}")


@jira_app.command(name="set-base-url", help="Set the Jira base URL, e.g. https://your-org.atlassian.net")
def set_base_url_command(base_url: str) -> None:
    set_jira_base_url(base_url)
    typer.echo(f"Jira base URL set to {get_jira_base_url()}")


@jira_app.command(name="unset-base-url", help="Clear the configured Jira base URL")
def unset_base_url_command() -> None:
    unset_jira_base_url()
    typer.echo("Jira base URL unset.")


@jira_app.command(name="show", help="Show the current Jira configuration")
def show_command() -> None:
    base_url = get_jira_base_url()
    if base_url:
        typer.echo(f"Jira base URL: {base_url}")
    else:
        typer.echo("Jira base URL is not set.")
