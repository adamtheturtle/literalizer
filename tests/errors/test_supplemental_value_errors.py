"""Error contracts for cyclic and deeply nested supplemental Python values.

These values cannot be declared in a rejection manifest.
"""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import InvalidValueInputError
from literalizer.languages import Python

type _RecursiveIntValue = int | list[_RecursiveIntValue]


def test_cyclic_supplemental_values_raise_typed_error() -> None:
    """Cyclic Python-value arguments never leak ``RecursionError``."""
    cycle: list[_RecursiveIntValue] = []
    cycle.append(cycle)

    with pytest.raises(
        expected_exception=InvalidValueInputError,
        match="ref_values",
    ):
        _ = literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=Python(),
            ref_values={"value": cycle},
        )
    with pytest.raises(
        expected_exception=InvalidValueInputError,
        match="bound_refs",
    ):
        _ = literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=Python(),
            bound_refs={"value": cycle},
        )
    with pytest.raises(
        expected_exception=InvalidValueInputError,
        match="record_null_substitutions",
    ):
        _ = literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=Python(),
            record_null_substitutions={"value": cycle},
        )


def test_deep_supplemental_value_raises_typed_error() -> None:
    """Deep cycle-free Python values avoid leaking recursion errors."""
    value: _RecursiveIntValue = 0
    for _ in range(2_000):
        value = [value]

    with pytest.raises(
        expected_exception=InvalidValueInputError,
        match=(
            "ref_values must contain an acyclic value within the supported "
            "nesting depth"
        ),
    ):
        _ = literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=Python(),
            ref_values={"value": value},
        )
