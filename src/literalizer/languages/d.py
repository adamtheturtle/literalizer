"""D language specification."""

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
    CommentConfig,
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
def _to_val(value: str) -> str:
    """Wrap a pre-formatted value string in a D ``JSONValue(...)`` call.

    Inspects the string representation to determine whether wrapping is
    needed.  Values that are already ``JSONValue(...)`` or ``parseJSON(...)``
    expressions are returned unchanged; ``null``, ``true``, and ``false``
    literals and numeric and string literals are all wrapped.
    """
    if value.startswith(("JSONValue(", 'parseJSON("')):
        return value
    if value in {"null", "true", "false"}:
        return f"JSONValue({value})"
    if value.startswith('"') and value.endswith('"'):
        return f"JSONValue({value})"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"JSONValue({value})"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f"JSONValue({value})"
    except ValueError:  # pragma: no cover
        pass
    if float_result is not None:
        return float_result
    return value  # pragma: no cover


@beartype
def _format_d_dict_entry(key: str, value: str) -> str:
    """Format a D associative-array entry as ``key: JSONValue(value)``."""
    return f"{key}: {_to_val(value=value)}"


@beartype
def _format_d_sequence_entry(item: str) -> str:
    """Format a D array entry as a ``JSONValue(item)`` call."""
    return _to_val(value=item)


@beartype
def _format_d_set_entry(item: str) -> str:
    """Format a D set entry (represented as array) as
    ``JSONValue(item)``.
    """
    return _to_val(value=item)


@beartype
def _format_d_omap_entry(key: str, value: str) -> str:
    """Format a D ordered-map entry as a two-element ``JSONValue``
    array.
    """
    return f"JSONValue([JSONValue({key}), {_to_val(value=value)}])"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a D ``auto`` variable declaration using ``JSONValue``."""
    return f"auto {name} = {_to_val(value=value)};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a D assignment to an existing variable."""
    return f"{name} = {_to_val(value=value)};"


_string_format: Callable[[str], str] = format_string_backslash


@beartype
class D(metaclass=HasFormatEnums):
    """D language specification."""

    class DateFormats(enum.Enum):
        """Date format options for D."""

        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for D."""

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
        """Sequence type options for D."""

        ARRAY = SequenceFormatConfig(
            open_str="JSONValue([",
            close="])",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence='parseJSON("[]")',
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for D."""

        SET = SetFormatConfig(
            open_str="JSONValue([",
            close="])",
            empty_set='parseJSON("[]")',
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
        """Initialize D language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str=fmt.open_str
        )
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="JSONValue(["
        )
        self.dict_close = "])"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_d_dict_entry
        )
        self.multiline_trailing_comma = True
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_dict: str | None = 'parseJSON("{}")'
        self.format_sequence_entry: Callable[[str], str] = (
            _format_d_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = _format_d_set_entry
        self.comment_config = CommentConfig(prefix="//", suffix="")
        self.omap_format_config = OmapFormatConfig(
            open_str="JSONValue([",
            close="])",
        )
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_d_omap_entry
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
