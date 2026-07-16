"""Validation tests for invalid TypeScript ``NewVariable`` names."""

import re

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import InvalidVariableNameError
from literalizer.languages import Scheme, TypeScript


@pytest.mark.parametrize("name", ["a-b", "1value"])
def test_invalid_typescript_new_variable_name_raises(name: str) -> None:
    """Invalid names are rejected instead of silently being rewritten."""
    with pytest.raises(
        expected_exception=InvalidVariableNameError,
        match=(
            "^TypeScript cannot use NewVariable name "
            rf"'{re.escape(name)}': it must be a valid identifier$"
        ),
    ):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=TypeScript(),
            variable_form=NewVariable(
                name=name,
                modifiers=frozenset(),
            ),
            wrap_in_file=True,
        )


def test_scheme_kebab_new_variable_name_remains_valid() -> None:
    """Languages that support kebab-case retain that valid syntax."""
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=Scheme(),
        variable_form=NewVariable(
            name="my-data",
            modifiers=frozenset(),
        ),
        wrap_in_file=True,
    )

    assert result.code
