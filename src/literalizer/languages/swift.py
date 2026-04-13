"""Swift language specification."""

import datetime
import enum
import functools
from collections.abc import Callable, Sequence
from types import MappingProxyType
from typing import assert_never

from beartype import beartype

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
    sequence_format_factory,
    set_format_factory,
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
    format_integer_underscore,
)
from literalizer._formatters.format_strings import (
    format_string_backslash_control,
)
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
    date_scalar_preamble,
    no_call_stub,
    no_type_hint_preamble,
    wrap_combined_in_file_noop,
    wrap_in_file_noop,
)
from literalizer._types import Value


@beartype
def _format_date_swift(value: datetime.date) -> str:
    """Format a date as a Swift ``DateComponents`` expression."""
    return (
        "DateComponents("
        "calendar: Calendar(identifier: .gregorian), "
        f"year: {value.year}, month: {value.month}, day: {value.day}"
        ").date!"
    )


@beartype
def _format_datetime_swift(value: datetime.datetime) -> str:
    """Format a datetime as a Swift ``DateComponents`` expression."""
    parts = (
        "DateComponents("
        "calendar: Calendar(identifier: .gregorian), "
        f"year: {value.year}, month: {value.month}, day: {value.day}, "
        f"hour: {value.hour}, minute: {value.minute}, second: {value.second}"
    )
    if value.microsecond:
        nanosecond = value.microsecond * 1000
        parts += f", nanosecond: {nanosecond}"
    return parts + ").date!"


@beartype
def _tuple_sequence_entry(original: Value, entry: str) -> str:
    """Format a tuple sequence entry, casting nil to Any? for Swift."""
    if original is None:
        return "nil as Any?"
    return entry


def _swift_call_stub(name: str, params: Sequence[str], /) -> tuple[str, ...]:
    """Return Swift stub declarations for a call name."""
    param_list = ", ".join(f"{p}: Any = 0" for p in params)
    parts = name.split(sep=".")
    if len(parts) == 1:
        return (f"func {parts[0]}({param_list}) -> Any {{ 0 }}",)
    root, method = parts[0], parts[1]
    cls = f"_{root}Type"
    return (
        f"class {cls} {{ func {method}({param_list}) -> Any {{ 0 }} }}",
        f"let {root} = {cls}()",
    )


@beartype
def _swift_type_hint(  # pylint: disable=too-complex,too-many-branches  # noqa: C901, PLR0911, PLR0912
    data: Value,
    *,
    date_hint: str,
    datetime_hint: str,
    default_set_element_type: str,
    default_sequence_element_type: str,
    default_dict_value_type: str,
    sequence_is_tuple: bool,
) -> str:
    """Derive a Swift type annotation from *data*."""
    recurse = functools.partial(
        _swift_type_hint,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        default_set_element_type=default_set_element_type,
        default_sequence_element_type=default_sequence_element_type,
        default_dict_value_type=default_dict_value_type,
        sequence_is_tuple=sequence_is_tuple,
    )
    match data:
        case bool():
            return "Bool"
        case int():
            return "Int"
        case float():
            return "Double"
        case str():
            return "String"
        case bytes():
            return "String"
        case datetime.datetime():
            return datetime_hint
        case datetime.date():
            return date_hint
        case None:
            return "Any?"
        case dict():
            if not data:
                return f"[String: {default_dict_value_type}]"
            val_types = [recurse(data=v) for v in data.values()]
            unique = list(dict.fromkeys(val_types))
            has_nil = "Any?" in unique
            val_type = (
                unique[0]
                if len(unique) == 1
                else ("Any?" if has_nil else "Any")
            )
            return f"[String: {val_type}]"
        case set():
            return f"Set<{default_set_element_type}>"
        case list():
            if not data:
                if sequence_is_tuple:
                    return "()"
                return f"[{default_sequence_element_type}]"
            if sequence_is_tuple:
                elem_types = [recurse(data=e) for e in data]
                return f"({', '.join(elem_types)})"
            elem_types = [recurse(data=e) for e in data]
            unique = list(dict.fromkeys(elem_types))
            has_nil = "Any?" in unique
            elem_type = (
                unique[0]
                if len(unique) == 1
                else ("Any?" if has_nil else "Any")
            )
            return f"[{elem_type}]"
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _format_swift_typed_declaration(
    name: str,
    value: str,
    data: Value,
    *,
    keyword: str,
    date_hint: str,
    datetime_hint: str,
    default_set_element_type: str,
    default_sequence_element_type: str,
    default_dict_value_type: str,
    sequence_is_tuple: bool,
) -> str:
    """Format a Swift variable declaration with a specific type."""
    hint = _swift_type_hint(
        data=data,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        default_set_element_type=default_set_element_type,
        default_sequence_element_type=default_sequence_element_type,
        default_dict_value_type=default_dict_value_type,
        sequence_is_tuple=sequence_is_tuple,
    )
    return f"{keyword} {name}: {hint} = {value}"


