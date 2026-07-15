"""Regression tests for generated names in ``NewVariable`` bindings."""

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import V


def test_v_new_variable_valid_name_is_unchanged() -> None:
    """A valid NewVariable name must remain unchanged."""
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=V(),
        variable_form=NewVariable(name="value", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert "value := 1" in result.code


def test_v_new_variable_reserved_name_is_normalized() -> None:
    """A reserved NewVariable name must not produce invalid Zig."""
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=V(),
        variable_form=NewVariable(name="type", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert "literalizer_type := 1" in result.code
