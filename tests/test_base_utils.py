import pytest
from unittest.mock import patch, mock_open
from AIFoundationKit.base.utils import load_config, generate_session_id
from AIFoundationKit.base.exception.custom_exception import ConfigException


def test_load_config_success():
    yaml_content = "key: value"
    with patch("os.path.exists", return_value=True), \
            patch("builtins.open", mock_open(read_data=yaml_content)):
        config = load_config("config.yaml")
        assert config == {"key": "value"}


def test_load_config_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(ConfigException) as excinfo:
            load_config("config.yaml")
        assert "Config file not found" in str(excinfo.value)


def test_load_config_invalid_yaml():
    with patch("os.path.exists", return_value=True), \
            patch("builtins.open", mock_open(read_data=": invalid yaml")):
        with pytest.raises(ConfigException) as excinfo:
            load_config("config.yaml")
        assert "Error parsing YAML file" in str(excinfo.value)


def test_generate_session_id():
    session_id = generate_session_id()
    assert session_id.startswith("session_")
    parts = session_id.split("_")
    assert len(parts) == 4  # session, date, time, uuid
