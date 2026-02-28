# tests/unit/commands/test_doctor.py
from unittest.mock import Mock, call, patch

from ciopen.commands.doctor import doctor_command


@patch(f"{doctor_command.__module__}.get_current_branch", spec=True)
@patch(f"{doctor_command.__module__}.extract_repository_slug", spec=True)
@patch(f"{doctor_command.__module__}.detect_provider", spec=True)
@patch(f"{doctor_command.__module__}.get_remote_url", spec=True)
@patch(f"{doctor_command.__module__}.is_inside_git_repo", spec=True)
@patch(f"{doctor_command.__module__}.get_version", spec=True)
@patch(f"{doctor_command.__module__}.typer.echo", spec=True)
@patch(f"{doctor_command.__module__}.__version__", "1.2.3")
def test_doctor_command_happy_path_prints_checks_and_environment_details(
    m_echo,
    m_get_version,
    m_is_inside_git_repo,
    m_get_remote_url,
    m_detect_provider,
    m_extract_repository_slug,
    m_get_current_branch,
):
    # Setup mocks
    provider = Mock(
        name="GitHub",
        remote_url="https://github.com/org/repo.git",
        repository_url="https://github.com/org/repo",
        pipeline_url="https://github.com/org/repo/actions",
        pull_request_url="https://github.com/org/repo/pulls",
    )

    m_get_version.return_value = "git version 2.x"
    m_is_inside_git_repo.return_value = True
    m_get_remote_url.return_value = provider.remote_url
    m_detect_provider.return_value = provider
    m_extract_repository_slug.return_value = "org/repo"
    m_get_current_branch.return_value = "main"

    # Act
    assert doctor_command() is None

    # Ensure everything was printed
    assert m_echo.mock_calls == [
        call("ciopen 1.2.3"),
        call("Running diagnostics...\n"),
        call("✅ Git installed"),
        call("✅ Inside a Git repository"),
        call("✅ Remote origin found"),
        call("✅ CI Provider detected"),
        call("\nEnvironment details:\n"),
        call(f"Provider\t: {provider.name}"),
        call("Repository\t: org/repo"),
        call("Current branch\t: main"),
        call("Repository URL\t: https://github.com/org/repo"),
        call("Pipeline URL\t: https://github.com/org/repo/actions"),
        call("Pull Request URL: https://github.com/org/repo/pulls"),
    ]

    # Ensure that everything is called correctly
    assert m_get_version.mock_calls == [call()]
    assert m_is_inside_git_repo.mock_calls == [call()]
    assert m_get_remote_url.mock_calls == [call()]
    assert m_detect_provider.mock_calls == [call()]
    assert m_extract_repository_slug.mock_calls == [call(remote_url=provider.remote_url)]
    assert m_get_current_branch.mock_calls == [call()]


@patch(f"{doctor_command.__module__}.get_current_branch", spec=True)
@patch(f"{doctor_command.__module__}.extract_repository_slug", spec=True)
@patch(f"{doctor_command.__module__}.detect_provider", spec=True)
@patch(f"{doctor_command.__module__}.get_remote_url", side_effect=Exception("No remote found"))
@patch(f"{doctor_command.__module__}.is_inside_git_repo", side_effect=Exception("Not a git repo"))
@patch(f"{doctor_command.__module__}.get_version", side_effect=Exception("No git installed!"))
@patch(f"{doctor_command.__module__}.typer.echo", spec=True)
@patch(f"{doctor_command.__module__}.__version__", "1.2.3")
def test_doctor_command_when_remote_missing_skips_provider_and_details(
    m_echo,
    m_get_version,
    m_is_inside_git_repo,
    m_get_remote_url,
    m_detect_provider,
    m_extract_repository_slug,
    m_get_current_branch,
):
    # Act
    assert doctor_command() is None

    # Ensure everything was printed correctly
    assert m_echo.mock_calls == [
        call("ciopen 1.2.3"),
        call("Running diagnostics...\n"),
        call("❌ Git installed"),
        call("❌ Inside a Git repository"),
        call("❌ Remote origin found"),
    ]

    # Ensure that everything is called correctly
    assert m_get_version.mock_calls == [call()]
    assert m_is_inside_git_repo.mock_calls == [call()]
    assert m_get_remote_url.mock_calls == [call()]
    assert m_detect_provider.mock_calls == []
    assert m_extract_repository_slug.mock_calls == []
    assert m_get_current_branch.mock_calls == []


