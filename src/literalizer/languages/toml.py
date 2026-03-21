"""TOML language specification."""

from __future__ import annotations

import enum
import re
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value

_BARE_KEY_PATTERN: re.Pattern[str] = re.compile(pattern=r"^[A-Za-z0-9_-]+$")
_MIN_QUOTED_KEY_LENGTH = 2


@beartype
def _format_toml_dict_entry(key: str, value: str) -> str:
    """Format a TOML dict entry as ``key = value``.

    If the key is a double-quoted string that is also a valid bare key
    (alphanumeric, dashes, underscores only), the quotes are stripped for
    cleaner idiomatic output.
    """
    if (
        key.startswith('"')
        and key.endswith('"')
        and len(key) >= _MIN_QUOTED_KEY_LENGTH
    ):
        inner = key[1:-1]
        if _BARE_KEY_PATTERN.match(string=inner):
            return f"{inner} = {value}"
    return f"{key} = {value}"


@beartype
def _format_toml_date(value: datetime.date) -> str:
    """Format a date as a TOML local date literal (unquoted).

    Example: ``datetime.date(2024, 1, 15)`` → ``2024-01-15``.
    """
    return value.isoformat()


@beartype
def _format_toml_datetime(value: datetime.datetime) -> str:
    """Format a datetime as a TOML offset or local datetime literal
    (unquoted).

    Example: ``datetime.datetime(2024, 1, 15, 12, 30, tzinfo=UTC)`` →
    ``2024-01-15T12:30:00+00:00``.
    """
    return value.isoformat()


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a TOML key-value assignment as ``name = value``."""
    return f"{name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a TOML key-value assignment as ``name = value``.

    TOML has no distinction between declaration and re-assignment;
    this produces the same output as
    :func:`_format_variable_declaration`.
    """
    return f"{name} = {value}"


@beartype
class Toml:
    """TOML language specification.

    Produces TOML inline values — inline tables for mappings, and
    arrays for sequences and sets — using TOML v1.1 multiline inline
    table syntax, which permits newlines and comments within braces.

    ``null`` is not a TOML type; dict entries whose value is ``null``
    are omitted (``skip_null_dict_values = True``), and ``null`` values
    in sequences are rendered as the empty string ``""``.

    Dates and datetimes are rendered as unquoted TOML native date /
    datetime literals, which are a distinct TOML type.
    """

    class DateFormat(enum.Enum):
        """Date format options for Toml."""

        TOML = enum.member(value=_format_toml_date)

    class DatetimeFormat(enum.Enum):
        """Datetime format options for Toml."""

        TOML = enum.member(value=_format_toml_datetime)

    class BytesFormat(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

    class SequenceFormat(enum.Enum):
        """Sequence type options for TOML."""

        ARRAY = "array"

    class SetFormat(enum.Enum):
        """Set type options for TOML."""

        SET = "set"

    @property
    def bytes_formats(self) -> type[BytesFormat]:
        """Enum class whose members list the available bytes formats."""
        return type(self).BytesFormat

    @property
    def set_formats(self) -> type[SetFormat]:
        """Enum class whose members list the available set formats."""
        return type(self).SetFormat

    @property
    def date_formats(self) -> type[DateFormat]:
        """Enum class whose members list the available date formats."""
        return type(self).DateFormat

    @property
    def datetime_formats(self) -> type[DatetimeFormat]:
        """Enum class whose members list the available datetime
        formats.
        """
        return type(self).DatetimeFormat

    @property
    def sequence_formats(self) -> type[SequenceFormat]:
        """Enum class whose members list the available sequence
        formats.
        """
        return type(self).SequenceFormat

    def __init__(
        self,
        *,
        date_format: DateFormat,
        datetime_format: DatetimeFormat,
        bytes_format: BytesFormat,
        sequence_format: SequenceFormat,
    ) -> None:
        """Initialize TOML language specification."""
        self.sequence_format = sequence_format
        self.null_literal = '""'
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="["
        )
        self.sequence_close = "]"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="{"
        )
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_toml_dict_entry
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_date: Callable[[datetime.date], str] = date_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        )
        self.format_string: Callable[[str], str] = format_string_backslash
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "["
        self.set_close = "]"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "#"
        self.comment_suffix = ""
        self.omap_open = "{"
        self.omap_close = "}"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_toml_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = True
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
