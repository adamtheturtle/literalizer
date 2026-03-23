"""Tests for literalizer formatters."""

# pyright: reportUnknownMemberType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownVariableType=false
# pyright: reportAttributeAccessIssue=false

import datetime
from collections.abc import Callable

import pytest

from literalizer.languages import (
    Cpp,
    CSharp,
    Elixir,
    Go,
    Haskell,
    Java,
    JavaScript,
    Kotlin,
    Matlab,
    Perl,
    Python,
    Ruby,
    Rust,
    Scala,
    Swift,
    VisualBasic,
    Zig,
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
            Python.DateFormats.PYTHON,
            _SAMPLE_DATE,
            "datetime.date(year=2024, month=1, day=15)",
            id="format_date_python",
        ),
        pytest.param(
            Python.DatetimeFormats.PYTHON,
            _SAMPLE_DATETIME,
            "datetime.datetime("
            "year=2024, month=1, day=15, "
            "hour=12, minute=30, second=0)",
            id="format_datetime_python",
        ),
        pytest.param(
            Python.DatetimeFormats.PYTHON,
            _SAMPLE_DATETIME_MICRO,
            "datetime.datetime("
            "year=2024, month=1, day=15, "
            "hour=12, minute=30, second=0, "
            "microsecond=123456)",
            id="format_datetime_python_microsecond",
        ),
        pytest.param(
            Elixir.DateFormats.ELIXIR,
            _SAMPLE_DATE,
            "~D[2024-01-15]",
            id="format_date_elixir",
        ),
        pytest.param(
            Elixir.DatetimeFormats.ELIXIR,
            _SAMPLE_DATETIME,
            "~N[2024-01-15 12:30:00]",
            id="format_datetime_elixir_naive",
        ),
        pytest.param(
            Elixir.DatetimeFormats.ELIXIR,
            datetime.datetime.fromisoformat("2024-01-15T12:30:00+00:00"),
            "~U[2024-01-15 12:30:00+00:00]",
            id="format_datetime_elixir_utc",
        ),
        pytest.param(
            Elixir.DatetimeFormats.ELIXIR,
            datetime.datetime.fromisoformat("2024-01-15T18:00:00+05:30"),
            "~U[2024-01-15 12:30:00+00:00]",
            id="format_datetime_elixir_non_utc",
        ),
        pytest.param(
            Java.DateFormats.JAVA,
            _SAMPLE_DATE,
            "LocalDate.of(2024, 1, 15)",
            id="format_date_java",
        ),
        pytest.param(
            Java.DatetimeFormats.INSTANT,
            _SAMPLE_DATETIME,
            'Instant.parse("2024-01-15T12:30:00")',
            id="format_datetime_java_instant",
        ),
        pytest.param(
            Java.DatetimeFormats.ZONED,
            _SAMPLE_DATETIME,
            'ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0, ZoneId.of("UTC"))',
            id="format_datetime_java_zoned",
        ),
        pytest.param(
            Ruby.DateFormats.RUBY,
            _SAMPLE_DATE,
            "Date.new(2024, 1, 15)",
            id="format_date_ruby",
        ),
        pytest.param(
            Ruby.DatetimeFormats.RUBY,
            _SAMPLE_DATETIME,
            "Time.new(2024, 1, 15, 12, 30, 0)",
            id="format_datetime_ruby",
        ),
        pytest.param(
            JavaScript.DateFormats.JS,
            _SAMPLE_DATE,
            'new Date("2024-01-15")',
            id="format_date_js",
        ),
        pytest.param(
            JavaScript.DatetimeFormats.JS,
            _SAMPLE_DATETIME,
            'new Date("2024-01-15T12:30:00")',
            id="format_datetime_js",
        ),
        pytest.param(
            CSharp.DateFormats.CSHARP,
            _SAMPLE_DATE,
            "new DateOnly(2024, 1, 15)",
            id="format_date_csharp",
        ),
        pytest.param(
            CSharp.DatetimeFormats.CSHARP,
            _SAMPLE_DATETIME,
            "new DateTime(2024, 1, 15, 12, 30, 0)",
            id="format_datetime_csharp",
        ),
        pytest.param(
            Go.DateFormats.GO,
            _SAMPLE_DATE,
            "time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC)",
            id="format_date_go",
        ),
        pytest.param(
            Go.DatetimeFormats.GO,
            _SAMPLE_DATETIME,
            "time.Date(2024, time.January, 15, 12, 30, 0, 0, time.UTC)",
            id="format_datetime_go",
        ),
        pytest.param(
            Kotlin.DateFormats.KOTLIN,
            _SAMPLE_DATE,
            "LocalDate.of(2024, 1, 15)",
            id="format_date_kotlin",
        ),
        pytest.param(
            Kotlin.DatetimeFormats.KOTLIN,
            _SAMPLE_DATETIME,
            "LocalDateTime.of(2024, 1, 15, 12, 30, 0)",
            id="format_datetime_kotlin",
        ),
        pytest.param(
            Rust.DateFormats.RUST,
            _SAMPLE_DATE,
            "NaiveDate::from_ymd_opt(2024, 1, 15).unwrap()",
            id="format_date_rust",
        ),
        pytest.param(
            Rust.DatetimeFormats.RUST,
            _SAMPLE_DATETIME,
            "NaiveDateTime::new("
            "NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), "
            "NaiveTime::from_hms_opt(12, 30, 0).unwrap())",
            id="format_datetime_rust",
        ),
        pytest.param(
            Rust.DatetimeFormats.RUST,
            datetime.datetime.fromisoformat("2024-01-15T12:30:00.123456"),
            "NaiveDateTime::new("
            "NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), "
            "NaiveTime::from_hms_micro_opt(12, 30, 0, 123456).unwrap())",
            id="format_datetime_rust_microsecond",
        ),
        pytest.param(
            Matlab.DatetimeFormats.MATLAB,
            _SAMPLE_DATETIME_MICRO,
            "datetime(2024, 1, 15, 12, 30, 0, 123.456)",
            id="format_datetime_matlab_microsecond",
        ),
        pytest.param(
            Swift.DatetimeFormats.SWIFT,
            _SAMPLE_DATETIME_MICRO,
            "DateComponents("
            "calendar: Calendar(identifier: .gregorian), "
            "year: 2024, month: 1, day: 15, "
            "hour: 12, minute: 30, second: 0, "
            "nanosecond: 123456000).date!",
            id="format_datetime_swift_microsecond",
        ),
        pytest.param(
            Haskell.DatetimeFormats.HASKELL,
            _SAMPLE_DATETIME_MICRO,
            "HDatetime (UTCTime "
            "(fromGregorian 2024 1 15) "
            "(picosecondsToDiffTime 45000123456000000))",
            id="format_datetime_haskell_microsecond",
        ),
        pytest.param(
            Haskell.DatetimeFormats.HASKELL,
            datetime.datetime.fromisoformat(
                "2024-01-15T18:00:00+05:30",
            ),
            "HDatetime (UTCTime "
            "(fromGregorian 2024 1 15) "
            "(secondsToDiffTime 45000))",
            id="format_datetime_haskell_non_utc",
        ),
        pytest.param(
            Scala.DatetimeFormats.SCALA,
            _SAMPLE_DATETIME_MICRO,
            "ZonedDateTime.of(2024, 1, 15, 12, 30, 0, "
            '123456000, ZoneId.of("UTC"))',
            id="format_datetime_scala_microsecond",
        ),
        pytest.param(
            Perl.DateFormats.PERL,
            _SAMPLE_DATE,
            "DateTime->new(year => 2024, month => 1, day => 15)",
            id="format_date_perl",
        ),
        pytest.param(
            Perl.DatetimeFormats.PERL,
            _SAMPLE_DATETIME,
            "DateTime->new("
            "year => 2024, month => 1, day => 15, "
            "hour => 12, minute => 30, second => 0, "
            "time_zone => 'UTC')",
            id="format_datetime_perl",
        ),
        pytest.param(
            Perl.DatetimeFormats.PERL,
            _SAMPLE_DATETIME_MICRO,
            "DateTime->new("
            "year => 2024, month => 1, day => 15, "
            "hour => 12, minute => 30, second => 0, "
            "nanosecond => 123456000, "
            "time_zone => 'UTC')",
            id="format_datetime_perl_microsecond",
        ),
        pytest.param(
            Perl.DatetimeFormats.PERL,
            datetime.datetime.fromisoformat(
                "2024-01-15T18:00:00+05:30",
            ),
            "DateTime->new("
            "year => 2024, month => 1, day => 15, "
            "hour => 12, minute => 30, second => 0, "
            "time_zone => 'UTC')",
            id="format_datetime_perl_non_utc",
        ),
    ],
)
def test_format_date_datetime(
    func: Callable[..., str],
    value: datetime.date | datetime.datetime,
    expected: str,
) -> None:
    """Each format function returns the expected string."""
    assert func(value) == expected


def test_format_datetime_epoch() -> None:
    """``format_datetime_epoch`` returns a numeric timestamp."""
    result = Python.DatetimeFormats.EPOCH(_SAMPLE_DATETIME)
    # The exact value depends on local timezone for naive datetimes,
    # so just check it parses as a float.
    float(result)


def test_format_datetime_zig_naive() -> None:
    """Zig datetime treats naive datetimes as UTC."""
    result = Zig.DatetimeFormats.ZIG(_SAMPLE_DATETIME)
    assert result == "1705321800"


def test_format_date_cpp() -> None:
    """``format_date_cpp`` returns a year_month_day literal."""
    result = Cpp.DateFormats.CPP(_SAMPLE_DATE)
    expected = (
        "std::chrono::year_month_day{"
        "std::chrono::year{2024}, "
        "std::chrono::month{1}, "
        "std::chrono::day{15}}"
    )
    assert result == expected


def test_format_datetime_cpp() -> None:
    """``format_datetime_cpp`` returns a sys_days expression."""
    result = Cpp.DatetimeFormats.CPP(_SAMPLE_DATETIME)
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
    result = Cpp.DatetimeFormats.CPP(midnight)
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
    result = Cpp.DatetimeFormats.CPP(dt)
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
