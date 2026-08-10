"""COBOL empty-string representation tests."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableStringError
from literalizer.languages import Cobol


def test_cobol_rejects_empty_string_literal() -> None:
    """Plain COBOL never emits an illegal zero-length literal."""
    with pytest.raises(expected_exception=UnrepresentableStringError):
        literalize(
            source='{"e": ""}',
            input_format=InputFormat.JSON,
            language=Cobol(),
        )
