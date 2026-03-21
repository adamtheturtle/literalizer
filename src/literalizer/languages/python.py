"""Python language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_bytes_python,
    format_date_iso,
    format_date_python,
    format_datetime_epoch,
    format_datetime_iso,
    format_datetime_python,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value


@beartype
def _format_python_omap_entry(key: str, value: str) -> str:
    """Format one Python ``OrderedDict`` entry as a ``(key, value)`` tuple."""
    return f"({key}, {value})"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Python variable declaration."""
    return f"{name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Python variable assignment."""
    return f"{name} = {value}"


_EXACT_TYPE_HINTS: dict[str, str] = {
    "True": "bool",
    "False": "bool",
    "None": "None",
    "set()": "set[Any]",
}

_PREFIX_TYPE_HINTS: tuple[tuple[str, str], ...] = (
    ("b'", "bytes"),
    ('b"', "bytes"),
    ("datetime.datetime(year=", "datetime.datetime"),
    ("datetime.date(year=", "datetime.date"),
    ("OrderedDict(", "OrderedDict[str, Any]"),
    ("frozenset(", "frozenset[Any]"),
    ("[", "list[Any]"),
    ("(", "tuple[Any, ...]"),
    ('"', "str"),
    ("'", "str"),
)


@beartype
def _infer_python_type_hint(value: str) -> str:
    """Infer a Python type hint string from a formatted value."""
    if value in _EXACT_TYPE_HINTS:
        return _EXACT_TYPE_HINTS[value]
    for prefix, hint in _PREFIX_TYPE_HINTS:
        if value.startswith(prefix):
            return hint
    if value.startswith("{"):
        if _is_dict_literal(value=value):
            return "dict[str, Any]"
        return "set[Any]"
    try:
        int(value)
    except ValueError:
        return "float"
    return "int"


@beartype
def _is_dict_literal(*, value: str) -> bool:
    """Check whether a ``{``-prefixed formatted value is a dict literal.

    In a dict, the first element is a quoted key followed by ``": "``.
    In a set, the first element is a formatted value followed by ``,``
    or ``}``.  To distinguish them we parse the first quoted string
    (respecting backslash escapes) and check whether ``": "`` or
    ``":`` immediately follows the closing quote.
    """
    content = value[1:].lstrip()
    if not content or content[0] != '"':
        return False
    # Find the closing quote of the first key, skipping backslash escapes.
    # In a dict, ``": "`` or ``":\n`` follows the closing quote.
    i = 1
    while content[i] == "\\" or content[i] != '"':
        i += 1 + (content[i] == "\\")
    rest = content[i + 1 :]
    return rest.startswith((": ", ":\n"))


@beartype
def _format_variable_declaration_inline_hint(name: str, value: str) -> str:
    """Format a Python variable declaration with an inline type hint."""
    hint = _infer_python_type_hint(value=value)
    return f"{name}: {hint} = {value}"


