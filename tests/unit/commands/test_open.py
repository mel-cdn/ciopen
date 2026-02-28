from unittest.mock import Mock, call, patch

from ciopen.commands.open import open_command


@patch(f"{open_command.__module__}.open_url", spec=True)
@patch(f"{open_command.__module__}.detect_provider", spec=True)
def test_open_command_when_no_subcommand_opens_url(m_detect, m_open):
    provider = Mock(pipeline_url="https://example.com/pipeline")
    m_detect.return_value = provider

    ctx = Mock(invoked_subcommand=None)

    assert open_command(ctx) is None
    assert m_detect.mock_calls == [call()]
    assert m_open.mock_calls == [call(url=provider.pipeline_url)]


@patch(f"{open_command.__module__}.open_url", spec=True)
@patch(f"{open_command.__module__}.detect_provider", spec=True)
def test_open_command_when_subcommand_is_invoked_does_nothing(m_detect, m_open):
    ctx = Mock(invoked_subcommand="version")

    assert open_command(ctx) is None
    assert m_detect.mock_calls == []
    assert m_open.mock_calls == []
