"""R language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_r,
    format_datetime_r,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer._language import (
    CommentConfig,
    DictFormatConfig,
    HasFormatEnums,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
)
from literalizer.exceptions import EmptyDictKeyError

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value


@beartype
def _format_r_dict_entry_positional(key: str, value: str) -> str:
    """Format an R named list entry.

    R list syntax does not allow zero-length names (``"" = value`` is a
    parse error), so empty-string keys are emitted as positional (unnamed)
    elements.
    """
    if key == '""':
        return value
    return f"{key} = {value}"


@beartype
def _format_r_dict_entry_error(key: str, value: str) -> str:
    """Format an R named list entry, raising on empty-string keys."""
    if key == '""':
        msg = (
            "R does not support empty-string dict keys. "
            "Use empty_dict_key=R.EmptyDictKey.POSITIONAL to emit them "
            "as unnamed list elements instead."
        )
        raise EmptyDictKeyError(msg)
    return f"{key} = {value}"


@beartype
def _format_r_ordered_map_entry(key: str, value: str) -> str:
    """Format an R named list entry for an ordered map."""
    return f"{key} = {value}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format an R variable declaration."""
    return f"{name} <- {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format an R variable assignment."""
    return f"{name} <- {value}"


@beartype
class R(metaclass=HasFormatEnums):
    """R language specification.

    Dicts are represented as named ``list()`` calls where each entry is
    written as ``"key" = value``.  R's parser rejects zero-length names, so
    by default **dict keys that are empty strings are emitted as positional
    (unnamed) list elements** rather than as ``"" = value``.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.R`` — ``as.Date(...)`` call,
              e.g. ``as.Date("2024-01-15")``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.R`` — ``as.POSIXct(...)`` call,
              e.g. ``as.POSIXct("2024-01-15T12:30:00")``.

        empty_dict_key: How to handle empty-string dict keys.

            * ``EmptyDictKey.POSITIONAL`` — emit as an unnamed
              positional list element.
            * ``EmptyDictKey.ERROR`` — raise
              :class:`~literalizer.exceptions.EmptyDictKeyError`.
    """

    class DateFormats(enum.Enum):
        """Date formatting options for R."""

        R = enum.member(value=format_date_r)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime formatting options for R."""

        R = enum.member(value=format_datetime_r)

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value(value=dt_value)

    class EmptyDictKey(enum.Enum):
        """How to handle empty-string dict keys in R.

        R's parser rejects zero-length names (``"" = value`` is a parse
        error).
        """

        POSITIONAL = enum.member(value=_format_r_dict_entry_positional)
        ERROR = enum.member(value=_format_r_dict_entry_error)

        def __call__(self, key: str, value: str, /) -> str:
            """Format a dict entry."""
            return self.value(key=key, value=value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for R."""

        LIST = SequenceFormatConfig(
            open_str="list(",
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
        """Set type options for R."""

        SET = SetFormatConfig(
            open_str="list(",
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

    class VariableTypeHints(enum.Enum):
        """Variable type hint options."""

        NONE = "none"

    variable_type_hints_formats = VariableTypeHints

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.R,
        datetime_format: DatetimeFormats = DatetimeFormats.R,
        empty_dict_key: EmptyDictKey = EmptyDictKey.POSITIONAL,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        comment_format: CommentFormats = CommentFormats.HASH,
    ) -> None:
        """Initialize R language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "NULL"
        self.true_literal = "TRUE"
        self.false_literal = "FALSE"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str=fmt.open_str
        )
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="list("),
            close=")",
            format_entry=empty_dict_key,
            empty_dict=None,
        )
        self.multiline_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = format_string_backslash
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="list(",
                close=")",
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_r_ordered_map_entry
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
