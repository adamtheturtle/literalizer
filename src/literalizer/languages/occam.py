"""Occam-pi language specification."""

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
    """Format an occam-pi dict or ordered-map entry as a ``MOBILE
    LIT(lit.pair;
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
class Occam(metaclass=LanguageCls):
    """Occam-pi language specification."""

    extension = ".occ"

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

        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(
                open_str="MOBILE LIT(lit.list; MOBILE []MOBILE LIT [",
            ),
            close="])",
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
        """Set type options for Occam."""

        SET = SetFormatConfig(
            open_str="MOBILE LIT(lit.set; MOBILE []MOBILE LIT [",
            close="])",
            empty_set=None,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_DASH = CommentConfig(
            prefix="--",
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
        comment_format: CommentFormats = CommentFormats.DOUBLE_DASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
    ) -> None:
        """Initialize Occam language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "MOBILE LIT(lit.null)"
        self.true_literal = "MOBILE LIT(lit.bool; TRUE)"
        self.false_literal = "MOBILE LIT(lit.bool; FALSE)"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(
                open_str="MOBILE LIT(lit.map; MOBILE []MOBILE LIT [",
            ),
            close="])",
            format_entry=_format_occam_dict_entry,
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
            _format_occam_list_entry
        )
        self.format_set_entry: Callable[[str], str] = _format_occam_set_entry
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="MOBILE LIT(lit.map; MOBILE []MOBILE LIT [",
                close="])",
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_occam_dict_entry
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
