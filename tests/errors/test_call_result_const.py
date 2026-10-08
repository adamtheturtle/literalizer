"""Runtime calls cannot initialize C# compile-time constants."""

import pytest

from literalizer import InputFormat, NewVariable, literalize_call
from literalizer.exceptions import IncompatibleFormatsError
from literalizer.languages import CSharp


def test_const_call_result_is_rejected() -> None:
    """Reject runtime call initializers regardless of the input type."""
    with pytest.raises(
        expected_exception=IncompatibleFormatsError,
        match="cannot bind a runtime call result",
    ):
        _ = literalize_call(
            source="1",
            input_format=InputFormat.JSON,
            language=CSharp(),
            target_function="process",
            parameter_names=("item",),
            per_element=False,
            variable_form=NewVariable(
                name="data", modifiers=frozenset({CSharp.modifiers.CONST})
            ),
        )
