"""PowerShell language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    passthrough_set_entry,
)
from literalizer._language import (
    CommentConfig,
    DictFormatConfig,
    HasFormatEnums,
    OmapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
)

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value


@beartype
def _format_sequence_entry(item: str) -> str:
    """Prevent nested array flattening with a unary comma prefix.

    In PowerShell ``@()`` collects pipeline output and arrays written to the
    pipeline are automatically unrolled.  Prefixing a nested ``@(…)`` with
    the unary comma operator keeps it as a single array element.

    Example: ``"@(1; 2)"`` → ``",@(1; 2)"``; ``"42"`` → ``"42"``.
    """
    if item.startswith("@("):
        return f",{item}"
    return item


@beartype
def _format_string(value: str) -> str:
    """Format a string using PowerShell back-tick escaping."""
    escaped = (
        value.replace("`", "``")
        .replace("$", "`$")
        .replace('"', '`"')
        .replace("\n", "`n")
        .replace("\t", "`t")
    )
    return f'"{escaped}"'


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a PowerShell variable declaration."""
    return f"${name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a PowerShell variable assignment."""
    return f"${name} = {value}"


_string_format: Callable[[str], str] = _format_string


@beartype
class PowerShell(metaclass=HasFormatEnums):
    """PowerShell language specification."""

    class DateFormats(enum.Enum):
        """Date format options for PowerShell."""

        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for PowerShell."""

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
        """Sequence type options for PowerShell."""

        ARRAY = SequenceFormatConfig(
            open_str="@(",
            close=")",
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
        """Set type options for PowerShell."""

        SET = SetFormatConfig(
            open_str="@(",
            close=")",
            empty_set=None,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        HASH = CommentConfig(
            prefix="#",
            suffix="",
        )

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.SET,
        comment_format: CommentFormats = CommentFormats.HASH,
    ) -> None:
        """Initialize PowerShell language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "$null"
        self.true_literal = "$true"
        self.false_literal = "$false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str=fmt.open_str
        )
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="@{"),
            close="}",
            format_entry=dict_entry_with_separator(separator=" = "),
            empty_dict=None,
        )
        self.multiline_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.format_sequence_entry: Callable[[str], str] = (
            _format_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_config: CommentConfig = comment_format.value
        self.omap_format_config: OmapFormatConfig = OmapFormatConfig(
            open_str="[ordered]@{",
            close="}",
        )
        self.format_omap_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=" = ")
        )
        self.multiline_close_indent = ""
        self.element_separator = "; "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
