"""Fortran language specification."""

import datetime
import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_template,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_strings import format_string_concat_control
from literalizer._language import (
    CallStyleConfig,
    CallStyleKind,
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
    no_call_stub,
    no_type_hint_preamble,
)
from literalizer._types import Value

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


@beartype
def _format_fortran_entry(original: Value, formatted: str) -> str:
    """Wrap a formatted entry in the appropriate ``fval_t``
    constructor.
    """
    match original:
        case bool():
            return formatted
        case int():
            return f"fint({formatted})"
        case float():
            return f"freal({formatted})"
        case str() | bytes() | datetime.date():
            return f"fstr({formatted})"
        case _:
            return formatted


@beartype
def _fortran_comment_pos(line: str) -> int | None:
    """Return the index of the ``!`` comment character in *line* that
    lies outside any string literal, or ``None`` if there is no comment.
    """
    in_single_quote = False
    in_double_quote = False
    i = 0
    while i < len(line):
        c = line[i]
        if c == "'" and not in_double_quote:
            if in_single_quote and i + 1 < len(line) and line[i + 1] == "'":
                i += 2
                continue
            in_single_quote = not in_single_quote
        elif c == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
        elif c == "!" and not in_single_quote and not in_double_quote:
            return i
        i += 1
    return None


@beartype
def _add_continuation(value: str) -> str:
    """Add Fortran ``&`` line-continuation to non-comment, non-last
    lines.

    In Fortran free-form source a logical line may span multiple physical
    lines.  The ``&`` continuation character must be the last
    non-whitespace, non-comment character on the physical line.  Pure
    comment lines (blank or starting with ``!``) are transparent to the
    continuation mechanism and receive no ``&``.
    """
    lines = value.splitlines()
    if len(lines) <= 1:
        return value
    result: list[str] = []
    for i, line in enumerate(iterable=lines):
        is_last = i == len(lines) - 1
        stripped = line.strip()
        is_pure_comment = not stripped or stripped.startswith("!")
        if is_last or is_pure_comment:
            result.append(line)
        else:
            pos = _fortran_comment_pos(line=line)
            if pos is not None:
                result.append(line[:pos].rstrip() + " &  " + line[pos:])
            else:
                result.append(line + " &")
    return "\n".join(result)


@beartype
def _format_variable_declaration(name: str, value: str, data: Value) -> str:
    r"""Format a Fortran variable declaration and initialisation.

    Example: ``"x"`` and ``"flist([fval_t :: fint(1)])"`` →
    ``"type(fval_t) :: x\nx = flist([fval_t :: fint(1)])"``
    """
    fval = _format_fortran_entry(original=data, formatted=value)
    continued = _add_continuation(value=fval)
    return f"type(fval_t) :: {name}\n{name} = {continued}"


@beartype
def _format_variable_assignment(name: str, value: str, data: Value) -> str:
    """Format a Fortran assignment to an existing ``fval_t`` variable.

    Example: ``"x"`` and ``"flist([fval_t :: fint(1)])"`` →
    ``"x = flist([fval_t :: fint(1)])"``
    """
    fval = _format_fortran_entry(original=data, formatted=value)
    continued = _add_continuation(value=fval)
    return f"{name} = {continued}"


@beartype
class Fortran(metaclass=LanguageCls):
    """Fortran language specification."""

    extension = ".f90"
    pygments_name = "fortran"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True

    class DateFormats(enum.Enum):
        """Date format options for Fortran."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Fortran."""

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
        """Sequence type options for Fortran."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="flist([fval_t :: "),
            close="])",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Fortran."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="fset([fval_t :: "),
            close="])",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            coerce_mixed_to_str=False,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        EXCLAMATION = CommentConfig(
            prefix="!",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        TYPED = DeclarationStyleConfig(
            formatter=_format_variable_declaration,
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = enum.auto()

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="ieee_value(0.0, ieee_positive_inf)",
        negative_infinity="ieee_value(0.0, ieee_negative_inf)",
        nan="ieee_value(0.0, ieee_quiet_nan)",
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

    def __init__(  # noqa: PLR0915
        self,
        *,
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.EXCLAMATION,
        declaration_style: DeclarationStyles = DeclarationStyles.TYPED,
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
        """Initialize Fortran language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "fnull()"
        self.true_literal = "fbool(.true.)"
        self.false_literal = "fbool(.false.)"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            dict_open=fixed_dict_open(open_str="fmap([fval_t :: "),
            close="])",
            format_entry=dict_entry_with_template(
                template="fentry({key}, {value})",
                format_value=_format_fortran_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
        )
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = (
            format_string_concat_control(
                quote_char="'",
                quote_escape="''",
                control_char_template="achar({})",
                concat_operator=" // ",
                escape_backslash=False,
            )
        )
        self.format_float: Callable[[float], str] = float_format
        self.format_integer: Callable[[int], str] = str
        self.format_sequence_entry: Callable[[Value, str], str] = (
            _format_fortran_entry
        )
        self.format_set_entry: Callable[[Value, str], str] = (
            _format_fortran_entry
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
            OrderedMapFormatConfig(
                open_str="fmap([fval_t :: ",
                close="])",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            dict_entry_with_template(
                template="fentry({key}, {value})",
                format_value=_format_fortran_entry,
            )
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.supports_scalar_before_comments = False
        self.supports_scalar_inline_comments = False
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            declaration_style.value.formatter
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_variable_assignment
        )
        self.static_preamble: Sequence[str] = ("module fval_m",)
        self.static_body_preamble: Sequence[str] = (
            "  implicit none",
            "  type :: fval_t",
            "    integer :: t = 0",
            "  end type fval_t",
            "contains",
            "  function fnull() result(v); type(fval_t) :: v; end function",
            "  function fbool(b) result(v)"
            "; logical, intent(in) :: b"
            "; type(fval_t) :: v; end function",
            "  function fint(n) result(v)"
            "; integer, intent(in) :: n"
            "; type(fval_t) :: v; end function",
            "  function freal(x) result(v)"
            "; real, intent(in) :: x"
            "; type(fval_t) :: v; end function",
            "  function fstr(s) result(v)"
            "; character(len=*), intent(in) :: s"
            "; type(fval_t) :: v; end function",
            "  function flist(a) result(v)"
            "; type(fval_t), intent(in) :: a(:)"
            "; type(fval_t) :: v; end function",
            "  function fmap(a) result(v)"
            "; type(fval_t), intent(in) :: a(:)"
            "; type(fval_t) :: v; end function",
            "  function fset(a) result(v)"
            "; type(fval_t), intent(in) :: a(:)"
            "; type(fval_t) :: v; end function",
            "  function fentry(k, u) result(v)"
            "; character(len=*), intent(in) :: k"
            "; type(fval_t), intent(in) :: u"
            "; type(fval_t) :: v; end function",
            "end module fval_m",
        )
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
        )

        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.special_float_preamble: tuple[str, ...] = (
            "  use, intrinsic :: ieee_arithmetic",
        )
        self.call_style_config: CallStyleConfig = CallStyleConfig(
            kind=CallStyleKind.KEYWORD,
            keyword_separator="=",
        )
        self.format_call_stub = no_call_stub
        self.format_call_preamble_stub = no_call_stub
