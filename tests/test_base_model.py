import pytest
from unittest.mock import patch, MagicMock
import os
from AIFoundationKit.base.model import ApiKeyManager
from AIFoundationKit.base.exception.custom_exception import ModelException


def test_api_key_manager_init_env(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "groq_key")
    monkeypatch.setenv("GOOGLE_API_KEY", "google_key")
    mgr = ApiKeyManager(check_keys=True)
    assert mgr.get("GROQ_API_KEY") == "groq_key"
    assert mgr.get("GOOGLE_API_KEY") == "google_key"


def test_api_key_manager_init_json(monkeypatch):
    monkeypatch.setenv(
        "API_KEYS", '{"GROQ_API_KEY": "groq_json", "GOOGLE_API_KEY": "google_json"}')
    mgr = ApiKeyManager(check_keys=True)
    assert mgr.get("GROQ_API_KEY") == "groq_json"
    assert mgr.get("GOOGLE_API_KEY") == "google_json"


def test_api_key_manager_missing_keys(monkeypatch):
    # Ensure no env vars
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("API_KEYS", raising=False)

    # Mock os.getenv to return None for keys
    with patch("os.getenv", return_value=None):
        with pytest.raises(ModelException) as excinfo:
            ApiKeyManager(check_keys=True)
        assert "Missing API keys" in str(excinfo.value)


def test_api_key_manager_get_missing():
    mgr = ApiKeyManager(check_keys=False)
    with pytest.raises(KeyError):
        mgr.get("NONEXISTENT_KEY")
