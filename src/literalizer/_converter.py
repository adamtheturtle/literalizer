"""Convert JSON data to native language literals."""

from __future__ import annotations

import dataclasses
import datetime
import json
from collections.abc import Iterable  # noqa: TC003
from io import StringIO
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

from beartype import BeartypeConf, beartype
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.error import YAMLError
from ruamel.yaml.tokens import CommentToken  # noqa: TC002

from literalizer.exceptions import JSONParseError, YAMLParseError

if TYPE_CHECKING:
    from collections.abc import Callable

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
    def dict_open(self) -> str:
        """The opening delimiter for dict literals."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dict_close(self) -> str:
        """The closing delimiter for dict literals."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_dict_entry(self) -> Callable[[str, str], str] | None:
        """Callable that formats a dict entry from a pre-formatted key
        and value string, or ``None`` to use ``dict_separator``.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a :class:`datetime.date` as a string
        literal.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def trailing_comma(self) -> bool:
        """Whether to append a trailing comma after the last entry."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a :class:`datetime.datetime` as a
        string literal.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def comment_prefix(self) -> str:
        """The comment prefix for the language (e.g. ``"#"`` or
        ``"//"``).
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
    dict_open: str = "{"
    dict_close: str = "}"
    format_dict_entry: Callable[[str, str], str] | None = None
    trailing_comma: bool = True
    format_date: Callable[[datetime.date], str] = format_date_iso
    format_datetime: Callable[[datetime.datetime], str] = format_datetime_iso
    comment_prefix: str = "//"


PYTHON = LanguageSpec(
    null_literal="None",
    true_literal="True",
    false_literal="False",
    collection_open="(",
    collection_close=")",
    dict_separator=": ",
    comment_prefix="#",
)


def _format_csharp_dict_entry(key: str, value: str) -> str:
    """Format a C# dictionary indexer entry."""
    return f"[{key}] = {value}"


CSHARP = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="(",
    collection_close=")",
    dict_separator=": ",
    dict_open="new Dictionary<string, object> {",
    dict_close="}",
    format_dict_entry=_format_csharp_dict_entry,
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
    comment_prefix="#",
)

GO = LanguageSpec(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    collection_open="{",
    collection_close="}",
    dict_separator=": ",
    dict_open="map[string]any{",
)


def _format_cpp_dict_entry(key: str, value: str) -> str:
    """Format a C++ dict entry as a brace-enclosed pair."""
    return f"{{{key}, {value}}}"


CPP = LanguageSpec(
    null_literal="nullptr",
    true_literal="true",
    false_literal="false",
    collection_open="{",
    collection_close="}",
    dict_separator=": ",
    format_dict_entry=_format_cpp_dict_entry,
)


def _format_java_dict_entry(key: str, value: str) -> str:
    """Format a Java ``Map.entry(key, value)`` call."""
    return f"Map.entry({key}, {value})"


JAVA = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="new Object[]{",
    collection_close="}",
    dict_separator=": ",
    dict_open="Map.ofEntries(",
    dict_close=")",
    format_dict_entry=_format_java_dict_entry,
    trailing_comma=False,
)

KOTLIN = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="listOf<Any?>(",
    collection_close=")",
    dict_separator=" to ",
    dict_open="mapOf<String, Any?>(",
    dict_close=")",
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
    else:
        result = spec.format_date(value)
    return result


@beartype
def _build_dict_entry(*, key_str: str, val_str: str, spec: Language) -> str:
    """Format a single dict key-value entry using the language spec."""
    if spec.format_dict_entry is not None:
        return spec.format_dict_entry(key_str, val_str)
    return f"{key_str}{spec.dict_separator}{val_str}"


