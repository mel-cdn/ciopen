from ciopen.providers.base import BaseProvider


class BitbucketProvider(BaseProvider):
    """
    BitbucketProvider (Bitbucket Cloud)

    Supports:
        SSH:   git@bitbucket.org:workspace/repo.git
        HTTPS: https://bitbucket.org/workspace/repo.git
    """

    def __init__(self, remote_url: str):
        super().__init__(remote_url=remote_url)

    def _extract_repo_path(self) -> str:
        url = self.remote_url
        if url.startswith("git@"):
            path = url.split(":", 1)[1]
        else:
            path = url.split("bitbucket.org/")[1]
        return path.removesuffix(".git")

    @property
    def name(self) -> str:
        return "Bitbucket"

    @property
    def repository_url(self) -> str:
        return f"https://bitbucket.org/{self.repo_path}"

    @property
    def pipeline_url(self) -> str:
        return f"https://bitbucket.org/{self.repo_path}/pipelines"

    @property
    def pull_request_url(self) -> str:
        return f"https://bitbucket.org/{self.repo_path}/pull-requests"
