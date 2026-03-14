"""Convert JSON data to native language literals."""

from __future__ import annotations

import dataclasses
import datetime
import json
from collections.abc import Callable, Mapping, Sequence
from typing import Any, Protocol, cast, runtime_checkable

import yaml
from beartype import BeartypeConf, beartype

type _Scalar = (
    str | int | float | bool | None | datetime.date | datetime.datetime
)
type _Value = _Scalar | list[_Value] | dict[str, _Value]


def format_date_iso(value: datetime.date) -> str:
    """Format a date as an ISO 8601 quoted string literal.

    Example: ``datetime.date(2024, 1, 15)`` → ``"2024-01-15"``.
    """
    return f'"{value.isoformat()}"'


def format_datetime_iso(value: datetime.datetime) -> str:
    """Format a datetime as an ISO 8601 quoted string literal.

    Example: ``datetime.datetime(2024, 1, 15, 12, 30)`` →
    ``"2024-01-15T12:30:00"``.
    """
    return f'"{value.isoformat()}"'


def format_date_python(value: datetime.date) -> str:
    """Format a date as a Python ``datetime.date(...)`` constructor call.

    Example: ``datetime.date(2024, 1, 15)``.
    """
    return f"datetime.date({value.year}, {value.month}, {value.day})"


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


def format_datetime_epoch(value: datetime.datetime) -> str:
    """Format a datetime as seconds since the Unix epoch.

    Uses :meth:`datetime.datetime.timestamp`, so the result depends on
    whether the datetime is naive (assumed local time) or aware.

    Example: ``1705312200.0``.
    """
    return repr(value.timestamp())


def format_date_java(value: datetime.date) -> str:
    """Format a date as a Java ``LocalDate.of(...)`` call.

    Example: ``LocalDate.of(2024, 1, 15)``.
    """
    return f"LocalDate.of({value.year}, {value.month}, {value.day})"


def format_datetime_java_instant(value: datetime.datetime) -> str:
    """Format a datetime as a Java ``Instant.parse(...)`` call.

    Example: ``Instant.parse("2024-01-15T12:30:00")``.
    """
    return f'Instant.parse("{value.isoformat()}")'


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


def format_date_ruby(value: datetime.date) -> str:
    """Format a date as a Ruby ``Date.new(...)`` call.

    Example: ``Date.new(2024, 1, 15)``.
    """
    return f"Date.new({value.year}, {value.month}, {value.day})"


def format_datetime_ruby(value: datetime.datetime) -> str:
    """Format a datetime as a Ruby ``Time.new(...)`` call.

    Example: ``Time.new(2024, 1, 15, 12, 30, 0)``.
    """
    return (
        f"Time.new({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second})"
    )


def format_date_js(value: datetime.date) -> str:
    """Format a date as a JavaScript ``new Date(...)`` call.

    Example: ``new Date("2024-01-15")``.
    """
    return f'new Date("{value.isoformat()}")'


def format_datetime_js(value: datetime.datetime) -> str:
    """Format a datetime as a JavaScript ``new Date(...)`` call.

    Example: ``new Date("2024-01-15T12:30:00")``.
    """
    return f'new Date("{value.isoformat()}")'


def format_date_csharp(value: datetime.date) -> str:
    """Format a date as a C# ``new DateOnly(...)`` call.

    Example: ``new DateOnly(2024, 1, 15)``.
    """
    return f"new DateOnly({value.year}, {value.month}, {value.day})"


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


def format_date_go(value: datetime.date) -> str:
    """Format a date as a Go ``time.Date(...)`` call.

    Example: ``time.Date(2024, time.January, 15, 0, 0, 0, 0,
    time.UTC)``.
    """
    month = _GO_MONTHS[value.month]
    return (
        f"time.Date({value.year}, {month}, {value.day}, 0, 0, 0, 0, time.UTC)"
    )


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


def format_date_kotlin(value: datetime.date) -> str:
    """Format a date as a Kotlin ``LocalDate.of(...)`` call.

    Example: ``LocalDate.of(2024, 1, 15)``.
    """
    return f"LocalDate.of({value.year}, {value.month}, {value.day})"


