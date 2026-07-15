"""Rejection of same-key-set sibling dicts whose field types conflict
under the Rust ``RECORD`` strategy.

Two dicts with the same key set share a generated struct, but when a
field's value type differs between them (a different scalar type, or a
tuple-eligible array versus a homogeneous list) one struct cannot
describe both, so the struct declaration would take the field types
of the first dict and the literal for the other dict would not
compile (issue #2881).  Such dicts now resolve to distinct record
shapes, so sibling lists spanning them fail the mixed-record-shape
gate with
:class:`~literalizer.exceptions.HeterogeneousSiblingListsError`
rather than silently emitting mismatched field types.  A field whose
sibling values are nested *maps* of divergent or disjoint shape is the
exception: the widening pass renders it as a plain map instead of
rejecting the list (issue #2910), verified here to no longer raise.
The integration framework only exercises golden output that compiles,
so these contracts need unit coverage.
"""

import pytest

from literalizer import InputFormat, Language, literalize
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


def test_sibling_records_with_conflicting_scalar_field_types_raise() -> None:
    """Sibling dicts with equal key sets but a conflicting scalar field
    type resolve to distinct record shapes, so the sibling list is
    rejected rather than emitting one struct with mismatched field
    types.  A scalar field is not a nested map, so the sibling-map
    widening (issue #2910) does not touch it.
    """
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD,
    )
    with pytest.raises(expected_exception=HeterogeneousSiblingListsError):
        literalize(
            source=_SCALAR_TYPE_CONFLICT_YAML,
            input_format=InputFormat.YAML,
            language=language,
        )


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        Rust(heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD),
        Rust(
            heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD,
            record_unify_optional_fields=True,
        ),
    ],
    ids=["no_unify", "unify"],
)
def test_divergent_nested_sibling_maps_widen_instead_of_raising(
    language: Language,
) -> None:
    """Sibling records whose nested map under one key has divergent or
    disjoint shape widen to a plain map (issue #2910): the field wraps
    its scalar leaves in the value enum, so the sibling list renders
    instead of being rejected.  Unification only merges nested shapes
    that share a key, so the disjoint nested maps here still widen under
    ``record_unify_optional_fields`` too.
    """
    result = literalize(
        source=_NESTED_SHAPE_CONFLICT_YAML,
        input_format=InputFormat.YAML,
        language=language,
    )
    widened_struct = (
        "struct Record0 {\n    outer: HashMap<&'static str, Value>,\n}"
    )
    assert result.preamble == (
        "use std::collections::HashMap;",
        "enum Value {\n    Str(&'static str),\n    Bool(bool),\n}",
        widened_struct,
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
