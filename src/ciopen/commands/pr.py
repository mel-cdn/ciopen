from ciopen.detector import detect_provider
from ciopen.opener import open_url


def pr_command() -> None:
    provider = detect_provider()
    open_url(url=provider.pull_request_url)
