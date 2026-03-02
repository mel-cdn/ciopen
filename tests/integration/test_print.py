from contextlib import chdir

from ciopen import __author__, __version__, cli


def test_version_command_should_print_current_version(fx_git_repo, fx_cli_runner):
    with chdir(fx_git_repo):
        result = fx_cli_runner.invoke(cli.app, ["version"])

    assert result.exit_code == 0
    assert f"ciopen {__version__}" in result.output


def test_info_command_should_print_information(fx_git_repo, fx_cli_runner):
    with chdir(fx_git_repo):
        result = fx_cli_runner.invoke(cli.app, ["info"])

    assert result.exit_code == 0
    assert f"ciopen {__version__}" in result.output
    assert f"Author: {__author__}" in result.output
    assert f"Homepage: https://github.com/mel-cdn/ciopen" in result.output
