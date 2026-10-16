"""Public contracts for null reference knowledge and optional hints."""

import pytest

from literalizer import (
    InputFormat,
    ValueInput,
    literalize_call,
)
from literalizer.languages import Cpp


@pytest.mark.parametrize(
    argnames=("bound_value", "hint", "expected_code"),
    argvalues=[
        ([1, 2], None, "consume(std::move(item));"),
        (None, [1, 2], "consume(item);"),
    ],
)
def test_cpp_null_consumption_uses_bound_value(
    bound_value: ValueInput, hint: ValueInput, expected_code: str
) -> None:
    """Actual bindings determine null ownership without replacing
    hints.
    """
    result = literalize_call(
        source='{"$ref": "item"}',
        input_format=InputFormat.JSON,
        language=Cpp(),
        target_function="consume",
        parameter_names=["value"],
        per_element=False,
        ref_key="$ref",
        bound_refs={"item": bound_value},
        ref_values={"item": hint},
        consumable_refs=frozenset({"item"}),
    )
    assert result.code == expected_code
    assert result.source_data == hint
