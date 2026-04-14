"""TypeScript language specification."""

import datetime
import enum
import functools
from collections import OrderedDict
from collections.abc import Callable, Sequence
from types import MappingProxyType
from typing import assert_never

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._formatters.collection_openers import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
)
from literalizer._formatters.format_dates import (
    date_iso_formatter,
    datetime_iso_formatter,
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_separator,
    dict_entry_with_template,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
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
    format_integer_underscore,
)
from literalizer._formatters.format_strings import (
    format_string_backslash,
    format_string_backslash_single,
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
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    no_call_stub,
    no_type_hint_preamble,
    prepend_body_preamble,
)
from literalizer._types import Value


def _ts_call_stub(
    name: str,
    _params: Sequence[str],
    _stub_return: StubReturn,
    /,
) -> tuple[str, ...]:
    """Return TypeScript stub declarations for a call name."""
    root = name.split(sep=".", maxsplit=1)[0]
    return (f"declare const {root}: any;",)


@beartype
def _ts_element_union(*, types: list[str]) -> str:
    """Remove duplicate types and join into a TypeScript union."""
    unique: list[str] = list(dict.fromkeys(types))
    if len(unique) == 1:
        return unique[0]
    return " | ".join(unique)


@beartype
def _ts_type_hint(  # pylint: disable=too-complex,too-many-branches  # noqa: C901, PLR0911, PLR0912
    data: Value,
    *,
    date_hint: str,
    datetime_hint: str,
    dict_hint_template: str,
    sequence_is_tuple: bool,
) -> str:
    """Derive a TypeScript type annotation from *data*."""
    recurse = functools.partial(
        _ts_type_hint,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        dict_hint_template=dict_hint_template,
        sequence_is_tuple=sequence_is_tuple,
    )
    match data:
        case bool():
            return "boolean"
        case int():
            return "number"
        case float():
            return "number"
        case str():
            return "string"
        case bytes():
            return "string"
        case datetime.datetime():
            return datetime_hint
        case datetime.date():
            return date_hint
        case None:
            return "null"
        case dict():
            template = (
                "Record<string, {val}>"
                if isinstance(data, (ordereddict, OrderedDict))
                else dict_hint_template
            )
            # The MAP opener always uses ``unknown`` as the value
            # type, so the annotation must match.
            if not data or "Map<" in template:
                return template.format(val="unknown")
            val_types = [recurse(data=v) for v in data.values()]  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType,reportUnknownVariableType]
            val_union = _ts_element_union(types=val_types)
            return template.format(val=val_union)
        case set():
            if not data:
                return "Set<unknown>"
            elem_types = sorted(recurse(data=e) for e in data)
            elem_union = _ts_element_union(types=elem_types)
            return f"Set<{elem_union}>"
        case list():
            if not data:
                return "readonly []" if sequence_is_tuple else "unknown[]"
            if sequence_is_tuple:
                elem_types = [recurse(data=e) for e in data]
                return f"readonly [{', '.join(elem_types)}]"
            elem_types = [recurse(data=e) for e in data]
            elem_union = _ts_element_union(types=elem_types)
            if " | " in elem_union:
                return f"({elem_union})[]"
            return f"{elem_union}[]"
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _format_ts_typed_declaration(
    name: str,
    value: str,
    data: Value,
    *,
    keyword: str,
    date_hint: str,
    datetime_hint: str,
    dict_hint_template: str,
    sequence_is_tuple: bool,
) -> str:
    """Format a TypeScript variable declaration with an explicit type."""
    hint = _ts_type_hint(
        data=data,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        dict_hint_template=dict_hint_template,
        sequence_is_tuple=sequence_is_tuple,
    )
    return f"{keyword} {name}: {hint} = {value};"


