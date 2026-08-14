from pathlib import Path
from unittest.mock import patch

from ciopen import config


@patch.dict("os.environ", {"XDG_CONFIG_HOME": "/xdg/config"}, clear=False)
def test_get_config_path_uses_xdg_config_home():
    assert config.get_config_path() == Path("/xdg/config/ciopen/config.json")


@patch.dict("os.environ", {}, clear=True)
@patch(f"{config.__name__}.Path.home", return_value=Path("/home/user"))
def test_get_config_path_defaults_to_dot_config(m_home):
    assert config.get_config_path() == Path("/home/user/.config/ciopen/config.json")


def test_load_config_returns_empty_dict_when_file_missing(tmp_path):
    with patch(f"{config.__name__}.get_config_path", return_value=tmp_path / "missing.json"):
        assert config.load_config() == {}


def test_save_config_then_load_config_round_trips(tmp_path):
    path = tmp_path / "nested" / "config.json"

    with patch(f"{config.__name__}.get_config_path", return_value=path):
        config.save_config({"jira_base_url": "https://example.atlassian.net"})
        assert config.load_config() == {"jira_base_url": "https://example.atlassian.net"}


def test_get_jira_base_url_returns_none_when_not_set(tmp_path):
    with patch(f"{config.__name__}.get_config_path", return_value=tmp_path / "config.json"):
        assert config.get_jira_base_url() is None


def test_set_jira_base_url_strips_trailing_slash_and_persists(tmp_path):
    path = tmp_path / "config.json"

    with patch(f"{config.__name__}.get_config_path", return_value=path):
        config.set_jira_base_url("https://example.atlassian.net/")
        assert config.get_jira_base_url() == "https://example.atlassian.net"


def test_set_jira_base_url_preserves_other_keys(tmp_path):
    path = tmp_path / "config.json"

    with patch(f"{config.__name__}.get_config_path", return_value=path):
        config.save_config({"other_key": "value"})
        config.set_jira_base_url("https://example.atlassian.net")
        assert config.load_config() == {
            "other_key": "value",
            "jira_base_url": "https://example.atlassian.net",
        }


def test_unset_jira_base_url_removes_key(tmp_path):
    path = tmp_path / "config.json"

    with patch(f"{config.__name__}.get_config_path", return_value=path):
        config.set_jira_base_url("https://example.atlassian.net")
        config.unset_jira_base_url()
        assert config.get_jira_base_url() is None


def test_unset_jira_base_url_preserves_other_keys(tmp_path):
    path = tmp_path / "config.json"

    with patch(f"{config.__name__}.get_config_path", return_value=path):
        config.save_config({"other_key": "value"})
        config.set_jira_base_url("https://example.atlassian.net")
        config.unset_jira_base_url()
        assert config.load_config() == {"other_key": "value"}


def test_unset_jira_base_url_noop_when_not_set(tmp_path):
    path = tmp_path / "config.json"

    with patch(f"{config.__name__}.get_config_path", return_value=path):
        config.unset_jira_base_url()
        assert config.get_jira_base_url() is None
