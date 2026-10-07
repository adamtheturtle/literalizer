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
from literalizer.languages import PureScript

_BELOW_GUARD_DEPTH = 400
"""A nesting depth the shared parse-depth guard admits."""


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
