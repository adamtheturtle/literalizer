"""MATLAB language specification."""

import datetime
import enum
import re
from collections.abc import Callable
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_matlab,
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

_CONTROL_CHAR_THRESHOLD = 32


@beartype
def _decode_matlab_string_expr(expr: str) -> str:
    r"""Decode a MATLAB string expression back to its raw string value.

    Reverses the output of ``format_string_matlab``.  Handles both the
    simple ``"..."`` form (with ``""`` for embedded double-quotes and
    ``\\\\`` for literal backslashes) and the ``"..." + char(N) + "..."``
    concatenation form used for control characters.
    """
    raw: list[str] = []
    for string_seg, char_code in re.findall(
        pattern=r'"((?:[^"]|"")*)"|char\((\d+)\)',
        string=expr,
    ):
        if char_code:
            raw.append(chr(int(char_code)))
        else:
            raw.append(string_seg.replace('""', '"').replace("\\\\", "\\"))
    return "".join(raw)


@beartype
def _matlab_char_key(s: str) -> str:
    """Build a MATLAB char-array expression for a struct key.

    Single quotes are doubled for valid char-vector literals.  Control
    characters (code points 0-31) cannot appear literally inside a
    MATLAB char vector, so they are emitted as ``char(N)`` calls and
    concatenated with ``[...]``.
    """
    parts: list[str] = []
    for segment in re.split(pattern=r"([\x00-\x1f])", string=s):
        if not segment:
            continue
        if len(segment) == 1 and ord(segment) < _CONTROL_CHAR_THRESHOLD:
            parts.append(f"char({ord(segment)})")
        else:
            escaped = segment.replace("'", "''")
            parts.append(f"'{escaped}'")
    if not parts:
        return "''"
    if len(parts) == 1:
        return parts[0]
    return "[" + ", ".join(parts) + "]"


@beartype
def _format_matlab_dict_entry(key: str, value: str) -> str:
    """Format a MATLAB ``struct`` field as a ``'key', value`` pair.

    MATLAB ``struct`` accepts alternating character-vector keys and values.
    Dictionary keys arrive as double-quoted strings; they are converted to
    single-quoted character vectors as required by ``struct``.  Internal
    single quotes are doubled to produce valid MATLAB char-vector literals.
    Control characters are emitted as ``char(N)`` concatenation expressions
    because MATLAB char vectors cannot contain literal control characters.

    Cell-array values are wrapped in an extra layer of braces so that
    ``struct`` stores them as a single cell-array field rather than
    expanding them into a struct array.
    """
    inner = _decode_matlab_string_expr(expr=key)
    key_expr = _matlab_char_key(s=inner)
    if value.startswith("{") and value.endswith("}"):
        value = f"{{{value}}}"
    return f"{key_expr}, {value}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a MATLAB variable declaration."""
    return f"{name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a MATLAB variable assignment."""
    return f"{name} = {value};"


_string_format: Callable[[str], str] = format_string_matlab


@beartype
class Matlab(metaclass=LanguageCls):
    """MATLAB language specification."""

    extension = ".m"

    class DateFormats(enum.Enum):
        """Date format options for Matlab."""

        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Matlab."""

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
        """Sequence type options for MATLAB."""

        CELL_ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="{"),
            close="}",
            empty_sequence="{}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for MATLAB."""

        SET = SetFormatConfig(
            open_str="{",
            close="}",
            empty_set="{}",
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        PERCENT = CommentConfig(
            prefix="%",
            suffix="",
        )
        BLOCK = CommentConfig(
            prefix="%{",
            suffix=" %}",
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
        sequence_format: SequenceFormats = SequenceFormats.CELL_ARRAY,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.PERCENT,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
    ) -> None:
        """Initialize Matlab language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "[]"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="struct("),
            close=")",
            format_entry=_format_matlab_dict_entry,
            empty_dict="struct()",
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
                open_str="struct(",
                close=")",
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_matlab_dict_entry
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
