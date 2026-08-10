"""Round-trip invariants for Bash string literals."""

import pytest

from literalizer.languages.bash import _format_string_double


@pytest.mark.parametrize(
    argnames="backslash_count",
    argvalues=[1, 2, 3, 4, 5],
)
def test_double_quoted_backslashes_before_newline_round_trip(
    backslash_count: int,
) -> None:
    """Backslashes before a physical newline remain literal in Bash."""
    expected = f"before{'\\' * backslash_count}\nafter"
    literal = _format_string_double(value=expected)
    expected_backslashes = "\\" * (backslash_count * 2)

    assert literal == f'"before{expected_backslashes}\nafter"'
