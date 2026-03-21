"""Common Lisp language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value


@beartype
def _format_cons_entry(key: str, value: str) -> str:
    """Format a Common Lisp association-list entry as a ``cons`` pair."""
    return f"(cons {key} {value})"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Common Lisp special-variable declaration with earmuffs."""
    return f"(defparameter *{name}* {value})"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Common Lisp special-variable assignment with earmuffs."""
    return f"(setf *{name}* {value})"


_string_format: Callable[[str], str] = format_string_backslash


@beartype
class CommonLisp:
    """Common Lisp language specification."""

    class DateFormat(enum.Enum):
        """Date format options for CommonLisp."""

        ISO = enum.member(value=format_date_iso)

    class DatetimeFormat(enum.Enum):
        """Datetime format options for CommonLisp."""

        ISO = enum.member(value=format_datetime_iso)

    class BytesFormat(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

    class SequenceFormat(enum.Enum):
        """Sequence type options for Common Lisp."""

        LIST = "list"

    class SetFormat(enum.Enum):
        """Set type options for Common Lisp."""

        SET = "set"

    @property
    def bytes_formats(self) -> type[BytesFormat]:
        """Enum class whose members list the available bytes formats."""
        return type(self).BytesFormat

    @property
    def set_formats(self) -> type[SetFormat]:
        """Enum class whose members list the available set formats."""
        return type(self).SetFormat

    @property
    def date_formats(self) -> type[DateFormat]:
        """Enum class whose members list the available date formats."""
        return type(self).DateFormat

    @property
    def datetime_formats(self) -> type[DatetimeFormat]:
        """Enum class whose members list the available datetime
        formats.
        """
        return type(self).DatetimeFormat

    @property
    def sequence_formats(self) -> type[SequenceFormat]:
        """Enum class whose members list the available sequence
        formats.
        """
        return type(self).SequenceFormat

    def __init__(
        self,
        *,
        date_format: DateFormat,
        datetime_format: DatetimeFormat,
        bytes_format: BytesFormat,
        sequence_format: SequenceFormat,
    ) -> None:
        """Initialize Common Lisp language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "nil"
        self.true_literal = "t"
        self.false_literal = "nil"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="(list "
        )
        self.sequence_close = ")"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="(list "
        )
        self.dict_close = ")"
        self.format_dict_entry: Callable[[str, str], str] = _format_cons_entry
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_date: Callable[[datetime.date], str] = date_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = "nil"
        self.empty_dict: str | None = "nil"
        self.set_open = "(list "
        self.set_close = ")"
        self.empty_set: str | None = "nil"
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = ";"
        self.comment_suffix = ""
        self.omap_open = "(list "
        self.omap_close = ")"
        self.format_omap_entry: Callable[[str, str], str] = _format_cons_entry
        self.multiline_close_indent = ""
        self.element_separator = " "
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
