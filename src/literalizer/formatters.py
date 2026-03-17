"""Functions for formatting scalars as language-specific literals."""

from __future__ import annotations

import datetime  # noqa: TC003
from typing import TYPE_CHECKING

from beartype import beartype

if TYPE_CHECKING:
    from collections.abc import Callable

__all__ = [
    "dict_entry_with_separator",
    "format_bytes_hex",
    "format_bytes_python",
    "format_date_cpp",
    "format_date_csharp",
    "format_date_dart",
    "format_date_go",
    "format_date_iso",
    "format_date_java",
    "format_date_js",
    "format_date_julia",
    "format_date_kotlin",
    "format_date_php",
    "format_date_python",
    "format_date_r",
    "format_date_ruby",
    "format_date_rust",
    "format_datetime_cpp",
    "format_datetime_csharp",
    "format_datetime_dart",
    "format_datetime_epoch",
    "format_datetime_go",
    "format_datetime_iso",
    "format_datetime_java_instant",
    "format_datetime_java_zoned",
    "format_datetime_js",
    "format_datetime_julia",
    "format_datetime_kotlin",
    "format_datetime_php",
    "format_datetime_python",
    "format_datetime_r",
    "format_datetime_ruby",
    "format_datetime_rust",
    "format_variable_assignment_clojure",
    "format_variable_assignment_cpp",
    "format_variable_assignment_csharp",
    "format_variable_assignment_dart",
    "format_variable_assignment_elixir",
    "format_variable_assignment_fsharp",
    "format_variable_assignment_go",
    "format_variable_assignment_haskell",
    "format_variable_assignment_java",
    "format_variable_assignment_js",
    "format_variable_assignment_kotlin",
    "format_variable_assignment_ocaml",
    "format_variable_assignment_php",
    "format_variable_assignment_python",
    "format_variable_assignment_r",
    "format_variable_assignment_ruby",
    "format_variable_assignment_rust",
    "format_variable_assignment_scala",
    "format_variable_assignment_swift",
    "format_variable_declaration_clojure",
    "format_variable_declaration_cpp",
    "format_variable_declaration_csharp",
    "format_variable_declaration_dart",
    "format_variable_declaration_elixir",
    "format_variable_declaration_fsharp",
    "format_variable_declaration_go",
    "format_variable_declaration_haskell",
    "format_variable_declaration_java",
    "format_variable_declaration_js",
    "format_variable_declaration_julia",
    "format_variable_declaration_kotlin",
    "format_variable_declaration_ocaml",
    "format_variable_declaration_php",
    "format_variable_declaration_python",
    "format_variable_declaration_r",
    "format_variable_declaration_ruby",
    "format_variable_declaration_rust",
    "format_variable_declaration_scala",
    "format_variable_declaration_swift",
    "passthrough_list_entry",
    "passthrough_set_entry",
    "to_fsharp_val",
    "to_ocaml_val",
]


@beartype
def format_date_iso(value: datetime.date) -> str:
    """Format a date as an ISO 8601 quoted string literal.

    Example: ``datetime.date(2024, 1, 15)`` → ``"2024-01-15"``.
    """
    return f'"{value.isoformat()}"'


@beartype
def format_datetime_iso(value: datetime.datetime) -> str:
    """Format a datetime as an ISO 8601 quoted string literal.

    Example: ``datetime.datetime(2024, 1, 15, 12, 30)`` →
    ``"2024-01-15T12:30:00"``.
    """
    return f'"{value.isoformat()}"'


@beartype
def format_date_python(value: datetime.date) -> str:
    """Format a date as a Python ``datetime.date(...)`` constructor call.

    Example: ``datetime.date(2024, 1, 15)``.
    """
    return f"datetime.date({value.year}, {value.month}, {value.day})"


