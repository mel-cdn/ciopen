from ciopen.detector import detect_provider
from ciopen.opener import open_url


def repo_command() -> None:
    provider = detect_provider()
    open_url(url=provider.repository_url)
