"""Focused tests for shared integer formatter composition.

These call the formatter factory with a pre-rendered string, so the
composition they check is not reachable from an input document
(issue #4699).
"""

import pytest

from literalizer._formatters.format_integers import (
    make_negative_nondecimal_i64_formatter,
)


@pytest.mark.parametrize(
    argnames=("rendered", "suffix", "expected"),
    argvalues=[
        ("-0x80000000LL", "LL", "-0x80000000LL"),
        ("-0x80000000L", "LL", "-0x80000000LL"),
    ],
)
def test_negative_nondecimal_suffix_composes_with_existing_suffix(
    rendered: str,
    suffix: str,
    expected: str,
) -> None:
    """Existing suffixes are retained or widened without duplication."""
    formatter = make_negative_nondecimal_i64_formatter(
        base=lambda _value: rendered,
        suffix=suffix,
    )

    assert formatter(-(2**31)) == expected