@beartype
def format_datetime_python(value: datetime.datetime) -> str:
    """Format a datetime as a Python ``datetime.datetime(...)``
    constructor call.

    Example: ``datetime.datetime(2024, 1, 15, 12, 30, 0)``.
    """
    parts = [
        value.year,
        value.month,
        value.day,
        value.hour,
        value.minute,
        value.second,
    ]
    if value.microsecond:
        parts.append(value.microsecond)
    args = ", ".join(str(object=p) for p in parts)
    return f"datetime.datetime({args})"


@beartype
def format_datetime_epoch(value: datetime.datetime) -> str:
    """Format a datetime as seconds since the Unix epoch.

    Uses :meth:`datetime.datetime.timestamp`, so the result depends on
    whether the datetime is naive (assumed local time) or aware.

    Example: ``1705312200.0``.
    """
    return repr(value.timestamp())


@beartype
def format_date_java(value: datetime.date) -> str:
    """Format a date as a Java ``LocalDate.of(...)`` call.

    Example: ``LocalDate.of(2024, 1, 15)``.
    """
    return f"LocalDate.of({value.year}, {value.month}, {value.day})"


@beartype
def format_datetime_java_instant(value: datetime.datetime) -> str:
    """Format a datetime as a Java ``Instant.parse(...)`` call.

    Example: ``Instant.parse("2024-01-15T12:30:00")``.
    """
    return f'Instant.parse("{value.isoformat()}")'


@beartype
def format_datetime_java_zoned(value: datetime.datetime) -> str:
    """Format a datetime as a Java ``ZonedDateTime.of(...)`` call.

    Example: ``ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0,
    ZoneId.of("UTC"))``.
    """
    tz = value.tzname() or "UTC"
    nanos = value.microsecond * 1000
    return (
        f"ZonedDateTime.of({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second}, "
        f'{nanos}, ZoneId.of("{tz}"))'
    )


@beartype
def format_date_ruby(value: datetime.date) -> str:
    """Format a date as a Ruby ``Date.new(...)`` call.

    Example: ``Date.new(2024, 1, 15)``.
    """
    return f"Date.new({value.year}, {value.month}, {value.day})"


@beartype
def format_datetime_ruby(value: datetime.datetime) -> str:
    """Format a datetime as a Ruby ``Time.new(...)`` call.

    Example: ``Time.new(2024, 1, 15, 12, 30, 0)``.
    """
    return (
        f"Time.new({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second})"
    )


@beartype
def format_date_js(value: datetime.date) -> str:
    """Format a date as a JavaScript ``new Date(...)`` call.

    Example: ``new Date("2024-01-15")``.
    """
    return f'new Date("{value.isoformat()}")'


@beartype
def format_datetime_js(value: datetime.datetime) -> str:
    """Format a datetime as a JavaScript ``new Date(...)`` call.

    Example: ``new Date("2024-01-15T12:30:00")``.
    """
    return f'new Date("{value.isoformat()}")'


@beartype
def format_date_csharp(value: datetime.date) -> str:
    """Format a date as a C# ``new DateOnly(...)`` call.

    Example: ``new DateOnly(2024, 1, 15)``.
    """
    return f"new DateOnly({value.year}, {value.month}, {value.day})"


@beartype
def format_datetime_csharp(value: datetime.datetime) -> str:
    """Format a datetime as a C# ``new DateTime(...)`` call.

    Example: ``new DateTime(2024, 1, 15, 12, 30, 0)``.
    """
    return (
        f"new DateTime({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second})"
    )


_GO_MONTHS: dict[int, str] = {
    1: "time.January",
    2: "time.February",
    3: "time.March",
    4: "time.April",
    5: "time.May",
    6: "time.June",
    7: "time.July",
    8: "time.August",
    9: "time.September",
    10: "time.October",
    11: "time.November",
    12: "time.December",
}


@beartype
def format_date_go(value: datetime.date) -> str:
    """Format a date as a Go ``time.Date(...)`` call.

    Example: ``time.Date(2024, time.January, 15, 0, 0, 0, 0,
    time.UTC)``.
    """
    month = _GO_MONTHS[value.month]
    return (
        f"time.Date({value.year}, {month}, {value.day}, 0, 0, 0, 0, time.UTC)"
    )