@beartype
class TypeScript(metaclass=LanguageCls):
    """TypeScript language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.JS`` — ``new Date(...)`` call,
              e.g. ``new Date("2024-01-15")``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.JS`` — ``new Date(...)`` call,
              e.g. ``new Date("2024-01-15T12:30:00")``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.

        sequence_format: Which TypeScript sequence type to use.

            * ``sequence_formats.ARRAY`` — array literal,
              e.g. ``[1, 2, 3]``.
            * ``sequence_formats.TUPLE`` — ``as const`` tuple literal,
              e.g. ``[1, 2, 3] as const``.  TypeScript infers
              per-element types instead of a union array type.
    """

    extension = ".ts"
    pygments_name = "typescript"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True
    supports_variable_names = True
    supports_dotted_calls = True

    class DateFormats(enum.Enum):
        """Date formatting options for TypeScript."""

        JS = DateFormatConfig(
            formatter=date_iso_formatter(template='new Date("{iso}")'),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime formatting options for TypeScript."""

        JS = DatetimeFormatConfig(
            formatter=datetime_iso_formatter(
                template='new Date("{iso}")',
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
        """Sequence type options for TypeScript."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="["),
            close="]",
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
        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="["),
            close="] as const",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence="[] as const",
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
        """Set type options for TypeScript."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="new Set(["),
            close="])",
            empty_set="new Set()",
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
            prefix="/*",
            suffix=" */",
        )

    class LineEndings(enum.Enum):
        """Line ending options."""

        SEMICOLON = "semicolon"
        NONE = "none"

        def wrap_formatter(
            self,
            formatter: Callable[[str, str, Value], str],
        ) -> Callable[[str, str, Value], str]:
            """Wrap a formatter to match this line ending style."""
            if self.value != "none":
                return formatter

            def without_semicolon(name: str, value: str, data: Value) -> str:
                """Format without a trailing semicolon."""
                return formatter(name, value, data).removesuffix(";")

            return without_semicolon

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        CONST = DeclarationStyleConfig(
            formatter=variable_formatter(template="const {name} = {value};"),
            supports_redefinition=False,
        )
        LET = DeclarationStyleConfig(
            formatter=variable_formatter(template="let {name} = {value};"),
            supports_redefinition=True,
        )
        VAR = DeclarationStyleConfig(
            formatter=variable_formatter(template="var {name} = {value};"),
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        OBJECT = DictFormatConfig(
            dict_open=fixed_dict_open(open_str="{"),
            close="}",
            format_entry=dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
        )
        MAP = DictFormatConfig(
            dict_open=fixed_dict_open(open_str="new Map<string, unknown>(["),
            close="])",
            format_entry=dict_entry_with_template(
                template="[{key}, {value}]",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict="new Map()",
            preamble_lines=(),
            narrowed_open=None,
        )

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="Infinity",
        negative_infinity="-Infinity",
        nan="NaN",
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

    class NumericStyles(enum.Enum):
        """Numeric literal style options."""

        OVERLOADED = enum.auto()

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.member(value=format_string_backslash)
        SINGLE = enum.member(value=format_string_backslash_single)

        def __call__(self, value: str, /) -> str:
            """Format a string."""
            return self.value(value=value)

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
            dict_hint_template: str,
            sequence_is_tuple: bool,
        ) -> Callable[[str, str, Value], str]:
            """Return the variable declaration formatter."""
            if self is type(self).AUTO:
                return auto_formatter
            return functools.partial(
                _format_ts_typed_declaration,
                keyword=keyword,
                date_hint=date_hint,
                datetime_hint=datetime_hint,
                dict_hint_template=dict_hint_template,
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
    numeric_styles = NumericStyles
    string_formats = StringFormats
    trailing_commas = TrailingCommas
    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """TypeScript call style options."""

        OBJECT = CallStyleConfig(
            kind=CallStyleKind.OBJECT,
            keyword_separator=": ",
        )
        POSITIONAL = CallStyleConfig(kind=CallStyleKind.POSITIONAL)

    call_styles = CallStyles

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a TypeScript declaration as a module."""
        del variable_name
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        return f"{content}\nexport {{}};"

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap TypeScript declaration + assignment as a module."""
        return TypeScript.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    def __init__(  # noqa: PLR0915
        self,
        *,
        date_format: DateFormats = DateFormats.JS,
        datetime_format: DatetimeFormats = DatetimeFormats.JS,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        declaration_style: DeclarationStyles = DeclarationStyles.CONST,
        dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT,
        dict_format: DictFormats = DictFormats.OBJECT,
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
        call_style: CallStyles = CallStyles.OBJECT,
        indent: str = "    ",
    ) -> None:
        """Initialize TypeScript language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = dict_format.value
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )

        self.format_string: Callable[[str], str] = string_format
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
                open_str="{",
                close="}",
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
        self.supports_scalar_before_comments = True
        self.supports_scalar_inline_comments = True
        _base_decl = variable_type_hints.formatter(
            auto_formatter=declaration_style.value.formatter,
            keyword=declaration_style.name.lower(),
            date_hint=(
                "string" if date_format.value.type_produced is str else "Date"
            ),
            datetime_hint=(
                "string"
                if datetime_format.value.type_produced is str
                else "Date"
            ),
            dict_hint_template=(
                "Map<string, {val}>"
                if dict_format.name == "MAP"
                else "Record<string, {val}>"
            ),
            sequence_is_tuple=(sequence_format.name == "TUPLE"),
        )
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            line_ending.wrap_formatter(formatter=_base_decl)
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            line_ending.wrap_formatter(
                formatter=variable_formatter(template="{name} = {value};"),
            )
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
        self.call_style = call_style
        self.call_style_config: CallStyleConfig | None = call_style.value
        self.statement_terminator = ";"
        self.format_call_stub = _ts_call_stub
        self.format_call_preamble_stub = no_call_stub
