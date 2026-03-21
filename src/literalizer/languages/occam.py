"""Occam-pi language specification."""

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
)
from literalizer._language import HasFormatEnums

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value


@beartype
def _to_val(value: str) -> str:
    """Convert a value to an occam-pi MOBILE LIT expression."""
    if value.startswith("MOBILE LIT("):
        return value
    if value.startswith('"') and value.endswith('"'):
        return f"MOBILE LIT(lit.str; MOBILE []BYTE {value})"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"MOBILE LIT(lit.int; {value})"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f"MOBILE LIT(lit.float; {value}(REAL32))"
    except ValueError:  # pragma: no cover
        pass
    if float_result is not None:
        return float_result
    return value  # pragma: no cover


@beartype
def _format_occam_dict_entry(key: str, value: str) -> str:
    """Format an occam-pi dict or omap entry as a ``MOBILE LIT(lit.pair;
    ...)`` constructor.
    """
    val = _to_val(value=value)
    return f"MOBILE LIT(lit.pair; MOBILE []BYTE {key}; {val})"


@beartype
def _format_occam_list_entry(item: str) -> str:
    """Format an occam-pi list entry with the appropriate ``LIT``
    constructor.
    """
    return _to_val(value=item)


@beartype
def _format_occam_set_entry(item: str) -> str:
    """Format an occam-pi set entry with the appropriate ``LIT``
    constructor.
    """
    return _to_val(value=item)


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format an occam-pi variable declaration."""
    return f"VAL MOBILE LIT {name} IS {value}:"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format an occam-pi variable assignment."""
    return f"{name} := {value}"


_string_format: Callable[[str], str] = format_string_backslash


@beartype
class Occam(metaclass=HasFormatEnums):
    """Occam-pi language specification."""

    class DateFormats(enum.Enum):
        """Date format options for Occam."""

        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Occam."""

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
        """Sequence type options for Occam."""

        LIST = "list"

    class SetFormats(enum.Enum):
        """Set type options for Occam."""

        SET = "set"

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
    ) -> None:
        """Initialize Occam language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "MOBILE LIT(lit.null)"
        self.true_literal = "MOBILE LIT(lit.bool; TRUE)"
        self.false_literal = "MOBILE LIT(lit.bool; FALSE)"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="MOBILE LIT(lit.list; MOBILE []MOBILE LIT ["
        )
        self.sequence_close = "])"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="MOBILE LIT(lit.map; MOBILE []MOBILE LIT ["
        )
        self.dict_close = "])"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_occam_dict_entry
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "MOBILE LIT(lit.set; MOBILE []MOBILE LIT ["
        self.set_close = "])"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            _format_occam_list_entry
        )
        self.format_set_entry: Callable[[str], str] = _format_occam_set_entry
        self.comment_prefix = "--"
        self.comment_suffix = ""
        self.omap_open = "MOBILE LIT(lit.map; MOBILE []MOBILE LIT ["
        self.omap_close = "])"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_occam_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_scalars_to_strings = False
        self.coerce_heterogeneous_collection_values_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
