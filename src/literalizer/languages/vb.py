"""Visual Basic (.NET) language specification."""

import datetime
import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    MixedNumeric,
    fixed_dict_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    make_element_to_type,
    make_type_to_opener,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_sequence_open,
    typed_set_open,
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

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

_VB_CHAR_REPLACEMENTS: dict[str, str] = {
    "\n": "Chr(10)",
    "\r": "Chr(13)",
    "\t": "vbTab",
}

_VB_CONTROL_CHAR_THRESHOLD = 32


@beartype
def _flush_vb_current(
    *,
    parts: list[str],
    current: str,
) -> str:
    """Flush accumulated literal characters into parts."""
    if current:
        parts.append(f'"{current}"')
    return ""


@beartype
def _vb_string_parts(value: str) -> list[str]:
    """Generate VB.NET string parts for control character handling."""
    parts: list[str] = []
    current = ""
    i = 0
    while i < len(value):
        c = value[i]
        if c == '"':
            current += '""'
            i += 1
        elif c == "\r" and i + 1 < len(value) and value[i + 1] == "\n":
            current = _flush_vb_current(parts=parts, current=current)
            parts.append("vbCrLf")
            i += 2
        elif c in _VB_CHAR_REPLACEMENTS:
            current = _flush_vb_current(parts=parts, current=current)
            parts.append(_VB_CHAR_REPLACEMENTS[c])
            i += 1
        elif ord(c) < _VB_CONTROL_CHAR_THRESHOLD:
            current = _flush_vb_current(parts=parts, current=current)
            parts.append(f"Chr({ord(c)})")
            i += 1
        else:
            current += c
            i += 1
    _flush_vb_current(parts=parts, current=current)
    return parts


@beartype
def _format_string_vb(value: str) -> str:
    r"""Format a string using VB.NET string escaping rules.

    VB.NET strings use ``""`` to escape embedded double quotes and do not
    support backslash escapes.  Control characters such as newlines and
    tabs are expressed via ``vbCrLf``, ``vbTab``, or ``Chr(N)`` string
    concatenation.
    """
    parts = _vb_string_parts(value)  # type: ignore[misc]
    if not parts:
        return '""'
    if len(parts) == 1:
        return parts[0]
    return " & ".join(parts)


_VB_SCALAR_TYPES: dict[type, str] = {
    str: "String",
    bool: "Boolean",
    int: "Integer",
    float: "Double",
    MixedNumeric: "Double",
    bytes: "String",
    datetime.date: "String",
    datetime.datetime: "String",
}

_vb_element_to_type = make_element_to_type(
    scalar_types=_VB_SCALAR_TYPES,
    list_template="{inner}()",
)

_vb_set_type_to_opener = make_type_to_opener(
    element_to_type=_vb_element_to_type,
    opener_template="New HashSet(Of {type_name}) From {{",
)

_vb_type_to_opener = make_type_to_opener(
    element_to_type=_vb_element_to_type,
    opener_template="New {type_name}() {{",
)


@beartype
def _format_vb_dict_entry(key: str, value: str) -> str:
    """Format a VB.NET dictionary initializer entry."""
    return f"{{{key}, {value}}}"


@beartype
def _format_variable_declaration(name: str, value: str, _data: Value) -> str:
    """Format a VB.NET variable declaration.

    Leading comment lines (starting with ``'``) are hoisted before the
    ``Dim`` statement so that the result remains valid VB.NET when the
    value is used in a ``Dim`` declaration.
    """
    lines = value.split(sep="\n")
    comment_lines: list[str] = []
    while lines and lines[0].lstrip().startswith("'"):
        comment_lines.append(lines.pop(0))
    rest = "\n".join(lines)
    dim_line = f"Dim {name} = {rest}"
    if comment_lines:
        return "\n".join([*comment_lines, dim_line])
    return dim_line


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format a VB.NET variable assignment."""
    return f"{name} = {value}"


@beartype
class VisualBasic(metaclass=LanguageCls):
    """Visual Basic (.NET) language specification.

    VB.NET collection initializers (``New T() { ... }``,
    ``New HashSet(Of T) From { ... }``, etc.) do not support comments
    inside the ``{ ... }`` block.  YAML comments associated with
    collection elements are therefore emitted as standalone comment lines
    *before* the collection — or before the variable declaration when a
    variable name is supplied.
    """

    extension = ".vb"
    pygments_name = "vb.net"

    class DateFormats(enum.Enum):
        """Date format options for VisualBasic."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for VisualBasic."""

        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            type_produced=str,
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
        """Sequence type options for Visual Basic."""

        ARRAY = SequenceFormatConfig(
            sequence_open=typed_sequence_open(
                type_to_opener=_vb_type_to_opener,
                fallback="New Object() {",
            ),
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence="New Object() {}",
            preamble_lines=("Imports System.Collections.Generic",),
            format_entry=passthrough_sequence_entry,
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Visual Basic."""

        HASH_SET = SetFormatConfig(
            set_open=typed_set_open(
                type_to_opener=_vb_set_type_to_opener,
                fallback="New HashSet(Of Object) From {",
            ),
            close="}",
            empty_set="New HashSet(Of Object)()",
            preamble_lines=(),
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        APOSTROPHE = CommentConfig(
            prefix="'",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        DIM = "dim"

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = "default"

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
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.HASH_SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.APOSTROPHE,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.DIM,
        dict_format: DictFormats = DictFormats.DEFAULT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
    ) -> None:
        """Initialize VisualBasic language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "Nothing"
        self.true_literal = "True"
        self.false_literal = "False"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(
                open_str="New Dictionary(Of String, Object) From {",
            ),
            close="}",
            format_entry=_format_vb_dict_entry,
            empty_dict=None,
            preamble_lines=("Imports System.Collections.Generic",),
        )
        self.multiline_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _format_string_vb
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
                open_str="New Dictionary(Of String, Object) From {",
                close="}",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_vb_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = False
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_variable_assignment
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
