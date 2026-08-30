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
