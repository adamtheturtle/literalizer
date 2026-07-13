"""Rejection of same-key-set sibling dicts whose field types conflict
under the Rust ``RECORD`` strategy.

Two dicts with the same key set share a generated struct, but when a
field's value type differs between them (a nested record with
different fields, or a different scalar type) one struct cannot
describe both, so the struct declaration would take the field types
of the first dict and the literal for the other dict would not
compile (issue #2881).  Such dicts now resolve to distinct record
shapes, so sibling lists spanning them fail the mixed-record-shape
gate with
:class:`~literalizer.exceptions.HeterogeneousSiblingListsError`
rather than silently emitting mismatched field types.  The
integration framework only exercises golden output that compiles, so
these contracts need unit coverage.
"""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import (
    HeterogeneousScalarCollectionError,
    HeterogeneousSiblingListsError,
    UnrepresentableInputError,
)
from literalizer.languages import Rust

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

_TUPLE_VERSUS_LIST_CONFLICT_YAML = """
- a:
    - 1
    - x
- a:
    - 2
    - 3
"""

_MIXED_LIST_FIELD_YAML = """
- a:
    - 1
    - x
"""


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
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD,
    )
    with pytest.raises(expected_exception=HeterogeneousSiblingListsError):
        literalize(
            source=source,
            input_format=InputFormat.YAML,
            language=language,
        )


def test_conflict_not_rescued_by_optional_field_unification() -> None:
    """Unification only merges nested shapes that share a key; nested
    records with disjoint key sets still conflict, so the sibling list
    is rejected under ``record_unify_optional_fields`` too.
    """
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD,
        record_unify_optional_fields=True,
    )
    with pytest.raises(expected_exception=HeterogeneousSiblingListsError):
        literalize(
            source=_NESTED_SHAPE_CONFLICT_YAML,
            input_format=InputFormat.YAML,
            language=language,
        )


def test_tuple_field_versus_homogeneous_list_field_raises() -> None:
    """Under ``TUPLE``, a record whose field is a tuple-eligible
    heterogeneous array conflicts with a same-key-set sibling whose
    field is a homogeneous list (fixed-size tuple versus ``Vec``), so
    the sibling list is rejected.
    """
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.TUPLE,
    )
    with pytest.raises(expected_exception=HeterogeneousSiblingListsError):
        literalize(
            source=_TUPLE_VERSUS_LIST_CONFLICT_YAML,
            input_format=InputFormat.YAML,
            language=language,
        )


def test_custom_name_for_split_key_set_raises() -> None:
    """A ``record_shape_names`` entry cannot identify one struct when
    its key set splits into conflicting field-type shapes, so the
    input is rejected rather than emitting duplicate declarations
    under the custom name.
    """
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD,
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


def test_mixed_list_field_still_rejected_after_shape_computation() -> None:
    """A record field holding a list of mixed scalar types (not
    tuple-eligible because ``TUPLE`` is not active) passes shape
    computation without splitting anything and is still rejected by
    the heterogeneous-scalar gate that runs afterwards.
    """
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD,
    )
    with pytest.raises(expected_exception=HeterogeneousScalarCollectionError):
        literalize(
            source=_MIXED_LIST_FIELD_YAML,
            input_format=InputFormat.YAML,
            language=language,
        )
