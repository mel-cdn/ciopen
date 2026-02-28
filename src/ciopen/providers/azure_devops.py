from urllib.parse import urlparse

from ciopen.providers.base import BaseProvider


class AzureDevOpsProvider(BaseProvider):
    """
    AzureDevOpsProvider

    Supports:
        HTTPS: https://dev.azure.com/{org}/{project}/_git/{repo}
               https://{org}@dev.azure.com/{org}/{project}/_git/{repo}
        SSH:   git@ssh.dev.azure.com:v3/{org}/{project}/{repo}
    """

    def __init__(self, remote_url: str):
        super().__init__(remote_url=remote_url)

    def _extract_repo_path(self) -> str:
        url = self.remote_url
        # SSH format: git@ssh.dev.azure.com:v3/org/project/repo
        if "ssh.dev.azure.com" in url:
            path = url.split(":", 1)[1]  # v3/org/project/repo
            path = path.removeprefix("v3/")
            return path

        # HTTPS formats (optionally with userinfo like `org@` in the netloc):
        # - https://dev.azure.com/org/project/_git/repo
        # - https://org@dev.azure.com/org/project/_git/repo
        parsed = urlparse(url)
        path = parsed.path.lstrip("/")  # org/project/_git/repo
        return path.removesuffix(".git")

    @property
    def name(self) -> str:
        return "Azure DevOps"

    @property
    def repository_url(self) -> str:
        # Expect repo_path to be: org/project/_git/repo  OR org/project/repo (ssh-derived)
        if "/_git/" in self.repo_path:
            return f"https://dev.azure.com/{self.repo_path}"

        # If extracted from SSH, normalize to HTTPS repo URL
        org, project, repo = self.repo_path.split("/", 2)
        return f"https://dev.azure.com/{org}/{project}/_git/{repo}"

    @property
    def pipeline_url(self) -> str:
        # Pipelines are project-scoped; this opens the build/pipelines area for the project.
        if "/_git/" in self.repo_path:
            org, project, _git, _repo = self.repo_path.split("/", 3)
        else:
            org, project, _repo = self.repo_path.split("/", 2)
        return f"https://dev.azure.com/{org}/{project}/_build"

    @property
    def pull_request_url(self) -> str:
        # PRs are repo-scoped.
        if "/_git/" in self.repo_path:
            return f"https://dev.azure.com/{self.repo_path}/pullrequests"

        org, project, repo = self.repo_path.split("/", 2)
        return f"https://dev.azure.com/{org}/{project}/_git/{repo}/pullrequests"
