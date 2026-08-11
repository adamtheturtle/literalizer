"""MATLAB string backslash regression tests."""

import pytest

from literalizer.languages.matlab import (
    _decode_matlab_string_expr,  # pyright: ignore[reportPrivateUsage]
    _format_matlab_string,  # pyright: ignore[reportPrivateUsage]
)


@pytest.mark.parametrize(
    argnames="value",
    argvalues=[
        "trailing\\",
        "before\\\nafter",
        'hello \\"world\\"',
    ],
)
def test_matlab_backslashes_round_trip(value: str) -> None:
    """Backslashes survive formatting, including at segment boundaries."""
    expression = _format_matlab_string(value=value)

    assert _decode_matlab_string_expr(expr=expression) == value


def test_matlab_trailing_backslash_uses_char_expression() -> None:
    """A trailing backslash cannot escape Octave's closing delimiter."""
    assert _format_matlab_string(value="trailing\\") == (
        "sprintf('%s%s', \"trailing\", char(92))"
    )
