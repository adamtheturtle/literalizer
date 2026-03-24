"""Functions for formatting scalars as language-specific literals."""

import datetime
import functools
import re
from collections.abc import Callable
from dataclasses import dataclass

from beartype import beartype

from literalizer._types import Value


@dataclass(frozen=True)
class ListType:
    """Represents a homogeneous list element type for type inference.

    For nested lists, ``inner`` is another ``ListType``.
    For leaf lists, ``inner`` is a Python ``type``.
    """

    inner: "type | ListType"


class MixedNumeric:
    """Sentinel class representing mixed int/float element types.

    Used as a key in scalar type mapping dicts so each language can
    decide how to handle collections containing both int and float
    values.
    """


@beartype
def _infer_element_type(
    items: list[Value],
) -> type | ListType | None:
    """Infer the common element type from a list of values.

    Returns ``None`` when the list is empty or contains mixed types
    that cannot be unified.  Returns ``MixedNumeric`` when the list
    contains a mix of ``int`` and ``float`` values.
    """
    if not items:
        return None
    element_types: set[type | ListType] = set()
    for item in items:
        if isinstance(item, list):
            inner = _infer_element_type(items=item)
            if inner is None:
                return None
            element_types.add(ListType(inner=inner))
        else:
            element_types.add(type(item))
    if len(element_types) == 1:
        return next(iter(element_types))
    if element_types == {int, float}:
        return MixedNumeric
    return None


@beartype
def variable_formatter(*, template: str) -> Callable[[str, str, Value], str]:
    """Return a ``format_variable_declaration`` or
    ``format_variable_assignment`` callable from a template string.

    The *template* must contain ``{name}`` and ``{value}`` placeholders.

    Example::

        assign = variable_formatter(template="{name} = {value};")
        assign("x", "42", None)  # => "x = 42;"
    """

    @beartype
    def _format(name: str, value: str, _data: Value) -> str:
        """Format a variable declaration or assignment."""
        return template.format(name=name, value=value)

    return _format


@beartype
def tuple_dict_entry(
    *,
    format_value: Callable[[Value, str], str],
) -> Callable[[str, Value, str], str]:
    """Return a ``format_dict_entry`` callable that formats entries as
    tuples ``(key, value)``.

    *format_value* is applied to the raw value and formatted string
    before embedding.

    Example: ``tuple_dict_entry(...)("k", ..., "v")``
    → ``"(k, v)"``.
    """

    @beartype
    def _format(key: str, val: Value, value: str) -> str:
        """Format a dict entry as a tuple."""
        return f"({key}, {format_value(val, value)})"

    return _format


@beartype
def braced_dict_entry(
    *,
    format_value: Callable[[Value, str], str],
) -> Callable[[str, Value, str], str]:
    r"""Return a ``format_dict_entry`` callable that formats entries as
    ``{key, value}``.

    *format_value* is applied to the raw value and formatted string
    before embedding.

    Example: ``braced_dict_entry(...)("k", ..., "v")``
    → ``"{k, v}"``.
    """

    @beartype
    def _format(key: str, val: Value, value: str) -> str:
        """Format a dict entry with braces."""
        return f"{{{key}, {format_value(val, value)}}}"

    return _format


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
def date_ymd_formatter(
    *,
    template: str,
) -> Callable[[datetime.date], str]:
    """Return a date formatter that substitutes year, month, and day
    into *template*.

    The *template* must contain ``{year}``, ``{month}``, and ``{day}``
    placeholders.

    Example::

        fmt = date_ymd_formatter(
            template="LocalDate.of({year}, {month}, {day})",
        )
        fmt(datetime.date(2024, 1, 15))  # => "LocalDate.of(2024, 1, 15)"
    """

    @beartype
    def _format(value: datetime.date) -> str:
        """Format a date using the template."""
        return template.format(
            year=value.year,
            month=value.month,
            day=value.day,
        )

    return _format


@beartype
def datetime_ymdhms_formatter(
    *,
    template: str,
) -> Callable[[datetime.datetime], str]:
    """Return a datetime formatter that substitutes year, month, day,
    hour, minute, and second into *template*.

    The *template* must contain ``{year}``, ``{month}``, ``{day}``,
    ``{hour}``, ``{minute}``, and ``{second}`` placeholders.

    Example::

        fmt = datetime_ymdhms_formatter(
            template="new DateTime({year}, {month}, {day}, "
                     "{hour}, {minute}, {second})",
        )
    """

    @beartype
    def _format(value: datetime.datetime) -> str:
        """Format a datetime using the template."""
        return template.format(
            year=value.year,
            month=value.month,
            day=value.day,
            hour=value.hour,
            minute=value.minute,
            second=value.second,
        )

    return _format


