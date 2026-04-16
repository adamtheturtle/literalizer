"""Standard ML language specification."""

import dataclasses
import datetime
import enum
import functools
from collections.abc import Callable
from types import MappingProxyType
from typing import TYPE_CHECKING

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
    format_integer_hex,
)
from literalizer._formatters.format_strings import (
    format_string_backslash_control,
)
from literalizer._language import (
    CallStyleConfig,
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
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    identity_call_target,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    prepend_body_preamble,
)
from literalizer._types import Value, ValueKind

if TYPE_CHECKING:
    from collections.abc import Sequence


def _sml_negate_int(
    formatter: Callable[[int], str],
) -> Callable[[int], str]:
    """Wrap an integer formatter to use SML's ``~`` for negation."""

    @beartype
    def _format(value: int) -> str:
        """Format an integer, replacing ``-`` with ``~``."""
        result = formatter(value)
        if result.startswith("-"):
            return "~" + result[1:]
        return result

    return _format


def _sml_negate_float(
    formatter: Callable[[float], str],
) -> Callable[[float], str]:
    """Wrap a float formatter to use SML's ``~`` for negation."""

    @beartype
    def _format(value: float) -> str:
        """Format a float, replacing ``-`` with ``~``."""
        result = formatter(value)
        if result.startswith("-"):
            return "~" + result[1:]
        return result

    return _format


@beartype
def _sml_scientific(value: float) -> str:
    """Format a float in SML scientific notation.

    SML uses ``E`` (not ``e``) and ``~`` for negative exponents.
    """
    result = format_float_scientific(value=value)
    if result.startswith("-"):
        result = "~" + result[1:]
    # Convert Python's 'e' to SML's 'E', with ~ for negative exponents.
    return result.replace("e-", "E~").replace("e", "E")


def _build_sml_entry_formatter(
    prefix: str,
) -> Callable[[Value, str], str]:
    """Build an entry formatter that wraps values in SML ``datatype``
    constructors using the given *prefix*.
    """

    @beartype
    def _format(original: Value, formatted: str) -> str:
        """Wrap a formatted entry in the appropriate SML ``datatype``
        constructor.
        """
        match original:
            case bool():
                return formatted
            case int():
                negative = formatted.startswith("~")
                return (
                    f"{prefix}Int ({formatted})"
                    if negative
                    else f"{prefix}Int {formatted}"
                )
            case float():
                negative = formatted.startswith(("~", "("))
                return (
                    f"{prefix}Real ({formatted})"
                    if negative
                    else f"{prefix}Real {formatted}"
                )
            case str() | bytes():
                return f"{prefix}Str {formatted}"
            case datetime.date() if formatted.startswith('"'):
                return f"{prefix}Str {formatted}"
            case _:
                return formatted

    return _format


@beartype
def _build_sml_declaration(
    *,
    sequence_declared_type: str,
    scalar_declared_type: str,
    entry_formatter: Callable[[Value, str], str],
) -> Callable[[str, str, Value, ValueKind], str]:
    """Build an SML variable declaration formatter."""

    @beartype
    def _format(name: str, value: str, data: Value, _kind: ValueKind) -> str:
        """Format a variable declaration."""
        decl_type = (
            sequence_declared_type
            if isinstance(data, list)
            else scalar_declared_type
        )
        wrapped = entry_formatter(data, value)
        return f"val {name} : {decl_type} = {wrapped}"

    return _format


def _format_sml_preamble_lines(lines: list[str]) -> tuple[str, ...]:
    """Format de-duplicated preamble lines with SML ``datatype`` syntax.

    The first constructor is indented; subsequent constructors are
    prefixed with ``|``.
    """
    return (
        lines[0],
        "    " + lines[1],
        *(f"  | {line}" for line in lines[2:]),
    )


