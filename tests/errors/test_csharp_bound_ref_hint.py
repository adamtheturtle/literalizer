"""C# errors for incompatible explicit hints on emitted bound values."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import CSharp


def test_csharp_rejects_bound_tuple_with_scalar_hint() -> None:
    """An explicit scalar hint cannot type a tuple-valued static field."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="C# reference hints must have the same declaration type",
    ):
        _ = literalize(
            source='{ "$ref": "ref_data" }',
            input_format=InputFormat.JSON,
            language=CSharp(),
            ref_key="$ref",
            bound_refs={"ref_data": [1, 2]},
            ref_values={"ref_data": 1},
            variable_form=NewVariable(
                name="my_data", modifiers=frozenset({CSharp.modifiers.STATIC})
            ),
            wrap_in_file=True,
        )