@beartype
def format_datetime_go(value: datetime.datetime) -> str:
    """Format a datetime as a Go ``time.Date(...)`` call.

    Example: ``time.Date(2024, time.January, 15, 12, 30, 0, 0,
    time.UTC)``.
    """
    month = _GO_MONTHS[value.month]
    nanos = value.microsecond * 1000
    return (
        f"time.Date({value.year}, {month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second}, "
        f"{nanos}, time.UTC)"
    )


@beartype
def format_date_kotlin(value: datetime.date) -> str:
    """Format a date as a Kotlin ``LocalDate.of(...)`` call.

    Example: ``LocalDate.of(2024, 1, 15)``.
    """
    return f"LocalDate.of({value.year}, {value.month}, {value.day})"


@beartype
def format_datetime_kotlin(value: datetime.datetime) -> str:
    """Format a datetime as a Kotlin ``LocalDateTime.of(...)`` call.

    Example: ``LocalDateTime.of(2024, 1, 15, 12, 30, 0)``.
    """
    return (
        f"LocalDateTime.of({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second})"
    )


@beartype
def format_date_cpp(value: datetime.date) -> str:
    """Format a date as a C++ chrono year_month_day literal.

    Example:
    ``std::chrono::year_month_day{std::chrono::year{2024},
    std::chrono::month{1}, std::chrono::day{15}}``.
    """
    return (
        f"std::chrono::year_month_day{{"
        f"std::chrono::year{{{value.year}}}, "
        f"std::chrono::month{{{value.month}}}, "
        f"std::chrono::day{{{value.day}}}}}"
    )


@beartype
def format_datetime_cpp(value: datetime.datetime) -> str:
    """Format a datetime as a C++ chrono time_point construction.

    Uses ``std::chrono::sys_days`` combined with a time-of-day
    duration.

    Example: ``std::chrono::sys_days{std::chrono::year_month_day{...}}
    + std::chrono::hours{12} + ...``.
    """
    ymd = format_date_cpp(value=value)
    parts = [f"std::chrono::sys_days{{{ymd}}}"]
    if value.hour:
        parts.append(f"std::chrono::hours{{{value.hour}}}")
    if value.minute:
        parts.append(f"std::chrono::minutes{{{value.minute}}}")
    if value.second:
        parts.append(f"std::chrono::seconds{{{value.second}}}")
    if value.microsecond:
        parts.append(f"std::chrono::microseconds{{{value.microsecond}}}")
    return " + ".join(parts)


def format_bytes_hex(value: bytes) -> str:
    """Format bytes as a hex string literal.

    Example: ``b"Hello"`` → ``"48656c6c6f"``.
    """
    return f'"{value.hex()}"'


def format_bytes_python(value: bytes) -> str:
    """Format bytes as a Python ``bytes`` literal.

    Example: ``b"Hello"`` → ``b'Hello'``.
    """
    return repr(value)


@beartype
def format_date_rust(value: datetime.date) -> str:
    """Format a date as a Rust ``NaiveDate::from_ymd_opt(...)`` call.

    Example: ``NaiveDate::from_ymd_opt(2024, 1, 15).unwrap()``.
    """
    return (
        f"NaiveDate::from_ymd_opt({value.year}, {value.month}, {value.day})"
        ".unwrap()"
    )


@beartype
def format_datetime_rust(value: datetime.datetime) -> str:
    """Format a datetime as a Rust ``NaiveDateTime::new(...)`` call.

    Example:
    ``NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(),
    NaiveTime::from_hms_opt(12, 30, 0).unwrap())``.
    """
    date = format_date_rust(value=value)
    if value.microsecond:
        time_call = (
            f"NaiveTime::from_hms_micro_opt("
            f"{value.hour}, {value.minute}, {value.second}, "
            f"{value.microsecond}).unwrap()"
        )
    else:
        time_call = (
            f"NaiveTime::from_hms_opt("
            f"{value.hour}, {value.minute}, {value.second}).unwrap()"
        )
    return f"NaiveDateTime::new({date}, {time_call})"


