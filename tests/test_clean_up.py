import clean_up
import pytest
from unittest.mock import patch, MagicMock, call, mock_open


def test_clean_artifacts():
    with patch("os.path.exists", side_effect=[True, False, False]), patch(
        "shutil.rmtree"
    ) as mock_rmtree, patch("os.walk", return_value=[(".", ["__pycache__"], [])]):

        clean_up.clean_artifacts()

        # Verify build/dist/egg-info removal
        mock_rmtree.assert_any_call("build")

        # Verify __pycache__ removal
        mock_rmtree.assert_any_call("./__pycache__")


def test_should_skip_dir():
    assert clean_up.should_skip_dir(".git") is True
    assert clean_up.should_skip_dir("src") is False


def test_remove_comments_from_file():
    content = """#!/bin/bash
    # This is a comment
    code_line = 1
    # Another comment
    """
    expected = """#!/bin/bash
    code_line = 1
    """

    with patch("builtins.open", mock_open(read_data=content)) as mock_file:
        clean_up.remove_comments_from_file("test.py")

        mock_file.assert_called_with("test.py", "w", encoding="utf-8")
        handle = mock_file()
        # Verify write calls. Approximate check
        args = handle.writelines.call_args[0][0]
        result = "".join(args)
        assert "code_line = 1" in result
        assert "# This is a comment" not in result


def test_process_files():
    with patch("os.walk", return_value=[(".", [], ["test.py"])]), patch(
        "clean_up.remove_comments_from_file"
    ) as mock_remove:

        clean_up.process_files()

        mock_remove.assert_called_with("./test.py")
