"""Dict entry, sequence entry, and variable formatting functions."""

import base64
import enum
import re
from collections.abc import Callable
from dataclasses import dataclass

from beartype import beartype

from literalizer._types import Value


@beartype
def strip_key_quotes(key: str) -> str:
    """Strip the surrounding quotes from a formatted key string.

    Handles double- and single-quoted strings.

    Example::

        strip_key_quotes('"name"')  # => 'name'

    All current input formats produce quoted string keys, so *key*
    is always surrounded by matching quotes.
    """
    # All current input formats produce quoted string keys.
    # If a new format introduces unquoted keys, this will need updating.
    return key[1:-1]


@beartype
def _format_variable(
    name: str, value: str, _data: Value, template: str
) -> str:
    """Format a variable declaration or assignment."""
    return template.format(name=name, value=value)


@beartype
def variable_formatter(*, template: str) -> Callable[[str, str, Value], str]:
    """Return a ``format_variable_assignment`` callable from a template
    string.

    The *template* must contain ``{name}`` and ``{value}`` placeholders.

    Example::

        assign = variable_formatter(template="{name} = {value};")
        assign("x", "42", None)  # => "x = 42;"
    """

    def _format(name: str, value: str, _data: Value) -> str:
        """Delegate to module-level implementation."""
        return _format_variable(
            name=name, value=value, _data=_data, template=template
        )

    return _format


@beartype
def assignment_formatter_from_declaration(
    formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
) -> Callable[[str, str, Value], str]:
    """Return a 3-arg assignment formatter wrapping a declaration
    formatter.

    Modifiers are passed as an empty :class:`frozenset` — assignments
    never carry modifiers.  Use this when a language's declaration and
    assignment syntax are identical and can share a single
    implementation.
    """

    @beartype
    def _format(name: str, value: str, data: Value) -> str:
        """Format a variable assignment by delegating to the declaration
        formatter.
        """
        return formatter(name, value, data, frozenset())

    return _format


@beartype
def declaration_formatter_ignoring_modifiers(
    formatter: Callable[[str, str, Value], str],
) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
    """Adapt a 3-arg callable to the 4-arg declaration formatter shape.

    Use in language cached-properties whose declaration formatter does
    not process modifiers; the modifiers parameter is accepted and
    silently dropped.
    """

    @beartype
    def _format(
        name: str,
        value: str,
        data: Value,
        _modifiers: frozenset[enum.Enum],
    ) -> str:
        """Delegate to the wrapped 3-arg formatter, dropping modifiers."""
        return formatter(name, value, data)

    return _format


@beartype
def variable_declaration_formatter(
    *,
    template: str,
) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
    """Return a ``format_variable_declaration`` callable from a template
    string.

    The *template* must contain ``{name}`` and ``{value}`` placeholders.
    The resulting callable accepts (but silently ignores) the modifier
    set — use this for languages that do not define a modifier enum.
    Languages with concrete modifier syntax should provide their own
    formatter rather than calling this helper.

    Example::

        fmt = variable_declaration_formatter(
            template="const {name} = {value};",
        )
        fmt("x", "42", None, frozenset())  # => "const x = 42;"
    """

    @beartype
    def _format(
        name: str,
        value: str,
        _data: Value,
        _modifiers: frozenset[enum.Enum],
    ) -> str:
        """Delegate to module-level implementation, ignoring modifiers."""
        return _format_variable(
            name=name, value=value, _data=_data, template=template
        )

    return _format


@beartype
def _format_tuple_dict_entry(
    key: str,
    raw_value: Value,
    formatted_value: str,
    format_value: Callable[[Value, str], str],
) -> str:
    """Format a dict entry as a tuple."""
    return f"({key}, {format_value(raw_value, formatted_value)})"


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

    def _format(key: str, raw_value: Value, formatted_value: str) -> str:
        """Delegate to module-level implementation."""
        return _format_tuple_dict_entry(
            key=key,
            raw_value=raw_value,
            formatted_value=formatted_value,
            format_value=format_value,
        )

    return _format


@beartype
def _format_braced_dict_entry(
    key: str,
    raw_value: Value,
    formatted_value: str,
    format_value: Callable[[Value, str], str],
) -> str:
    """Format a dict entry with braces."""
    return f"{{{key}, {format_value(raw_value, formatted_value)}}}"


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

    def _format(key: str, raw_value: Value, formatted_value: str) -> str:
        """Delegate to module-level implementation."""
        return _format_braced_dict_entry(
            key=key,
            raw_value=raw_value,
            formatted_value=formatted_value,
            format_value=format_value,
        )

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


_QUOTED_DICT_KEY = re.compile(pattern=r"""(["'])(.*)\1""", flags=re.DOTALL)


