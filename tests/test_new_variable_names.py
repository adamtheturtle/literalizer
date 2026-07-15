"""Regression tests for generated names in ``NewVariable`` bindings."""

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Zig


def test_zig_new_variable_valid_name_is_unchanged() -> None:
    """A valid NewVariable name must remain unchanged."""
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=Zig(),
        variable_form=NewVariable(name="value", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert "const value: ZVal = .{ .int = 1 };" in result.code


def test_zig_new_variable_malformed_name_is_normalized() -> None:
    """A malformed NewVariable name must not produce invalid Zig."""
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=Zig(),
        variable_form=NewVariable(name="a-b", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert "const a_b: ZVal = .{ .int = 1 };" in result.code


def test_zig_new_variable_leading_digit_is_normalized() -> None:
    """A leading digit must not produce invalid Zig."""
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=Zig(),
        variable_form=NewVariable(name="1value", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert "const literalizer_1value: ZVal = .{ .int = 1 };" in result.code
