"""Tests for literalizer formatters."""

import datetime
from collections.abc import Callable

import pytest

from literalizer._formatters import (
    format_bytes_hex,
    format_date_js,
    format_datetime_js,
)
from literalizer.languages import Java, Python
from literalizer.languages.cpp import (
    _format_date_cpp as format_date_cpp,
)
from literalizer.languages.cpp import (
    _format_datetime_cpp as format_datetime_cpp,
)
from literalizer.languages.csharp import (
    _format_date_csharp as format_date_csharp,
)
from literalizer.languages.csharp import (
    _format_datetime_csharp as format_datetime_csharp,
)
from literalizer.languages.go import (
    _format_date_go as format_date_go,
)
from literalizer.languages.go import (
    _format_datetime_go as format_datetime_go,
)
from literalizer.languages.java import (
    _format_date_java as format_date_java,
)
from literalizer.languages.java import (
    _format_datetime_java_instant as format_datetime_java_instant,
)
from literalizer.languages.java import (
    _format_datetime_java_zoned as format_datetime_java_zoned,
)
from literalizer.languages.kotlin import (
    _format_date_kotlin as format_date_kotlin,
)
from literalizer.languages.kotlin import (
    _format_datetime_kotlin as format_datetime_kotlin,
)
from literalizer.languages.python import (
    _format_bytes_python as format_bytes_python,
)
from literalizer.languages.python import (
    _format_date_python as format_date_python,
)
from literalizer.languages.python import (
    _format_datetime_epoch as format_datetime_epoch,
)
from literalizer.languages.python import (
    _format_datetime_python as format_datetime_python,
)
from literalizer.languages.ruby import (
    _format_date_ruby as format_date_ruby,
)
from literalizer.languages.ruby import (
    _format_datetime_ruby as format_datetime_ruby,
)
from literalizer.languages.rust import (
    _format_date_rust as format_date_rust,
)
from literalizer.languages.rust import (
    _format_datetime_rust as format_datetime_rust,
)
from literalizer.languages.vb import (
    _format_string_vb as format_string_vb,
)

PYTHON = Python(
    date_format=Python.date_formats.PYTHON,
    datetime_format=Python.datetime_formats.PYTHON,
    bytes_format=Python.bytes_formats.HEX,
    sequence_format=Python.sequence_formats.TUPLE,
    set_format=Python.set_formats.SET,
    variable_type_hints=Python.variable_type_hints_formats.NONE,
)
JAVA = Java(
    date_format=Java.date_formats.JAVA,
    datetime_format=Java.datetime_formats.INSTANT,
    bytes_format=Java.bytes_formats.HEX,
    sequence_format=Java.sequence_formats.ARRAY,
)

_SAMPLE_DATE = datetime.date(year=2024, month=1, day=15)
_SAMPLE_DATETIME = datetime.datetime.fromisoformat("2024-01-15T12:30:00")
_SAMPLE_DATETIME_MICRO = datetime.datetime.fromisoformat(
    "2024-01-15T12:30:00.123456"
)


