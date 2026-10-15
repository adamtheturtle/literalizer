"""Nim native call arrays must have a consistent nested shape."""

import pytest

from literalizer import InputFormat, NewVariable, literalize_call
from literalizer.exceptions import CallArgNotSupportedError
from literalizer.languages import Nim


@pytest.mark.parametrize(
    argnames="source",
    argvalues=[
        "[[1,2],[3]]",
        "[[[1],[2]],[[3,4]]]",
        '{"first": [1, 2], "second": [3]}',
    ],
)
@pytest.mark.parametrize(argnames="per_element", argvalues=[False, True])
def test_ragged_call_arguments_are_rejected(
    source: str, *, per_element: bool
) -> None:
    """Default calls refuse fixed arrays of incompatible lengths."""
    if per_element:
        source = f"[[{source}]]"
    with pytest.raises(
        expected_exception=CallArgNotSupportedError, match="Nim"
    ):
        _ = literalize_call(
            source=source,
            input_format=InputFormat.JSON,
            language=Nim(),
            target_function="make_widget",
            parameter_names=["items"],
            per_element=per_element,
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
            wrap_in_file=True,
        )
