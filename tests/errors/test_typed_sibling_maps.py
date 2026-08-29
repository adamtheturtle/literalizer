"""Sibling maps whose value types agree, and the check that pools them.

The rejections are declared in ``tests/errors/rejections`` and run by
``test_rejections.py``.  What is left here is the acceptance side --
which no rejection manifest expresses -- and the one call that reaches
the pooling check directly, for a shape ``literalize`` cannot build.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer._checks import (
    _has_unrepresentable_sibling_maps,  # pyright: ignore[reportPrivateUsage]
)
from literalizer.languages import Rust, V

if TYPE_CHECKING:
    from literalizer._types import Scalar, Value


@pytest.mark.parametrize(argnames="language", argvalues=[Rust(), V()])
def test_typed_sibling_maps_allow_same_value_type(language: Language) -> None:
    """Different keys do not matter when every map value type agrees."""
    for source in ('[{"s": 1}, {"t": 3}]', '[{"m": {}}, {"m": {}}]'):
        literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(name="value", modifiers=frozenset()),
            wrap_in_file=True,
        )


@pytest.mark.parametrize(argnames="language", argvalues=[Rust(), V()])
def test_unrelated_record_does_not_exempt_typed_sibling_maps(
    language: Language,
) -> None:
    """A record elsewhere must not disable this list's type check."""
    unrelated_record: dict[Scalar, Value] = {"value": 1}
    string_map: dict[Scalar, Value] = {"s": "y"}
    integer_map: dict[Scalar, Value] = {"t": 3}
    incompatible_maps: list[Value] = [string_map, integer_map]
    data: list[Value] = [unrelated_record, incompatible_maps]

    assert _has_unrepresentable_sibling_maps(
        data=data,
        spec=language,
        record_dict_ids=frozenset({id(unrelated_record)}),
        tuple_list_ids=frozenset(),
    )
