"""Functions for formatting scalars as language-specific literals."""

import datetime
import functools
import re
from collections.abc import Callable
from typing import Any

from beartype import beartype
from json_to_schema import (  # pyrefly: ignore[missing-import]
    infer_schema,
)

from literalizer._types import Value

# JSON-native Python types that json-to-schema can represent accurately.
# literalizer's Value type also includes bytes, date, and datetime, which
# exist in YAML but not in JSON.  json-to-schema misclassifies these as
# "string", so when any non-JSON-native value is present we skip schema
# inference entirely and let the language mapper fall through to its
# fallback opener.
_JSON_NATIVE_TYPES = (str, int, float, bool, type(None), list, dict)


def _all_json_native(values: Value) -> bool:
    """Check whether every scalar in *values* is a JSON-native type.

    Walks into nested lists and dict values so that YAML-only types
    (``bytes``, ``date``, ``datetime``) are detected at any depth.
    """
    if isinstance(values, list):
        return all(_all_json_native(values=v) for v in values)
    if isinstance(values, dict):
        return all(_all_json_native(values=v) for v in values.values())
    return isinstance(values, _JSON_NATIVE_TYPES)


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


@beartype
def format_bytes_hex(value: bytes) -> str:
    """Format bytes as a hex string literal.

    Example: ``b"Hello"`` → ``"48656c6c6f"``.
    """
    return f'"{value.hex()}"'


@beartype
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
def passthrough_sequence_entry(item: str) -> str:
    """Return *item* unchanged.

    Use this as ``format_sequence_entry`` for languages where sequence entries
    need no extra formatting.
    """
    return item


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


_MATLAB_CONTROL_CHAR_THRESHOLD = 32


@beartype
def format_string_matlab(value: str) -> str:
    r"""Format a string using MATLAB double-quoted string escaping rules.

    MATLAB double-quoted strings (the ``string`` type) interpret backslash
    escape sequences: ``\\`` for a literal backslash, ``\n`` for newline,
    ``\t`` for tab, etc.  Double quotes are escaped by doubling (``""``).
    Control characters (code points 0-31) are emitted as ``char(N)``
    expressions joined with ``+``.

    Example: ``hello "world" bye`` -> ``"hello ""world"" bye"``.
    """
    parts: list[str] = []
    for segment in re.split(pattern=r"([\x00-\x1f])", string=value):
        if not segment:
            continue
        if len(segment) == 1 and ord(segment) < _MATLAB_CONTROL_CHAR_THRESHOLD:
            parts.append(f"char({ord(segment)})")
        else:
            escaped = segment.replace("\\", "\\\\").replace('"', '""')
            parts.append(f'"{escaped}"')
    if not parts:
        return '""'
    if len(parts) == 1:
        return parts[0]
    return " + ".join(parts)


@beartype
def format_string_ada(value: str) -> str:
    r"""Format a string using Ada double-quote escaping.

    Ada has no backslash escaping — backslashes are literal characters.
    Only double quotes are escaped, by doubling them (``""``).
    Newlines and tabs are rendered as ``\n`` / ``\t`` for readability
    since Ada string literals cannot span lines.

    Example: ``hello "world" bye`` → ``"hello ""world"" bye"``.
    """
    escaped = (
        value.replace("\n", "\\n").replace("\t", "\\t").replace('"', '""')
    )
    return f'"{escaped}"'


@beartype
def format_string_backslash(value: str) -> str:
    r"""Format a string using backslash escaping.

    Escapes backslashes, double quotes, and newlines with a backslash
    prefix, then wraps the result in double quotes.

    Example: ``hello "world"`` → ``"hello \"world\""``.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    return f'"{escaped}"'


@beartype
def format_string_backslash_dollar(value: str) -> str:
    r"""Format a string using backslash escaping, including ``$``.

    Escapes backslashes, double quotes, newlines, tabs, and dollar signs
    with a backslash prefix, then wraps the result in double quotes.

    Example: ``price $10`` → ``"price \$10"``.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("$", "\\$")
    )
    return f'"{escaped}"'


def _vb_string_parts(value: str) -> list[str]:  # noqa: C901,PLR0912  # pylint: disable=too-complex,too-many-branches
    """Generate VB.NET string parts for control character handling."""
    vb_control_char_threshold = 32
    parts: list[str] = []
    current = ""
    i = 0
    while i < len(value):
        c = value[i]
        if c == '"':
            current += '""'
            i += 1
        elif c == "\r" and i + 1 < len(value) and value[i + 1] == "\n":
            if current:
                parts.append(f'"{current}"')
                current = ""
            parts.append("vbCrLf")
            i += 2
        elif c == "\n":
            if current:
                parts.append(f'"{current}"')
                current = ""
            parts.append("Chr(10)")
            i += 1
        elif c == "\r":
            if current:
                parts.append(f'"{current}"')
                current = ""
            parts.append("Chr(13)")
            i += 1
        elif c == "\t":
            if current:
                parts.append(f'"{current}"')
                current = ""
            parts.append("vbTab")
            i += 1
        elif ord(c) < vb_control_char_threshold:
            if current:
                parts.append(f'"{current}"')
                current = ""
            parts.append(f"Chr({ord(c)})")
            i += 1
        else:
            current += c
            i += 1
    if current:
        parts.append(f'"{current}"')
    return parts


