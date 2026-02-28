from unittest.mock import Mock, call, patch

from ciopen.commands.pr import pr_command


@patch(f"{pr_command.__module__}.open_url", spec=True)
@patch(f"{pr_command.__module__}.detect_provider", spec=True)
def test_pr_command_should_open_pr_url(m_detect, m_open):
    provider = Mock(pull_request_url="https://example.com/prs")
    m_detect.return_value = provider

    assert pr_command() is None
    assert m_detect.mock_calls == [call()]
    assert m_open.mock_calls == [call(url=provider.pull_request_url)]
