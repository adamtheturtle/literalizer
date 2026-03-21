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
from literalizer._language import (
    HasFormatEnums,
    SequenceFormatConfig,
    SetFormatConfig,
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
class CommonLisp(metaclass=HasFormatEnums):
    """Common Lisp language specification."""

    class DateFormats(enum.Enum):
        """Date format options for CommonLisp."""

        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for CommonLisp."""

        ISO = enum.member(value=format_datetime_iso)

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value(value=dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Common Lisp."""

        LIST = SequenceFormatConfig(
            open_str="(list ",
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence="nil",
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Common Lisp."""

        SET = SetFormatConfig(
            open_str="(list ",
            close=")",
            empty_set="nil",
        )

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
    ) -> None:
        """Initialize Common Lisp language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "nil"
        self.true_literal = "t"
        self.false_literal = "nil"
        fmt = sequence_format.value
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str=fmt.open_str
        )
        self.sequence_close: str = fmt.close
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="(list "
        )
        self.dict_close = ")"
        self.format_dict_entry: Callable[[str, str], str] = _format_cons_entry
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma: bool = (
            fmt.single_element_trailing_comma
        )
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = fmt.empty_sequence
        self.empty_dict: str | None = "nil"
        self.set_open: str = set_format.value.open_str
        self.set_close: str = set_format.value.close
        self.empty_set: str | None = set_format.value.empty_set
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
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
