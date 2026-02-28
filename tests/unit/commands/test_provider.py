from unittest.mock import Mock, call, patch

from ciopen.commands.provider import provider_command


@patch(f"{provider_command.__module__}.typer.echo", spec=True)
@patch(f"{provider_command.__module__}.detect_provider", spec=True)
def test_provider_command_should_show_provider_name(m_detect, m_echo):
    provider = Mock(name="Provider Name")
    m_detect.return_value = provider

    assert provider_command() is None
    assert m_detect.mock_calls == [call()]
    assert m_echo.mock_calls == [call(provider.name)]
