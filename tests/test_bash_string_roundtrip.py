"""Runtime round-trip tests for Bash string literals."""

import subprocess

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

    completed = subprocess.run(
        args=["/bin/bash", "-c", f"printf %s {literal}"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert completed.stdout == expected
