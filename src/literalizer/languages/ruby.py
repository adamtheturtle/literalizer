"""Ruby language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Sequence
from functools import cached_property, partial
from types import MappingProxyType
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_symbol_style,
    dict_entry_with_separator,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    variable_declaration_formatter,
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
    format_string_backslash_single_minimal,
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
    ModifierCombination,
    OrderedMapFormatConfig,
    PositionalCallStyle,
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
from literalizer.exceptions import CallArgNotSupportedError


def _to_pascal_case(name: str) -> str:
    """Convert *name* to PascalCase."""
    return IdentifierCase.PASCAL.convert(name=name)


def _ruby_call_stub(
    format_class_name: Callable[[str], str],
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    /,
) -> tuple[str, ...]:
    """Return Ruby stub declarations for a call name."""
    if len(parts) == 1:
        return (f"def {parts[0]}(*a); end",)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        cls = format_class_name(root) + "Type"
        return (
            f"class {cls}; def {method}(*a, **kw); end; end",
            f"{root} = {cls}.new",
        )
    lines: list[str] = []
    inner_cls = format_class_name(fields[-1]) + "Type"
    lines.append(f"class {inner_cls}; def {method}(*a, **kw); end; end")
    prev_cls = inner_cls
    for i in range(len(fields) - 2, -1, -1):
        cls = format_class_name(fields[i]) + "Type"
        field = fields[i + 1]
        lines.append(f"class {cls}; def {field}; {prev_cls}.new; end; end")
        prev_cls = cls
    root_cls = format_class_name(root) + "Type"
    lines.append(
        f"class {root_cls}; def {fields[0]}; {prev_cls}.new; end; end"
    )
    lines.append(f"{root} = {root_cls}.new")
    return tuple(lines)


@beartype
def _format_datetime_ruby(value: datetime.datetime) -> str:
    """Format a datetime as a Ruby Time constructor call.

    UTC-aware datetimes use ``Time.utc``. Datetimes with a non-UTC
    offset use ``Time.new`` with the offset string. Naive datetimes use
    ``Time.new`` without an offset.
    """
    args = (
        f"{value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second}"
    )
    offset = value.utcoffset()
    if offset is None:
        return f"Time.new({args})"
    if not offset:
        return f"Time.utc({args})"
    total_seconds = int(offset.total_seconds())
    sign = "+" if total_seconds >= 0 else "-"
    abs_seconds = abs(total_seconds)
    hours, remainder = divmod(abs_seconds, 3600)
    minutes = remainder // 60
    offset_str = f"{sign}{hours:02d}:{minutes:02d}"
    return f'Time.new({args}, "{offset_str}")'


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Ruby(metaclass=LanguageCls):
    """Ruby language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.RUBY`` — ``Date.new(...)`` call,
              e.g. ``Date.new(2024, 1, 15)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.RUBY`` — ``Time.new(...)`` call,
              e.g. ``Time.new(2024, 1, 15, 12, 30, 0)``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.

        dict_entry_style: How to format dict/hash entries.

            * ``dict_entry_styles.ROCKET`` — rocket notation,
              e.g. ``"name" => "Alice"``.
            * ``dict_entry_styles.SYMBOL`` — symbol notation,
              e.g. ``name: "Alice"``.
    """

    extension = ".rb"
    pygments_name = "ruby"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_special_floats = True
    supports_variable_names = False
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    allows_bare_call_statement = True
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_inline_multiline_dict_args = True
    supports_module_name = False

    class DateFormats(enum.Enum):
        """Date format options for Ruby."""

        RUBY = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="Date.new({year}, {month}, {day})",
            ),
            preamble_lines=("require 'date'",),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Ruby."""

        RUBY = DatetimeFormatConfig(
            formatter=_format_datetime_ruby,
        )
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            type_produced=str,
        )

        EPOCH = DatetimeFormatConfig(
            formatter=format_datetime_epoch,
            type_produced=int,
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
        """Sequence type options for Ruby."""

        ARRAY = SequenceFormatConfig(
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
        """Set type options for Ruby."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="Set.new(["),
            close="])",
            empty_set="Set.new",
            preamble_lines=("require 'set'",),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        HASH = CommentConfig(
            prefix="#",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        ASSIGN = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="{name} = {value}"
            ),
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options for Ruby.

        * ``ROCKET`` — rocket notation, e.g. ``"key" => "value"``.
        * ``SYMBOL`` — symbol notation, e.g. ``key: "value"``.
        """

        ROCKET = (
            dict_entry_with_separator(
                separator=" => ",
                format_value=passthrough_sequence_entry,
            ),
        )
        SYMBOL = (
            dict_entry_symbol_style(
                format_value=passthrough_sequence_entry,
            ),
        )

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = enum.auto()

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="Float::INFINITY",
        negative_infinity="-Float::INFINITY",
        nan="Float::NAN",
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
        SINGLE = enum.member(value=format_string_backslash_single_minimal)

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

        SEMICOLON = enum.auto()

    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """Ruby call style options."""

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

    class VersionFormats(enum.Enum):
        """Version options for Ruby."""

        V3 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.UPPER_SNAKE,
        IdentifierCase.PASCAL,
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

    date_format: DateFormats = DateFormats.RUBY
    datetime_format: DatetimeFormats = DatetimeFormats.RUBY
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.HASH
    declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN
    dict_entry_style: DictEntryStyles = DictEntryStyles.ROCKET
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
    language_version: VersionFormats = VersionFormats.V3
    indent: str = "  "

    null_literal: ClassVar[str] = "nil"
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
        return partial(_ruby_call_stub, _to_pascal_case)

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
        """Raise for any ``{"$ref": "name"}`` identifier.

        Ruby output is not wrapped in a function body; variable
        references require a surrounding assignment that cannot be
        injected via the call framework.
        """

        def _raise_for_ruby_ref(name: str, /) -> str:
            """Raise ``CallArgNotSupportedError`` unconditionally."""
            raise CallArgNotSupportedError(
                language_name="Ruby",
                reason=(
                    "Ruby output is not wrapped in a function body; "
                    f"variable references require a surrounding "
                    f"assignment (got {name!r})"
                ),
            )

        return _raise_for_ruby_ref

    @cached_property
    def format_call_arg_ref_identifier(self) -> Callable[[str], str]:
        """Rewrite a ``{"$ref": "name"}`` call-argument identifier.

        Unlike :attr:`format_call_ref_identifier`, this is used only when
        the ``$ref`` appears as a direct call argument (via
        :func:`~literalizer.literalize_call`).  In that context the
        referenced variable has already been emitted at the same top-level
        scope, so the reference is valid.
        """
        return identity_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier_consumable(
        self,
    ) -> Callable[[str], str]:
        """Format a ``$ref`` the caller authorized as consumable.

        Delegates to :attr:`format_call_arg_ref_identifier`.  Override
        this to opt into a consuming form (e.g. C++ ``std::move``).
        """
        return self.format_call_arg_ref_identifier

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return self.sequence_format.value

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return self.set_format.value

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format.value.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        (format_entry,) = self.dict_entry_style.value
        return DictFormatConfig(
            dict_open=fixed_open(open_str="{"),
            close="}",
            format_entry=format_entry,
            empty_dict=None,
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
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        return self.string_format

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        return self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="{"),
            close="}",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return dict_entry_with_separator(
            separator=" => ",
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
        """Per-instance scalar preamble computed from date/datetime format."""
        return date_scalar_preamble(
            date_format=self.date_format,
            datetime_format=self.datetime_format,
        )

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Ruby needs none)."""
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