@beartype
def format_date_php(value: datetime.date) -> str:
    """Format a date as a PHP ``new DateTime(...)`` call.

    Example: ``new DateTime("2024-01-15")``.
    """
    return f'new DateTime("{value.isoformat()}")'


@beartype
def format_datetime_php(value: datetime.datetime) -> str:
    """Format a datetime as a PHP ``new DateTime(...)`` call.

    Example: ``new DateTime("2024-01-15T12:30:00")``.
    """
    return f'new DateTime("{value.isoformat()}")'


@beartype
def format_variable_declaration_python(name: str, value: str) -> str:
    """Format a Python variable declaration.

    Example: ``"x"`` and ``"[1, 2]"`` → ``"x = [1, 2]"``.
    """
    return f"{name} = {value}"


@beartype
def format_variable_declaration_js(name: str, value: str) -> str:
    """Format a JavaScript/TypeScript ``const`` declaration.

    Example: ``"x"`` and ``"[1, 2]"`` → ``"const x = [1, 2];"``
    """
    return f"const {name} = {value};"


@beartype
def format_variable_declaration_go(name: str, value: str) -> str:
    """Format a Go short variable declaration.

    Example: ``"x"`` and ``"[]any{1, 2}"`` → ``"x := []any{1, 2}"``.
    """
    return f"{name} := {value}"


@beartype
def format_variable_declaration_ruby(name: str, value: str) -> str:
    """Format a Ruby variable assignment.

    Example: ``"x"`` and ``"[1, 2]"`` → ``"x = [1, 2]"``.
    """
    return f"{name} = {value}"


@beartype
def format_variable_declaration_csharp(name: str, value: str) -> str:
    """Format a C# ``var`` declaration.

    Example: ``"x"`` and ``"new object[]{1}"`` → ``"var x = new object[]{1};"``
    """
    return f"var {name} = {value};"


@beartype
def format_variable_declaration_cpp(name: str, value: str) -> str:
    """Format a C++ ``auto`` declaration.

    Example: ``"x"`` and ``"{1, 2}"`` → ``"auto x = {1, 2};"``
    """
    return f"auto {name} = {value};"


@beartype
def format_variable_declaration_java(name: str, value: str) -> str:
    """Format a Java ``var`` declaration.

    Example: ``"x"`` and ``"new Object[]{1}"`` → ``"var x = new Object[]{1};"``
    """
    return f"var {name} = {value};"


@beartype
def format_variable_declaration_kotlin(name: str, value: str) -> str:
    """Format a Kotlin ``val`` declaration.

    Example: ``"x"`` and ``"listOf(1, 2)"`` → ``"val x = listOf(1, 2)"``
    """
    return f"val {name} = {value}"


@beartype
def format_variable_declaration_swift(name: str, value: str) -> str:
    """Format a Swift ``let`` declaration.

    Example: ``"x"`` and ``"[1, 2]"`` → ``"let x = [1, 2]"``
    """
    return f"let {name} = {value}"


@beartype
def format_variable_declaration_rust(name: str, value: str) -> str:
    """Format a Rust ``let`` declaration.

    Example: ``"x"`` and ``"vec![1, 2]"`` → ``"let x = vec![1, 2];"``
    """
    return f"let {name} = {value};"


@beartype
def format_variable_declaration_php(name: str, value: str) -> str:
    """Format a PHP variable assignment.

    The ``$`` sigil is prepended automatically.

    Example: ``"x"`` and ``"[1, 2]"`` → ``"$x = [1, 2];"``
    """
    return f"${name} = {value};"


@beartype
def format_variable_declaration_elixir(name: str, value: str) -> str:
    """Format an Elixir variable assignment.

    Example: ``"x"`` and ``"[1, 2]"`` → ``"x = [1, 2]"``
    """
    return f"{name} = {value}"


@beartype
def format_variable_declaration_clojure(name: str, value: str) -> str:
    """Format a Clojure ``def`` binding.

    Example: ``"my_data"`` and ``"{:a 1}"`` → ``"(def my_data {:a 1})"``
    """
    return f"(def {name} {value})"


