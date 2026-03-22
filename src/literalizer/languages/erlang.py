"""Erlang language specification."""

import datetime
import enum
from collections.abc import Callable
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    fixed_dict_open,
    fixed_sequence_open,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer._language import (
    CommentConfig,
    DictFormatConfig,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
)

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
def _format_erlang_ordered_map_entry(key: str, value: str) -> str:
    """Format an Erlang ordered-map entry as a ``{key, value}`` tuple."""
    return f"{{{key}, {value}}}"


@beartype
def _format_bytes(value: bytes) -> str:
    """Format bytes as an Erlang binary literal."""
    parts = ", ".join(f"{b}" for b in value)
    return f"<<{parts}>>"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format an Erlang variable declaration."""
    erlang_name = name[0].upper() + name[1:]
    return f"{erlang_name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format an Erlang variable assignment."""
    erlang_name = name[0].upper() + name[1:]
    return f"{erlang_name} = {value}"


_string_format: Callable[[str], str] = format_string_backslash


@beartype
class Erlang(metaclass=LanguageCls):
    """Erlang language specification.

    Args:
        sequence_format: Which Erlang sequence type to use.

            * ``sequence_formats.LIST`` — list literal,
              e.g. ``[1, 2, 3]``.
            * ``sequence_formats.TUPLE`` — tuple literal,
              e.g. ``{1, 2, 3}``.
    """

    extension = ".erl"

    class DateFormats(enum.Enum):
        """Date format options for Erlang."""

        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Erlang."""

        ISO = enum.member(value=format_datetime_iso)

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value(value=dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        BINARY = enum.member(value=_format_bytes)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Erlang."""

        LIST = SequenceFormatConfig(
            open_str="[",
            close="]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            schema_to_opener=None,
        )
        TUPLE = SequenceFormatConfig(
            open_str="{",
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            schema_to_opener=None,
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Erlang."""

        SET = SetFormatConfig(
            open_str="sets:from_list([",
            close="])",
            empty_set="sets:from_list([])",
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        PERCENT = CommentConfig(
            prefix="%",
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
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.BINARY,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.PERCENT,
    ) -> None:
        """Initialize Erlang language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "undefined"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str=fmt.open_str
        )
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="#{"),
            close="}",
            format_entry=dict_entry_with_separator(separator=" => "),
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
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="[",
                close="]",
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_erlang_ordered_map_entry
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
