"""Rejection of sibling maps with incompatible inferred value types."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer._checks import (
    _has_unrepresentable_sibling_maps,  # pyright: ignore[reportPrivateUsage]
)
from literalizer.exceptions import HeterogeneousSiblingMapsError
from literalizer.languages import Rust, V

if TYPE_CHECKING:
    from literalizer._types import Scalar, Value


@pytest.mark.parametrize(argnames="language", argvalues=[Rust(), V()])
def test_typed_sibling_maps_reject_different_value_types(
    language: Language,
) -> None:
    """Narrow map types must agree across one enclosing list slot."""
    with pytest.raises(expected_exception=HeterogeneousSiblingMapsError):
        literalize(
            source='[{"s": "y"}, {"t": 3}]',
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(name="value", modifiers=frozenset()),
            wrap_in_file=True,
        )


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


@pytest.mark.parametrize(argnames="language", argvalues=[Rust(), V()])
def test_deep_sibling_maps_still_reject_incompatible_types(
    language: Language,
) -> None:
    """Recursive empty borrowing must not hide real deep divergence."""
    with pytest.raises(expected_exception=HeterogeneousSiblingMapsError):
        literalize(
            source=(
                '[{"outer":{"inner":{"x":1}}},'
                '{"outer":{"inner":{"x":"different"}}}]'
            ),
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(name="value", modifiers=frozenset()),
            wrap_in_file=True,
        )
