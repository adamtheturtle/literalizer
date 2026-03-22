"""Ada language specification."""

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
    format_string_ada,
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
def _to_ada_val(value: str) -> str:
    """Wrap a pre-formatted value string in an Ada ``A_Val`` constructor.

    Inspects the string representation to determine the appropriate
    constructor: ``AStr``, ``AInt``, ``AFloat``, or passes through
    values that are already ``A_Val`` expressions
    (``ANull``, ``ABool``, ``AList``, ``AMap``, ``ASet``, ``AEntry``).
    """
    _val_prefixes = (
        "ANull",
        "ABool",
        "AInt",
        "AFloat",
        "AStr",
        "AList",
        "AMap",
        "ASet",
        "AEntry",
    )
    if any(value.startswith(p) for p in _val_prefixes):
        return value
    if value.startswith('"') and value.endswith('"'):
        return f"AStr ({value})"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"AInt ({value})"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f"AFloat ({value})"
    except ValueError:  # pragma: no cover
        pass
    if float_result is not None:
        return float_result
    return value  # pragma: no cover


@beartype
def _format_ada_dict_entry(key: str, value: str) -> str:
    """Format an Ada dict/map entry as an ``AEntry (key, AVal value)``
    call.
    """
    return f"AEntry ({key}, {_to_ada_val(value=value)})"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format an Ada object declaration.

    Example: ``"x"`` and ``"AList'(AInt (1))"`` →
    ``"x : A_Val := AList'(AInt (1));"``
    """
    return f"{name} : A_Val := {_to_ada_val(value=value)};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format an Ada assignment statement to an existing variable.

    Example: ``"x"`` and ``"AList'(AInt (1))"`` →
    ``"x := AList'(AInt (1));"``
    """
    return f"{name} := {_to_ada_val(value=value)};"


_string_format: Callable[[str], str] = format_string_ada


@beartype
class Ada(metaclass=LanguageCls):
    """Ada language specification."""

    extension = ".adb"
    pygments_name = "ada"

    class DateFormats(enum.Enum):
        """Date format options for Ada."""

        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Ada."""

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
        """Sequence type options for Ada."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="AList'("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence="AList'(1 .. 0 => ANull)",
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Ada."""

        SET = SetFormatConfig(
            open_str="ASet'(",
            close=")",
            empty_set="ASet'(1 .. 0 => ANull)",
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
        """Initialize Ada language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "ANull"
        self.true_literal = "ABool (True)"
        self.false_literal = "ABool (False)"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="AMap'("),
            close=")",
            format_entry=_format_ada_dict_entry,
            empty_dict="AMap'(1 .. 0 => ANull)",
        )
        self.multiline_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.format_sequence_entry: Callable[[str], str] = _to_ada_val
        self.format_set_entry: Callable[[str], str] = _to_ada_val
        self.comment_format = comment_format
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="AMap'(",
                close=")",
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_ada_dict_entry
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