@beartype
def format_variable_declaration_scala(name: str, value: str) -> str:
    """Format a Scala ``val`` declaration.

    Example: ``"x"`` and ``"List(1, 2)"`` → ``"val x = List(1, 2)"``
    """
    return f"val {name} = {value}"


@beartype
def format_variable_declaration_haskell(name: str, value: str) -> str:
    """Format a Haskell variable binding.

    Example: ``"x"`` and ``"HList [1, 2]"`` → ``"x = HList [1, 2]"``
    """
    return f"{name} = {value}"


@beartype
def format_variable_declaration_fsharp(name: str, value: str) -> str:
    """Format an F# ``let`` declaration with explicit ``Val`` type.

    Example: ``"x"`` and ``"FList [...]"`` → ``"let x: Val = FList [...]"``
    """
    return f"let {name}: Val = {value}"


def to_fsharp_val(value: str) -> str:
    """Wrap a pre-formatted value string in an F# ``Val`` constructor.

    Inspects the string representation to determine the appropriate
    discriminated-union constructor: ``FStr``, ``FInt``, ``FFloat``,
    or passes through values that are already ``Val`` expressions
    (``FNull``, ``FBool``, ``FList``, ``FMap``, ``FSet``).
    """
    _val_prefixes = (
        "FNull",
        "FBool",
        "FList",
        "FMap",
        "FSet",
        "FStr",
        "FInt",
        "FFloat",
    )
    if any(value.startswith(p) for p in _val_prefixes):
        return value
    if value.startswith('"') and value.endswith('"'):
        return f"FStr {value}"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"FInt({value}L)" if negative else f"FInt {value}L"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f"FFloat({value})" if negative else f"FFloat {value}"
    except ValueError:
        pass
    if float_result is not None:
        return float_result
    return value


@beartype
def passthrough_list_entry(item: str) -> str:
    """Return *item* unchanged.

    Use this as ``format_list_entry`` for languages where list entries
    need no extra formatting.
    """
    return item


@beartype
def format_variable_assignment_clojure(name: str, value: str) -> str:
    """Format a Clojure ``def`` reassignment.

    Example: ``"my_data"`` and ``"{:a 1}"`` → ``"(def my_data {:a 1})"``
    """
    return f"(def {name} {value})"


@beartype
def format_date_r(value: datetime.date) -> str:
    """Format a date as an R ``as.Date(...)`` call.

    Example: ``datetime.date(2024, 1, 15)`` → ``as.Date("2024-01-15")``.
    """
    return f'as.Date("{value.isoformat()}")'


@beartype
def format_datetime_r(value: datetime.datetime) -> str:
    """Format a datetime as an R ``as.POSIXct(...)`` call.

    The ISO 8601 offset in the string is used for parsing, so no
    separate ``tz`` argument is needed.

    Example: ``datetime.datetime(2024, 1, 15, 12, 30)`` →
    ``as.POSIXct("2024-01-15T12:30:00")``.
    """
    return f'as.POSIXct("{value.isoformat()}")'


@beartype
def format_variable_declaration_r(name: str, value: str) -> str:
    """Format an R variable assignment using ``<-``.

    Example: ``"x"`` and ``"list(1, 2)"`` → ``"x <- list(1, 2)"``
    """
    return f"{name} <- {value}"


@beartype
def format_variable_assignment_r(name: str, value: str) -> str:
    """Format an R assignment to an existing variable using ``<-``.

    Example: ``"x"`` and ``"list(1, 2)"`` → ``"x <- list(1, 2)"``
    """
    return f"{name} <- {value}"


@beartype
def format_date_dart(value: datetime.date) -> str:
    """Format a date as a Dart ``DateTime.parse(...)`` call.

    Example: ``DateTime.parse("2024-01-15")``.
    """
    return f'DateTime.parse("{value.isoformat()}")'


