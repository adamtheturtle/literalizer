"""Fortran free-form source line limits."""

import json

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Fortran

_FORTRAN_MAX_LINE_LENGTH = 132


@pytest.mark.parametrize(argnames="value", argvalues=["z" * 200, "\x01" * 40])
def test_long_fortran_strings_stay_within_free_form_limit(value: str) -> None:
    """Long plain and control-heavy strings use continuation lines."""
    result = literalize(
        source=json.dumps(obj={"k": value}),
        input_format=InputFormat.JSON,
        language=Fortran(),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert " // &\n" in result.code
    assert (
        max(len(line) for line in result.code.splitlines())
        <= _FORTRAN_MAX_LINE_LENGTH
    )


def test_nested_fortran_expressions_use_continuation_lines() -> None:
    """Long nested constructor expressions split at safe commas."""
    result = literalize(
        source=json.dumps(
            obj={
                "nested": {
                    "numbers": [1, 2, 3, 4, 5],
                    "labels": ["alpha", "beta", "gamma"],
                    "enabled": True,
                }
            }
        ),
        input_format=InputFormat.JSON,
        language=Fortran(),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert ", &\n    & " in result.code
    assert (
        max(len(line) for line in result.code.splitlines())
        <= _FORTRAN_MAX_LINE_LENGTH
    )
