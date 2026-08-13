"""Regression tests for Lua long-bracket delimiter boundaries."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.languages import Lua


@pytest.mark.parametrize(
    argnames=("value", "expected"),
    argvalues=[
        ("]", "[=[]]=]"),
        ("a]", "[=[a]]=]"),
        ("a]=", "[[a]=]]"),
        ("a]b", "[[a]b]]"),
    ],
)
def test_multiline_avoids_closer_across_value_boundary(
    value: str,
    expected: str,
) -> None:
    """Choose a delimiter that cannot begin in the value's suffix."""
    string_format = next(
        member for member in Lua.string_formats if member.name == "MULTILINE"
    )
    result = literalize(
        source=f'"{value}"',
        input_format=InputFormat.JSON,
        language=Lua(string_format=string_format),
    )

    assert result.code == expected
