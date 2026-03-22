"""Functions for formatting scalars as language-specific literals."""

import datetime
import functools
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
def format_bytes_hex(value: bytes) -> str:
    """Format bytes as a hex string literal.

    Example: ``b"Hello"`` → ``"48656c6c6f"``.
    """
    return f'"{value.hex()}"'


@beartype
def passthrough_sequence_entry(item: str) -> str:
    """Return *item* unchanged.

    Use this as ``format_sequence_entry`` for languages where sequence entries
    need no extra formatting.
    """
    return item


@beartype
def passthrough_set_entry(item: str) -> str:
    """Return *item* unchanged.

    Use this as ``format_set_entry`` for languages where set entries
    need no extra formatting.
    """
    return item


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
