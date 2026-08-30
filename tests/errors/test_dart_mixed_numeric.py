"""Dart mixed-numeric container validation."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableIntegerError
from literalizer.languages import Dart


def test_dart_rejects_integer_too_large_to_convert_to_double() -> None:
    """An overflowing conversion is an ordinary imprecise integer."""
    huge = "1" + ("0" * 400)
    with pytest.raises(expected_exception=UnrepresentableIntegerError):
        literalize(
            source=f'{{"f": 1.5, "n": {huge}}}',
            input_format=InputFormat.JSON,
            language=Dart(),
        )


def test_dart_mixed_numeric_set_keeps_integer_identity() -> None:
    """A set infers ``num`` and need not convert its integer to double."""
    result = literalize(
        source="!!set\n1.5: null\n9007199254740993: null\n",
        input_format=InputFormat.YAML,
        language=Dart(),
    )
    assert "9007199254740993" in result.code
