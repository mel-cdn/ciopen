from unittest.mock import Mock, call, patch

from ciopen.commands.repo import repo_command


@patch(f"{repo_command.__module__}.open_url", spec=True)
@patch(f"{repo_command.__module__}.detect_provider", spec=True)
def test_repo_command_should_open_repo_url(m_detect, m_open):
    provider = Mock(repository_url="https://example.com/repo")
    m_detect.return_value = provider

    assert repo_command() is None
    assert m_detect.mock_calls == [call()]
    assert m_open.mock_calls == [call(url=provider.repository_url)]
