"""Regression tests for generated names in ``NewVariable`` bindings."""

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import TypeScript


def test_typescript_new_variable_malformed_name_is_normalized() -> None:
    """A malformed NewVariable name must not produce invalid
    TypeScript.
    """
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=TypeScript(),
        variable_form=NewVariable(name="a-b", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert "const a_b = 1;" in result.code


def test_typescript_new_variable_reserved_name_is_normalized() -> None:
    """A reserved NewVariable name must not produce invalid TypeScript."""
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=TypeScript(),
        variable_form=NewVariable(name="class", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert "const literalizer_class = 1;" in result.code
