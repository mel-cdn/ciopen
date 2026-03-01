import shutil
import subprocess
from pathlib import Path

import pytest
from typer.testing import CliRunner


def _git(cwd, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    )


@pytest.fixture
def fx_cli_runner():
    return CliRunner()


@pytest.fixture
def fx_git_repo(tmp_path: Path) -> Path:
    """Create a temporary git repository"""

    assert shutil.which("git"), "Installed Git is required for integration tests"

    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()

    # Initialize git
    _git(repo_dir, "init")
    _git(repo_dir, "config", "user.email", "integration@test.com")
    _git(repo_dir, "config", "user.name", "Integration Test User")

    # Create repo file and commit
    (repo_dir / "README.md").write_text("# Temp Repo")
    _git(repo_dir, "add", ".")
    _git(repo_dir, "commit", "-m", "Initial commit")

    return repo_dir
