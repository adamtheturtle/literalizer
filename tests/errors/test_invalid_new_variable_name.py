"""Validation tests for reserved TypeScript ``NewVariable`` names."""

import pytest

from literalizer import InputFormat, NewVariable, literalize, literalize_call
from literalizer.exceptions import ReservedVariableNameError
from literalizer.languages import TypeScript


def test_reserved_typescript_new_variable_name_raises() -> None:
    """Reserved names are rejected instead of silently being rewritten."""
    with pytest.raises(
        expected_exception=ReservedVariableNameError,
        match=(
            r"^TypeScript cannot use NewVariable name 'class': "
            "it is a reserved identifier$"
        ),
    ):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=TypeScript(),
            variable_form=NewVariable(
                name="class",
                modifiers=frozenset(),
            ),
            wrap_in_file=True,
        )


def test_typescript_reserved_property_call_remains_valid() -> None:
    """Reserved variable names do not block valid property calls."""
    result = literalize_call(
        source="[1]",
        input_format=InputFormat.JSON,
        language=TypeScript(),
        target_function="foo.class",
        parameter_names=["value"],
    )

    assert result.code
