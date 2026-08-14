import json
import os
from pathlib import Path

CONFIG_DIR_NAME = "ciopen"
CONFIG_FILE_NAME = "config.json"


def get_config_path() -> Path:
    """Path to the ciopen config file, honoring XDG_CONFIG_HOME."""
    config_home = os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")
    return Path(config_home) / CONFIG_DIR_NAME / CONFIG_FILE_NAME


def load_config() -> dict:
    path = get_config_path()
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def save_config(config: dict) -> None:
    path = get_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, indent=2))


def get_jira_base_url() -> str | None:
    return load_config().get("jira_base_url")


def set_jira_base_url(base_url: str) -> None:
    config = load_config()
    config["jira_base_url"] = base_url.rstrip("/")
    save_config(config)


def unset_jira_base_url() -> None:
    config = load_config()
    config.pop("jira_base_url", None)
    save_config(config)