@beartype
def format_datetime_dart(value: datetime.datetime) -> str:
    """Format a datetime as a Dart ``DateTime.parse(...)`` call.

    Example: ``DateTime.parse("2024-01-15T12:30:00")``.
    """
    return f'DateTime.parse("{value.isoformat()}")'


@beartype
def format_variable_declaration_dart(name: str, value: str) -> str:
    """Format a Dart ``final`` declaration.

    Example: ``"x"`` and ``"[1, 2]"`` → ``"final x = [1, 2];"``
    """
    return f"final {name} = {value};"


@beartype
def format_variable_declaration_julia(name: str, value: str) -> str:
    """Format a Julia variable assignment.

    Example: ``"x"`` and ``"[1, 2]"`` → ``"x = [1, 2]"``
    """
    return f"{name} = {value}"


@beartype
def format_date_julia(value: datetime.date) -> str:
    """Format a date as a Julia ``Date(...)`` constructor call.

    Example: ``datetime.date(2024, 1, 15)`` → ``Date(2024, 1, 15)``.
    """
    return f"Date({value.year}, {value.month}, {value.day})"


@beartype
def format_datetime_julia(value: datetime.datetime) -> str:
    """Format a datetime as a Julia ``DateTime(...)`` constructor call.

    Example: ``datetime.datetime(2024, 1, 15, 12, 30, 0)`` →
    ``DateTime(2024, 1, 15, 12, 30, 0)``.
    """
    return (
        f"DateTime({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second})"
    )


@beartype
def format_variable_assignment_python(name: str, value: str) -> str:
    """Format a Python variable assignment to an existing variable.

    Example: ``"x"`` and ``"[1, 2]"`` → ``"x = [1, 2]"``.
    """
    return f"{name} = {value}"


@beartype
def format_variable_assignment_js(name: str, value: str) -> str:
    """Format a JavaScript/TypeScript assignment to an existing variable.

    Example: ``"x"`` and ``"[1, 2]"`` → ``"x = [1, 2];"``
    """
    return f"{name} = {value};"


@beartype
def format_variable_assignment_go(name: str, value: str) -> str:
    """Format a Go assignment to an existing variable.

    Example: ``"x"`` and ``"[]any{1, 2}"`` → ``"x = []any{1, 2}"``.
    """
    return f"{name} = {value}"


@beartype
def format_variable_assignment_ruby(name: str, value: str) -> str:
    """Format a Ruby assignment to an existing variable.

    Example: ``"x"`` and ``"[1, 2]"`` → ``"x = [1, 2]"``.
    """
    return f"{name} = {value}"


@beartype
def format_variable_assignment_csharp(name: str, value: str) -> str:
    """Format a C# assignment to an existing variable.

    Example: ``"x"`` and ``"new object[]{1}"`` → ``"x = new object[]{1};"``
    """
    return f"{name} = {value};"


@beartype
def format_variable_assignment_cpp(name: str, value: str) -> str:
    """Format a C++ assignment to an existing variable.

    Example: ``"x"`` and ``"{1, 2}"`` → ``"x = {1, 2};"``
    """
    return f"{name} = {value};"


@beartype
def format_variable_assignment_java(name: str, value: str) -> str:
    """Format a Java assignment to an existing variable.

    Example: ``"x"`` and ``"new Object[]{1}"`` → ``"x = new Object[]{1};"``
    """
    return f"{name} = {value};"


@beartype
def format_variable_assignment_kotlin(name: str, value: str) -> str:
    """Format a Kotlin assignment to an existing variable.

    Example: ``"x"`` and ``"listOf(1, 2)"`` → ``"x = listOf(1, 2)"``
    """
    return f"{name} = {value}"


@beartype
def format_variable_assignment_swift(name: str, value: str) -> str:
    """Format a Swift assignment to an existing variable.

    Example: ``"x"`` and ``"[1, 2]"`` → ``"x = [1, 2]"``
    """
    return f"{name} = {value}"


@beartype
def format_variable_assignment_rust(name: str, value: str) -> str:
    """Format a Rust assignment to an existing variable.

    Example: ``"x"`` and ``"vec![1, 2]"`` → ``"x = vec![1, 2];"``
    """
    return f"{name} = {value};"