def format_datetime_kotlin(value: datetime.datetime) -> str:
    """Format a datetime as a Kotlin ``LocalDateTime.of(...)`` call.

    Example: ``LocalDateTime.of(2024, 1, 15, 12, 30, 0)``.
    """
    return (
        f"LocalDateTime.of({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second})"
    )


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


@runtime_checkable
class Language(Protocol):
    """Protocol describing how a language formats scalar literals and
    collections.

    Implement this protocol to add support for additional languages
    beyond the built-in defaults.
    """

    @property
    def null_literal(self) -> str:
        """The literal representing null/None."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def true_literal(self) -> str:
        """The literal representing true/True."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def false_literal(self) -> str:
        """The literal representing false/False."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def collection_open(self) -> str:
        """The opening delimiter for collections."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def collection_close(self) -> str:
        """The closing delimiter for collections."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dict_separator(self) -> str:
        """The separator between dict keys and values."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a :class:`datetime.date` as a string
        literal.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a :class:`datetime.datetime` as a
        string literal.
        """
        ...  # pylint: disable=unnecessary-ellipsis


@dataclasses.dataclass(frozen=True)
class LanguageSpec:
    """A concrete implementation of :class:`Language`.

    Predefined specs for common languages are available as module-level
    constants (e.g. :data:`PYTHON`, :data:`JAVASCRIPT`).  Create custom
    instances to support additional languages or override defaults.
    """

    null_literal: str
    true_literal: str
    false_literal: str
    collection_open: str
    collection_close: str
    dict_separator: str
    format_date: Callable[[datetime.date], str] = format_date_iso
    format_datetime: Callable[[datetime.datetime], str] = format_datetime_iso


PYTHON = LanguageSpec(
    null_literal="None",
    true_literal="True",
    false_literal="False",
    collection_open="(",
    collection_close=")",
    dict_separator=": ",
)

CSHARP = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="(",
    collection_close=")",
    dict_separator=": ",
)

JAVASCRIPT = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="[",
    collection_close="]",
    dict_separator=": ",
)

TYPESCRIPT = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="[",
    collection_close="]",
    dict_separator=": ",
)

RUBY = LanguageSpec(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    collection_open="[",
    collection_close="]",
    dict_separator=" => ",
)

GO = LanguageSpec(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    collection_open="{",
    collection_close="}",
    dict_separator=": ",
)

CPP = LanguageSpec(
    null_literal="nullptr",
    true_literal="true",
    false_literal="false",
    collection_open="{",
    collection_close="}",
    dict_separator=": ",
)

JAVA = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="{",
    collection_close="}",
    dict_separator=": ",
)

KOTLIN = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="listOf(",
    collection_close=")",
    dict_separator=": ",
)


@beartype
def _format_scalar(*, value: _Scalar, spec: Language) -> str:
    """Format a scalar JSON value as a native language literal."""
    if value is None:
        result = spec.null_literal
    elif isinstance(value, bool):
        result = spec.true_literal if value else spec.false_literal
    elif isinstance(value, int):
        result = str(object=value)
    elif isinstance(value, float):
        result = repr(value)
    elif isinstance(value, str):
        escaped = (
            value.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
        )
        result = f'"{escaped}"'
    elif isinstance(value, datetime.datetime):
        result = spec.format_datetime(value)
    elif isinstance(value, datetime.date):
        result = spec.format_date(value)
    else:
        msg = f"Unsupported scalar type: {type(value)}"
        raise TypeError(msg)
    return result


@beartype
def _format_value(*, value: _Value, spec: Language) -> str:
    """Format any JSON value as a native language literal.

    Handles scalars, lists (recursively), and dicts.
    """
    if isinstance(value, dict):
        pairs = [
            f"{_format_value(value=k, spec=spec)}{spec.dict_separator}"
            f"{_format_value(value=v, spec=spec)}"
            for k, v in value.items()
        ]
        return "{" + ", ".join(pairs) + "}"

    if isinstance(value, list):
        items = [_format_value(value=v, spec=spec) for v in value]
        joined = ", ".join(items)
        # Single-element tuples need a trailing comma in Python/C#.
        if len(items) == 1 and spec.collection_open == "(":
            joined += ","
        return f"{spec.collection_open}{joined}{spec.collection_close}"

    return _format_scalar(value=value, spec=spec)


@beartype(conf=BeartypeConf(is_pep484_tower=True))
def literalize(
    *,
    data: Sequence[Any] | Mapping[str, Any] | float | bool | None,
    language: Language,
    prefix: str,
    wrap: bool,
) -> str:
    r"""Convert data to native language literal text.

    Each element (or key-value pair) is formatted as a native literal
    for the given language with a trailing comma and the specified prefix.

    Args:
        data: A scalar, sequence, or mapping.  Scalars (strings,
            numbers, booleans, ``None``) are formatted as a single
            literal value.  Sequences may contain scalars, sequences,
            or mappings with nesting to arbitrary depth.  Mappings are
            formatted as one key-value pair per line using the
            language's dict separator.
        language: A :class:`Language` instance describing how to format
            literals.  Use one of the built-in constants
            (e.g. :data:`PYTHON`, :data:`GO`) or provide your own.
        prefix: String to prepend to each output line (e.g. ``"        "``
            for 8-space indent, or ``"\t\t"`` for 2-tab indent).
        wrap: If True, wrap the output in delimiters
            (``[`` … ``]`` for arrays, ``{`` … ``}`` for dicts).
            Ignored for scalar values.
    """
    spec = language

    # Handle scalars (check str before Sequence since str is a Sequence).
    if isinstance(data, (str, int, float, bool)) or data is None:
        return f"{prefix}{_format_scalar(value=data, spec=spec)}"

    effective_prefix = prefix if not wrap else (prefix or "    ")
    lines: list[str] = []

    if isinstance(data, dict):
        for k, v in cast("dict[str, object]", data).items():
            formatted_key = _format_value(value=k, spec=spec)
            formatted_val = _format_value(value=v, spec=spec)
            lines.append(
                f"{effective_prefix}{formatted_key}{spec.dict_separator}{formatted_val},"
            )
    else:
        for item in data:
            formatted = _format_value(value=item, spec=spec)
            lines.append(f"{effective_prefix}{formatted},")

    body = "\n".join(lines)

    if not wrap or not body:
        return body

    if isinstance(data, dict):
        return f"{{\n{body}\n}}"

    return f"[\n{body}\n]"


@beartype
def literalize_json(
    *,
    json_string: str,
    language: Language,
    prefix: str,
    wrap: bool,
) -> str:
    r"""Convert a JSON string to native language literal text.

    This is a convenience wrapper around :func:`literalize` that
    accepts JSON as a string rather than a pre-parsed data structure.

    Args:
        json_string: A JSON string representing a scalar, array, or
            object.
        language: A :class:`Language` instance describing how to format
            literals.  Use one of the built-in constants
            (e.g. :data:`PYTHON`, :data:`GO`) or provide your own.
        prefix: String to prepend to each output line (e.g. ``"        "``
            for 8-space indent, or ``"\t\t"`` for 2-tab indent).
        wrap: If True, wrap the output in delimiters
            (``[`` … ``]`` for arrays, ``{`` … ``}`` for dicts).

    Raises:
        json.JSONDecodeError: If *json_string* is not valid JSON.
    """
    data = json.loads(s=json_string)
    return literalize(
        data=data,
        language=language,
        prefix=prefix,
        wrap=wrap,
    )


@beartype
def literalize_yaml(
    *,
    yaml_string: str,
    language: Language,
    prefix: str,
    wrap: bool,
) -> str:
    r"""Convert a YAML string to native language literal text.

    This is a convenience wrapper around :func:`literalize` that
    accepts YAML as a string rather than a pre-parsed data structure.

    Args:
        yaml_string: A YAML string representing a scalar, sequence, or
            mapping.
        language: A :class:`Language` instance describing how to format
            literals.  Use one of the built-in constants
            (e.g. :data:`PYTHON`, :data:`GO`) or provide your own.
        prefix: String to prepend to each output line (e.g. ``"        "``
            for 8-space indent, or ``"\t\t"`` for 2-tab indent).
        wrap: If True, wrap the output in delimiters
            (``[`` … ``]`` for arrays, ``{`` … ``}`` for dicts).

    Raises:
        yaml.YAMLError: If *yaml_string* is not valid YAML.
    """
    data = yaml.safe_load(stream=yaml_string)
    return literalize(
        data=data,
        language=language,
        prefix=prefix,
        wrap=wrap,
    )