@beartype
def date_iso_formatter(
    *,
    template: str,
) -> Callable[[datetime.date], str]:
    """Return a date formatter that substitutes the ISO 8601 string
    into *template*.

    The *template* must contain an ``{iso}`` placeholder.

    Example::

        fmt = date_iso_formatter(
            template='DateTime.parse("{iso}")',
        )
        fmt(datetime.date(2024, 1, 15))  # => 'DateTime.parse("2024-01-15")'
    """

    @beartype
    def _format(value: datetime.date) -> str:
        """Format a date using the ISO template."""
        return template.format(iso=value.isoformat())

    return _format


@beartype
def datetime_iso_formatter(
    *,
    template: str,
) -> Callable[[datetime.datetime], str]:
    """Return a datetime formatter that substitutes the ISO 8601 string
    into *template*.

    The *template* must contain an ``{iso}`` placeholder.

    Example::

        fmt = datetime_iso_formatter(
            template='new Date("{iso}")',
        )
    """

    @beartype
    def _format(value: datetime.datetime) -> str:
        """Format a datetime using the ISO template."""
        return template.format(iso=value.isoformat())

    return _format


@dataclass(frozen=True)
class TypeOpeners:
    """Resolved type-to-opener functions for sequences, dicts, and
    sets.
    """

    seq: Callable[[type | ListType], str | None]
    dict: Callable[[type | ListType], str | None]
    set: Callable[[type | ListType], str | None]


class TypedOpenerConfig:
    """Configuration for typed collection openers in a language.

    Holds scalar type mappings and template strings needed to build
    type-to-opener functions.
    """

    @beartype
    def __init__(
        self,
        *,
        str_type: str | None,
        bool_type: str | None,
        int_type: str | None,
        float_type: str | None,
        bytes_type: str | None,
        mixed_numeric_type: str | None,
        date_type: str | None,
        datetime_type: str | None,
        list_template: str,
        sequence_opener_template: str,
        dict_opener_template: str,
        set_opener_template: str,
    ) -> None:
        """Initialize with scalar type mappings and template strings."""
        self._str_type = str_type
        self._bool_type = bool_type
        self._int_type = int_type
        self._float_type = float_type
        self._bytes_type = bytes_type
        self._mixed_numeric_type = mixed_numeric_type
        self._date_type = date_type
        self._datetime_type = datetime_type
        self._list_template = list_template
        self._sequence_opener_template = sequence_opener_template
        self._dict_opener_template = dict_opener_template
        self._set_opener_template = set_opener_template

    @beartype
    def type_name(self, py_type: type) -> str | None:
        """Look up the language type name for a Python type."""
        return self._scalar_types().get(py_type)

    def _scalar_types(self) -> dict[type, str]:
        """Build a dict mapping Python types to language type names."""
        return {
            py_type: name
            for py_type, name in (
                (str, self._str_type),
                (bool, self._bool_type),
                (int, self._int_type),
                (float, self._float_type),
                (bytes, self._bytes_type),
                (MixedNumeric, self._mixed_numeric_type),
                (datetime.date, self._date_type),
                (datetime.datetime, self._datetime_type),
            )
            if name is not None
        }

    @beartype
    def element_to_type(
        self,
        *,
        list_template: str | None = None,
        date_type: str | None = None,
        datetime_type: str | None = None,
    ) -> Callable[[type | ListType], str | None]:
        """Build an element-to-type resolver.

        If *list_template* is given it overrides the default.
        If *date_type* or *datetime_type* is given they override the
        base values.
        """
        return make_element_to_type(
            str_type=self._str_type,
            bool_type=self._bool_type,
            int_type=self._int_type,
            float_type=self._float_type,
            bytes_type=self._bytes_type,
            mixed_numeric_type=self._mixed_numeric_type,
            date_type=date_type or self._date_type,
            datetime_type=datetime_type or self._datetime_type,
            list_template=list_template or self._list_template,
        )

    @beartype
    def build(
        self,
        *,
        date_type: str | None = None,
        datetime_type: str | None = None,
        set_opener_template: str | None = None,
    ) -> TypeOpeners:
        """Build openers from the base scalar type mapping plus
        overrides.

        If *date_type* or *datetime_type* is given, they override the
        base values.  If *set_opener_template* is given it overrides
        the template used for ``set`` openers, allowing a single
        ``TypedOpenerConfig`` to serve multiple set formats.
        """
        element_type_resolver = self.element_to_type(
            date_type=date_type,
            datetime_type=datetime_type,
        )
        return TypeOpeners(
            seq=make_type_to_opener(
                element_to_type=element_type_resolver,
                opener_template=self._sequence_opener_template,
            ),
            dict=make_type_to_opener(
                element_to_type=element_type_resolver,
                opener_template=self._dict_opener_template,
            ),
            set=make_type_to_opener(
                element_to_type=element_type_resolver,
                opener_template=(
                    set_opener_template or self._set_opener_template
                ),
            ),
        )