@beartype
class Swift(metaclass=LanguageCls):
    """Swift language specification."""

    extension = ".swift"
    pygments_name = "swift"
    supports_default_set_element_type = True
    supports_default_sequence_element_type = True
    supports_default_dict_value_type = True
    supports_default_dict_key_type = True
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True
    supports_variable_names = True
    supports_call = True

    class DateFormats(enum.Enum):
        """Date format options for Swift."""

        SWIFT = DateFormatConfig(
            formatter=_format_date_swift,
            preamble_lines=("import Foundation",),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Swift."""

        SWIFT = DatetimeFormatConfig(
            formatter=_format_datetime_swift,
            preamble_lines=("import Foundation",),
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
        """Sequence type options for Swift."""

        ARRAY = enum.member(
            value=sequence_format_factory(
                open_template="[",
                close="]",
                supports_heterogeneity=True,
                single_element_trailing_comma=False,
                supports_trailing_comma=True,
                empty_template="[{type}]()",
                preamble_lines=(),
                format_entry=passthrough_sequence_entry,
                typed_opener_fallback_template=None,
            )
        )
        TUPLE = enum.member(
            value=sequence_format_factory(
                open_template="(",
                close=")",
                supports_heterogeneity=True,
                single_element_trailing_comma=False,
                supports_trailing_comma=True,
                empty_template=None,
                preamble_lines=(),
                format_entry=_tuple_sequence_entry,
                typed_opener_fallback_template=None,
            )
        )

        def __call__(self, default_type: str) -> SequenceFormatConfig:
            """Create a sequence format config for the given type."""
            return self.value(default_type)

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self(default_type="Any").supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Swift."""

        SET = enum.member(
            value=set_format_factory(
                open_template="Set<{type}>([",
                close="])",
                empty_template="Set<{type}>()",
                preamble_lines=(),
                set_opener_template="",
                coerce_mixed_to_str=False,
            )
        )

        def __call__(self, default_type: str) -> SetFormatConfig:
            """Create a set format config for the given type."""
            return self.value(default_type)

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_SLASH = CommentConfig(
            prefix="//",
            suffix="",
        )
        BLOCK = CommentConfig(
            prefix="/*",
            suffix=" */",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        LET = DeclarationStyleConfig(
            formatter=variable_formatter(template="let {name}: Any = {value}"),
            supports_redefinition=False,
        )
        VAR = DeclarationStyleConfig(
            formatter=variable_formatter(template="var {name}: Any = {value}"),
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = enum.member(
            value=dict_format_factory(
                open_template="[",
                close="]",
                format_entry=dict_entry_with_separator(
                    separator=": ",
                    format_value=passthrough_sequence_entry,
                ),
                empty_template="[{key_type}: {type}]()",
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
        positive_infinity="Double.infinity",
        negative_infinity="-Double.infinity",
        nan="Double.nan",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = MappingProxyType(
            mapping={
                "NONE": str,
                "UNDERSCORE": format_integer_underscore,
            }
        )
        HEX = MappingProxyType(
            mapping={
                "NONE": format_integer_hex,
                "UNDERSCORE": format_integer_hex,
            }
        )
        OCTAL = MappingProxyType(
            mapping={
                "NONE": format_integer_octal,
                "UNDERSCORE": format_integer_octal,
            }
        )
        BINARY = MappingProxyType(
            mapping={
                "NONE": format_integer_binary,
                "UNDERSCORE": format_integer_binary,
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
        UNDERSCORE = enum.auto()

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
        ALWAYS = enum.auto()

        def formatter(
            self,
            *,
            auto_formatter: Callable[[str, str, Value], str],
            keyword: str,
            date_hint: str,
            datetime_hint: str,
            default_set_element_type: str,
            default_sequence_element_type: str,
            default_dict_value_type: str,
            sequence_is_tuple: bool,
        ) -> Callable[[str, str, Value], str]:
            """Return the variable declaration formatter."""
            if self is type(self).AUTO:
                return auto_formatter
            return functools.partial(
                _format_swift_typed_declaration,
                keyword=keyword,
                date_hint=date_hint,
                datetime_hint=datetime_hint,
                default_set_element_type=default_set_element_type,
                default_sequence_element_type=(default_sequence_element_type),
                default_dict_value_type=default_dict_value_type,
                sequence_is_tuple=sequence_is_tuple,
            )

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
        date_format: DateFormats = DateFormats.SWIFT,
        datetime_format: DatetimeFormats = DatetimeFormats.SWIFT,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.SET,
        default_set_element_type: str = "AnyHashable",
        default_sequence_element_type: str = "Any",
        default_dict_key_type: str = "String",
        default_dict_value_type: str = "Any",
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
        trailing_comma: TrailingCommas = TrailingCommas.YES,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
    ) -> None:
        """Initialize Swift language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "nil"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format(default_type=default_sequence_element_type)
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.default_set_element_type = default_set_element_type
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
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = functools.partial(
            format_string_backslash_control,
            control_char_fmt="\\u{{{:x}}}",
        )
        self.format_float: Callable[[float], str] = float_format
        self.format_integer: Callable[[int], str] = (
            integer_format.get_formatter(
                numeric_separator=numeric_separator,
            )
        )
        self.format_sequence_entry: Callable[[Value, str], str] = (
            fmt.format_entry
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
            OrderedMapFormatConfig(
                open_str="[",
                close="]",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            )
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.supports_scalar_before_comments = False
        self.supports_scalar_inline_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            variable_type_hints.formatter(
                auto_formatter=declaration_style.value.formatter,
                keyword=declaration_style.name.lower(),
                date_hint=(
                    "String"
                    if date_format.value.type_produced is str
                    else "Date"
                ),
                datetime_hint=(
                    "String"
                    if datetime_format.value.type_produced is str
                    else "Date"
                ),
                default_set_element_type=default_set_element_type,
                default_sequence_element_type=(default_sequence_element_type),
                default_dict_value_type=default_dict_value_type,
                sequence_is_tuple=(sequence_format.name == "TUPLE"),
            )
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name} = {value}")
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = (
            date_scalar_preamble(
                date_format=date_format,
                datetime_format=datetime_format,
            )
        )
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )

        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.special_float_preamble: tuple[str, ...] = ()
        self.call_style_config: CallStyleConfig = CallStyleConfig(
            kind=CallStyleKind.KEYWORD,
            keyword_separator=": ",
        )
        self.statement_terminator = ";"
        self.format_call_stub = _swift_call_stub
        self.format_call_preamble_stub = no_call_stub
