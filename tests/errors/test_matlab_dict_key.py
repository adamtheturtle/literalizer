"""Tests for MATLAB dict-key formatting errors."""

import pytest

from literalizer.exceptions import InvalidDictKeyError
from literalizer.languages import Matlab


def test_matlab_key_formatter_rejects_non_string_source_key() -> None:
    """Reject a non-string key even if called after normal validation."""
    with pytest.raises(
        expected_exception=InvalidDictKeyError,
        match="dict key 1",
    ):
        _ = Matlab().dict_format_config.format_key(1, "1")
