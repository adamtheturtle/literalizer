"""Reference markers reject names that are not target identifiers."""

import pytest

from literalizer import InputFormat, literalize, literalize_call
from literalizer.exceptions import (
    InvalidNewVariableNameError,
    ReservedVariableNameError,
)
from literalizer.languages import Python


@pytest.mark.parametrize(
    argnames="name", argvalues=["", "9lives", "x; import os"]
)
def test_literalize_rejects_invalid_ref_name(name: str) -> None:
    """Literal refs cannot inject arbitrary source text."""
    with pytest.raises(
        expected_exception=InvalidNewVariableNameError,
        match="cannot use reference name",
    ):
        literalize(
            source=f'{{"a": {{"$ref": "{name}"}}}}',
            input_format=InputFormat.JSON,
            language=Python(),
            ref_key="$ref",
        )


def test_literalize_call_rejects_reserved_ref_name() -> None:
    """Call refs apply the target language's reserved-word rules."""
    with pytest.raises(
        expected_exception=ReservedVariableNameError,
        match="cannot use reference name",
    ):
        literalize_call(
            source='{"$ref": "class"}',
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="consume",
            parameter_names=("value",),
            per_element=False,
            ref_key="$ref",
        )
