"""Tests for integer literal formatters."""

from literalizer.languages import C, Cpp, Fortran, ObjectiveC


def test_c_family_i64_min_avoids_out_of_range_positive_literal() -> None:
    """C-family backends spell INT64_MIN as an in-range expression."""
    value = -(2**63)
    expected = "(-9223372036854775807LL - 1)"

    assert C().format_integer(value) == expected
    assert Cpp().format_integer(value) == expected
    assert ObjectiveC().format_integer(value) == expected


def test_fortran_i64_min_avoids_out_of_range_positive_literal() -> None:
    """Fortran spells INT64_MIN with explicitly typed in-range terms."""
    assert Fortran().format_integer(-(2**63)) == (
        "(-9223372036854775807_int64 - 1_int64)"
    )
