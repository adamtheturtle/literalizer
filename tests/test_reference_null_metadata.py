"""Public contracts for null reference knowledge and optional hints."""

import pytest

from literalizer import (
    InputFormat,
    ValueInput,
    literalize_call,
)
from literalizer.languages import Cpp


@pytest.mark.parametrize(
    argnames=("bound_value", "hint"),
    argvalues=[
        ([1, 2], None),
        (None, [1, 2]),
    ],
)
def test_cpp_bound_consumption_preserves_source_hint(
    bound_value: ValueInput, hint: ValueInput
) -> None:
    """Actual bindings do not replace caller-supplied source metadata.

    Rendering and ownership are covered by compiling call-ref goldens.
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
    assert result.source_data == hint
