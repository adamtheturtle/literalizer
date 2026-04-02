"""Dict entry, sequence entry, and variable formatting functions."""

import base64
from collections.abc import Callable

from beartype import beartype

from literalizer._types import Value


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
    -> ``"(k, v)"``.
    """

    @beartype
    def _format(key: str, val: Value, value: str) -> str:
        """Format a dict entry as a tuple."""
        return f"({key}, {format_value(val, value)})"

    return _format


@beartype
def hash_tuple_dict_entry(
    *,
    format_value: Callable[[Value, str], str],
) -> Callable[[str, Value, str], str]:
    r"""Return a ``format_dict_entry`` callable that formats entries as
    ``#(key, value)``.

    *format_value* is applied to the raw value and formatted string
    before embedding.

    Example: ``hash_tuple_dict_entry(...)("k", ..., "v")``
    -> ``"#(k, v)"``.
    """

    @beartype
    def _format(key: str, val: Value, value: str) -> str:
        """Format a dict entry as a hash tuple."""
        return f"#({key}, {format_value(val, value)})"

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
    -> ``"{k, v}"``.
    """

    @beartype
    def _format(key: str, val: Value, value: str) -> str:
        """Format a dict entry with braces."""
        return f"{{{key}, {format_value(val, value)}}}"

    return _format


@beartype
def format_bytes_hex(value: bytes) -> str:
    """Format bytes as a hex string literal.

    Example: ``b"Hello"`` -> ``"48656c6c6f"``.
    """
    return f'"{value.hex()}"'


@beartype
def format_bytes_base64(value: bytes) -> str:
    """Format bytes as a base64 string literal.

    Example: ``b"Hello"`` -> ``"SGVsbG8="``.
    """
    encoded = base64.b64encode(s=value)
    return f'"{encoded.decode(encoding="ascii")}"'


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
    -> ``"k: v"``.
    """

    @beartype
    def _format(key: str, val: Value, value: str) -> str:
        """Format a dict entry by joining key and value with separator."""
        return f"{key}{separator}{format_value(val, value)}"

    return _format


@beartype
def dict_entry_symbol_style(
    *,
    format_value: Callable[[Value, str], str],
) -> Callable[[str, Value, str], str]:
    r"""Return a ``format_dict_entry`` callable that formats entries in
    Ruby symbol style: ``key: value``.

    The key is expected to be a quoted string (e.g. ``"name"``); the
    surrounding quotes are stripped so the result is ``name: value``.

    *format_value* is applied to the raw value and formatted string
    before embedding.

    Example: ``dict_entry_symbol_style(...)("\"name\"", ..., "\"Alice\"")``
    -> ``'name: "Alice"'``.
    """

    @beartype
    def _format(key: str, val: Value, value: str) -> str:
        """Format a dict entry in symbol style."""
        # *key* arrives already formatted as a quoted string literal
        # (e.g. '"name"' or "'name'").  Strip the surrounding quote
        # characters so the symbol-style output is ``name: value``
        # rather than ``"name": value``.
        stripped_key = key[1:-1]
        return f"{stripped_key}: {format_value(val, value)}"

    return _format


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
