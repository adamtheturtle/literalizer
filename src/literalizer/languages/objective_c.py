"""Objective-C language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
)

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value

_OBJC_PREFIXES = (
    "@",
    "[NSNull null]",
    "[NSSet setWithArray:",
)


@beartype
def _to_objc_val(value: str) -> str:
    """Convert a pre-formatted value string to an Objective-C NSObject
    expression.

    Strings, booleans, null, and nested collections already start with
    ``@`` or ``[`` and are returned unchanged.  Bare numeric strings are
    wrapped in ``@(...)`` to produce an ``NSNumber`` literal.
    """
    if any(value.startswith(p) for p in _OBJC_PREFIXES):
        return value
    return f"@({value})"


@beartype
def _format_objc_dict_entry(key: str, value: str) -> str:
    """Format an Objective-C NSDictionary literal entry."""
    return f"{key}: {_to_objc_val(value=value)}"


@beartype
def _format_objc_string(value: str) -> str:
    r"""Format a string as an Objective-C ``NSString`` literal.

    Escapes backslashes, double quotes, newlines, and tabs, then wraps
    the result in ``@"..."``.

    Example: ``hello "world"`` → ``@"hello \"world\""``.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    return f'@"{escaped}"'


@beartype
def _format_objc_bytes(value: bytes) -> str:
    """Format bytes as an Objective-C ``NSString`` hex literal.

    Example: ``b"Hi"`` → ``@"4869"``.
    """
    return f'@"{value.hex()}"'


@beartype
def _format_objc_date(value: datetime.date) -> str:
    """Format a date as an Objective-C ``NSString`` ISO 8601 literal.

    Example: ``datetime.date(2024, 1, 15)`` → ``@"2024-01-15"``.
    """
    return f'@"{value.isoformat()}"'


@beartype
def _format_objc_datetime(value: datetime.datetime) -> str:
    """Format a datetime as an Objective-C ``NSString`` ISO 8601
    literal.

    Example: ``datetime.datetime(2024, 1, 15, 12, 30)`` →
    ``@"2024-01-15T12:30:00"``.
    """
    return f'@"{value.isoformat()}"'


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format an Objective-C ``id`` variable declaration.

    Example: ``"x"`` and ``@[@YES, @NO]`` →
    ``"id x = @[@YES, @NO];"``.
    """
    return f"id {name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format an Objective-C variable assignment.

    Example: ``"x"`` and ``@[@YES, @NO]`` → ``"x = @[@YES, @NO];"``
    """
    return f"{name} = {value};"


_string_format: Callable[[str], str] = _format_objc_string


@beartype
class ObjectiveC:
    """Objective-C language specification."""

    class date_formats(enum.Enum):  # noqa: N801
        """Date format options for ObjectiveC."""

        OBJC = enum.member(value=_format_objc_date)

    class datetime_formats(enum.Enum):  # noqa: N801
        """Datetime format options for ObjectiveC."""

        OBJC = enum.member(value=_format_objc_datetime)

    class bytes_formats(enum.Enum):  # noqa: N801
        """Bytes formatting options."""

        HEX = enum.member(value=_format_objc_bytes)

    class sequence_formats(enum.Enum):  # noqa: N801
        """Sequence type options for Objective-C."""

        ARRAY = "array"

    class set_formats(enum.Enum):  # noqa: N801
        """Set type options for Objective-C."""

        SET = "set"

    def __init__(
        self,
        *,
        date_format: date_formats,
        datetime_format: datetime_formats,
        bytes_format: bytes_formats,
        sequence_format: sequence_formats,
    ) -> None:
        """Initialize Objective-C language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "[NSNull null]"
        self.true_literal = "@YES"
        self.false_literal = "@NO"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="@["
        )
        self.sequence_close = "]"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="@{"
        )
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_objc_dict_entry
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_date: Callable[[datetime.date], str] = date_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = "@[]"
        self.empty_dict: str | None = "@{}"
        self.set_open = "[NSSet setWithArray:@["
        self.set_close = "]]"
        self.empty_set: str | None = "[NSSet set]"
        self.format_sequence_entry: Callable[[str], str] = _to_objc_val
        self.format_set_entry: Callable[[str], str] = _to_objc_val
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "@{"
        self.omap_close = "}"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_objc_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_scalars_to_strings = False
        self.coerce_heterogeneous_sibling_lists_to_strings = False
        self.coerce_heterogeneous_dict_values_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
