from unittest import mock
from unittest.mock import patch

from ciopen.opener import open_url


@patch(f"{open_url.__module__}.typer.echo", spec=True)
@patch(f"{open_url.__module__}.webbrowser.open", spec=True)
def test_open_url_calls_browser_and_echo(m_open, m_echo):
    test_url = "https://github.com/user/repo"

    assert open_url(test_url) is None
    assert m_open.mock_calls == [mock.call(url=test_url)]
    assert m_echo.mock_calls == [mock.call(f"Opening {test_url}")]
