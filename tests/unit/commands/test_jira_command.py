from unittest.mock import Mock, call, patch

import pytest
import typer

from ciopen.commands.jira import (
    jira_command,
    set_base_url_command,
    show_command,
    unset_base_url_command,
)


@patch(f"{jira_command.__module__}.open_url", spec=True)
@patch(f"{jira_command.__module__}.extract_ticket_key", spec=True)
@patch(f"{jira_command.__module__}.get_current_branch", spec=True)
@patch(f"{jira_command.__module__}.get_jira_base_url", spec=True)
def test_jira_command_opens_ticket_url_when_no_subcommand(m_get_base_url, m_get_branch, m_extract_key, m_open):
    m_get_base_url.return_value = "https://example.atlassian.net"
    m_get_branch.return_value = "JIRA-1234-my-branch"
    m_extract_key.return_value = "JIRA-1234"

    ctx = Mock(invoked_subcommand=None)

    assert jira_command(ctx) is None
    assert m_open.mock_calls == [call(url="https://example.atlassian.net/browse/JIRA-1234")]


@patch(f"{jira_command.__module__}.open_url", spec=True)
@patch(f"{jira_command.__module__}.get_jira_base_url", spec=True)
def test_jira_command_does_nothing_when_subcommand_invoked(m_get_base_url, m_open):
    ctx = Mock(invoked_subcommand="show")

    assert jira_command(ctx) is None
    assert m_get_base_url.mock_calls == []
    assert m_open.mock_calls == []


@patch(f"{jira_command.__module__}.typer.echo", spec=True)
@patch(f"{jira_command.__module__}.get_jira_base_url", spec=True)
def test_jira_command_exits_when_base_url_not_set(m_get_base_url, m_echo):
    m_get_base_url.return_value = None
    ctx = Mock(invoked_subcommand=None)

    with pytest.raises(typer.Exit) as exc_info:
        jira_command(ctx)

    assert exc_info.value.exit_code == 1


@patch(f"{jira_command.__module__}.typer.echo", spec=True)
@patch(f"{jira_command.__module__}.extract_ticket_key", spec=True)
@patch(f"{jira_command.__module__}.get_current_branch", spec=True)
@patch(f"{jira_command.__module__}.get_jira_base_url", spec=True)
def test_jira_command_exits_when_no_ticket_found(m_get_base_url, m_get_branch, m_extract_key, m_echo):
    m_get_base_url.return_value = "https://example.atlassian.net"
    m_get_branch.return_value = "main"
    m_extract_key.return_value = None

    ctx = Mock(invoked_subcommand=None)

    with pytest.raises(typer.Exit) as exc_info:
        jira_command(ctx)

    assert exc_info.value.exit_code == 1


@patch(f"{set_base_url_command.__module__}.typer.echo", spec=True)
@patch(f"{set_base_url_command.__module__}.get_jira_base_url", spec=True)
@patch(f"{set_base_url_command.__module__}.set_jira_base_url", spec=True)
def test_set_base_url_command_saves_and_confirms(m_set, m_get, m_echo):
    m_get.return_value = "https://example.atlassian.net"

    assert set_base_url_command("https://example.atlassian.net") is None
    assert m_set.mock_calls == [call("https://example.atlassian.net")]
    assert m_echo.mock_calls == [call("Jira base URL set to https://example.atlassian.net")]


@patch(f"{unset_base_url_command.__module__}.typer.echo", spec=True)
@patch(f"{unset_base_url_command.__module__}.unset_jira_base_url", spec=True)
def test_unset_base_url_command_clears_and_confirms(m_unset, m_echo):
    assert unset_base_url_command() is None
    assert m_unset.mock_calls == [call()]
    assert m_echo.mock_calls == [call("Jira base URL unset.")]


@patch(f"{show_command.__module__}.typer.echo", spec=True)
@patch(f"{show_command.__module__}.get_jira_base_url", spec=True)
def test_show_command_prints_base_url_when_set(m_get, m_echo):
    m_get.return_value = "https://example.atlassian.net"

    assert show_command() is None
    assert m_echo.mock_calls == [call("Jira base URL: https://example.atlassian.net")]


@patch(f"{show_command.__module__}.typer.echo", spec=True)
@patch(f"{show_command.__module__}.get_jira_base_url", spec=True)
def test_show_command_prints_message_when_not_set(m_get, m_echo):
    m_get.return_value = None

    assert show_command() is None
    assert m_echo.mock_calls == [call("Jira base URL is not set.")]
