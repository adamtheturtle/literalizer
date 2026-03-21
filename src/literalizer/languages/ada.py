"""Ada language specification."""

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
    format_string_ada,
)
from literalizer._language import HasFormatEnums

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

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
class Ada(metaclass=HasFormatEnums):
    """Ada language specification."""

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

        LIST = "list"

    class SetFormats(enum.Enum):
        """Set type options for Ada."""

        SET = "set"

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats

    def __init__(
        self,
        *,
        date_format: DateFormats,
        datetime_format: DatetimeFormats,
        bytes_format: BytesFormats,
        sequence_format: SequenceFormats,
    ) -> None:
        """Initialize Ada language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "ANull"
        self.true_literal = "ABool (True)"
        self.false_literal = "ABool (False)"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="AList'("
        )
        self.sequence_close = ")"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="AMap'("
        )
        self.dict_close = ")"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_ada_dict_entry
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = "AList'(1 .. 0 => ANull)"
        self.empty_dict: str | None = "AMap'(1 .. 0 => ANull)"
        self.set_open = "ASet'("
        self.set_close = ")"
        self.empty_set: str | None = "ASet'(1 .. 0 => ANull)"
        self.format_sequence_entry: Callable[[str], str] = _to_ada_val
        self.format_set_entry: Callable[[str], str] = _to_ada_val
        self.comment_prefix = "--"
        self.comment_suffix = ""
        self.omap_open = "AMap'("
        self.omap_close = ")"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_ada_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_scalars_to_strings = False
        self.coerce_heterogeneous_sibling_lists_to_strings = False
        self.coerce_heterogeneous_dict_values_to_strings = False
        self.coerce_heterogeneous_list_values_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
