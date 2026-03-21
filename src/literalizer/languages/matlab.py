"""MATLAB language specification."""

import datetime
import enum
import re
from collections.abc import Callable
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_matlab,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from literalizer._types import Value

_CONTROL_CHAR_THRESHOLD = 32


@beartype
def _decode_matlab_string_expr(expr: str) -> str:
    r"""Decode a MATLAB string expression back to its raw string value.

    Reverses the output of ``format_string_matlab``.  Handles both the
    simple ``"..."`` form (with ``""`` for embedded double-quotes and
    ``\\\\`` for literal backslashes) and the ``"..." + char(N) + "..."``
    concatenation form used for control characters.
    """
    raw: list[str] = []
    for string_seg, char_code in re.findall(
        pattern=r'"((?:[^"]|"")*)"|char\((\d+)\)',
        string=expr,
    ):
        if char_code:
            raw.append(chr(int(char_code)))
        else:
            raw.append(string_seg.replace('""', '"').replace("\\\\", "\\"))
    return "".join(raw)


@beartype
def _matlab_char_key(s: str) -> str:
    """Build a MATLAB char-array expression for a struct key.

    Single quotes are doubled for valid char-vector literals.  Control
    characters (code points 0-31) cannot appear literally inside a
    MATLAB char vector, so they are emitted as ``char(N)`` calls and
    concatenated with ``[...]``.
    """
    parts: list[str] = []
    for segment in re.split(pattern=r"([\x00-\x1f])", string=s):
        if not segment:
            continue
        if len(segment) == 1 and ord(segment) < _CONTROL_CHAR_THRESHOLD:
            parts.append(f"char({ord(segment)})")
        else:
            escaped = segment.replace("'", "''")
            parts.append(f"'{escaped}'")
    if not parts:
        return "''"
    if len(parts) == 1:
        return parts[0]
    return "[" + ", ".join(parts) + "]"


@beartype
def _format_matlab_dict_entry(key: str, value: str) -> str:
    """Format a MATLAB ``struct`` field as a ``'key', value`` pair.

    MATLAB ``struct`` accepts alternating character-vector keys and values.
    Dictionary keys arrive as double-quoted strings; they are converted to
    single-quoted character vectors as required by ``struct``.  Internal
    single quotes are doubled to produce valid MATLAB char-vector literals.
    Control characters are emitted as ``char(N)`` concatenation expressions
    because MATLAB char vectors cannot contain literal control characters.

    Cell-array values are wrapped in an extra layer of braces so that
    ``struct`` stores them as a single cell-array field rather than
    expanding them into a struct array.
    """
    inner = _decode_matlab_string_expr(expr=key)
    key_expr = _matlab_char_key(s=inner)
    if value.startswith("{") and value.endswith("}"):
        value = f"{{{value}}}"
    return f"{key_expr}, {value}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a MATLAB variable declaration."""
    return f"{name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a MATLAB variable assignment."""
    return f"{name} = {value};"


_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = format_string_matlab


@beartype
class Matlab:
    """MATLAB language specification."""

    class BytesFormat(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormat(enum.Enum):
        """Sequence type options for MATLAB."""

        CELL_ARRAY = "cell_array"

    class SetFormat(enum.Enum):
        """Set type options for MATLAB."""

        SET = "set"

    def __init__(
        self,
        *,
        bytes_format: BytesFormat,
        sequence_format: SequenceFormat,
    ) -> None:
        """Initialize Matlab language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "[]"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="{"
        )
        self.sequence_close = "}"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="struct("
        )
        self.dict_close = ")"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_matlab_dict_entry
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = _date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = "{}"
        self.empty_dict: str | None = "struct()"
        self.set_open = "{"
        self.set_close = "}"
        self.empty_set: str | None = "{}"
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "%"
        self.comment_suffix = ""
        self.omap_open = "struct("
        self.omap_close = ")"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_matlab_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_scalars_to_strings = False
        self.coerce_heterogeneous_sibling_lists_to_strings = False
        self.coerce_heterogeneous_dict_values_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
