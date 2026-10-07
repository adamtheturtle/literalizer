"""Error contracts for input beyond the shared parse-depth guard."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import JSONParseError
from literalizer.languages import PureScript

_ABOVE_GUARD_DEPTH = 800
"""A nesting depth the shared parse-depth guard refuses."""


def test_above_guard_depth_is_a_typed_error() -> None:
    """Past the guard the failure is typed, not a ``RecursionError``."""
    source = "[" * _ABOVE_GUARD_DEPTH + "1" + "]" * _ABOVE_GUARD_DEPTH
    with pytest.raises(
        expected_exception=JSONParseError,
        match="exceeds the supported nesting depth",
    ):
        _ = literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=PureScript(),
        )
