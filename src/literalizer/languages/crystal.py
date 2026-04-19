"""Crystal language specification."""

import datetime
import enum
from collections.abc import Callable, Sequence
from types import MappingProxyType
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_dict_open,
    fixed_sequence_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_separator,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    variable_formatter,
)
from literalizer._formatters.format_factories import (
    dict_format_factory,
    set_format_factory,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import format_integer_underscore
from literalizer._formatters.format_strings import format_string_backslash_hash
from literalizer._language import (
    CallStyle,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    KeywordCallStyle,
    LanguageCls,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    wrap_combined_in_file_noop,
    wrap_in_file_noop,
)

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
def _crystal_call_stub(
    name: str, _params: Sequence[str], _stub_return: StubReturn, /
) -> tuple[str, ...]:
    """Return Crystal stub declarations for a call name."""
    parts = name.split(sep=".")
    if len(parts) == 1:
        return (f"def {parts[0]}(*a, **kw); 0; end",)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        cls = root.capitalize() + "Type_"
        return (
            f"class {cls}; def {method}(*a, **kw); 0; end; end",
            f"{root} = {cls}.new",
        )
    lines: list[str] = []
    inner_cls = fields[-1].capitalize() + "Type_"
    lines.append(f"class {inner_cls}; def {method}(*a, **kw); 0; end; end")
    prev_cls = inner_cls
    for i in range(len(fields) - 2, -1, -1):
        cls = fields[i].capitalize() + "Type_"
        lines.append(
            f"class {cls}; def {fields[i + 1]}; {prev_cls}.new; end; end"
        )
        prev_cls = cls
    root_cls = root.capitalize() + "Type_"
    lines.append(
        f"class {root_cls}; def {fields[0]}; {prev_cls}.new; end; end"
    )
    lines.append(f"{root} = {root_cls}.new")
    return tuple(lines)


@beartype
class Crystal(metaclass=LanguageCls):
    """Crystal language specification.

    Args:
        sequence_format: Which Crystal sequence type to use.

            * ``sequence_formats.ARRAY`` — array literal,
              e.g. ``[1, 2, 3]``.
            * ``sequence_formats.TUPLE`` — tuple literal,
              e.g. ``{1, 2, 3}``.
    """

    extension = ".cr"
    pygments_name = "crystal"
    supports_default_set_element_type = True
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = True
    supports_default_dict_key_type = True
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True
    supports_variable_names = True
    supports_dotted_calls = True

    class DateFormats(enum.Enum):
        """Date format options for Crystal."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Crystal."""

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
        """Sequence type options for Crystal."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="["),
            close="]",
            empty_sequence="[] of Nil",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
        )
        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="{"),
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Crystal."""

        SET = enum.member(
            value=set_format_factory(
                open_template="Set{{",
                close="}}",
                empty_template="Set({type}).new",
                preamble_lines=('require "set"',),
                set_opener_template="",
                coerce_mixed_to_str=False,
            )
        )

        def __call__(self, default_type: str) -> SetFormatConfig:
            """Create a set format config for the given type."""
            return self.value(default_type)

    class CommentFormats(enum.Enum):
        """Comment style options."""

        HASH = CommentConfig(
            prefix="#",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        ASSIGN = DeclarationStyleConfig(
            formatter=variable_formatter(template="{name} = {value}"),
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = enum.member(
            value=dict_format_factory(
                open_template="{{",
                close="}",
                format_entry=dict_entry_with_separator(
                    separator=" => ",
                    format_value=passthrough_sequence_entry,
                ),
                empty_template="{{}} of {key_type} => {type}",
                preamble_lines=(),
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
        positive_infinity="Float64::INFINITY",
        negative_infinity="-Float64::INFINITY",
        nan="Float64::NAN",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = MappingProxyType(
            mapping={
                "NONE": lambda value: str(object=value),
                "UNDERSCORE": format_integer_underscore,
            }
        )

        def get_formatter(
            self,
            numeric_separator: enum.Enum,
        ) -> Callable[[int], str]:
            """Return the integer formatter for the given separator."""
            return self.value[numeric_separator.name]

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = enum.auto()
        UNDERSCORE = enum.auto()

    class NumericStyles(enum.Enum):
        """Numeric literal style options."""

        OVERLOADED = enum.auto()

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = "double"

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        YES = TrailingCommaConfig(multiline_trailing_comma=True)
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
        """Crystal call style options."""

        KEYWORD = KeywordCallStyle(separator=": ")
        POSITIONAL = PositionalCallStyle()

    call_styles = CallStyles

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap code in a valid file (no-op)."""
        return wrap_in_file_noop(
            content=content,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap declaration and assignment in a valid file (no-op)."""
        return wrap_combined_in_file_noop(
            declaration=declaration,
            assignment=assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    def __init__(  # noqa: PLR0915
        self,
        *,
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.SET,
        default_set_element_type: str = "String",
        default_dict_key_type: str = "String",
        default_dict_value_type: str = "String",
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.HASH,
        declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN,
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
        trailing_comma: TrailingCommas = TrailingCommas.YES,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        call_style: CallStyles = CallStyles.KEYWORD,
        indent: str = "    ",
    ) -> None:
        """Initialize Crystal language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "nil"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format

        self.set_format_config: SetFormatConfig = set_format(
            default_type=default_set_element_type,
        )
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = dict_format(
            default_type=default_dict_value_type,
            default_key_type=default_dict_key_type,
        )
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.date_format: enum.Enum = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.datetime_format: enum.Enum = datetime_format
        self.format_string: Callable[[str], str] = format_string_backslash_hash
        self.format_float: Callable[[float], str] = float_format
        self.format_integer: Callable[[int], str] = (
            integer_format.get_formatter(
                numeric_separator=numeric_separator,
            )
        )
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
        self.numeric_style = numeric_style
        self.string_format = string_format
        self.trailing_comma = trailing_comma
        self.line_ending = line_ending
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                ordered_map_open=fixed_dict_open(open_str="{"),
                close="}",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            dict_entry_with_separator(
                separator=" => ",
                format_value=passthrough_sequence_entry,
            )
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
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
        self.data_dependent_preamble = no_data_preamble
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
        self.call_style = call_style
        self.call_style_config: CallStyle | None = call_style.value
        self.statement_terminator = ";"
        self.format_call_stub: Callable[
            [str, Sequence[str], StubReturn], tuple[str, ...]
        ] = _crystal_call_stub
        self.format_call_preamble_stub: Callable[
            [str, Sequence[str], StubReturn], tuple[str, ...]
        ] = no_call_stub
