from ciopen.providers.base import BaseProvider


class GitLabProvider(BaseProvider):
    """
    GitLabProvider (GitLab.com)

    Supports:
        SSH:   git@gitlab.com:group/subgroup/repo.git
        HTTPS: https://gitlab.com/group/subgroup/repo.git
    """

    def __init__(self, remote_url: str):
        super().__init__(remote_url=remote_url)

    def _extract_repo_path(self) -> str:
        url = self.remote_url
        if url.startswith("git@"):
            path = url.split(":", 1)[1]
        else:
            path = url.split("gitlab.com/")[1]
        return path.removesuffix(".git")

    @property
    def name(self) -> str:
        return "GitLab"

    @property
    def repository_url(self) -> str:
        return f"https://gitlab.com/{self.repo_path}"

    @property
    def pipeline_url(self) -> str:
        return f"https://gitlab.com/{self.repo_path}/-/pipelines"

    @property
    def pull_request_url(self) -> str:
        # GitLab calls them Merge Requests
        return f"https://gitlab.com/{self.repo_path}/-/merge_requests"