@beartype
def format_string_vb(value: str) -> str:
    r"""Format a string using VB.NET string escaping rules.

    VB.NET strings use ``""`` to escape embedded double quotes and do not
    support backslash escapes.  Control characters such as newlines and
    tabs are expressed via ``vbCrLf``, ``vbTab``, or ``Chr(N)`` string
    concatenation.

    Example: ``hi "world" bye`` → ``"hi ""world"" bye"``.
    Example: ``line1\nline2`` → ``"line1" & Chr(10) & "line2"``.
    """
    parts = _vb_string_parts(value)  # type: ignore[misc]
    if not parts:
        return '""'
    if len(parts) == 1:
        return parts[0]
    return " & ".join(parts)


@beartype
def passthrough_set_entry(item: str) -> str:
    """Return *item* unchanged.

    Use this as ``format_set_entry`` for languages where set entries
    need no extra formatting.
    """
    return item


@beartype
def fixed_sequence_open(*, open_str: str) -> Callable[[list[Value]], str]:
    """Return a ``sequence_open`` callable that always returns *open_str*.

    Use this as ``sequence_open`` when the opening delimiter for sequences
    is a fixed string that does not depend on the sequence contents.

    Example: ``fixed_sequence_open(open_str="[")([1, 2, 3])`` → ``"["``.
    """

    @beartype
    def _open(_items: list[Value]) -> str:
        """Return the fixed opening delimiter."""
        return open_str

    return _open


@beartype
def fixed_dict_open(*, open_str: str) -> Callable[[dict[str, Value]], str]:
    """Return a ``dict_open`` callable that always returns *open_str*.

    Use this as ``dict_open`` when the opening delimiter for dicts
    is a fixed string that does not depend on the dict contents.

    Example: ``fixed_dict_open(open_str="{")({"a": 1})`` → ``"{"``.
    """

    @beartype
    def _open(_items: dict[str, Value]) -> str:
        """Return the fixed opening delimiter."""
        return open_str

    return _open


@beartype
def _typed_sequence_open(
    items: list[Value],
    *,
    schema_to_opener: Callable[[dict[str, Any]], str | None],
    fallback: str,
) -> str:
    """Infer an item schema and return the language-specific opener.

    Uses ``json-to-schema`` to infer a JSON Schema from the list
    values, then passes the ``items`` sub-schema to
    *schema_to_opener* which returns the language-specific opening
    delimiter.  When inference is not possible or *schema_to_opener*
    returns ``None``, *fallback* is returned instead.

    See ``_JSON_NATIVE_TYPES`` for why we skip inference for
    YAML-only types.
    """
    if not _all_json_native(values=items):
        return fallback
    schema: dict[str, Any] = infer_schema(value=items)
    item_schema: dict[str, Any] = schema.get("items", {})
    return schema_to_opener(item_schema) or fallback


@beartype
def typed_sequence_open(
    *,
    schema_to_opener: Callable[[dict[str, Any]], str | None],
    fallback: str,
) -> Callable[[list[Value]], str]:
    """Return a ``sequence_open`` callable that infers an item schema and
    delegates to *schema_to_opener*.

    When inference is not possible or *schema_to_opener* returns
    ``None``, *fallback* is used instead.

    Example::

        def my_opener(item_schema: dict[str, Any]) -> str | None:
            if item_schema.get("type") == "string":
                return "[]string{"
            return None

        sequence_open = typed_sequence_open(
            schema_to_opener=my_opener,
            fallback="[]any{",
        )
    """
    return functools.partial(
        _typed_sequence_open,
        schema_to_opener=schema_to_opener,
        fallback=fallback,
    )


@beartype
def _typed_dict_open(
    items: dict[str, Value],
    *,
    schema_to_opener: Callable[[dict[str, Any]], str | None],
    fallback: str,
) -> str:
    """Infer a value schema and return the language-specific opener.

    Uses ``json-to-schema`` to infer a JSON Schema from the dict
    values (treated as a list), then passes the ``items`` sub-schema
    to *schema_to_opener* which returns the language-specific opening
    delimiter.  When inference is not possible or *schema_to_opener*
    returns ``None``, *fallback* is returned instead.

    See ``_JSON_NATIVE_TYPES`` for why we skip inference for
    YAML-only types.
    """
    values = list(items.values())
    if not _all_json_native(values=values):
        return fallback
    schema: dict[str, Any] = infer_schema(value=values)
    value_schema: dict[str, Any] = schema.get("items", {})
    return schema_to_opener(value_schema) or fallback


@beartype
def typed_dict_open(
    *,
    schema_to_opener: Callable[[dict[str, Any]], str | None],
    fallback: str,
) -> Callable[[dict[str, Value]], str]:
    """Return a ``dict_open`` callable that infers a value schema and
    delegates to *schema_to_opener*.

    When inference is not possible or *schema_to_opener* returns
    ``None``, *fallback* is used instead.

    Example::

        def my_opener(value_schema: dict[str, Any]) -> str | None:
            if value_schema.get("type") == "string":
                return "map[string]string{"
            return None

        dict_open = typed_dict_open(
            schema_to_opener=my_opener,
            fallback="map[string]any{",
        )
    """
    return functools.partial(
        _typed_dict_open,
        schema_to_opener=schema_to_opener,
        fallback=fallback,
    )
