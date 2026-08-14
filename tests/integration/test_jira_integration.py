from contextlib import chdir

from ciopen import cli
from tests.integration.conftest import _git


def test_jira_show_reports_unset_base_url(fx_git_repo, fx_cli_runner, monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))

    with chdir(fx_git_repo):
        result = fx_cli_runner.invoke(cli.app, ["jira", "show"])

    assert result.exit_code == 0
    assert "Jira base URL is not set." in result.output


def test_jira_set_base_url_then_show_round_trips(fx_git_repo, fx_cli_runner, monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))

    with chdir(fx_git_repo):
        set_result = fx_cli_runner.invoke(cli.app, ["jira", "set-base-url", "https://example.atlassian.net/"])
        show_result = fx_cli_runner.invoke(cli.app, ["jira", "show"])

    assert set_result.exit_code == 0
    assert "Jira base URL set to https://example.atlassian.net" in set_result.output
    assert show_result.exit_code == 0
    assert "Jira base URL: https://example.atlassian.net" in show_result.output


def test_jira_unset_base_url_then_show_reports_unset(fx_git_repo, fx_cli_runner, monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))

    with chdir(fx_git_repo):
        fx_cli_runner.invoke(cli.app, ["jira", "set-base-url", "https://example.atlassian.net"])
        unset_result = fx_cli_runner.invoke(cli.app, ["jira", "unset-base-url"])
        show_result = fx_cli_runner.invoke(cli.app, ["jira", "show"])

    assert unset_result.exit_code == 0
    assert "Jira base URL unset." in unset_result.output
    assert show_result.exit_code == 0
    assert "Jira base URL is not set." in show_result.output


def test_jira_open_fails_without_base_url_configured(fx_git_repo, fx_cli_runner, monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))

    with chdir(fx_git_repo):
        result = fx_cli_runner.invoke(cli.app, ["jira"])

    assert result.exit_code == 1
    assert "Jira base URL is not set." in result.output


def test_jira_open_fails_when_branch_has_no_ticket(fx_git_repo, fx_cli_runner, monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))

    with chdir(fx_git_repo):
        fx_cli_runner.invoke(cli.app, ["jira", "set-base-url", "https://example.atlassian.net"])
        result = fx_cli_runner.invoke(cli.app, ["jira"])

    assert result.exit_code == 1
    assert "No Jira ticket detected in branch name: main" in result.output


def test_jira_open_opens_ticket_url_from_branch_name(fx_git_repo, fx_cli_runner, monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))
    monkeypatch.setattr("webbrowser.open", lambda url: True)

    _git(fx_git_repo, "checkout", "-b", "feature/JIRA-1234-add-thing")

    with chdir(fx_git_repo):
        fx_cli_runner.invoke(cli.app, ["jira", "set-base-url", "https://example.atlassian.net"])
        result = fx_cli_runner.invoke(cli.app, ["jira"])

    assert result.exit_code == 0
    assert "Opening https://example.atlassian.net/browse/JIRA-1234" in result.output
