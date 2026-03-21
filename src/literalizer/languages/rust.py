"""Rust language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_rust,
    format_datetime_rust,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer._language import HasFormatEnums

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value


@beartype
def _format_rust_dict_entry(key: str, value: str) -> str:
    """Format a Rust HashMap entry as a tuple ``(key, value)``."""
    return f"({key}, {value})"


@beartype
def _format_rust_omap_entry(key: str, value: str) -> str:
    """Format a Rust ordered-map entry as a tuple ``(key, value)``."""
    return f"({key}, {value})"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Rust variable declaration."""
    return f"let {name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Rust variable assignment."""
    return f"{name} = {value};"


@beartype
class Rust(metaclass=HasFormatEnums):
    """Rust language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.RUST`` —
              ``NaiveDate::from_ymd_opt(...)`` call,
              e.g. ``NaiveDate::from_ymd_opt(2024, 1, 15).unwrap()``.
              Requires the ``chrono`` crate.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.RUST`` —
              ``NaiveDateTime::new(...)`` call, e.g.
              ``NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15)
              .unwrap(), NaiveTime::from_hms_opt(12, 30, 0).unwrap())``.
              Requires the ``chrono`` crate.

        sequence_format: Which Rust sequence type to use.

            * ``sequence_formats.VEC`` — ``vec![]`` macro,
              e.g. ``vec![1, 2, 3]``.  Because ``Vec`` is
              homogeneous, mixed-type sequences have all elements
              coerced to strings.
            * ``sequence_formats.ARRAY`` — fixed-size array literal,
              e.g. ``[1, 2, 3]``.  Because Rust arrays are
              homogeneous, mixed-type sequences have all elements
              coerced to strings.
            * ``sequence_formats.TUPLE`` — tuple literal,
              e.g. ``(1, 2, 3)``.
    """

    class DateFormats(enum.Enum):
        """Date format options for Rust."""

        RUST = enum.member(value=format_date_rust)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Rust."""

        RUST = enum.member(value=format_datetime_rust)

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
        """Sequence type options for Rust."""

        VEC = "vec"
        ARRAY = "array"
        TUPLE = "tuple"

    class SetFormats(enum.Enum):
        """Set type options for Rust."""

        HASH_SET = "hash_set"

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats

    def __init__(
        self,
        *,
        date_format: DateFormats,
        datetime_format: DatetimeFormats,
        bytes_format: BytesFormats,
        sequence_format: SequenceFormats,
    ) -> None:
        """Initialize Rust language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "None::<()>"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str]
        self.sequence_close: str
        if sequence_format == Rust.sequence_formats.TUPLE:
            self.sequence_open = fixed_sequence_open(open_str="(")
            self.sequence_close = ")"
        elif sequence_format == Rust.sequence_formats.ARRAY:
            self.sequence_open = fixed_sequence_open(open_str="[")
            self.sequence_close = "]"
        else:
            self.sequence_open = fixed_sequence_open(open_str="vec![")
            self.sequence_close = "]"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="HashMap::from(["
        )
        self.dict_close = "])"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_rust_dict_entry
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )

        self.format_string: Callable[[str], str] = format_string_backslash
        self.empty_sequence: str | None = (
            "Vec::<String>::new()"
            if sequence_format == Rust.SequenceFormat.VEC
            else None
        )
        self.empty_dict: str | None = None
        self.set_open = "HashSet::from(["
        self.set_close = "])"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "HashMap::from(["
        self.omap_close = "])"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_rust_omap_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_scalars_to_strings: bool = (
            sequence_format != Rust.sequence_formats.TUPLE
        )
        self.coerce_heterogeneous_sibling_lists_to_strings: bool = (
            sequence_format != Rust.SequenceFormat.TUPLE
        )
        self.coerce_heterogeneous_dict_values_to_strings: bool = (
            sequence_format != Rust.SequenceFormat.TUPLE
        )
        self.coerce_heterogeneous_list_values_to_strings: bool = (
            sequence_format != Rust.SequenceFormat.TUPLE
        )
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
