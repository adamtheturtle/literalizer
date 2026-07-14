"""Rejection of same-key-set sibling dicts whose field types conflict
under Go's shared ``RECORD`` strategy.

Two dicts with the same key set share a generated struct, but when a
field's value type differs between them (a nested record with different
fields, or a different scalar type) one struct cannot describe both, so
the struct declaration would take the field types of the first dict and
the literal for the other dict would not compile.  The shared record
strategy now splits such dicts into distinct record shapes (issue
#2888), so sibling lists spanning them fail the mixed-record-shape gate
with :class:`~literalizer.exceptions.HeterogeneousSiblingListsError`
rather than silently emitting mismatched field types.  The integration
framework only exercises golden output that compiles, so these
rejection contracts need unit coverage.
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
    urgent: true
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


@pytest.mark.parametrize(
    argnames="source",
    argvalues=[
        _NESTED_SHAPE_CONFLICT_YAML,
        _SCALAR_TYPE_CONFLICT_YAML,
    ],
)
def test_sibling_records_with_conflicting_field_types_raise(
    source: str,
) -> None:
    """Sibling dicts with equal key sets but conflicting field types
    resolve to distinct record shapes, so the sibling list is rejected
    rather than emitting one struct with mismatched field types.
    """
    language = Go(heterogeneous_strategy=_GO_RECORD_STRATEGY)
    with pytest.raises(expected_exception=HeterogeneousSiblingListsError):
        literalize(
            source=source,
            input_format=InputFormat.YAML,
            language=language,
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
