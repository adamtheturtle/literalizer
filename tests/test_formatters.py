"""Tests for literalizer formatters."""

import datetime
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

from literalizer._formatters import (
    format_bytes_hex,
    format_bytes_python,
    format_date_cpp,
    format_date_csharp,
    format_date_go,
    format_date_java,
    format_date_js,
    format_date_kotlin,
    format_date_python,
    format_date_ruby,
    format_date_rust,
    format_datetime_cpp,
    format_datetime_csharp,
    format_datetime_epoch,
    format_datetime_go,
    format_datetime_java_instant,
    format_datetime_java_zoned,
    format_datetime_js,
    format_datetime_kotlin,
    format_datetime_python,
    format_datetime_ruby,
    format_datetime_rust,
    format_string_vb,
)
from literalizer.languages import Java, Python

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


def test_format_date_datetime(subtests: pytest.Subtests) -> None:
    """Each format function returns the expected string."""
    cases: list[tuple[str, Callable[..., str], Any, str]] = [
        (
            "format_date_python",
            format_date_python,
            _SAMPLE_DATE,
            "datetime.date(year=2024, month=1, day=15)",
        ),
        (
            "format_datetime_python",
            format_datetime_python,
            _SAMPLE_DATETIME,
            "datetime.datetime("
            "year=2024, month=1, day=15, "
            "hour=12, minute=30, second=0)",
        ),
        (
            "format_datetime_python_microsecond",
            format_datetime_python,
            _SAMPLE_DATETIME_MICRO,
            "datetime.datetime("
            "year=2024, month=1, day=15, "
            "hour=12, minute=30, second=0, "
            "microsecond=123456)",
        ),
        (
            "format_date_java",
            format_date_java,
            _SAMPLE_DATE,
            "LocalDate.of(2024, 1, 15)",
        ),
        (
            "format_datetime_java_instant",
            format_datetime_java_instant,
            _SAMPLE_DATETIME,
            'Instant.parse("2024-01-15T12:30:00")',
        ),
        (
            "format_datetime_java_zoned",
            format_datetime_java_zoned,
            _SAMPLE_DATETIME,
            'ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0, ZoneId.of("UTC"))',
        ),
        (
            "format_date_ruby",
            format_date_ruby,
            _SAMPLE_DATE,
            "Date.new(2024, 1, 15)",
        ),
        (
            "format_datetime_ruby",
            format_datetime_ruby,
            _SAMPLE_DATETIME,
            "Time.new(2024, 1, 15, 12, 30, 0)",
        ),
        (
            "format_date_js",
            format_date_js,
            _SAMPLE_DATE,
            'new Date("2024-01-15")',
        ),
        (
            "format_datetime_js",
            format_datetime_js,
            _SAMPLE_DATETIME,
            'new Date("2024-01-15T12:30:00")',
        ),
        (
            "format_date_csharp",
            format_date_csharp,
            _SAMPLE_DATE,
            "new DateOnly(2024, 1, 15)",
        ),
        (
            "format_datetime_csharp",
            format_datetime_csharp,
            _SAMPLE_DATETIME,
            "new DateTime(2024, 1, 15, 12, 30, 0)",
        ),
        (
            "format_date_go",
            format_date_go,
            _SAMPLE_DATE,
            "time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC)",
        ),
        (
            "format_datetime_go",
            format_datetime_go,
            _SAMPLE_DATETIME,
            "time.Date(2024, time.January, 15, 12, 30, 0, 0, time.UTC)",
        ),
        (
            "format_date_kotlin",
            format_date_kotlin,
            _SAMPLE_DATE,
            "LocalDate.of(2024, 1, 15)",
        ),
        (
            "format_datetime_kotlin",
            format_datetime_kotlin,
            _SAMPLE_DATETIME,
            "LocalDateTime.of(2024, 1, 15, 12, 30, 0)",
        ),
        (
            "format_date_rust",
            format_date_rust,
            _SAMPLE_DATE,
            "NaiveDate::from_ymd_opt(2024, 1, 15).unwrap()",
        ),
        (
            "format_datetime_rust",
            format_datetime_rust,
            _SAMPLE_DATETIME,
            "NaiveDateTime::new("
            "NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), "
            "NaiveTime::from_hms_opt(12, 30, 0).unwrap())",
        ),
        (
            "format_datetime_rust_microsecond",
            format_datetime_rust,
            datetime.datetime.fromisoformat("2024-01-15T12:30:00.123456"),
            "NaiveDateTime::new("
            "NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), "
            "NaiveTime::from_hms_micro_opt(12, 30, 0, 123456).unwrap())",
        ),
    ]
    for name, func, value, expected in cases:
        with subtests.test(msg=name):
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


def test_format_bytes(subtests: pytest.Subtests) -> None:
    """Each bytes format function returns the expected string."""
    cases = [
        ("format_bytes_hex", format_bytes_hex, b"Hello", '"48656c6c6f"'),
        ("format_bytes_hex_empty", format_bytes_hex, b"", '""'),
        ("format_bytes_python", format_bytes_python, b"Hello", "b'Hello'"),
        (
            "format_bytes_python_non_printable",
            format_bytes_python,
            b"\x00\x01\x02",
            "b'\\x00\\x01\\x02'",
        ),
    ]
    for name, func, value, expected in cases:
        with subtests.test(msg=name):
            assert func(value=value) == expected


def test_format_string_vb(subtests: pytest.Subtests) -> None:
    """``format_string_vb`` formats strings using VB.NET escaping
    rules.
    """
    cases = [
        ("empty", "", '""'),
        ("plain", "hello", '"hello"'),
        ("quotes", 'say "hi"', '"say ""hi"""'),
        ("crlf", "line1\r\nline2", '"line1" & vbCrLf & "line2"'),
        ("crlf_at_start", "\r\nline2", 'vbCrLf & "line2"'),
        ("lf", "line1\nline2", '"line1" & Chr(10) & "line2"'),
        ("lf_at_start", "\nline2", 'Chr(10) & "line2"'),
        ("cr", "line1\rline2", '"line1" & Chr(13) & "line2"'),
        ("cr_at_start", "\rline2", 'Chr(13) & "line2"'),
        ("tab", "col1\tcol2", '"col1" & vbTab & "col2"'),
        ("tab_at_start", "\tcol2", 'vbTab & "col2"'),
        ("control_char", "\x01", "Chr(1)"),
        ("control_char_then_text", "\x01text", 'Chr(1) & "text"'),
        ("text_then_control_char", "text\x01", '"text" & Chr(1)'),
    ]
    for name, value, expected in cases:
        with subtests.test(msg=name):
            assert format_string_vb(value=value) == expected
