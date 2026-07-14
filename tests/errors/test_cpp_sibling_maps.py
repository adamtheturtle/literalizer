"""Rejection of unrepresentable sibling maps under C++'s variant typing.

Sibling dict values that are themselves maps share one declared value
type in the enclosing container.  Go and Kotlin widen the narrower inner
maps to a stable "accepts anything" value type (``map[string]any`` /
``Any?``) so each literal fits its declared slot (issue #2878), but
C++'s dict opener builds a content-specific ``std::variant`` value type
with no such fallback, so a narrower inner map does not convert to the
widened slot.  ``literalize`` therefore raises
:class:`~literalizer.exceptions.HeterogeneousSiblingMapsError` rather
than emitting non-compiling code (issue #2891).  The integration
framework catches :class:`HeterogeneousCollectionError` and silently
skips, so this contract has no golden-file surface and needs unit
coverage.
"""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import HeterogeneousSiblingMapsError
from literalizer.languages import Cpp

# The issue #2878 reproducer: two elements whose ``input`` and
# ``expected`` maps disagree on their value types, so the enclosing
# vector declares a widened map slot the narrower maps do not fit.
_SIBLING_MAPS_YAML = (
    "- input: {kind: add, item_id: item_1, urgent: true}\n"
    "  expected: {item_id: item_1, state: pending}\n"
    "- input: {kind: remove, item_id: item_9}\n"
    "  expected: {error: not_found}\n"
)
# Divergent sibling maps within a single dict's value slot.
_WITHIN_DICT_YAML = "a: {x: 1}\nb: {y: two}\n"


@pytest.mark.parametrize(
    argnames="source",
    argvalues=[_SIBLING_MAPS_YAML, _WITHIN_DICT_YAML],
)
def test_cpp_rejects_unrepresentable_sibling_maps(source: str) -> None:
    """C++ raises rather than emitting non-compiling variant maps."""
    with pytest.raises(expected_exception=HeterogeneousSiblingMapsError):
        literalize(
            source=source,
            input_format=InputFormat.YAML,
            language=Cpp(),
        )
