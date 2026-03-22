"""Zig language specification."""

import datetime
import enum
from collections.abc import Callable
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
    DictFormatConfig,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
)

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
def _to_val(value: str) -> str:
    """Wrap a pre-formatted value string in a Zig ``ZVal`` union literal.

    Inspects the string representation to determine the appropriate union
    tag: ``.int`` for integers, ``.float`` for floats, ``.str`` for
    strings.  Values that are already tagged (starting with ``.``) are
    returned unchanged.
    """
    if value.startswith("."):
        return value
    if value.startswith('"') and value.endswith('"'):
        return f".{{ .str = {value} }}"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    try:
        int(rest)
    except ValueError:
        return f".{{ .float = {value} }}"
    return f".{{ .int = {value} }}"


@beartype
def _format_zig_dict_entry(key: str, value: str) -> str:
    """Format a Zig dict entry as a ``ZKV`` anonymous struct literal."""
    return f".{{ .key = {key}, .val = {_to_val(value=value)} }}"


@beartype
def _format_zig_sequence_entry(item: str) -> str:
    """Format a Zig sequence entry as a ``ZVal`` union literal."""
    return _to_val(value=item)


@beartype
def _format_zig_set_entry(item: str) -> str:
    """Format a Zig set entry as a ``ZVal`` union literal."""
    return _to_val(value=item)


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Zig ``const`` declaration with explicit ``ZVal`` type."""
    return f"const {name}: ZVal = {_to_val(value=value)};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Zig assignment to an existing ``ZVal`` variable."""
    return f"{name} = {_to_val(value=value)};"


_string_format: Callable[[str], str] = format_string_backslash


@beartype
class Zig(metaclass=LanguageCls):
    """Zig language specification."""

    extension = ".zig"

    class DateFormats(enum.Enum):
        """Date format options for Zig."""

        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Zig."""

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
        """Sequence type options for Zig."""

        ARRAY = SequenceFormatConfig(
            open_str=".{ .arr = &.{",
            close="}}",
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
        """Set type options for Zig."""

        SET = SetFormatConfig(
            open_str=".{ .set = &.{",
            close="}}",
            empty_set=None,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_SLASH = CommentConfig(
            prefix="//",
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
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
    ) -> None:
        """Initialize Zig language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = ".nil"
        self.true_literal = ".{ .bool = true }"
        self.false_literal = ".{ .bool = false }"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str=fmt.open_str
        )
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str=".{ .map = &.{"),
            close="}}",
            format_entry=_format_zig_dict_entry,
            empty_dict=None,
        )
        self.multiline_trailing_comma = True
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.format_sequence_entry: Callable[[str], str] = (
            _format_zig_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = _format_zig_set_entry
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str=".{ .map = &.{",
                close="}}",
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_zig_dict_entry
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
