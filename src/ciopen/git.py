import re
import subprocess


def _run_command(args: list[str]) -> str:
    """Run a git command and return the output."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def extract_repository_slug(remote_url: str) -> str:
    """
    Convert git remote URL to 'owner/repo' format.
    Works for HTTPS and SSH URLs, strips trailing '.git'.
    """
    # Remove .git if present
    slug = remote_url.rstrip(".git")
    # Remove protocol/host
    slug = re.sub(r"^(git@[^:]+:|https://[^/]+/)", "", slug)

    # Azure DevOps SSH remotes have an extra `v3/` prefix:
    # git@ssh.dev.azure.com:v3/org/project/repo  -> org/project/repo
    # org/project/_git/repo -> org/project/repo
    slug = slug.removeprefix("v3/")
    slug = slug.replace("/_git/", "/")

    return slug


def get_version() -> str:
    """Get the version of git installed on the system."""
    return _run_command(["version"])


def get_remote_url() -> str:
    """Get the remote URL for the current repository."""
    return _run_command(["remote", "get-url", "origin"])


def is_inside_git_repo() -> bool:
    """Check if the current directory is inside a git repository."""
    return _run_command(["rev-parse", "--is-inside-work-tree"]) == "true"


def get_current_branch() -> str:
    """Get the name of the current branch."""
    return _run_command(["rev-parse", "--abbrev-ref", "HEAD"])
