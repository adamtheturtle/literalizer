"""Tests for literalizer formatters."""

import datetime
from collections.abc import Callable

import pytest

from literalizer.languages import (
    Elixir,
    Haskell,
    Perl,
    Python,
    VisualBasic,
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


def test_format_datetime_epoch() -> None:
    """``format_datetime_epoch`` returns a numeric timestamp."""
    result = Python.datetime_formats.EPOCH(_SAMPLE_DATETIME)
    # The exact value depends on local timezone for naive datetimes,
    # so just check it parses as a float.
    float(result)


_VB = VisualBasic()


@pytest.mark.parametrize(
    argnames=("value", "expected"),
    argvalues=[
        pytest.param("", '""', id="empty"),
        pytest.param("hello", '"hello"', id="plain"),
        pytest.param('say "hi"', '"say ""hi"""', id="quotes"),
        pytest.param(
            "line1\r\nline2", '"line1" & vbCrLf & "line2"', id="crlf"
        ),
        pytest.param("\r\nline2", 'vbCrLf & "line2"', id="crlf_at_start"),
        pytest.param("line1\nline2", '"line1" & Chr(10) & "line2"', id="lf"),
        pytest.param("\nline2", 'Chr(10) & "line2"', id="lf_at_start"),
        pytest.param("line1\rline2", '"line1" & Chr(13) & "line2"', id="cr"),
        pytest.param("\rline2", 'Chr(13) & "line2"', id="cr_at_start"),
        pytest.param("col1\tcol2", '"col1" & vbTab & "col2"', id="tab"),
        pytest.param("\tcol2", 'vbTab & "col2"', id="tab_at_start"),
        pytest.param("\x01", "Chr(1)", id="control_char"),
        pytest.param(
            "\x01text",
            'Chr(1) & "text"',
            id="control_char_then_text",
        ),
        pytest.param(
            "text\x01",
            '"text" & Chr(1)',
            id="text_then_control_char",
        ),
    ],
)
def test_format_string_vb(value: str, expected: str) -> None:
    """``format_string_vb`` formats strings using VB.NET escaping
    rules.
    """
    assert _VB.format_string(value) == expected
