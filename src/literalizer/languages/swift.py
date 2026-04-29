"""Swift language specification."""

import dataclasses
import datetime
import enum
import functools
from collections.abc import Callable, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar, assert_never

from beartype import beartype

from literalizer._formatters.collection_openers import fixed_open
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
    variable_declaration_formatter,
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
    make_overflow_fallback_formatter,
    raise_for_unrepresentable_int,
)
from literalizer._formatters.format_strings import (
    format_string_backslash_control,
)
from literalizer._language import (
    NO_HETEROGENEOUS_BEHAVIOR,
    CallStyle,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    HeterogeneousBehavior,
    IdentifierCase,
    KeywordCallStyle,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    date_scalar_preamble,
    default_wrap_calls_with_declarations,
    identity_call_ref_identifier,
    identity_call_target,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    no_validate_spec_for_data,
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


def _swift_param(name: str, /) -> str:
    """Format a single Swift parameter for a stub signature."""
    if name.startswith("_"):
        return f"_ {name}: Any = 0"
    return f"{name}: Any = 0"


def _swift_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    /,
) -> tuple[str, ...]:
    """Return Swift stub declarations for a call name."""
    param_list = ", ".join(_swift_param(p) for p in params)
    if len(parts) == 1:
        return (
            f"@discardableResult func {parts[0]}({param_list}) -> Any {{ 0 }}",
        )
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    method_decl = (
        f"@discardableResult func {method}({param_list}) -> Any {{ 0 }}"
    )
    if not fields:
        cls = f"_{root}Type"
        return (
            f"class {cls} {{ {method_decl} }}",
            f"let {root} = {cls}()",
        )
    lines: list[str] = []
    inner_cls = f"_{fields[-1]}Type"
    lines.append(f"class {inner_cls} {{ {method_decl} }}")
    prev_cls = inner_cls
    for i in range(len(fields) - 2, -1, -1):
        cls = f"_{fields[i]}Type"
        lines.append(f"class {cls} {{ var {fields[i + 1]} = {prev_cls}() }}")
        prev_cls = cls
    root_cls = f"_{root}Type"
    lines.append(f"class {root_cls} {{ var {fields[0]} = {prev_cls}() }}")
    lines.append(f"let {root} = {root_cls}()")
    return tuple(lines)


@beartype
def _swift_type_hint(  # pylint: disable=too-complex,too-many-branches  # noqa: C901, PLR0911, PLR0912
    *,
    data: Value,
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
            match unique:
                case [single]:
                    val_type = single
                case _ if "Any?" in unique:
                    val_type = "Any?"
                case _:
                    val_type = "Any"
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
            match unique:
                case [single]:
                    elem_type = single
                case _ if "Any?" in unique:
                    elem_type = "Any?"
                case _:
                    elem_type = "Any"
            return f"[{elem_type}]"
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _format_swift_typed_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
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
def _apply_swift_optional_nil_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
    base_formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
    keyword: str,
) -> str:
    """Format a Swift variable declaration, guarding top-level ``nil``."""
    if data is None:
        return f"{keyword} {name}: Any? = {value}"
    return base_formatter(name, value, data, _modifiers)