@beartype
def format_variable_assignment_scala(name: str, value: str) -> str:
    """Format a Scala assignment to an existing variable.

    Example: ``"x"`` and ``"List(1, 2)"`` → ``"x = List(1, 2)"``
    """
    return f"{name} = {value}"


@beartype
def format_variable_assignment_php(name: str, value: str) -> str:
    """Format a PHP assignment to an existing variable.

    The ``$`` sigil is prepended automatically.

    Example: ``"x"`` and ``"[1, 2]"`` → ``"$x = [1, 2];"``
    """
    return f"${name} = {value};"


@beartype
def format_variable_assignment_elixir(name: str, value: str) -> str:
    """Format an Elixir assignment to an existing variable.

    Example: ``"x"`` and ``"[1, 2]"`` → ``"x = [1, 2]"``
    """
    return f"{name} = {value}"


@beartype
def format_variable_assignment_haskell(name: str, value: str) -> str:
    """Format a Haskell variable binding (same syntax for new and
    existing).

    Example: ``"x"`` and ``"HList [1, 2]"`` → ``"x = HList [1, 2]"``
    """
    return f"{name} = {value}"


@beartype
def format_variable_assignment_dart(name: str, value: str) -> str:
    """Format a Dart assignment to an existing variable.

    Example: ``"x"`` and ``"[1, 2]"`` → ``"x = [1, 2];"``
    """
    return f"{name} = {value};"


@beartype
def format_variable_assignment_fsharp(name: str, value: str) -> str:
    """Format an F# variable assignment to an existing binding.

    Example: ``"x"`` and ``"FList [1; 2]"`` → ``"let x: Val = FList [1; 2]"``
    """
    return f"let {name}: Val = {value}"


@beartype
def format_variable_declaration_ocaml(name: str, value: str) -> str:
    """Format an OCaml ``let`` declaration with explicit ``val_t`` type.

    Example: ``"x"`` and ``"OList [...]"`` → ``"let x : val_t = OList [...]"``
    """
    return f"let {name} : val_t = {value}"


@beartype
def format_variable_assignment_ocaml(name: str, value: str) -> str:
    """Format an OCaml ``let`` re-binding with explicit ``val_t`` type.

    Example: ``"x"`` and ``"OList [...]"`` → ``"let x : val_t = OList [...]"``
    """
    return f"let {name} : val_t = {value}"


def to_ocaml_val(value: str) -> str:
    """Wrap a pre-formatted value string in an OCaml ``val_t`` constructor.

    Inspects the string representation to determine the appropriate
    variant constructor: ``OStr``, ``OInt``, ``OFloat``, or passes through
    values that are already ``val_t`` expressions
    (``ONull``, ``OBool``, ``OList``, ``OMap``, ``OSet``).
    """
    _val_prefixes = (
        "ONull",
        "OBool",
        "OList",
        "OMap",
        "OSet",
        "OStr",
        "OInt",
        "OFloat",
    )
    if any(value.startswith(p) for p in _val_prefixes):
        return value
    if value.startswith('"') and value.endswith('"'):
        return f"OStr {value}"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"OInt ({value})" if negative else f"OInt {value}"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f"OFloat ({value})" if negative else f"OFloat {value}"
    except ValueError:
        pass
    if float_result is not None:
        return float_result
    return value


def dict_entry_with_separator(separator: str) -> Callable[[str, str], str]:
    """Return a ``format_dict_entry`` callable that joins key and value
    with *separator*.

    Example: ``dict_entry_with_separator(": ")("k", "v")`` → ``"k: v"``.
    """

    @beartype
    def _format(key: str, value: str) -> str:
        """Format a dict entry by joining key and value with separator."""
        return f"{key}{separator}{value}"

    return _format


@beartype
def passthrough_set_entry(item: str) -> str:
    """Return *item* unchanged.

    Use this as ``format_set_entry`` for languages where set entries
    need no extra formatting.
    """
    return item
