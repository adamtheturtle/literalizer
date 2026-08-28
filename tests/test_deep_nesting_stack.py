"""Tests that deep input reaches the shared guard, not the stack limit.

A document deeper than the parse-depth guard allows is refused with a
typed error.  Anything below it has to render, which means a per-value
walk must not call itself: a beartype-wrapped call costs several
interpreter frames per level, so such a walk runs out of stack long
before the guard is reached (issue #4560).

The depths here are far too large for a golden fixture, so this stays an
ordinary test.
"""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import JSONParseError
from literalizer.languages import PureScript

_BELOW_GUARD_DEPTH = 400
"""A nesting depth the shared parse-depth guard admits."""

_ABOVE_GUARD_DEPTH = 800
"""A nesting depth the shared parse-depth guard refuses."""


@pytest.mark.parametrize(
    argnames=("opener", "closer"),
    argvalues=[
        pytest.param("[", "]", id="lists"),
        pytest.param('{"a":', "}", id="mappings"),
    ],
)
def test_below_guard_depth_renders(opener: str, closer: str) -> None:
    """Input the guard admits renders rather than exhausting the stack."""
    source = opener * _BELOW_GUARD_DEPTH + "1" + closer * _BELOW_GUARD_DEPTH
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=PureScript(),
    )
    assert result.declaration_code.count("PInt 1") == 1


def test_above_guard_depth_is_a_typed_error() -> None:
    """Past the guard the failure is typed, not a ``RecursionError``."""
    source = "[" * _ABOVE_GUARD_DEPTH + "1" + "]" * _ABOVE_GUARD_DEPTH
    with pytest.raises(
        expected_exception=JSONParseError,
        match="exceeds the supported nesting depth",
    ):
        literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=PureScript(),
        )
