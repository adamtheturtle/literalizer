"""C language specification."""

import datetime
import enum
from collections.abc import Callable
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
)

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
def _to_val(value: str) -> str:
    """Convert a value to a C union cast expression."""
    if value.startswith("((_CVal)"):
        return value
    if value.startswith('"') and value.endswith('"'):
        return f"((_CVal){{.s = {value}}})"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"((_CVal){{.i = {value}}})"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f"((_CVal){{.f = {value}}})"
    except ValueError:  # pragma: no cover
        pass
    if float_result is not None:
        return float_result
    return value  # pragma: no cover


@beartype
def _format_c_dict_entry(key: str, value: str) -> str:
    """Format a C dict entry as a ``_CKV`` compound literal."""
    return f"{{{key}, {_to_val(value=value)}}}"


@beartype
def _format_c_list_entry(item: str) -> str:
    """Format a C list entry as a ``_CVal`` compound literal."""
    return _to_val(value=item)


@beartype
def _format_c_set_entry(item: str) -> str:
    """Format a C set entry as a ``_CVal`` compound literal."""
    return _to_val(value=item)


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a C variable declaration."""
    return f"_CVal {name} = {_to_val(value=value)};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a C variable assignment."""
    return f"{name} = {_to_val(value=value)};"


_bytes_format: Callable[[bytes], str] = format_bytes_hex
_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = format_string_backslash


@beartype
class C:
    """C language specification."""

    class SequenceFormat(enum.Enum):
        """Sequence type options for C."""

        ARRAY = "array"

    class SetFormat(enum.Enum):
        """Set type options for C."""

        SET = "set"

    def __init__(
        self,
        *,
        sequence_format: SequenceFormat,
    ) -> None:
        """Initialize C language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "((_CVal){.s = NULL})"
        self.true_literal = "((_CVal){.b = true})"
        self.false_literal = "((_CVal){.b = false})"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="((_CVal){.a = (_CVal[]){"
        )
        self.sequence_close = "}})"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="((_CVal){.m = (_CKV[]){"
        )
        self.dict_close = "}})"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_c_dict_entry
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = _bytes_format
        self.format_date: Callable[[datetime.date], str] = _date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "((_CVal){.a = (_CVal[]){"
        self.set_close = "}})"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = _format_c_list_entry
        self.format_set_entry: Callable[[str], str] = _format_c_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "((_CVal){.m = (_CKV[]){"
        self.omap_close = "}})"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_c_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_to_strings = False
        self.coerce_heterogeneous_lists_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