@beartype
def format_string_concat_control(
    *,
    quote_char: str,
    quote_escape: str,
    control_char_template: str,
    concat_operator: str,
    escape_backslash: bool,
) -> Callable[[str], str]:
    """Return a string formatter that splits on control characters and
    concatenates parts with a language-specific operator.

    Text segments are wrapped in *quote_char* with embedded quotes
    escaped to *quote_escape*.  Control characters (code points 0-31)
    are emitted using *control_char_template* (which receives the code
    point as a positional format argument) and joined with
    *concat_operator*.

    When *escape_backslash* is ``True``, literal backslashes in text
    segments are doubled before quote escaping.

    Example::

        format_string = format_string_concat_control(
            quote_char="'",
            quote_escape="''",
            control_char_template="achar({})",
            concat_operator=" // ",
        )
        format_string("hello")  # => "'hello'"
    """
    empty = f"{quote_char}{quote_char}"

    @beartype
    def _format(value: str) -> str:
        """Format a string with control character concatenation."""
        control_char_threshold = 32
        parts: list[str] = []
        for segment in re.split(pattern=r"([\x00-\x1f])", string=value):
            if not segment:
                continue
            if len(segment) == 1 and ord(segment) < control_char_threshold:
                parts.append(control_char_template.format(ord(segment)))
            else:
                escaped = segment
                if escape_backslash:
                    escaped = escaped.replace("\\", "\\\\")
                escaped = escaped.replace(quote_char, quote_escape)
                parts.append(f"{quote_char}{escaped}{quote_char}")
        if not parts:
            return empty
        if len(parts) == 1:
            return parts[0]
        return concat_operator.join(parts)

    return _format


@beartype
def format_bytes_hex(value: bytes) -> str:
    """Format bytes as a hex string literal.

    Example: ``b"Hello"`` → ``"48656c6c6f"``.
    """
    return f'"{value.hex()}"'


@beartype
def passthrough_sequence_entry(_value: Value, item: str) -> str:
    """Return *item* unchanged.

    Use this as ``format_sequence_entry`` for languages where sequence entries
    need no extra formatting.
    """
    return item


@beartype
def passthrough_set_entry(_value: Value, item: str) -> str:
    """Return *item* unchanged.

    Use this as ``format_set_entry`` for languages where set entries
    need no extra formatting.
    """
    return item


@beartype
def dict_entry_with_separator(
    separator: str,
    *,
    format_value: Callable[[Value, str], str],
) -> Callable[[str, Value, str], str]:
    """Return a ``format_dict_entry`` callable that joins key and value
    with *separator*.

    *format_value* is applied to the raw value and formatted string
    before embedding.

    Example: ``dict_entry_with_separator(": ", ...)("k", ..., "v")``
    → ``"k: v"``.
    """

    @beartype
    def _format(key: str, val: Value, value: str) -> str:
        """Format a dict entry by joining key and value with separator."""
        return f"{key}{separator}{format_value(val, value)}"

    return _format


@beartype
def escape_control_chars(value: str, *, fmt: str) -> str:
    r"""Replace C0 control characters (U+0000-U+001F) with escape sequences.

    Call **after** replacing named escapes (``\t``, ``\n``, ``\r``) so that
    only truly unhandled control characters are affected.

    The format pattern passed in ``fmt`` receives the code point as a
    positional integer, e.g. ``"\\x{:02x}"`` → ``\\x01``.
    """
    return re.sub(
        pattern=r"[\x00-\x1f]",
        repl=lambda m: fmt.format(ord(m.group())),
        string=value,
    )


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
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    return f'"{escaped}"'