@beartype
def _format_value(*, value: _Value, spec: Language) -> str:
    """Format any JSON value as a native language literal.

    Handles scalars, lists (recursively), and dicts.
    """
    if isinstance(value, dict):
        pairs = [
            _build_dict_entry(
                key_str=_format_value(value=k, spec=spec),
                val_str=_format_value(value=v, spec=spec),
                spec=spec,
            )
            for k, v in value.items()
        ]
        return spec.dict_open + ", ".join(pairs) + spec.dict_close

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
    data: list[Any]
    | dict[str, Any]
    | str
    | datetime.date
    | float
    | bool
    | None,
    language: Language,
    prefix: str,
    wrap: bool,
) -> str:
    r"""Convert data to native language literal text.

    Each element (or key-value pair) is formatted as a native literal
    for the given language with a trailing comma and the specified prefix.

    Args:
        data: A scalar, sequence, or mapping.  Scalars (strings,
            numbers, booleans, ``None``, :class:`datetime.date`,
            :class:`datetime.datetime`) are formatted as a single
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

    # Handle scalars (check ``str`` before Sequence since ``str`` is a
    # Sequence, and datetime before date since datetime subclasses
    # date).
    scalar_types = (
        str,
        int,
        float,
        bool,
        datetime.datetime,
        datetime.date,
    )
    if isinstance(data, scalar_types) or data is None:
        return f"{prefix}{_format_scalar(value=data, spec=spec)}"

    effective_prefix = prefix if not wrap else (prefix or "    ")
    lines: list[str] = []

    if isinstance(data, dict):
        entries = list(data.items())
        last_idx = len(entries) - 1
        for i, (k, v) in enumerate(iterable=entries):
            formatted_key = _format_value(value=k, spec=spec)
            formatted_val = _format_value(value=v, spec=spec)
            entry = _build_dict_entry(
                key_str=formatted_key, val_str=formatted_val, spec=spec
            )
            comma = "" if i == last_idx and not spec.trailing_comma else ","
            lines.append(f"{effective_prefix}{entry}{comma}")
    else:
        items = list(data)
        last_idx = len(items) - 1
        for i, item in enumerate(iterable=items):
            formatted = _format_value(value=item, spec=spec)
            comma = "" if i == last_idx and not spec.trailing_comma else ","
            lines.append(f"{effective_prefix}{formatted}{comma}")

    body = "\n".join(lines)

    if not wrap or not body:
        return body

    if isinstance(data, dict):
        return f"{spec.dict_open}\n{body}\n{spec.dict_close}"

    return f"{spec.collection_open}\n{body}\n{spec.collection_close}"


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
        JSONParseError: If *json_string* is not valid JSON.
    """
    try:
        data = json.loads(s=json_string)
    except json.JSONDecodeError as exc:
        message = (
            f"Invalid JSON: {exc.msg} at line {exc.lineno} column {exc.colno}"
        )
        raise JSONParseError(message) from exc
    return literalize(
        data=data,
        language=language,
        prefix=prefix,
        wrap=wrap,
    )


@dataclasses.dataclass(frozen=True)
class _ElementComments:
    """Comments associated with a single top-level YAML element."""

    before: tuple[str, ...]
    inline: str


@beartype
def _strip_comment_marker(*, text: str) -> str:
    """Strip the leading ``#`` and one optional space from a comment line.

    Only the first ``#`` is removed so that ``## heading`` becomes
    ``# heading`` rather than ``heading``.

    The caller must ensure *text* starts with ``#`` (after stripping
    whitespace).
    """
    after_hash = text.strip()[1:]
    if after_hash.startswith(" "):
        return after_hash[1:]
    return after_hash


@beartype
def _token_comment_lines(*, value: str) -> list[str]:
    r"""Extract comment text lines from a ruamel.yaml token value.

    Token values look like ``"# text\n"`` or
    ``"# line1\n# line2\n"``.
    """
    return [
        _strip_comment_marker(text=line)
        for line in value.split(sep="\n")
        if line.strip().startswith("#")
    ]


@dataclasses.dataclass(frozen=True)
class _ParsedAfterToken:
    """Result of parsing an after-element comment token."""

    inline: str
    before_next: list[str]


@beartype
def _parse_after_token(
    *,
    token: CommentToken,
) -> _ParsedAfterToken:
    """Parse an after-element comment token.

    The *column* of the token determines whether its first line
    is an inline comment (column > 0) or a standalone comment.
    """
    value: str = token.value
    column: int = token.column
    lines = value.split(sep="\n")
    inline = ""
    start = 0

    if column > 0 and lines:
        inline = _strip_comment_marker(text=lines[0])
        start = 1

    before_next = [
        _strip_comment_marker(text=line)
        for line in lines[start:]
        if line.strip().startswith("#")
    ]
    return _ParsedAfterToken(inline=inline, before_next=before_next)


