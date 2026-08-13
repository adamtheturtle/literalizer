"""Regression tests for long Fortran character constants."""

import json

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Fortran

_FORTRAN_MAXIMUM_LINE_LENGTH = 132


def test_long_string_is_split_across_source_lines() -> None:
    """Keep every generated free-form source line within 132 columns."""
    result = literalize(
        source=json.dumps(obj=["A" * 300]),
        input_format=InputFormat.JSON,
        language=Fortran(),
        wrap_in_file=True,
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
    )

    assert "' // &\n" in result.code
    maximum_line_length = max(len(line) for line in result.code.splitlines())
    assert maximum_line_length <= _FORTRAN_MAXIMUM_LINE_LENGTH