@beartype
def format_string_backslash_control(
    value: str,
    *,
    control_char_fmt: str,
) -> str:
    r"""Format a string using backslash escaping plus control-char escaping.

    Combines :func:`format_string_backslash`-style replacements with
    :func:`escape_control_chars` in one step.  The *control_char_fmt*
    is passed directly to :func:`escape_control_chars`.

    Example with ``control_char_fmt="\\x{:02x}"``::

        format_string_backslash_control("\x01hi", control_char_fmt="\\x{:02x}")
        # => '"\\x01hi"'
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    escaped = escape_control_chars(value=escaped, fmt=control_char_fmt)
    return f'"{escaped}"'


@beartype
def format_string_backslash_single(value: str) -> str:
    r"""Format a string using backslash escaping with single quotes.

    Escapes backslashes, single quotes, and newlines with a backslash
    prefix, then wraps the result in single quotes.

    Example: ``hello 'world'`` → ``'hello \'world\''``.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    return f"'{escaped}'"


@beartype
def format_string_backslash_single_minimal(value: str) -> str:
    r"""Format a string with single quotes, escaping only ``\\`` and ``\'``.

    For languages like Ruby, Perl, and PHP where single-quoted strings
    only recognize ``\\`` and ``\'`` as escape sequences.  Actual
    newline, carriage-return, and tab characters are embedded literally.

    Example: ``hello 'world'`` → ``'hello \'world\''``.
    """
    escaped = value.replace("\\", "\\\\").replace("'", "\\'")
    return f"'{escaped}'"


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
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("$", "\\$")
    )
    return f'"{escaped}"'


