"""Mojo language specification."""

import datetime
import enum
from collections.abc import Callable
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
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
def _format_mojo_ordered_map_entry(key: str, value: str) -> str:
    """Format one Mojo ordered-map entry as a ``Tuple(key, value)``."""
    return f"Tuple({key}, {value})"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Mojo variable declaration in Python-compatible script
    style.
    """
    return f"var {name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Mojo variable assignment."""
    return f"{name} = {value}"


_string_format: Callable[[str], str] = format_string_backslash


@beartype
class Mojo(metaclass=LanguageCls):
    """Mojo language specification.

    Mojo does not support heterogeneous collections — every element in a
    list or set must share a single type.  When a collection contains
    scalar values of mixed types (e.g. ``[1, 2.5, 3]``), **all values
    are coerced to their string representations** so that the resulting
    literal is valid Mojo (e.g. ``["1", "2.5", "3"]``).

    For sets, this coercion can cause the output to have fewer elements
    than the input when distinct values of different types coerce to the
    same string (e.g. ``{1, "1"}`` both become ``"1"``).
    """

    extension = ".mojo"

    class DateFormats(enum.Enum):
        """Date format options for Mojo."""

        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Mojo."""

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
        """Sequence type options for Mojo."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="["),
            close="]",
            supports_heterogeneity=False,
            single_element_trailing_comma=False,
            empty_sequence="List[String]()",
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Mojo."""

        SET = SetFormatConfig(
            open_str="[",
            close="]",
            empty_set="Set[String]()",
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
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.HASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
    ) -> None:
        """Initialize Mojo language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "None"
        self.true_literal = "True"
        self.false_literal = "False"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="{"),
            close="}",
            format_entry=dict_entry_with_separator(separator=": "),
            empty_dict="Dict[String, String]()",
        )
        self.multiline_trailing_comma = True
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
            _format_mojo_ordered_map_entry
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
