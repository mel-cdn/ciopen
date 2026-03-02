from unittest.mock import call, patch

from ciopen.commands.info import info_command


@patch(f"{info_command.__module__}.typer.echo", spec=True)
@patch(f"{info_command.__module__}.__author__", spec=True)
@patch(f"{info_command.__module__}.__version__", spec=True)
def test_info_command_should_show_version(m_version, m_author, m_echo):
    m_version.__str__.return_value = "1.2.3"
    m_author.__str__.return_value = "Name of Author"

    assert info_command() is None
    assert m_echo.mock_calls == [
        call("ciopen 1.2.3"),
        call("Author: Name of Author"),
        call("Homepage: https://github.com/mel-cdn/ciopen"),
    ]
