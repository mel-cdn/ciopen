from ciopen.providers.base import BaseProvider


class GitHubProvider(BaseProvider):
    """
    GitHubProvider

    Supports:
        SSH: git@github.com:org/repo.git
        HTTPS: https://github.com/org/repo.git
    """

    def __init__(self, remote_url: str):
        super().__init__(remote_url=remote_url)

    def _extract_repo_path(self) -> str:
        url = self.remote_url
        if url.startswith("git@"):
            path = url.split(":", 1)[1]
        else:
            path = url.split("github.com/")[1]
        return path.removesuffix(".git")

    @property
    def name(self) -> str:
        return "GitHub"

    @property
    def repository_url(self) -> str:
        return f"https://github.com/{self.repo_path}"

    @property
    def pipeline_url(self) -> str:
        return f"https://github.com/{self.repo_path}/actions"

    @property
    def pull_request_url(self) -> str:
        return f"https://github.com/{self.repo_path}/pulls"
