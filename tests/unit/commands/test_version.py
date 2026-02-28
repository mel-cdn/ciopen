from unittest.mock import call, patch

from ciopen.commands.version import version_command


@patch(f"{version_command.__module__}.typer.echo", spec=True)
@patch(f"{version_command.__module__}.__version__", spec=True)
def test_version_command_should_show_version(m_version, m_echo):
    m_version.__str__.return_value = "1.2.3"

    assert version_command() is None
    assert m_echo.mock_calls == [call("ciopen 1.2.3")]
