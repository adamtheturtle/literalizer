"""Comment capability errors for JSONC and JSON5 call input."""

import pytest

from literalizer import InputFormat, literalize_call
from literalizer.exceptions import UnsupportedCallShapeError
from literalizer.languages import Erlang


@pytest.mark.parametrize(
    argnames="input_format",
    argvalues=[InputFormat.JSONC, InputFormat.JSON5],
)
@pytest.mark.parametrize(argnames="per_element", argvalues=[False, True])
def test_wrapped_calls_reject_unsupported_comments(
    *, input_format: InputFormat, per_element: bool
) -> None:
    """Source comments obey the existing wrapped-call capability check."""
    with pytest.raises(
        expected_exception=UnsupportedCallShapeError,
        match="standalone comments cannot be preserved",
    ):
        _ = literalize_call(
            source="/* heading */ [[1]]",
            input_format=input_format,
            language=Erlang(),
            target_function="f",
            parameter_names=["a"],
            per_element=per_element,
            wrap_in_file=True,
        )
