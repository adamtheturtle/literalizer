"""Tests for literalizer formatters."""

import datetime
from collections.abc import Callable

import pytest

from literalizer.languages import (
    Elixir,
    Haskell,
    Perl,
)

_SAMPLE_DATETIME = datetime.datetime.fromisoformat("2024-01-15T12:30:00")

_NON_UTC_DATETIME = datetime.datetime.fromisoformat(
    "2024-01-15T18:00:00+05:30",
)


@pytest.mark.parametrize(
    argnames=("func", "value", "expected"),
    argvalues=[
        pytest.param(
            Elixir.datetime_formats.ELIXIR,
            _NON_UTC_DATETIME,
            "~U[2024-01-15 12:30:00+00:00]",
            id="format_datetime_elixir_non_utc",
        ),
        pytest.param(
            Haskell.datetime_formats.HASKELL,
            _NON_UTC_DATETIME,
            "HDatetime (UTCTime "
            "(fromGregorian 2024 1 15) "
            "(secondsToDiffTime 45000))",
            id="format_datetime_haskell_non_utc",
        ),
        pytest.param(
            Perl.datetime_formats.PERL,
            _NON_UTC_DATETIME,
            "DateTime->new("
            "year => 2024, month => 1, day => 15, "
            "hour => 12, minute => 30, second => 0, "
            "time_zone => 'UTC')",
            id="format_datetime_perl_non_utc",
        ),
    ],
)
def test_format_datetime_non_utc(
    func: Callable[..., str],
    value: datetime.datetime,
    expected: str,
) -> None:
    """Non-UTC datetimes are converted to UTC before formatting."""
    assert func(value) == expected