@beartype
class Python:
    """Python language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``DateFormat.ISO`` — ISO 8601 string,
              e.g. ``"2024-01-15"``.
            * ``DateFormat.PYTHON`` — ``datetime.date`` constructor call,
              e.g. ``datetime.date(year=2024, month=1, day=15)``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``DatetimeFormat.ISO`` — ISO 8601 string,
              e.g. ``"2024-01-15T12:30:00"``.
            * ``DatetimeFormat.PYTHON`` — ``datetime.datetime`` constructor
              call, e.g. ``datetime.datetime(year=2024, month=1,
              day=15, hour=12, minute=30, second=0)``.
            * ``DatetimeFormat.EPOCH`` — Unix epoch float,
              e.g. ``1705312200.0``.

        bytes_format: How to format :class:`bytes` values.

            * ``BytesFormat.HEX`` — lowercase hex string,
              e.g. ``"48656c6c6f"``.
            * ``BytesFormat.PYTHON`` — Python bytes literal,
              e.g. ``b'Hello'``.

        sequence_format: Which Python sequence type to use.

            * ``SequenceFormat.TUPLE`` — tuple literal,
              e.g. ``(1, 2, 3)``.
            * ``SequenceFormat.LIST`` — list literal,
              e.g. ``[1, 2, 3]``.

        set_format: Which Python set type to use.

            * ``SetFormat.SET`` — mutable set literal,
              e.g. ``{1, 2, 3}``.
            * ``SetFormat.FROZENSET`` — immutable frozenset,
              e.g. ``frozenset({1, 2, 3})``.

        variable_type_hints: Whether to add inline type hints to
            variable declarations.

            * ``VariableTypeHints.NONE`` — bare assignment,
              e.g. ``my_var = {...}``.
            * ``VariableTypeHints.INLINE`` — with type annotation,
              e.g. ``my_var: dict[str, Any] = {...}``.
    """

    class DateFormat(enum.Enum):
        """Date formatting options for Python."""

        ISO = enum.member(value=format_date_iso)
        PYTHON = enum.member(value=format_date_python)

    class DatetimeFormat(enum.Enum):
        """Datetime formatting options for Python."""

        ISO = enum.member(value=format_datetime_iso)
        PYTHON = enum.member(value=format_datetime_python)
        EPOCH = enum.member(value=format_datetime_epoch)

    class BytesFormat(enum.Enum):
        """Bytes formatting options for Python."""

        HEX = enum.member(value=format_bytes_hex)
        PYTHON = enum.member(value=format_bytes_python)

    class SequenceFormat(enum.Enum):
        """Sequence type options for Python."""

        TUPLE = "tuple"
        LIST = "list"

    class SetFormat(enum.Enum):
        """Set type options for Python."""

        SET = "set"
        FROZENSET = "frozenset"

    class VariableTypeHints(enum.Enum):
        """Variable type hint options for Python."""

        NONE = "none"
        INLINE = "inline"

    def __init__(  # noqa: PLR0915  # pylint: disable=too-many-statements
        self,
        *,
        date_format: DateFormat,
        datetime_format: DatetimeFormat,
        bytes_format: BytesFormat,
        sequence_format: SequenceFormat,
        set_format: SetFormat,
        variable_type_hints: VariableTypeHints,
    ) -> None:
        """Initialize Python language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "None"
        self.true_literal = "True"
        self.false_literal = "False"
        self.sequence_open: Callable[[list[Value]], str]
        self.sequence_close: str
        self.single_element_trailing_comma: bool
        if sequence_format == Python.SequenceFormat.LIST:
            self.sequence_open = fixed_sequence_open(open_str="[")
            self.sequence_close = "]"
            self.single_element_trailing_comma = False
        else:
            self.sequence_open = fixed_sequence_open(open_str="(")
            self.sequence_close = ")"
            self.single_element_trailing_comma = True
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="{"
        )
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=": ")
        )
        self.multiline_trailing_comma = True

        self.format_bytes: Callable[[bytes], str] = bytes_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_date: Callable[[datetime.date], str] = date_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        )

        self.format_string: Callable[[str], str] = format_string_backslash
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open: str
        self.set_close: str
        self.empty_set: str | None
        if set_format == Python.SetFormat.FROZENSET:
            self.set_open = "frozenset({"
            self.set_close = "})"
            self.empty_set = "frozenset()"
        else:
            self.set_open = "{"
            self.set_close = "}"
            self.empty_set = "set()"
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "#"
        self.comment_suffix = ""
        self.omap_open = "OrderedDict(["
        self.omap_close = "])"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_python_omap_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_scalars_to_strings = False
        self.coerce_heterogeneous_sibling_lists_to_strings = False
        self.coerce_heterogeneous_dict_values_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration_inline_hint
            if variable_type_hints == Python.VariableTypeHints.INLINE
            else _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