@beartype
def format_string_backslash_dollar_single(value: str) -> str:
    r"""Format a string using backslash escaping with single quotes,
    including ``$``.

    Escapes backslashes, single quotes, newlines, tabs, and dollar signs
    with a backslash prefix, then wraps the result in single quotes.

    Example: ``price $10`` → ``'price \$10'``.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("$", "\\$")
    )
    return f"'{escaped}'"


@beartype
def fixed_set_open(*, open_str: str) -> Callable[[list[Value]], str]:
    """Return a ``set_open`` callable that always returns *open_str*.

    Use this as ``set_open`` when the opening delimiter for sets
    is a fixed string that does not depend on the set contents.

    Example: ``fixed_set_open(open_str="{")([1, 2, 3])`` → ``"{"``.
    """

    @beartype
    def _open(_items: list[Value]) -> str:
        """Return the fixed opening delimiter."""
        return open_str

    return _open


@beartype
def _typed_set_open(
    items: list[Value],
    *,
    type_to_opener: Callable[[type | ListType], str | None],
    fallback: str,
) -> str:
    """Infer the common element type and return the language-specific
    opener for sets.

    Uses direct ``type()`` checks on the Python runtime objects to
    determine the element type, then passes it to *type_to_opener*
    which returns the language-specific opening delimiter.  When
    inference is not possible or *type_to_opener* returns ``None``,
    *fallback* is returned instead.
    """
    element_type = _infer_element_type(items=items)
    if element_type is None:
        return fallback
    return type_to_opener(element_type) or fallback


@beartype
def typed_set_open(
    *,
    type_to_opener: Callable[[type | ListType], str | None],
    fallback: str,
) -> Callable[[list[Value]], str]:
    """Return a ``set_open`` callable that infers the common
    element type and delegates to *type_to_opener*.

    When inference is not possible or *type_to_opener* returns
    ``None``, *fallback* is used instead.

    Example::

        def my_opener(element_type: type | ListType) -> str | None:
            if element_type is str:
                return "Set[String]("
            return None

        set_open = typed_set_open(
            type_to_opener=my_opener,
            fallback="Set[String](",
        )
    """
    return functools.partial(
        _typed_set_open,
        type_to_opener=type_to_opener,
        fallback=fallback,
    )


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
def make_element_to_type(
    *,
    str_type: str | None = None,
    bool_type: str | None = None,
    int_type: str | None = None,
    float_type: str | None = None,
    bytes_type: str | None = None,
    mixed_numeric_type: str | None = None,
    date_type: str | None = None,
    datetime_type: str | None = None,
    list_template: str,
) -> Callable[[type | ListType], str | None]:
    """Create a recursive type resolver from scalar types and a list
    template.

    The *list_template* must contain ``{inner}`` which will be replaced
    with the recursively-resolved inner type name.

    Example::

        go_element_to_type = make_element_to_type(
            str_type="string",
            int_type="int",
            list_template="[]{inner}",
        )
    """
    scalar_types: dict[type, str] = {
        py_type: name
        for py_type, name in (
            (str, str_type),
            (bool, bool_type),
            (int, int_type),
            (float, float_type),
            (bytes, bytes_type),
            (MixedNumeric, mixed_numeric_type),
            (datetime.date, date_type),
            (datetime.datetime, datetime_type),
        )
        if name is not None
    }

    @beartype
    def element_to_type(element_type: type | ListType) -> str | None:
        """Resolve a Python element type to a language type name."""
        if isinstance(element_type, ListType):
            inner = element_to_type(element_type=element_type.inner)
            if inner is None:
                return None
            return list_template.format(inner=inner)
        return scalar_types.get(element_type)

    return element_to_type


@beartype
def make_type_to_opener(
    *,
    element_to_type: Callable[[type | ListType], str | None],
    opener_template: str,
) -> Callable[[type | ListType], str | None]:
    """Create a typed collection opener from an element-to-type resolver.

    The *opener_template* must contain ``{type_name}`` which will be
    replaced with the resolved type name.

    Example::

        go_type_to_opener = make_type_to_opener(
            element_to_type=go_element_to_type,
            opener_template="[]{type_name}{{",
        )
    """

    @beartype
    def type_to_opener(element_type: type | ListType) -> str | None:
        """Resolve a Python element type to a collection opener."""
        type_name = element_to_type(element_type)
        if type_name is None:
            return None
        return opener_template.format(type_name=type_name)

    return type_to_opener


@beartype
def _typed_sequence_open(
    items: list[Value],
    *,
    type_to_opener: Callable[[type | ListType], str | None],
    fallback: str,
) -> str:
    """Infer the common element type and return the language-specific
    opener.

    Uses direct ``type()`` checks on the Python runtime objects
    to determine the element type, then passes it to
    *type_to_opener* which returns the language-specific opening
    delimiter.  When inference is not possible or *type_to_opener*
    returns ``None``, *fallback* is returned instead.
    """
    element_type = _infer_element_type(items=items)
    if element_type is None:
        return fallback
    return type_to_opener(element_type) or fallback


@beartype
def typed_sequence_open(
    *,
    type_to_opener: Callable[[type | ListType], str | None],
    fallback: str,
) -> Callable[[list[Value]], str]:
    """Return a ``sequence_open`` callable that infers the common
    element type and delegates to *type_to_opener*.

    When inference is not possible or *type_to_opener* returns
    ``None``, *fallback* is used instead.

    Example::

        def my_opener(element_type: type | ListType) -> str | None:
            if element_type is str:
                return "[]string{"
            return None

        sequence_open = typed_sequence_open(
            type_to_opener=my_opener,
            fallback="[]any{",
        )
    """
    return functools.partial(
        _typed_sequence_open,
        type_to_opener=type_to_opener,
        fallback=fallback,
    )


@beartype
def _typed_dict_open(
    items: dict[str, Value],
    *,
    type_to_opener: Callable[[type | ListType], str | None],
    fallback: str,
) -> str:
    """Infer a common value type and return the language-specific
    opener.

    Treats the dict values as a list and infers a common element
    type, then passes it to *type_to_opener* which returns the
    language-specific opening delimiter.  When inference is not
    possible or *type_to_opener* returns ``None``, *fallback* is
    returned instead.
    """
    values = list(items.values())
    element_type = _infer_element_type(items=values)
    if element_type is None:
        return fallback
    return type_to_opener(element_type) or fallback


@beartype
def typed_dict_open(
    *,
    type_to_opener: Callable[[type | ListType], str | None],
    fallback: str,
) -> Callable[[dict[str, Value]], str]:
    """Return a ``dict_open`` callable that infers a common value type
    and delegates to *type_to_opener*.

    When inference is not possible or *type_to_opener* returns
    ``None``, *fallback* is used instead.

    Example::

        def my_opener(element_type: type | ListType) -> str | None:
            if element_type is str:
                return "map[string]string{"
            return None

        dict_open = typed_dict_open(
            type_to_opener=my_opener,
            fallback="map[string]any{",
        )
    """
    return functools.partial(
        _typed_dict_open,
        type_to_opener=type_to_opener,
        fallback=fallback,
    )


@beartype
def dict_entry_with_template(
    *,
    template: str,
    format_value: Callable[[Value, str], str],
) -> Callable[[str, Value, str], str]:
    """Return a ``format_dict_entry`` callable from a template string.

    The *template* must contain ``{key}`` and ``{value}`` placeholders.
    *format_value* is applied to the raw value and formatted string
    before embedding.

    Example: ``dict_entry_with_template(template=..., ...)``
    returns a callable producing ``"Map.entry(k, v)"``.
    """

    @beartype
    def _format(key: str, val: Value, value: str) -> str:
        """Format a dict entry using the template."""
        return template.format(key=key, value=format_value(val, value))

    return _format


@beartype
def format_integer_hex(value: int) -> str:
    """Format an integer as a hexadecimal literal.

    Negative values are formatted with a leading ``-``.

    Example: ``255`` → ``"0xff"``, ``-10`` → ``"-0xa"``.
    """
    if value < 0:
        return f"-0x{abs(value):x}"
    return f"0x{value:x}"


@beartype
def format_integer_octal(value: int) -> str:
    """Format an integer as an octal literal with ``0o`` prefix.

    Negative values are formatted with a leading ``-``.

    Example: ``255`` → ``"0o377"``, ``-10`` → ``"-0o12"``.
    """
    if value < 0:
        return f"-0o{abs(value):o}"
    return f"0o{value:o}"


@beartype
def format_integer_octal_c_style(value: int) -> str:
    """Format an integer as a C-style octal literal with ``0`` prefix.

    Negative values are formatted with a leading ``-``.

    Example: ``255`` → ``"0377"``, ``-10`` → ``"-012"``.
    """
    if value < 0:
        return f"-0{abs(value):o}"
    return f"0{value:o}"


@beartype
def format_integer_binary(value: int) -> str:
    """Format an integer as a binary literal with ``0b`` prefix.

    Negative values are formatted with a leading ``-``.

    Example: ``255`` → ``"0b11111111"``, ``-10`` → ``"-0b1010"``.
    """
    if value < 0:
        return f"-0b{abs(value):b}"
    return f"0b{value:b}"


@beartype
def format_integer_hex_erlang(value: int) -> str:
    """Format an integer as an Erlang hexadecimal literal.

    Negative values are formatted with a leading ``-``.

    Example: ``255`` → ``"16#FF"``, ``-10`` → ``"-16#A"``.
    """
    if value < 0:
        return f"-16#{abs(value):X}"
    return f"16#{value:X}"


@beartype
def format_integer_binary_erlang(value: int) -> str:
    """Format an integer as an Erlang binary literal.

    Negative values are formatted with a leading ``-``.

    Example: ``255`` → ``"2#11111111"``, ``-10`` → ``"-2#1010"``.
    """
    if value < 0:
        return f"-2#{abs(value):b}"
    return f"2#{value:b}"


@beartype
def _format_integer_grouped(value: int, *, separator: str) -> str:
    """Format an integer with digit-group separators every 3 digits.

    Example: ``_format_integer_grouped(1000000, separator="_")``
    → ``"1_000_000"``.
    """
    s = str(object=abs(value))
    group_size = 3
    groups: list[str] = []
    while len(s) > group_size:
        groups.append(s[-group_size:])
        s = s[:-group_size]
    groups.append(s)
    formatted = separator.join(reversed(groups))
    if value < 0:
        return f"-{formatted}"
    return formatted


format_integer_underscore: Callable[[int], str] = functools.partial(
    _format_integer_grouped,
    separator="_",
)
"""Format an integer with underscore separators every 3 digits.

Example: ``1000000`` → ``"1_000_000"``.
"""

format_integer_tick: Callable[[int], str] = functools.partial(
    _format_integer_grouped,
    separator="'",
)
"""Format an integer with tick (apostrophe) separators every 3 digits.

Used by C++ digit separators.

Example: ``1000000`` → ``"1'000'000"``.
"""