@beartype
def _optional_nil_declaration(
    *,
    base_formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
    keyword: str,
) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
    """Wrap *base_formatter* so top-level ``nil`` gets an optional type.

    ``Any`` is non-optional in Swift, so ``let my_data: Any = nil`` fails
    to compile.  Emit ``{keyword} {name}: Any? = nil`` when the value is
    ``None``.
    """

    def _format(
        name: str,
        value: str,
        data: Value,
        _modifiers: frozenset[enum.Enum],
    ) -> str:
        """Delegate to module-level implementation."""
        return _apply_swift_optional_nil_declaration(
            name=name,
            value=value,
            data=data,
            _modifiers=_modifiers,
            base_formatter=base_formatter,
            keyword=keyword,
        )

    return _format


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Swift(metaclass=LanguageCls):
    """Swift language specification."""

    extension = ".swift"
    pygments_name = "swift"
    language_version = "5.9"
    supports_default_set_element_type = True
    supports_default_sequence_element_type = True
    supports_default_dict_value_type = True
    supports_default_dict_key_type = True
    supports_default_ordered_map_value_type = False
    supports_special_floats = True
    supports_variable_names = True
    supports_dotted_calls = True

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

    class SetFormats(enum.Enum):
        """Set type options for Swift."""

        SET = enum.member(
            value=set_format_factory(
                open_template="Set<{type}>([",
                close="])",
                empty_template="Set<{type}>()",
                preamble_lines=(),
                set_opener_template="",
                supports_heterogeneity=True,
                supports_trailing_comma=True,
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
            formatter=variable_declaration_formatter(
                template="let {name}: Any = {value}"
            ),
            supports_redefinition=False,
        )
        VAR = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="var {name}: Any = {value}"
            ),
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
                supports_trailing_comma=True,
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
        ALWAYS = enum.auto()

        def formatter(
            self,
            *,
            auto_formatter: Callable[
                [str, str, Value, frozenset[enum.Enum]], str
            ],
            keyword: str,
            date_hint: str,
            datetime_hint: str,
            default_set_element_type: str,
            default_sequence_element_type: str,
            default_dict_value_type: str,
            sequence_is_tuple: bool,
        ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
            """Return the variable declaration formatter."""
            if self is type(self).AUTO:
                return _optional_nil_declaration(
                    base_formatter=auto_formatter,
                    keyword=keyword,
                )

            def _typed_formatter(
                name: str,
                value: str,
                data: Value,
                modifiers: frozenset[enum.Enum],
            ) -> str:
                """Adapt :func:`_format_swift_typed_declaration` to the
                positional formatter interface.
                """
                return _format_swift_typed_declaration(
                    name=name,
                    value=value,
                    data=data,
                    _modifiers=modifiers,
                    keyword=keyword,
                    date_hint=date_hint,
                    datetime_hint=datetime_hint,
                    default_set_element_type=default_set_element_type,
                    default_sequence_element_type=(
                        default_sequence_element_type
                    ),
                    default_dict_value_type=default_dict_value_type,
                    sequence_is_tuple=sequence_is_tuple,
                )

            return _typed_formatter

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
        """Swift call style options."""

        KEYWORD = KeywordCallStyle(separator=": ")

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Heterogeneous-scalar strategy options — this language only
        supports raising.
        """

        ERROR = NO_HETEROGENEOUS_BEHAVIOR

    heterogeneous_strategies = HeterogeneousStrategies

    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.CAMEL,
        IdentifierCase.PASCAL,
        IdentifierCase.UPPER_SNAKE,
    )

    validate_spec_for_data = no_validate_spec_for_data
    wrap_calls_with_declarations = default_wrap_calls_with_declarations

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

    date_format: DateFormats = DateFormats.SWIFT
    datetime_format: DatetimeFormats = DatetimeFormats.SWIFT
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.SET
    default_set_element_type: str = "AnyHashable"
    default_sequence_element_type: str = "Any"
    default_dict_key_type: str = "String"
    default_dict_value_type: str = "Any"
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.LET
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.DEFAULT
    float_format: FloatFormats = FloatFormats.REPR
    integer_format: IntegerFormats = IntegerFormats.DECIMAL
    numeric_literal_suffix: NumericLiteralSuffixes = (
        NumericLiteralSuffixes.NONE
    )
    numeric_separator: NumericSeparators = NumericSeparators.NONE
    numeric_style: NumericStyles = NumericStyles.OVERLOADED
    string_format: StringFormats = StringFormats.DOUBLE
    trailing_comma: TrailingCommas = TrailingCommas.YES
    line_ending: LineEndings = LineEndings.SEMICOLON
    call_style: CallStyles = CallStyles.KEYWORD
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    indent: str = "    "

    null_literal: ClassVar[str] = "nil"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = True
    statement_terminator: ClassVar[str] = ";"
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""

        def _format(value: str) -> str:
            """Format a string as a Swift quoted literal."""
            return format_string_backslash_control(
                value=value,
                control_char_fmt="\\u{{{:x}}}",
            )

        return _format

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        return variable_formatter(template="{name} = {value}")

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines."""
        return no_data_preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config."""
        return self.heterogeneous_strategy.value

    @cached_property
    def type_hint_collection_preamble_lines(
        self,
    ) -> Callable[[frozenset[type]], tuple[str, ...]]:
        """Return preamble lines for empty-collection type hints."""
        return no_type_hint_preamble

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return stub declarations for a call expression."""
        return _swift_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return file-scope stubs for a call expression."""
        return no_call_stub

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into the language's call
        syntax.
        """
        return identity_call_target

    @cached_property
    def format_call_ref_identifier(self) -> Callable[[str], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier into the
        language's call expression syntax.
        """
        return identity_call_ref_identifier

    scalar_body_preamble: ClassVar[dict[type, tuple[str, ...]]] = {}

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return self.sequence_format(
            default_type=self.default_sequence_element_type,
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return self.set_format(default_type=self.default_set_element_type)

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format_config.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return self.dict_format(
            default_type=self.default_dict_value_type,
            default_key_type=self.default_dict_key_type,
        )

    @cached_property
    def trailing_comma_config(self) -> TrailingCommaConfig:
        """Configuration for trailing-comma behavior."""
        return self.trailing_comma.value

    @cached_property
    def format_bytes(self) -> Callable[[bytes], str]:
        """Callable that formats a bytes value as a string literal."""
        return self.bytes_format

    @cached_property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a date as a string literal."""
        return self.date_format

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        return self.datetime_format

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        return make_overflow_fallback_formatter(
            base=self.integer_format.get_formatter(
                numeric_separator=self.numeric_separator,
            ),
            fallback=raise_for_unrepresentable_int(language_name="Swift"),
        )

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Callable that formats a sequence entry."""
        return self.sequence_format_config.format_entry

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="["),
            close="]",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return dict_entry_with_separator(
            separator=": ",
            format_value=passthrough_sequence_entry,
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return self.variable_type_hints.formatter(
            auto_formatter=self.declaration_style.value.formatter,
            keyword=self.declaration_style.name.lower(),
            date_hint=(
                "String"
                if self.date_format.value.type_produced is str
                else "Date"
            ),
            datetime_hint=(
                "String"
                if self.datetime_format.value.type_produced is str
                else "Date"
            ),
            default_set_element_type=self.default_set_element_type,
            default_sequence_element_type=self.default_sequence_element_type,
            default_dict_value_type=self.default_dict_value_type,
            sequence_is_tuple=(self.sequence_format.name == "TUPLE"),
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble computed from date/datetime format."""
        return date_scalar_preamble(
            date_format=self.date_format,
            datetime_format=self.datetime_format,
        )

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines from the scalar map."""
        return body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value
