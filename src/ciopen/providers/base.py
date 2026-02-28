from abc import ABC, abstractmethod


class BaseProvider(ABC):
    def __init__(self, remote_url: str):
        self.remote_url = remote_url
        self.repo_path = self._extract_repo_path()

    @abstractmethod
    def _extract_repo_path(self) -> str:
        ...

    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def repository_url(self) -> str:
        ...

    @abstractmethod
    def pipeline_url(self) -> str:
        ...

    @abstractmethod
    def pull_request_url(self) -> str:
        ...
