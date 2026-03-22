"""TOML language specification."""

import datetime
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
from literalizer._language import (
    CommentConfig,
    DictFormatConfig,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
)

if TYPE_CHECKING:
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
class Toml(metaclass=LanguageCls):
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

    extension = ".toml"

    class DateFormats(enum.Enum):
        """Date format options for Toml."""

        TOML = enum.member(value=_format_toml_date)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Toml."""

        TOML = enum.member(value=_format_toml_datetime)

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
        """Sequence type options for TOML."""

        ARRAY = SequenceFormatConfig(
            open_str="[",
            close="]",
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
        """Set type options for TOML."""

        SET = SetFormatConfig(
            open_str="[",
            close="]",
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
        date_format: DateFormats = DateFormats.TOML,
        datetime_format: DatetimeFormats = DatetimeFormats.TOML,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.HASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
    ) -> None:
        """Initialize TOML language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.null_literal = '""'
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str=fmt.open_str
        )
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="{"),
            close="}",
            format_entry=_format_toml_dict_entry,
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
        self.comment_format = comment_format
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="{",
                close="}",
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_toml_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = True
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
