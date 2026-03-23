"""Fortran language specification."""

import datetime
import enum
import re
from collections.abc import Callable, Sequence

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    passthrough_sequence_entry,
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


@beartype
def _format_string_fortran(value: str) -> str:
    r"""Format a string using Fortran single-quote string syntax.

    Fortran strings use single quotes, with ``''`` for embedded single
    quotes.  Control characters (code points 0-31) are emitted as
    ``achar(N)`` expressions concatenated with ``//``.
    """
    _fortran_control_char_threshold = 32
    parts: list[str] = []
    for segment in re.split(pattern=r"([\x00-\x1f])", string=value):
        if not segment:
            continue
        if (
            len(segment) == 1
            and ord(segment) < _fortran_control_char_threshold
        ):
            parts.append(f"achar({ord(segment)})")
        else:
            escaped = segment.replace("'", "''")
            parts.append(f"'{escaped}'")
    if not parts:
        return "''"
    if len(parts) == 1:
        return parts[0]
    return " // ".join(parts)


_FVAL_PREFIXES = (
    "fnull()",
    "fbool(",
    "fint(",
    "freal(",
    "fstr(",
    "flist(",
    "fmap(",
    "fset(",
    "fentry(",
)


@beartype
def _to_fval(value: str) -> str:
    """Convert a pre-formatted value string to an ``fval_t`` constructor.

    Inspects the string representation to determine the appropriate
    constructor: ``fstr``, ``fint``, ``freal``, or passes through values
    that are already ``fval_t`` expressions (``fnull``, ``fbool``,
    ``flist``, ``fmap``, ``fset``, ``fentry``).
    """
    if any(value.startswith(p) for p in _FVAL_PREFIXES):
        return value
    if (value.startswith("'") and value.endswith("'")) or (
        value.startswith('"') and value.endswith('"')
    ):
        return f"fstr({value})"
    if "achar(" in value:
        return f"fstr({value})"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"fint({value})"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float(rest)
    return f"freal({value})"


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
def _format_fortran_dict_entry(key: str, value: str) -> str:
    """Format a Fortran dict entry as an ``fentry(key, fval_t value)``
    call.
    """
    return f"fentry({key}, {_to_fval(value=value)})"


@beartype
def _format_variable_declaration(name: str, value: str, _data: Value) -> str:
    r"""Format a Fortran variable declaration and initialisation.

    Example: ``"x"`` and ``"flist([fval_t :: fint(1)])"`` →
    ``"type(fval_t) :: x\nx = flist([fval_t :: fint(1)])"``
    """
    fval = _to_fval(value=value)
    continued = _add_continuation(value=fval)
    return f"type(fval_t) :: {name}\n{name} = {continued}"


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format a Fortran assignment to an existing ``fval_t`` variable.

    Example: ``"x"`` and ``"flist([fval_t :: fint(1)])"`` →
    ``"x = flist([fval_t :: fint(1)])"``
    """
    fval = _to_fval(value=value)
    continued = _add_continuation(value=fval)
    return f"{name} = {continued}"


_string_format: Callable[[str], str] = _format_string_fortran


_FORTRAN_PREAMBLE: tuple[str, ...] = (
    "module fval_m",
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


@beartype
class Fortran(metaclass=LanguageCls):
    """Fortran language specification."""

    extension = ".f90"
    pygments_name = "fortran"

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
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
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
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        EXCLAMATION = CommentConfig(
            prefix="!",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        TYPED = "typed"

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
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.EXCLAMATION,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.TYPED,
        dict_format: DictFormats = DictFormats.DEFAULT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
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
            open_fn=fixed_dict_open(open_str="fmap([fval_t :: "),
            close="])",
            format_entry=_format_fortran_dict_entry,
            empty_dict=None,
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
        self.format_sequence_entry: Callable[[str], str] = _to_fval
        self.format_set_entry: Callable[[str], str] = _to_fval
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
                open_str="fmap([fval_t :: ",
                close="])",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_fortran_dict_entry
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
        self.static_preamble: Sequence[str] = _FORTRAN_PREAMBLE
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
