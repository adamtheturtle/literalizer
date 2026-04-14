"""F# language specification."""

import dataclasses
import datetime
import enum
import textwrap
from collections.abc import Callable, Sequence

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._formatters.collection_openers import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    datetime_ymdhms_formatter,
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    tuple_dict_entry,
    variable_formatter,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
)
from literalizer._formatters.format_strings import format_string_backslash
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
    prepend_body_preamble,
)
from literalizer._types import Value


def _build_fsharp_entry_formatter(
    prefix: str,
) -> Callable[[Value, str], str]:
    """Build an entry formatter that wraps values in F# constructors."""

    @beartype
    def _format(original: Value, formatted: str) -> str:
        """Wrap a formatted entry in the appropriate F# ``Val``
        constructor.
        """
        match original:
            case bool():
                return formatted
            case int():
                negative = formatted.startswith("-")
                return (
                    f"{prefix}Int({formatted}L)"
                    if negative
                    else f"{prefix}Int {formatted}L"
                )
            case float():
                negative = formatted.startswith("-")
                return (
                    f"{prefix}Float({formatted})"
                    if negative
                    else f"{prefix}Float {formatted}"
                )
            case str() | bytes() | datetime.date():
                if formatted.startswith("System."):
                    return f"{prefix}Str (string ({formatted}))"
                return f"{prefix}Str {formatted}"
            case _:
                return formatted

    return _format


_format_fsharp_entry = _build_fsharp_entry_formatter(prefix="F")


@beartype
def _build_fsharp_declaration(
    *,
    template: str,
    sequence_declared_type: str,
    scalar_declared_type: str,
    entry_formatter: Callable[[Value, str], str],
) -> Callable[[str, str, Value], str]:
    """Build an F# variable declaration/assignment formatter."""

    @beartype
    def _format(name: str, value: str, data: Value) -> str:
        """Format a variable declaration or assignment."""
        decl_type = (
            sequence_declared_type
            if isinstance(data, list)
            else scalar_declared_type
        )
        wrapped = entry_formatter(data, value)
        return template.format(
            name=name,
            declared_type=decl_type,
            wrapped=wrapped,
        )

    return _format


def _fsharp_call_stub(name: str, params: Sequence[str], /) -> tuple[str, ...]:
    """Return F# stub declarations for a call name."""
    parts = name.split(sep=".")
    if len(parts) == 1:
        param_list = ", ".join(f"_{p}: obj" for p in params)
        return (f"let {parts[0]} ({param_list}) : obj = null",)
    root = parts[0]
    method = parts[-1]
    param_list = ", ".join(f"_{p}: obj" for p in params)
    fields = parts[1:-1]
    if not fields:
        cls = f"{root.title()}Type_"
        return (
            f"type {cls}() =",
            f"    member _.{method}({param_list}) : obj = null",
            f"let {root} = {cls}()",
        )
    lines: list[str] = []
    inner_cls = f"{fields[-1].title()}Type_"
    lines.append(f"type {inner_cls}() =")
    lines.append(f"    member _.{method}({param_list}) : obj = null")
    prev_cls = inner_cls
    for i in range(len(fields) - 2, -1, -1):
        cls = f"{fields[i].title()}Type_"
        lines.append(f"type {cls}() =")
        lines.append(f"    member _.{fields[i + 1]} = {prev_cls}()")
        prev_cls = cls
    root_cls = f"{root.title()}Type_"
    lines.append(f"type {root_cls}() =")
    lines.append(f"    member _.{fields[0]} = {prev_cls}()")
    lines.append(f"let {root} = {root_cls}()")
    return tuple(lines)