@pytest.mark.parametrize(
    argnames=("func", "value", "expected"),
    argvalues=[
        pytest.param(
            format_date_python,
            _SAMPLE_DATE,
            "datetime.date(year=2024, month=1, day=15)",
            id="format_date_python",
        ),
        pytest.param(
            format_datetime_python,
            _SAMPLE_DATETIME,
            "datetime.datetime("
            "year=2024, month=1, day=15, "
            "hour=12, minute=30, second=0)",
            id="format_datetime_python",
        ),
        pytest.param(
            format_datetime_python,
            _SAMPLE_DATETIME_MICRO,
            "datetime.datetime("
            "year=2024, month=1, day=15, "
            "hour=12, minute=30, second=0, "
            "microsecond=123456)",
            id="format_datetime_python_microsecond",
        ),
        pytest.param(
            format_date_java,
            _SAMPLE_DATE,
            "LocalDate.of(2024, 1, 15)",
            id="format_date_java",
        ),
        pytest.param(
            format_datetime_java_instant,
            _SAMPLE_DATETIME,
            'Instant.parse("2024-01-15T12:30:00")',
            id="format_datetime_java_instant",
        ),
        pytest.param(
            format_datetime_java_zoned,
            _SAMPLE_DATETIME,
            'ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0, ZoneId.of("UTC"))',
            id="format_datetime_java_zoned",
        ),
        pytest.param(
            format_date_ruby,
            _SAMPLE_DATE,
            "Date.new(2024, 1, 15)",
            id="format_date_ruby",
        ),
        pytest.param(
            format_datetime_ruby,
            _SAMPLE_DATETIME,
            "Time.new(2024, 1, 15, 12, 30, 0)",
            id="format_datetime_ruby",
        ),
        pytest.param(
            format_date_js,
            _SAMPLE_DATE,
            'new Date("2024-01-15")',
            id="format_date_js",
        ),
        pytest.param(
            format_datetime_js,
            _SAMPLE_DATETIME,
            'new Date("2024-01-15T12:30:00")',
            id="format_datetime_js",
        ),
        pytest.param(
            format_date_csharp,
            _SAMPLE_DATE,
            "new DateOnly(2024, 1, 15)",
            id="format_date_csharp",
        ),
        pytest.param(
            format_datetime_csharp,
            _SAMPLE_DATETIME,
            "new DateTime(2024, 1, 15, 12, 30, 0)",
            id="format_datetime_csharp",
        ),
        pytest.param(
            format_date_go,
            _SAMPLE_DATE,
            "time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC)",
            id="format_date_go",
        ),
        pytest.param(
            format_datetime_go,
            _SAMPLE_DATETIME,
            "time.Date(2024, time.January, 15, 12, 30, 0, 0, time.UTC)",
            id="format_datetime_go",
        ),
        pytest.param(
            format_date_kotlin,
            _SAMPLE_DATE,
            "LocalDate.of(2024, 1, 15)",
            id="format_date_kotlin",
        ),
        pytest.param(
            format_datetime_kotlin,
            _SAMPLE_DATETIME,
            "LocalDateTime.of(2024, 1, 15, 12, 30, 0)",
            id="format_datetime_kotlin",
        ),
        pytest.param(
            format_date_rust,
            _SAMPLE_DATE,
            "NaiveDate::from_ymd_opt(2024, 1, 15).unwrap()",
            id="format_date_rust",
        ),
        pytest.param(
            format_datetime_rust,
            _SAMPLE_DATETIME,
            "NaiveDateTime::new("
            "NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), "
            "NaiveTime::from_hms_opt(12, 30, 0).unwrap())",
            id="format_datetime_rust",
        ),
        pytest.param(
            format_datetime_rust,
            datetime.datetime.fromisoformat("2024-01-15T12:30:00.123456"),
            "NaiveDateTime::new("
            "NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), "
            "NaiveTime::from_hms_micro_opt(12, 30, 0, 123456).unwrap())",
            id="format_datetime_rust_microsecond",
        ),
    ],
)
def test_format_date_datetime(
    func: Callable[..., str],
    value: datetime.date | datetime.datetime,
    expected: str,
) -> None:
    """Each format function returns the expected string."""
    assert func(value=value) == expected


def test_format_datetime_epoch() -> None:
    """``format_datetime_epoch`` returns a numeric timestamp."""
    result = format_datetime_epoch(value=_SAMPLE_DATETIME)
    # The exact value depends on local timezone for naive datetimes,
    # so just check it parses as a float.
    float(result)


def test_format_date_cpp() -> None:
    """``format_date_cpp`` returns a year_month_day literal."""
    result = format_date_cpp(value=_SAMPLE_DATE)
    expected = (
        "std::chrono::year_month_day{"
        "std::chrono::year{2024}, "
        "std::chrono::month{1}, "
        "std::chrono::day{15}}"
    )
    assert result == expected


def test_format_datetime_cpp() -> None:
    """``format_datetime_cpp`` returns a sys_days expression."""
    result = format_datetime_cpp(value=_SAMPLE_DATETIME)
    expected = (
        "std::chrono::sys_days{"
        "std::chrono::year_month_day{"
        "std::chrono::year{2024}, "
        "std::chrono::month{1}, "
        "std::chrono::day{15}}}"
        " + std::chrono::hours{12}"
        " + std::chrono::minutes{30}"
    )
    assert result == expected


def test_format_datetime_cpp_midnight() -> None:
    """``format_datetime_cpp`` at midnight omits zero time components."""
    midnight = datetime.datetime.fromisoformat("2024-01-15T00:00:00")
    result = format_datetime_cpp(value=midnight)
    expected = (
        "std::chrono::sys_days{"
        "std::chrono::year_month_day{"
        "std::chrono::year{2024}, "
        "std::chrono::month{1}, "
        "std::chrono::day{15}}}"
    )
    assert result == expected


def test_format_datetime_cpp_seconds_and_microseconds() -> None:
    """``format_datetime_cpp`` includes seconds and microseconds."""
    dt = datetime.datetime.fromisoformat("2024-01-15T12:30:45.123456")
    result = format_datetime_cpp(value=dt)
    expected = (
        "std::chrono::sys_days{"
        "std::chrono::year_month_day{"
        "std::chrono::year{2024}, "
        "std::chrono::month{1}, "
        "std::chrono::day{15}}}"
        " + std::chrono::hours{12}"
        " + std::chrono::minutes{30}"
        " + std::chrono::seconds{45}"
        " + std::chrono::microseconds{123456}"
    )
    assert result == expected


@pytest.mark.parametrize(
    argnames=("func", "value", "expected"),
    argvalues=[
        pytest.param(
            format_bytes_hex,
            b"Hello",
            '"48656c6c6f"',
            id="format_bytes_hex",
        ),
        pytest.param(
            format_bytes_hex,
            b"",
            '""',
            id="format_bytes_hex_empty",
        ),
        pytest.param(
            format_bytes_python,
            b"Hello",
            "b'Hello'",
            id="format_bytes_python",
        ),
        pytest.param(
            format_bytes_python,
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
    assert func(value=value) == expected


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
    assert format_string_vb(value=value) == expected
