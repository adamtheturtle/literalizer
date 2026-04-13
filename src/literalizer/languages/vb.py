"""Visual Basic (.NET) language specification."""

import datetime
import enum
import textwrap
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters.collection_openers import (
    make_element_to_type,
    make_type_to_opener,
    typed_collection_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    braced_dict_entry,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    variable_formatter,
)
from literalizer._formatters.format_factories import (
    dict_format_factory,
    ordered_map_format_factory,
    set_format_factory,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._language import (
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    no_type_hint_preamble,
    prepend_body_preamble,
)
from literalizer._types import Value

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


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
    control_char_threshold = 32
    parts: list[str] = []
    current = ""
    i = 0
    char_replacements = {"\n": "Chr(10)", "\r": "Chr(13)", "\t": "vbTab"}
    while i < len(value):
        c = value[i]
        if c == '"':
            current += '""'
            i += 1
        elif c == "\r" and i + 1 < len(value) and value[i + 1] == "\n":
            current = _flush_vb_current(parts=parts, current=current)
            parts.append("vbCrLf")
            i += 2
        elif c in char_replacements:
            current = _flush_vb_current(parts=parts, current=current)
            parts.append(char_replacements[c])
            i += 1
        elif ord(c) < control_char_threshold:
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
    parts = _vb_string_parts(value=value)
    if not parts:
        return '""'
    if len(parts) == 1:
        return parts[0]
    return " & ".join(parts)


@beartype
def _format_variable_declaration(name: str, value: str, _data: Value) -> str:
    """Format a VB.NET variable declaration."""
    return f"Dim {name} = {value}"


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
    supports_default_set_element_type = True
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = True
    supports_default_dict_key_type = True
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True
    supports_variable_names = True

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
        BASE64 = enum.member(value=format_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Visual Basic."""

        ARRAY = "array"

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return True

    class SetFormats(enum.Enum):
        """Set type options for Visual Basic."""

        HASH_SET = enum.member(
            value=set_format_factory(
                open_template="New HashSet(Of {type}) From {{",
                close="}}",
                empty_template="New HashSet(Of {type})()",
                preamble_lines=(),
                set_opener_template=("New HashSet(Of {type_name}) From {{"),
                coerce_mixed_to_str=False,
            )
        )

        def __call__(self, default_type: str) -> SetFormatConfig:
            """Create a set format config for the given type."""
            return self.value(default_type)

    class CommentFormats(enum.Enum):
        """Comment style options."""

        APOSTROPHE = CommentConfig(
            prefix="'",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        DIM = DeclarationStyleConfig(
            formatter=_format_variable_declaration,
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = enum.member(
            value=dict_format_factory(
                open_template=(
                    "New Dictionary(Of {key_type}, {type}) From {{"
                ),
                close="}",
                format_entry=braced_dict_entry(
                    format_value=passthrough_sequence_entry,
                ),
                empty_template=None,
                preamble_lines=("Imports System.Collections.Generic",),
                narrowed_open=None,
            )
        )

        def __call__(
            self,
            default_type: str,
            *,
            default_key_type: str = "String",
        ) -> DictFormatConfig:
            """Create a dict format config for the given type."""
            return self.value(
                default_type,
                default_key_type=default_key_type,
            )

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="Double.PositiveInfinity",
        negative_infinity="Double.NegativeInfinity",
        nan="Double.NaN",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = "decimal"

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = enum.auto()

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = "double"

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        NO = TrailingCommaConfig(multiline_trailing_comma=False)

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats

    class VariableTypeHints(enum.Enum):
        """Variable type hint options."""

        AUTO = enum.auto()

    variable_type_hints_formats = VariableTypeHints
    declaration_styles = DeclarationStyles
    dict_entry_styles = DictEntryStyles
    dict_formats = DictFormats
    empty_dict_keys = EmptyDictKey
    float_formats = FloatFormats
    integer_formats = IntegerFormats
    numeric_literal_suffixes = NumericLiteralSuffixes
    numeric_separators = NumericSeparators
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class LineEndings(enum.Enum):
        """Line ending options."""

        SEMICOLON = "semicolon"

    line_endings = LineEndings

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a VB.NET Dim declaration inside a Module."""
        del variable_name
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        indented = textwrap.indent(text=content, prefix="    ")
        return f"Module Check\n{indented}\nEnd Module"

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap VB.NET declaration + assignment in separate Subs."""
        declaration = prepend_body_preamble(
            content=declaration,
            body_preamble=body_preamble,
        )
        decl_indented = textwrap.indent(text=declaration, prefix="        ")
        assign_indented = textwrap.indent(text=assignment, prefix="        ")
        return (
            "Module Check\n"
            "    Sub _declaration()\n"
            f"{decl_indented}\n"
            "    End Sub\n"
            "    Sub _assignment()\n"
            f"        Dim {variable_name} As Object\n"
            f"{assign_indented}\n"
            "    End Sub\n"
            "End Module"
        )

    def __init__(  # noqa: PLR0915
        self,
        *,
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.HASH_SET,
        default_set_element_type: str = "Object",
        default_sequence_element_type: str = "Object",
        default_dict_key_type: str = "String",
        default_dict_value_type: str = "Object",
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.APOSTROPHE,
        declaration_style: DeclarationStyles = DeclarationStyles.DIM,
        dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT,
        dict_format: DictFormats = DictFormats.DEFAULT,
        float_format: FloatFormats = FloatFormats.REPR,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_literal_suffix: NumericLiteralSuffixes = (
            NumericLiteralSuffixes.NONE
        ),
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
    ) -> None:
        """Initialize VisualBasic language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "Nothing"
        self.true_literal = "True"
        self.false_literal = "False"
        element_to_type = make_element_to_type(
            str_type="String",
            bool_type="Boolean",
            int_type="Integer",
            float_type="Double",
            mixed_numeric_type="Double",
            bytes_type="String",
            date_type="String",
            datetime_type="String",
            list_template="{inner}()",
            dict_type_template=None,
            fallback_value_type=None,
        )
        vb_type_to_opener = make_type_to_opener(
            element_to_type=element_to_type,
            opener_template="New {type_name}() {{",
        )
        fmt = SequenceFormatConfig(
            sequence_open=typed_collection_open(
                type_to_opener=vb_type_to_opener,
                fallback=f"New {default_sequence_element_type}() {{",
            ),
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=f"New {default_sequence_element_type}() {{}}",
            preamble_lines=("Imports System.Collections.Generic",),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
        )
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format

        self.set_format_config: SetFormatConfig = set_format(
            default_type=default_set_element_type,
        )
        self.set_format_config = self.set_format_config.with_typed_opener(
            type_to_opener=make_type_to_opener(
                element_to_type=element_to_type,
                opener_template="New HashSet(Of {type_name}) From {{",
            ),
            fallback=self.set_format_config.set_open([]),
        )
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = dict_format(
            default_type=default_dict_value_type,
            default_key_type=default_dict_key_type,
        )
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _format_string_vb
        self.format_float: Callable[[float], str] = float_format
        self.format_integer: Callable[[int], str] = str
        self.format_sequence_entry: Callable[[Value, str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[Value, str], str] = (
            passthrough_set_entry
        )
        self.comment_format = comment_format
        self.declaration_style = declaration_style
        self.dict_entry_style = dict_entry_style
        self.dict_format = dict_format
        self.float_format = float_format
        self.integer_format = integer_format
        self.numeric_literal_suffix = numeric_literal_suffix
        self.numeric_separator = numeric_separator
        self.string_format = string_format
        self.trailing_comma = trailing_comma
        self.line_ending = line_ending
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            ordered_map_format_factory(
                open_template=(
                    "New Dictionary(Of {key_type}, {type}) From {{"
                ),
                close="}",
                preamble_lines=(),
            )(
                default_dict_value_type,
                default_key_type=default_dict_key_type,
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            braced_dict_entry(format_value=passthrough_sequence_entry)
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = False
        self.supports_scalar_before_comments = True
        self.supports_scalar_inline_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            declaration_style.value.formatter
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name} = {value}")
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )

        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.special_float_preamble: tuple[str, ...] = ()
