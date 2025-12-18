import logging
import pytest
from unittest.mock import patch, MagicMock
from AIFoundationKit.base.logger.custom_logger import (
    get_logger,
    JsonFormatter,
    ColorFormatter,
)
from AIFoundationKit.base.logger.logger_utils import add_context, ContextAdapter


def test_json_formatter():
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="message",
        args=(),
        exc_info=None,
    )
    formatted = formatter.format(record)
    assert '"message": "message"' in formatted
    assert '"level": "INFO"' in formatted


def test_color_formatter():
    formatter = ColorFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="message",
        args=(),
        exc_info=None,
    )
    formatted = formatter.format(record)
    assert "\033[0;32m" in formatted  # Green for INFO


def test_get_logger():
    # Patch os.makedirs to avoid creating directories
    with patch("os.makedirs"), patch("logging.FileHandler"):
        logger = get_logger("test_logger")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger"


def test_context_adapter():
    logger = MagicMock()
    adapter = add_context(logger, key="value")
    assert isinstance(adapter, ContextAdapter)
    assert adapter.extra["key"] == "value"

    msg, kwargs = adapter.process("msg", {})
    assert kwargs["extra"]["key"] == "value"
