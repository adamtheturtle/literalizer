"""Rejection of same-key-set sibling dicts whose field types conflict
under Java's shared ``RECORD`` strategy.

Two dicts with the same key set share a generated ``record``, but when a
field's scalar value type differs between them one declaration cannot
describe both: the declaration would take the field types of the first
dict and the constructor call for the other dict would not compile
(``incompatible types: String cannot be converted to int``).  The shared
record strategy now splits such dicts into distinct record shapes (issue
#2961, the Java manifestation of #2888), so sibling lists spanning them
fail the mixed-record-shape gate with
:class:`~literalizer.exceptions.HeterogeneousSiblingListsError` rather
than silently emitting mismatched field types.
"""

import textwrap

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import (
    HeterogeneousSiblingListsError,
    UnrepresentableInputError,
)
from literalizer.languages import Java

_SCALAR_TYPE_CONFLICT_YAML = textwrap.dedent(
    text="""\
    - a: 1
    - a: hello
    """,
)


_JAVA_RECORD_STRATEGY = next(
    strategy
    for strategy in Java().heterogeneous_strategies
    if strategy.name == "RECORD"
)


def test_sibling_records_with_conflicting_scalar_field_types_raise() -> None:
    """Sibling dicts with equal key sets but conflicting scalar types
    resolve to distinct record shapes, so the sibling list is rejected
    rather than emitting one record with a mismatched field type.
    """
    language = Java(heterogeneous_strategy=_JAVA_RECORD_STRATEGY)
    with pytest.raises(expected_exception=HeterogeneousSiblingListsError):
        literalize(
            source=_SCALAR_TYPE_CONFLICT_YAML,
            input_format=InputFormat.YAML,
            language=language,
        )


def test_custom_name_for_split_key_set_raises() -> None:
    """A ``record_shape_names`` entry cannot identify one record when
    its key set splits into conflicting field-type shapes, so the input
    is rejected rather than emitting duplicate declarations under the
    custom name.
    """
    language = Java(
        heterogeneous_strategy=_JAVA_RECORD_STRATEGY,
        record_shape_names={frozenset({"a"}): "Payload"},
    )
    source = textwrap.dedent(
        text="""\
        first:
          a: 1
        second:
          a: hello
        """,
    )
    with pytest.raises(expected_exception=UnrepresentableInputError):
        literalize(
            source=source,
            input_format=InputFormat.YAML,
            language=language,
        )