@dataclasses.dataclass(frozen=True)
class _CollectionComments:
    """Comments extracted from a YAML collection string."""

    elements: tuple[_ElementComments, ...]
    trailing: tuple[str, ...]


@beartype
def _extract_yaml_comments(
    *,
    ruamel_data: CommentedSeq | CommentedMap,
    is_sequence: bool,
) -> _CollectionComments:
    """Extract top-level comments from parsed ruamel.yaml data.

    Only works for sequences and mappings — *ruamel.yaml*'s
    round-trip loader preserves comment metadata in
    :class:`CommentedSeq` / :class:`CommentedMap` objects.
    Scalar values do not carry this metadata; use
    :func:`_extract_scalar_comments` for those.
    """
    # https://sourceforge.net/p/ruamel-yaml/tickets/328/
    ca = ruamel_data.ca  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]

    # Header comments (before the first element).
    pending_before: list[str] = []
    if ca.comment and len(ca.comment) > 1 and ca.comment[1]:  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
        for header_token in ca.comment[1]:  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
            header_value: str = header_token.value  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
            pending_before.extend(
                _token_comment_lines(value=header_value),  # pyright: ignore[reportUnknownArgumentType]
            )

    # Sequences store after-element tokens at index 0,
    # mappings at index 2.
    token_idx = 0 if is_sequence else 2

    if isinstance(ruamel_data, CommentedSeq):
        keys: list[object] = list(range(len(ruamel_data)))
    else:
        keys = list(ruamel_data.keys())  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]

    elements: list[_ElementComments] = []
    for key in keys:
        before = list(pending_before)
        inline = ""
        pending_before = []

        if key in ca.items:  # pyright: ignore[reportUnknownMemberType]
            item_token: CommentToken | None = ca.items[key][token_idx]  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
            if item_token is not None:
                parsed = _parse_after_token(token=item_token)  # pyright: ignore[reportUnknownArgumentType]
                inline = parsed.inline
                pending_before = parsed.before_next

        elements.append(
            _ElementComments(
                before=tuple(before),
                inline=inline,
            ),
        )

    return _CollectionComments(
        elements=tuple(elements),
        trailing=tuple(pending_before),
    )


@beartype
def _format_comment(
    *,
    text: str,
    comment_prefix: str,
    line_prefix: str,
) -> str:
    """Format a single comment line."""
    if text:
        return f"{line_prefix}{comment_prefix} {text}"
    return f"{line_prefix}{comment_prefix}"


@dataclasses.dataclass(frozen=True)
class _ScalarComments:
    """Comments extracted from a scalar YAML string."""

    before: list[str]
    inline: str


@beartype
def _extract_scalar_comments(
    *,
    tokens: Iterable[Any],
) -> _ScalarComments:
    """Extract comments from scanned YAML tokens for a scalar value.

    *ruamel.yaml*'s round-trip loader returns plain Python objects
    for scalars with no comment metadata.  The token scanner,
    however, attaches :class:`CommentToken` objects to tokens,
    so we use that instead.

    *tokens* should come from ``YAML().scan()``.
    """
    before_comments: list[str] = []
    inline = ""
    for token in tokens:
        comment: list[Any] | None = token.comment
        if not comment:
            continue
        inline_token: CommentToken | None = comment[0]
        before_tokens: list[CommentToken] = comment[1] or []
        if inline_token is not None:
            value: str = inline_token.value
            inline = _strip_comment_marker(text=value)
        for bt in before_tokens:
            bt_value: str = bt.value
            before_comments.extend(
                _token_comment_lines(value=bt_value),
            )
        break
    return _ScalarComments(before=before_comments, inline=inline)


@beartype
def _literalize_yaml_scalar(
    *,
    tokens: Iterable[Any],
    base: str,
    comment_prefix: str,
    prefix: str,
) -> str:
    """Preserve comments for scalar YAML values.

    Uses :func:`_extract_scalar_comments` to obtain comments
    from pre-scanned *ruamel.yaml* tokens.  Collection values
    use :func:`_extract_yaml_comments` instead.
    """
    scalar_comments = _extract_scalar_comments(
        tokens=tokens,
    )

    if not scalar_comments.before and not scalar_comments.inline:
        return base

    parts = [
        _format_comment(
            text=comment_text,
            comment_prefix=comment_prefix,
            line_prefix=prefix,
        )
        for comment_text in scalar_comments.before
    ]
    if scalar_comments.inline:
        parts.append(
            f"{base}  {comment_prefix} {scalar_comments.inline}",
        )
    else:
        parts.append(base)
    return "\n".join(parts)


