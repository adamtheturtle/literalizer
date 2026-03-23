"""MATLAB language specification."""

import datetime
import enum
import re
from collections.abc import Callable, Sequence

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer._language import (
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DictFormatConfig,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
)
from literalizer._types import Value

_MATLAB_CONTROL_CHAR_THRESHOLD = 32


@beartype
def _format_string_matlab(value: str) -> str:
    r"""Format a string using MATLAB double-quoted string escaping rules.

    MATLAB double-quoted strings (the ``string`` type) interpret backslash
    escape sequences: ``\\`` for a literal backslash, ``\n`` for newline,
    ``\t`` for tab, etc.  Double quotes are escaped by doubling (``""``).
    Control characters (code points 0-31) are emitted as ``char(N)``
    expressions joined with ``+``.
    """
    parts: list[str] = []
    for segment in re.split(pattern=r"([\x00-\x1f])", string=value):
        if not segment:
            continue
        if len(segment) == 1 and ord(segment) < _MATLAB_CONTROL_CHAR_THRESHOLD:
            parts.append(f"char({ord(segment)})")
        else:
            escaped = segment.replace("\\", "\\\\").replace('"', '""')
            parts.append(f'"{escaped}"')
    if not parts:
        return '""'
    if len(parts) == 1:
        return parts[0]
    return " + ".join(parts)


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
def _format_variable_declaration(name: str, value: str, _data: Value) -> str:
    """Format a MATLAB variable declaration."""
    return f"{name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format a MATLAB variable assignment."""
    return f"{name} = {value};"


@beartype
def _format_date_matlab(value: datetime.date) -> str:
    """Format a date as a MATLAB ``datetime`` expression."""
    return f"datetime({value.year}, {value.month}, {value.day})"


@beartype
def _format_datetime_matlab(value: datetime.datetime) -> str:
    """Format a datetime as a MATLAB ``datetime`` expression."""
    parts = (
        f"datetime({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second}"
    )
    if value.microsecond:
        millisecond = value.microsecond / 1000
        parts += f", {millisecond}"
    return parts + ")"


_string_format: Callable[[str], str] = _format_string_matlab


@beartype
class Matlab(metaclass=LanguageCls):
    """MATLAB language specification."""

    extension = ".m"
    pygments_name = "matlab"

    class DateFormats(enum.Enum):
        """Date format options for Matlab."""

        MATLAB = DateFormatConfig(formatter=_format_date_matlab)
        ISO = DateFormatConfig(formatter=format_date_iso, produces_string=True)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Matlab."""

        MATLAB = DatetimeFormatConfig(formatter=_format_datetime_matlab)
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            produces_string=True,
        )

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

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
            preamble_lines=(),
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
            preamble_lines=(),
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

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        ASSIGN = "assign"

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        STRUCT = "struct"

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = "decimal"

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = "none"

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = "double"

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        NO = "no"

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
    declaration_styles = DeclarationStyles
    dict_formats = DictFormats
    integer_formats = IntegerFormats
    numeric_separators = NumericSeparators
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.MATLAB,
        datetime_format: DatetimeFormats = DatetimeFormats.MATLAB,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.CELL_ARRAY,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.PERCENT,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN,
        dict_format: DictFormats = DictFormats.STRUCT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
    ) -> None:
        """Initialize Matlab language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "[]"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="struct("),
            close=")",
            format_entry=_format_matlab_dict_entry,
            empty_dict="struct()",
            preamble_lines=(),
        )
        self.multiline_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.format_integer: Callable[[int], str] = str
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_format = comment_format
        self.declaration_style = declaration_style
        self.dict_format = dict_format
        self.integer_format = integer_format
        self.numeric_separator = numeric_separator
        self.string_format = string_format
        self.trailing_comma = trailing_comma
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="struct(",
                close=")",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_matlab_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_variable_assignment
        )
        self.static_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