@beartype
class Sml(metaclass=LanguageCls):
    """Standard ML language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.SML`` — tuple literal,
              e.g. ``(2024, 1, 15)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.SML`` — pair of tuples,
              e.g. ``((2024, 1, 15), (12, 30, 0))``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.

        type_name: Name of the generated custom type.  Defaults to
            ``"val_t"``.

        constructor_prefix: Prefix for generated constructor names.
            Defaults to ``"S"``, producing constructors like ``SNull``,
            ``SBool``, ``SInt``, etc.
    """

    extension = ".sml"
    pygments_name = "sml"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True
    supports_variable_names = True
    supports_dotted_calls = True

    class DateFormats(enum.Enum):
        """Date format options for Standard ML."""

        SML = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="SDate ({year}, {month}, {day})",
            ),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Standard ML."""

        SML = DatetimeFormatConfig(
            formatter=datetime_ymdhms_formatter(
                template="SDatetime (({year}, {month}, {day}), "
                "({hour}, {minute}, {second}))",
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
        """Sequence type options for Standard ML."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="SList ["),
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
            declared_type="val_t",
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Standard ML."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="SSet ["),
            close="]",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            coerce_mixed_to_str=False,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        PAREN_STAR = CommentConfig(
            prefix="(*",
            suffix=" *)",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        VAL = DeclarationStyleConfig(
            formatter=variable_formatter(
                template="val {name} = {value}",
            ),
            supports_redefinition=False,
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
        positive_infinity="(1.0 / 0.0)",
        negative_infinity="(~1.0 / 0.0)",
        nan="(0.0 / 0.0)",
    ):
        """Float format options."""

        REPR = enum.member(
            value=_sml_negate_float(formatter=format_float_repr),
        )
        SCIENTIFIC = enum.member(value=_sml_scientific)
        FIXED = enum.member(
            value=_sml_negate_float(formatter=format_float_fixed),
        )

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = MappingProxyType(
            mapping={
                "NONE": _sml_negate_int(formatter=str),
            }
        )
        HEX = MappingProxyType(
            mapping={
                "NONE": _sml_negate_int(formatter=format_integer_hex),
            }
        )

        def get_formatter(
            self,
            numeric_separator: enum.Enum,
        ) -> Callable[[int], str]:
            """Return the integer formatter for the given separator."""
            formatter: Callable[[int], str] = self.value[
                numeric_separator.name
            ]
            return formatter

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = enum.auto()

    class NumericStyles(enum.Enum):
        """Numeric literal style options."""

        OVERLOADED = enum.auto()

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
    numeric_styles = NumericStyles
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class LineEndings(enum.Enum):
        """Line ending options."""

        SEMICOLON = "semicolon"

    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """Sml call style options."""

    call_styles = CallStyles

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap an SML val declaration in a structure."""
        del variable_name
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        return "structure Check = struct\n\n" + content + "\n\nend"

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap SML declaration + assignment in a structure."""
        return Sml.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    def __init__(  # noqa: PLR0915
        self,
        *,
        date_format: DateFormats = DateFormats.SML,
        datetime_format: DatetimeFormats = DatetimeFormats.SML,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.PAREN_STAR,
        declaration_style: DeclarationStyles = DeclarationStyles.VAL,
        dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT,
        dict_format: DictFormats = DictFormats.DEFAULT,
        float_format: FloatFormats = FloatFormats.REPR,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_literal_suffix: NumericLiteralSuffixes = (
            NumericLiteralSuffixes.NONE
        ),
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        numeric_style: NumericStyles = NumericStyles.OVERLOADED,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
        type_name: str = "val_t",
        constructor_prefix: str = "S",
    ) -> None:
        """Initialize Standard ML language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal: str = f"{constructor_prefix}Null"
        self.true_literal: str = f"{constructor_prefix}Bool true"
        self.false_literal: str = f"{constructor_prefix}Bool false"
        _entry_formatter = _build_sml_entry_formatter(
            prefix=constructor_prefix,
        )
        fmt = sequence_format.value
        _seq_open = fixed_sequence_open(
            open_str=f"{constructor_prefix}List [",
        )
        self.sequence_format_config: SequenceFormatConfig = (
            dataclasses.replace(fmt, sequence_open=_seq_open)
        )
        self.sequence_open: Callable[[list[Value]], str] = _seq_open
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
        if date_format.name == "SML":
            self.format_date = date_ymd_formatter(
                template=(
                    f"{constructor_prefix}Date ({{year}}, {{month}}, {{day}})"
                ),
            )
        if datetime_format.name == "SML":
            self.format_datetime = datetime_ymdhms_formatter(
                template=(
                    f"{constructor_prefix}Datetime "
                    f"(({{year}}, {{month}}, {{day}}), "
                    f"({{hour}}, {{minute}}, {{second}}))"
                ),
            )
        self.format_string: Callable[[str], str] = functools.partial(
            format_string_backslash_control,
            control_char_fmt="\\{:03d}",
        )
        self.format_float: Callable[[float], str] = float_format
        self.format_integer: Callable[[int], str] = (
            integer_format.get_formatter(
                numeric_separator=numeric_separator,
            )
        )
        self.format_set_entry: Callable[[Value, str], str] = _entry_formatter
        self.comment_format = comment_format
        self.declaration_style = declaration_style
        self.dict_entry_style = dict_entry_style
        self.dict_format = dict_format
        self.float_format = float_format
        self.integer_format = integer_format
        self.numeric_literal_suffix = numeric_literal_suffix
        self.numeric_separator = numeric_separator
        self.numeric_style = numeric_style
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
        self.supports_scalar_before_comments = True
        self.supports_scalar_inline_comments = True
        _raw_declared = sequence_format.value.declared_type
        _sequence_declared_type = (
            _raw_declared.replace("val_t", type_name)
            if _raw_declared is not None
            else type_name
        )
        _sml_decl = _build_sml_declaration(
            sequence_declared_type=_sequence_declared_type,
            scalar_declared_type=type_name,
            entry_formatter=_entry_formatter,
        )
        self.format_variable_declaration: Callable[
            [str, str, Value, ValueKind], str
        ] = _sml_decl
        self.format_variable_assignment: Callable[
            [str, str, Value, ValueKind], str
        ] = _sml_decl
        self.element_separator = ", "
        self.format_sequence_entry: Callable[[Value, str], str] = (
            _entry_formatter
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.data_dependent_preamble = no_data_preamble
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        p = constructor_prefix
        _h = f"datatype {type_name} ="
        _date_constructor = (
            f"{p}Str of string"
            if date_format.value.type_produced is str
            else f"{p}Date of (int * int * int)"
        )
        _datetime_constructor = (
            f"{p}Str of string"
            if datetime_format.value.type_produced is str
            else f"{p}Datetime of ((int * int * int) * (int * int * int))"
        )
        self.scalar_body_preamble: dict[
            type,
            tuple[str, ...],
        ] = {
            type(None): (_h, f"{p}Null"),
            bool: (_h, f"{p}Bool of bool"),
            int: (_h, f"{p}Int of int"),
            float: (_h, f"{p}Real of real"),
            str: (_h, f"{p}Str of string"),
            bytes: (_h, f"{p}Str of string"),
            datetime.date: (_h, _date_constructor),
            datetime.datetime: (_h, _datetime_constructor),
            list: (_h, f"{p}List of {type_name} list"),
            dict: (_h, f"{p}Map of (string * {type_name}) list"),
            ordereddict: (_h, f"{p}Map of (string * {type_name}) list"),
            set: (_h, f"{p}Set of {type_name} list"),
        }
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=_format_sml_preamble_lines,
        )
        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.special_float_preamble: tuple[str, ...] = ()
        self.call_style_config: CallStyleConfig | None = None
        self.statement_terminator = ""
        self.format_call_stub: Callable[
            [str, Sequence[str], StubReturn], tuple[str, ...]
        ] = no_call_stub
        self.format_call_preamble_stub: Callable[
            [str, Sequence[str], StubReturn], tuple[str, ...]
        ] = no_call_stub
        self.format_call_target: Callable[[str], str] = identity_call_target
