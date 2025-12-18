import pytest
from unittest.mock import MagicMock, patch, mock_open
import os
import json
from AIFoundationKit.base.file_manager import BaseFileManager
from AIFoundationKit.base.exception.custom_exception import AppException

# Concrete implementation for testing abstract base class


class ConcreteFileManager(BaseFileManager):
    pass


@pytest.fixture
def file_manager():
    return ConcreteFileManager()


def test_read_file_not_found(file_manager):
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            file_manager.read_file("nonexistent.txt")


def test_read_file_txt(file_manager):
    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data="content")
    ):
        assert file_manager.read_file("test.txt") == "content"


def test_read_file_unsupported(file_manager):
    with patch("os.path.exists", return_value=True):
        with pytest.raises(AppException) as excinfo:
            file_manager.read_file("test.xyz")
        assert "Unsupported file format" in str(excinfo.value)


def test_read_file_json(file_manager):
    data = {"key": "value"}
    json_str = json.dumps(data)
    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data=json_str)
    ):
        result = file_manager.read_file("test.json")
        assert '"key": "value"' in result


def test_read_file_exception(file_manager):
    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", side_effect=Exception("Read error")
    ):
        with pytest.raises(AppException) as excinfo:
            file_manager.read_file("test.txt")
        assert "Failed to read file" in str(excinfo.value)


def test_save_file_bytes(file_manager):
    with patch("pathlib.Path.mkdir"), patch("builtins.open", mock_open()) as mock_file:
        path = file_manager.save_file(b"content", "/tmp", "test.txt")
        mock_file.assert_called_with("/tmp/test.txt", "wb")
        mock_file().write.assert_called_with(b"content")
        assert path == os.path.abspath("/tmp/test.txt")


def test_save_file_obj_with_name(file_manager):
    mock_obj = MagicMock()
    mock_obj.name = "test.txt"
    mock_obj.read.return_value = b"content"

    with patch("pathlib.Path.mkdir"), patch("builtins.open", mock_open()) as mock_file:
        file_manager.save_file(mock_obj, "/tmp")
        mock_file().write.assert_called_with(b"content")


def test_save_file_no_name_error(file_manager):
    mock_obj = MagicMock(spec=[])  # No name attribute
    with patch("pathlib.Path.mkdir"):
        with pytest.raises(AppException) as excinfo:
            file_manager.save_file(mock_obj, "/tmp")
        assert "File name must be provided" in str(excinfo.value)
