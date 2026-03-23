"""Tests for literalizer formatters."""

# pyright: reportUnknownMemberType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownVariableType=false
# pyright: reportAttributeAccessIssue=false

import datetime
from collections.abc import Callable

import pytest

from literalizer.languages import (
    Elixir,
    Haskell,
    JavaScript,
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
            Elixir.DatetimeFormats.ELIXIR,
            _NON_UTC_DATETIME,
            "~U[2024-01-15 12:30:00+00:00]",
            id="format_datetime_elixir_non_utc",
        ),
        pytest.param(
            Haskell.DatetimeFormats.HASKELL,
            _NON_UTC_DATETIME,
            "HDatetime (UTCTime "
            "(fromGregorian 2024 1 15) "
            "(secondsToDiffTime 45000))",
            id="format_datetime_haskell_non_utc",
        ),
        pytest.param(
            Perl.DatetimeFormats.PERL,
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
    result = Python.DatetimeFormats.EPOCH(_SAMPLE_DATETIME)
    # The exact value depends on local timezone for naive datetimes,
    # so just check it parses as a float.
    float(result)


@pytest.mark.parametrize(
    argnames=("func", "value", "expected"),
    argvalues=[
        pytest.param(
            Python.BytesFormats.HEX,
            b"Hello",
            '"48656c6c6f"',
            id="format_bytes_hex",
        ),
        pytest.param(
            Python.BytesFormats.HEX,
            b"",
            '""',
            id="format_bytes_hex_empty",
        ),
        pytest.param(
            Python.BytesFormats.PYTHON,
            b"Hello",
            "b'Hello'",
            id="format_bytes_python",
        ),
        pytest.param(
            Python.BytesFormats.PYTHON,
            b"\x00\x01\x02",
            "b'\\x00\\x01\\x02'",
            id="format_bytes_python_non_printable",
        ),
    ],
)
def test_format_bytes(
    func: Callable[..., str],
    value: bytes,
    expected: str,
) -> None:
    """Each bytes format function returns the expected string."""
    assert func(value) == expected


def test_format_variable_declaration_let() -> None:
    """``_format_variable_declaration_let`` uses the ``let`` keyword."""
    js_let = JavaScript(declaration_style=JavaScript.DeclarationStyles.LET)
    result = js_let.format_variable_declaration("x", "[1, 2]", [1, 2])
    assert result == "let x = [1, 2];"


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