@dataclasses.dataclass(frozen=True)
class _YamlCollectionContext:
    """Context for formatting collection YAML with comments."""

    base: str
    element_comments: tuple[_ElementComments, ...]
    trailing: tuple[str, ...]
    comment_prefix: str
    prefix: str
    wrap: bool


@beartype
def _literalize_yaml_collection(
    *,
    ctx: _YamlCollectionContext,
) -> str:
    """Preserve comments for collection YAML values."""
    effective_prefix = ctx.prefix if not ctx.wrap else (ctx.prefix or "    ")
    all_lines = ctx.base.split(sep="\n")

    if ctx.wrap:
        header = all_lines[0]
        footer = all_lines[-1]
        body_lines = all_lines[1:-1]
    else:
        header = None
        footer = None
        body_lines = all_lines

    _empty = _ElementComments(before=(), inline="")
    padded = ctx.element_comments + (_empty,) * (
        len(body_lines) - len(ctx.element_comments)
    )

    result: list[str] = []
    for body_line, element_comment in zip(body_lines, padded, strict=True):
        result.extend(
            _format_comment(
                text=comment_text,
                comment_prefix=ctx.comment_prefix,
                line_prefix=effective_prefix,
            )
            for comment_text in element_comment.before
        )
        if element_comment.inline:
            inline_text = element_comment.inline
            output_line = f"{body_line}  {ctx.comment_prefix} {inline_text}"
        else:
            output_line = body_line
        result.append(output_line)

    result.extend(
        _format_comment(
            text=comment_text,
            comment_prefix=ctx.comment_prefix,
            line_prefix=effective_prefix,
        )
        for comment_text in ctx.trailing
    )

    if ctx.wrap and header is not None and footer is not None:
        return "\n".join([header, *result, footer])
    return "\n".join(result)


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

    YAML comments are preserved in the output using the target
    language's comment syntax.  The comment prefix is read from the
    ``comment_prefix`` attribute of *language* (defaulting to
    ``"#"`` when the attribute is absent).

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
        YAMLParseError: If *yaml_string* is not valid YAML.
    """
    ruamel_yaml = YAML(typ="safe")
    try:
        # https://sourceforge.net/p/ruamel-yaml/tickets/564/
        data = ruamel_yaml.load(stream=yaml_string)  # pyright: ignore[reportUnknownMemberType]
    except YAMLError as exc:
        message = f"Invalid YAML: {exc}"
        raise YAMLParseError(message) from exc
    base = literalize(
        data=data,
        language=language,
        prefix=prefix,
        wrap=wrap,
    )

    cp = language.comment_prefix

    if not isinstance(data, (list, dict)):
        stream = StringIO(initial_value=yaml_string)
        # https://sourceforge.net/p/ruamel-yaml/tickets/328/
        tokens = YAML().scan(stream=stream)  # pyright: ignore[reportUnknownMemberType]
        return _literalize_yaml_scalar(
            tokens=tokens,
            base=base,
            comment_prefix=cp,
            prefix=prefix,
        )

    if not base:
        return base

    is_sequence = isinstance(data, list)
    # https://sourceforge.net/p/ruamel-yaml/tickets/328/
    ruamel_data: CommentedSeq | CommentedMap = YAML().load(  # pyright: ignore[reportUnknownMemberType]
        stream=StringIO(initial_value=yaml_string),
    )
    collection_comments = _extract_yaml_comments(
        ruamel_data=ruamel_data,
        is_sequence=is_sequence,
    )

    has_comments = (
        any(
            element_comment.before or element_comment.inline
            for element_comment in collection_comments.elements
        )
        or collection_comments.trailing
    )
    if not has_comments:
        return base

    ctx = _YamlCollectionContext(
        base=base,
        element_comments=collection_comments.elements,
        trailing=collection_comments.trailing,
        comment_prefix=cp,
        prefix=prefix,
        wrap=wrap,
    )
    return _literalize_yaml_collection(ctx=ctx)
