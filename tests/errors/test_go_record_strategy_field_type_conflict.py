"""Rejection of same-key-set sibling dicts whose field types conflict
under Go's shared ``RECORD`` strategy.

Two dicts with the same key set share a generated struct, but when a
field's scalar value type differs between them one struct cannot describe
both, so
the struct declaration would take the field types of the first dict and
the literal for the other dict would not compile.  The shared record
strategy now splits such dicts into distinct record shapes (issue
#2888), so sibling lists spanning them fail the mixed-record-shape gate
with :class:`~literalizer.exceptions.HeterogeneousSiblingListsError`
rather than silently emitting mismatched field types.  Nested sibling
maps with divergent or disjoint shapes are widened to ``map[string]any``
instead (issue #2911), preserving the uniform outer record.
"""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import (
    HeterogeneousSiblingListsError,
    UnrepresentableInputError,
)
from literalizer.languages import Go

_NESTED_SHAPE_CONFLICT_YAML = """
- outer:
    kind: add
    priority: high
- outer:
    error: not_found
"""

_SCALAR_TYPE_CONFLICT_YAML = """
- a: 1
- a: hello
"""


_GO_RECORD_STRATEGY = next(
    strategy
    for strategy in Go().heterogeneous_strategies
    if strategy.name == "RECORD"
)


def test_sibling_records_with_conflicting_scalar_field_types_raise() -> None:
    """Sibling dicts with equal key sets but conflicting scalar types
    resolve to distinct record shapes, so the sibling list is rejected
    rather than emitting one struct with a mismatched field type.
    """
    language = Go(heterogeneous_strategy=_GO_RECORD_STRATEGY)
    with pytest.raises(expected_exception=HeterogeneousSiblingListsError):
        literalize(
            source=_SCALAR_TYPE_CONFLICT_YAML,
            input_format=InputFormat.YAML,
            language=language,
        )


def test_divergent_nested_sibling_maps_widen_instead_of_raising() -> None:
    """Divergent nested sibling maps fall back to ``map[string]any``
    while their enclosing sibling records keep one generated struct,
    even though every raw map value is a string and would otherwise
    infer the narrower ``map[string]string`` literal type.
    """
    language = Go(heterogeneous_strategy=_GO_RECORD_STRATEGY)

    result = literalize(
        source=_NESTED_SHAPE_CONFLICT_YAML,
        input_format=InputFormat.YAML,
        language=language,
    )

    assert result.preamble == (
        "package main",
        "type Record0 struct {\n\tOuter map[string]any\n}",
    )
    assert result.code == (
        "[]any{\n"
        '\tRecord0{Outer: map[string]any{"kind": "add", '
        '"priority": "high"}},\n'
        '\tRecord0{Outer: map[string]any{"error": "not_found"}},\n'
        "}"
    )


def test_custom_name_for_split_key_set_raises() -> None:
    """A ``record_shape_names`` entry cannot identify one struct when
    its key set splits into conflicting field-type shapes, so the input
    is rejected rather than emitting duplicate declarations under the
    custom name.
    """
    language = Go(
        heterogeneous_strategy=_GO_RECORD_STRATEGY,
        record_shape_names={frozenset({"a"}): "Payload"},
    )
    source = """
first:
  a: 1
second:
  a: hello
"""
    with pytest.raises(expected_exception=UnrepresentableInputError):
        literalize(
            source=source,
            input_format=InputFormat.YAML,
            language=language,
        )