@beartype
class FSharp(metaclass=LanguageCls):
    """F# language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.FSHARP`` — ``System.DateOnly(...)`` call,
              e.g. ``System.DateOnly(2024, 1, 15)``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.FSHARP`` — ``System.DateTime(...)`` call,
              e.g. ``System.DateTime(2024, 1, 15, 12, 30, 0)``.

        type_name: Name of the generated custom type.  Defaults to
            ``"Val"``.

        constructor_prefix: Prefix for generated constructor names.
            Defaults to ``"F"``, producing constructors like ``FNull``,
            ``FBool``, ``FInt``, etc.
    """

    extension = ".fs"
    pygments_name = "fsharp"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True
    supports_variable_names = True
    supports_call = True

    class DateFormats(enum.Enum):
        """Date format options for FSharp."""

        FSHARP = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="System.DateOnly({year}, {month}, {day})",
            ),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for FSharp."""

        FSHARP = DatetimeFormatConfig(
            formatter=datetime_ymdhms_formatter(
                template="System.DateTime({year}, {month}, {day}, "
                "{hour}, {minute}, {second})",
            ),
        )
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
        """Sequence type options for F#."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="FList ["),
            close="]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type="Val",
        )
        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="[|"),
            close="|]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type="Val array",
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for F#."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="FSet ["),
            close="]",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            coerce_mixed_to_str=False,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_SLASH = CommentConfig(
            prefix="//",
            suffix="",
        )
        BLOCK = CommentConfig(
            prefix="(*",
            suffix=" *)",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        LET = DeclarationStyleConfig(
            formatter=variable_formatter(
                template="let {name} = {value}",
            ),
            supports_redefinition=False,
        )
        LET_MUTABLE = DeclarationStyleConfig(
            formatter=variable_formatter(
                template="let mutable {name} = {value}",
            ),
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
        positive_infinity="infinity",
        negative_infinity="-infinity",
        nan="nan",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=str)
        HEX = enum.member(value=format_integer_hex)
        OCTAL = enum.member(value=format_integer_octal)
        BINARY = enum.member(value=format_integer_binary)

        def __call__(self, value: int, /) -> str:
            """Format an integer."""
            formatter: Callable[[int], str] = self.value
            return formatter(value)

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
        """Wrap an F# let declaration in a module."""
        del variable_name
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        return "module Check\n\n" + content

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap F# declaration + assignment in separate private
        functions.
        """
        del variable_name
        decl_indented = textwrap.indent(text=declaration, prefix="    ")
        assign_indented = textwrap.indent(text=assignment, prefix="    ")
        preamble = "\n".join(body_preamble) + "\n" if body_preamble else ""
        body = "module Check\n\n" + preamble
        body += (
            "let private _checkDeclaration () =\n"
            + decl_indented
            + "\n    ignore my_data\n\n"
            + "let private _checkAssignment () =\n"
            + assign_indented
            + "\n    ignore my_data"
        )
        return body

    def __init__(  # noqa: PLR0915
        self,
        *,
        date_format: DateFormats = DateFormats.FSHARP,
        datetime_format: DatetimeFormats = DatetimeFormats.FSHARP,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        declaration_style: DeclarationStyles = DeclarationStyles.LET,
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
        type_name: str = "Val",
        constructor_prefix: str = "F",
    ) -> None:
        """Initialize FSharp language specification."""
        _entry_formatter = _build_fsharp_entry_formatter(
            prefix=constructor_prefix,
        )
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal: str = f"{constructor_prefix}Null"
        self.true_literal: str = f"{constructor_prefix}Bool true"
        self.false_literal: str = f"{constructor_prefix}Bool false"
        fmt = sequence_format.value
        if sequence_format.name == "ARRAY":
            self.sequence_format_config: SequenceFormatConfig = fmt
            self.sequence_open: Callable[[list[Value]], str] = (
                fmt.sequence_open
            )
        else:
            _seq_open = fixed_sequence_open(
                open_str=f"{constructor_prefix}List [",
            )
            self.sequence_format_config = dataclasses.replace(
                fmt,
                sequence_open=_seq_open,
            )
            self.sequence_open = _seq_open
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = dataclasses.replace(
            set_format.value,
            set_open=fixed_set_open(
                open_str=f"{constructor_prefix}Set [",
            ),
        )
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            dict_open=fixed_dict_open(
                open_str=f"{constructor_prefix}Map [",
            ),
            close="]",
            format_entry=tuple_dict_entry(
                format_value=_entry_formatter,
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
        self.format_string: Callable[[str], str] = format_string_backslash
        self.format_float: Callable[[float], str] = float_format
        self.format_integer: Callable[[int], str] = integer_format
        self.format_set_entry: Callable[[Value, str], str] = _entry_formatter
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
                open_str=f"{constructor_prefix}Map [",
                close="]",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            tuple_dict_entry(format_value=_entry_formatter)
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.supports_scalar_before_comments = False
        self.supports_scalar_inline_comments = False
        _raw_declared = sequence_format.value.declared_type
        _sequence_declared_type = (
            _raw_declared.replace("Val", type_name)
            if _raw_declared is not None
            else type_name
        )
        _keyword = (
            "let mutable"
            if declaration_style.value.supports_redefinition
            else "let"
        )
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _build_fsharp_declaration(
                template=(
                    f"{_keyword} {{name}}: {{declared_type}} = {{wrapped}}"
                ),
                sequence_declared_type=_sequence_declared_type,
                scalar_declared_type=type_name,
                entry_formatter=_entry_formatter,
            )
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _build_fsharp_declaration(
                template="let {name}: {declared_type} = {wrapped}",
                sequence_declared_type=_sequence_declared_type,
                scalar_declared_type=type_name,
                entry_formatter=_entry_formatter,
            )
        )
        self.element_separator = "; "
        self.format_sequence_entry: Callable[[Value, str], str] = (
            _entry_formatter
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        p = constructor_prefix
        _header = f"type {type_name} ="
        _f_str = f"    | {p}Str of string"
        self.scalar_body_preamble: dict[
            type,
            tuple[str, ...],
        ] = {
            type(None): (_header, f"    | {p}Null"),
            bool: (_header, f"    | {p}Bool of bool"),
            int: (_header, f"    | {p}Int of int64"),
            float: (_header, f"    | {p}Float of float"),
            str: (_header, _f_str),
            bytes: (_header, _f_str),
            list: (_header, f"    | {p}List of {type_name} list"),
            dict: (_header, f"    | {p}Map of (string * {type_name}) list"),
            ordereddict: (
                _header,
                f"    | {p}Map of (string * {type_name}) list",
            ),
            set: (_header, f"    | {p}Set of {type_name} list"),
            datetime.date: (
                _header,
                _f_str,
                f"    | {p}Date of System.DateTime",
            ),
            datetime.datetime: (
                _header,
                _f_str,
                f"    | {p}Datetime of System.DateTime",
            ),
        }
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )
        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.special_float_preamble: tuple[str, ...] = ()
        self.call_style_config: CallStyleConfig = CallStyleConfig(
            kind=CallStyleKind.POSITIONAL,
        )
        self.statement_terminator = ""
        self.format_call_stub = _fsharp_call_stub
        self.format_call_preamble_stub = no_call_stub