@dataclass(frozen=True)
class DictEntryWithComputedNames:
    """A ``format_dict_entry`` that spells some keys as computed ones.

    A JavaScript object literal reads a ``__proto__`` property key --
    quoted or not -- as setting the prototype rather than defining an
    own property, so the entry is silently lost.  Only the computed
    form ``["__proto__"]`` defines a property, so those names are
    bracketed (issue #4523).
    """

    separator: str
    format_value: Callable[[Value, str], str]
    computed_names: frozenset[str]

    def __call__(
        self, key: str, raw_value: Value, formatted_value: str, /
    ) -> str:
        """Format a dict entry, bracketing a key that needs it."""
        formatted = self.format_value(raw_value, formatted_value)
        match = _QUOTED_DICT_KEY.fullmatch(string=key)
        needs_brackets = (
            match is not None and match.group(2) in self.computed_names
        )
        spelled = f"[{key}]" if needs_brackets else key
        return f"{spelled}{self.separator}{formatted}"


@beartype
def dict_entry_with_computed_names(
    *,
    separator: str,
    format_value: Callable[[Value, str], str],
    computed_names: frozenset[str],
) -> Callable[[str, Value, str], str]:
    """Return a ``format_dict_entry`` that brackets *computed_names*."""
    return DictEntryWithComputedNames(
        separator=separator,
        format_value=format_value,
        computed_names=computed_names,
    )


@dataclass(frozen=True)
class DictEntryWithSeparator:
    """A ``format_dict_entry`` that joins key and value with a separator.

    A class rather than a closure so callers can recognize the shape and
    read ``separator`` back off it.  The JSON-native document fast path
    (:mod:`literalizer._json_native_document`) uses that, together with
    a ``format_value`` of :func:`passthrough_sequence_entry`, to build
    the entry inline instead of calling through this hook per node.
    """

    separator: str
    format_value: Callable[[Value, str], str]

    def __call__(
        self, key: str, raw_value: Value, formatted_value: str, /
    ) -> str:
        """Format a dict entry by joining key and value with separator."""
        formatted = self.format_value(raw_value, formatted_value)
        return f"{key}{self.separator}{formatted}"


@beartype
def dict_entry_with_separator(
    *,
    separator: str,
    format_value: Callable[[Value, str], str],
) -> Callable[[str, Value, str], str]:
    """Return a ``format_dict_entry`` callable that joins key and value
    with *separator*.

    *format_value* is applied to the raw value and formatted string
    before embedding.

    Example: ``dict_entry_with_separator(": ", ...)("k", ..., "v")``
    -> ``"k: v"``.
    """
    return DictEntryWithSeparator(
        separator=separator,
        format_value=format_value,
    )


@beartype
def _format_dict_entry_symbol_style(
    key: str,
    raw_value: Value,
    formatted_value: str,
    format_value: Callable[[Value, str], str],
) -> str:
    """Format a dict entry in symbol style."""
    formatted = format_value(raw_value, formatted_value)
    identifier_key = re.fullmatch(
        pattern=r"""(["'])([A-Za-z_][A-Za-z0-9_]*[!?]?)\1""",
        string=key,
    )
    label = identifier_key.group(2) if identifier_key else key
    return f"{label}: {formatted}"


@beartype
def dict_entry_symbol_style(
    *,
    format_value: Callable[[Value, str], str],
) -> Callable[[str, Value, str], str]:
    r"""Return a ``format_dict_entry`` callable that formats entries in
    Ruby symbol style: ``key: value``.

    Identifier-shaped quoted keys lose their surrounding quotes, producing
    ``name: value``. Other keys keep their quotes, producing Ruby's quoted
    label syntax such as ``"a-b": value``.

    *format_value* is applied to the raw value and formatted string
    before embedding.

    Example: ``dict_entry_symbol_style(...)("\"name\"", ..., "\"Alice\"")``
    -> ``'name: "Alice"'``.
    """

    def _format(key: str, raw_value: Value, formatted_value: str) -> str:
        """Delegate to module-level implementation."""
        return _format_dict_entry_symbol_style(
            key=key,
            raw_value=raw_value,
            formatted_value=formatted_value,
            format_value=format_value,
        )

    return _format


@beartype
def _format_dict_entry_with_template(
    key: str,
    raw_value: Value,
    formatted_value: str,
    template: str,
    format_value: Callable[[Value, str], str],
) -> str:
    """Format a dict entry using the template."""
    formatted = format_value(raw_value, formatted_value)
    return template.format(key=key, value=formatted)


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

    def _format(key: str, raw_value: Value, formatted_value: str) -> str:
        """Delegate to module-level implementation."""
        return _format_dict_entry_with_template(
            key=key,
            raw_value=raw_value,
            formatted_value=formatted_value,
            template=template,
            format_value=format_value,
        )

    return _format