@patch(f"{doctor_command.__module__}.get_current_branch", spec=True)
@patch(f"{doctor_command.__module__}.extract_repository_slug", spec=True)
@patch(f"{doctor_command.__module__}.detect_provider", side_effect=Exception("No provider found"))
@patch(f"{doctor_command.__module__}.get_remote_url", spec=True)
@patch(f"{doctor_command.__module__}.is_inside_git_repo", side_effect=Exception("Not a git repo"))
@patch(f"{doctor_command.__module__}.get_version", side_effect=Exception("No git installed!"))
@patch(f"{doctor_command.__module__}.typer.echo", spec=True)
@patch(f"{doctor_command.__module__}.__version__", "1.2.3")
def test_doctor_command_with_remote_but_no_provider_skips_details(
    m_echo,
    m_get_version,
    m_is_inside_git_repo,
    m_get_remote_url,
    m_detect_provider,
    m_extract_repository_slug,
    m_get_current_branch,
):
    # Setup mocks
    m_get_remote_url.return_value = "https://github.com/org/repo.git"

    # Act
    assert doctor_command() is None

    # Ensure everything was printed correctly
    assert m_echo.mock_calls == [
        call("ciopen 1.2.3"),
        call("Running diagnostics...\n"),
        call("❌ Git installed"),
        call("❌ Inside a Git repository"),
        call("✅ Remote origin found"),
        call("❌ CI Provider detection failed"),
    ]

    # Ensure that everything is called correctly
    assert m_get_version.mock_calls == [call()]
    assert m_is_inside_git_repo.mock_calls == [call()]
    assert m_get_remote_url.mock_calls == [call()]
    assert m_detect_provider.mock_calls == [call()]
    assert m_extract_repository_slug.mock_calls == []
    assert m_get_current_branch.mock_calls == []


@patch(f"{doctor_command.__module__}.get_current_branch", side_effect=Exception("No git installed!"))
@patch(f"{doctor_command.__module__}.extract_repository_slug", spec=True)
@patch(f"{doctor_command.__module__}.detect_provider", spec=True)
@patch(f"{doctor_command.__module__}.get_remote_url", spec=True)
@patch(f"{doctor_command.__module__}.is_inside_git_repo", spec=True)
@patch(f"{doctor_command.__module__}.get_version", spec=True)
@patch(f"{doctor_command.__module__}.typer.echo", spec=True)
@patch(f"{doctor_command.__module__}.__version__", "1.2.3")
def test_doctor_command_when_show_results_fails_prints_warning(
    m_echo,
    m_get_version,
    m_is_inside_git_repo,
    m_get_remote_url,
    m_detect_provider,
    m_extract_repository_slug,
    m_get_current_branch,
):
    # Setup mocks
    provider = Mock(
        name="GitHub",
        remote_url="https://github.com/org/repo.git",
        repository_url="https://github.com/org/repo",
        pipeline_url="https://github.com/org/repo/actions",
        pull_request_url="https://github.com/org/repo/pulls",
    )

    m_get_version.return_value = "git version 2.x"
    m_is_inside_git_repo.return_value = True
    m_get_remote_url.return_value = provider.remote_url
    m_detect_provider.return_value = provider
    m_extract_repository_slug.return_value = "org/repo"

    # Act
    assert doctor_command() is None

    # Ensure everything was printed correctly
    assert m_echo.mock_calls == [
        call("ciopen 1.2.3"),
        call("Running diagnostics...\n"),
        call("✅ Git installed"),
        call("✅ Inside a Git repository"),
        call("✅ Remote origin found"),
        call("✅ CI Provider detected"),
        call("\nEnvironment details:\n"),
        call(f"Provider\t: {provider.name}"),
        call("Repository\t: org/repo"),
        call("\n⚠️  Unable to compute full environment details."),
    ]

    # Ensure that everything is called correctly
    assert m_get_version.mock_calls == [call()]
    assert m_is_inside_git_repo.mock_calls == [call()]
    assert m_get_remote_url.mock_calls == [call()]
    assert m_detect_provider.mock_calls == [call()]
    assert m_extract_repository_slug.mock_calls == [call(remote_url=provider.remote_url)]
    assert m_get_current_branch.mock_calls == [call()]
