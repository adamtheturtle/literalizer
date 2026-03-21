"""C language specification."""

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


_string_format: Callable[[str], str] = format_string_backslash


@beartype
class C(metaclass=HasFormatEnums):
    """C language specification."""

    class DateFormats(enum.Enum):
        """Date format options for C."""

        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for C."""

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
        """Sequence type options for C."""

        ARRAY = SequenceFormatConfig(
            open_str="((_CVal){.a = (_CVal[]){",
            close="}})",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for C."""

        SET = SetFormatConfig(
            open_str="((_CVal){.a = (_CVal[]){",
            close="}})",
            empty_set=None,
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
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.SET,
    ) -> None:
        """Initialize C language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "((_CVal){.s = NULL})"
        self.true_literal = "((_CVal){.b = true})"
        self.false_literal = "((_CVal){.b = false})"
        fmt = sequence_format.value
        self.sequence_format_config = fmt
        self.set_format_config = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str=fmt.open_str
        )
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="((_CVal){.m = (_CKV[]){"
        )
        self.dict_close = "}})"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_c_dict_entry
        )
        self.multiline_trailing_comma = True
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_dict: str | None = None
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
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
