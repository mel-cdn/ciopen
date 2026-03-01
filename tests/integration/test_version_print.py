from contextlib import chdir

from ciopen import __version__, cli


def test_version_command_should_print_current_version(fx_git_repo, fx_cli_runner):
    with chdir(fx_git_repo):
        result = fx_cli_runner.invoke(cli.app, ["version"])

    assert result.exit_code == 0
    assert f"ciopen {__version__}" in result.output
