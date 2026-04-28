"""Groovy language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Sequence
from functools import cached_property
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
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
    variable_declaration_formatter,
    variable_formatter,
)
from literalizer._formatters.format_factories import set_format_factory
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_strings import (
    format_string_backslash_dollar,
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
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
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


def _groovy_call_stub_factory(
    *,
    keyword_style: bool,
) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
    """Return a Groovy stub generator for the given call style.

    Named-argument calls pack every argument into a single
    ``LinkedHashMap`` first parameter, so stubs for ``KEYWORD`` calls
    must declare a single ``Map`` parameter.  ``POSITIONAL`` stubs keep
    the concrete parameter list, which documents the expected argument
    names.
    """

    def _stub(
        parts: Sequence[str],
        params: Sequence[str],
        _stub_return: StubReturn,
        /,
    ) -> tuple[str, ...]:
        """Return Groovy stub declarations for a call name."""
        param_list = "Map _args" if keyword_style else ", ".join(params)
        if len(parts) == 1:
            return (f"def {parts[0]}({param_list}) {{ null }}",)
        root = parts[0]
        method = parts[-1]
        fields = parts[1:-1]
        if not fields:
            cls = f"_{root.title()}Type"
            return (
                f"class {cls} {{ def {method}({param_list}) {{ null }} }}",
                f"def {root} = new {cls}()",
            )
        lines: list[str] = []
        inner_cls = f"_{fields[-1].title()}Type"
        lines.append(
            f"class {inner_cls} {{ def {method}({param_list}) {{ null }} }}"
        )
        prev_cls = inner_cls
        for i in range(len(fields) - 2, -1, -1):
            cls = f"_{fields[i].title()}Type"
            lines.append(
                f"class {cls} {{ def {fields[i + 1]} = new {prev_cls}() }}"
            )
            prev_cls = cls
        root_cls = f"_{root.title()}Type"
        lines.append(
            f"class {root_cls} {{ def {fields[0]} = new {prev_cls}() }}"
        )
        lines.append(f"def {root} = new {root_cls}()")
        return tuple(lines)

    return _stub


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Groovy(metaclass=LanguageCls):
    """Groovy language specification."""

    extension = ".groovy"
    pygments_name = "groovy"
    supports_default_set_element_type = True
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True
    supports_special_floats = True
    supports_variable_names = True
    supports_dotted_calls = True

    class DateFormats(enum.Enum):
        """Date format options for Groovy."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Groovy."""

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
        """Sequence type options for Groovy."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="["),
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
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Groovy."""

        SET = enum.member(
            value=set_format_factory(
                open_template="[",
                close="] as Set<{type}>",
                empty_template="[] as Set<{type}>",
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

        DEF = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="def {name} = {value}"
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
        positive_infinity="Double.POSITIVE_INFINITY",
        negative_infinity="Double.NEGATIVE_INFINITY",
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
        """Groovy call style options."""

        KEYWORD = KeywordCallStyle(separator=": ")
        POSITIONAL = PositionalCallStyle()

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

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    default_set_element_type: str = "Object"
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.DEF
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

    null_literal: ClassVar[str] = "null"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = True
    statement_terminator: ClassVar[str] = ""
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Format an int value as a literal."""
        return str

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash_dollar

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

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
        return _groovy_call_stub_factory(
            keyword_style=isinstance(self.call_style.value, KeywordCallStyle),
        )

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

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return self.sequence_format.value

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return self.set_format(default_type=self.default_set_element_type)

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format.value.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=fixed_open(open_str="["),
            close="]",
            format_entry=dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict="[:]",
            preamble_lines=(),
            narrowed_open=None,
            supports_trailing_comma=True,
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
        return self.declaration_style.value.formatter

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        return variable_formatter(template="{name} = {value}")

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Groovy needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Groovy needs none)."""
        return {}

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
        config: CallStyle = self.call_style.value
        return config
