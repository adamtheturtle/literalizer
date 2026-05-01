"""Standard ML language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Sequence
from functools import cached_property, partial
from types import MappingProxyType
from typing import ClassVar

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    datetime_ymdhms_formatter,
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    declaration_formatter_ignoring_modifiers,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    tuple_dict_entry,
    variable_declaration_formatter,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    format_integer_hex,
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
    LanguageCls,
    ModifierCombination,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    default_wrap_calls_with_declarations,
    identity_call_arg,
    identity_call_ref_identifier,
    identity_call_target,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import Value
from literalizer.exceptions import WrapCombinedInFileNotSupportedError


@beartype
def _apply_sml_negate_int(value: int, formatter: Callable[[int], str]) -> str:
    """Format an integer, replacing ``-`` with ``~``."""
    result = formatter(value)
    if result.startswith("-"):
        return "~" + result[1:]
    return result


def _sml_negate_int(
    formatter: Callable[[int], str],
) -> Callable[[int], str]:
    """Wrap an integer formatter to use SML's ``~`` for negation."""

    def _format(value: int) -> str:
        """Delegate to module-level implementation."""
        return _apply_sml_negate_int(value=value, formatter=formatter)

    return _format


@beartype
def _apply_sml_negate_float(
    value: float, formatter: Callable[[float], str]
) -> str:
    """Format a float, replacing ``-`` with ``~``."""
    result = formatter(value)
    if result.startswith("-"):
        return "~" + result[1:]
    return result


def _sml_negate_float(
    formatter: Callable[[float], str],
) -> Callable[[float], str]:
    """Wrap a float formatter to use SML's ``~`` for negation."""

    def _format(value: float) -> str:
        """Delegate to module-level implementation."""
        return _apply_sml_negate_float(value=value, formatter=formatter)

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


@beartype
def _apply_sml_entry_formatter(  # noqa: PLR0911
    original: Value, formatted: str, prefix: str
) -> str:
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
        case datetime.datetime() if formatted.lstrip("-").isdigit():
            negative = formatted.startswith("-")
            literal = f"~{formatted[1:]}" if negative else formatted
            return (
                f"{prefix}Int ({literal})"
                if negative
                else f"{prefix}Int {literal}"
            )
        case datetime.date() if formatted.startswith('"'):
            return f"{prefix}Str {formatted}"
        case _:
            return formatted


def _build_sml_entry_formatter(
    prefix: str,
) -> Callable[[Value, str], str]:
    """Build an entry formatter that wraps values in SML ``datatype``
    constructors using the given *prefix*.
    """

    def _format(original: Value, formatted: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_sml_entry_formatter(
            original=original, formatted=formatted, prefix=prefix
        )

    return _format


@beartype
def _apply_sml_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    sequence_declared_type: str,
    scalar_declared_type: str,
    entry_formatter: Callable[[Value, str], str],
) -> str:
    """Format a variable declaration."""
    decl_type = (
        sequence_declared_type
        if isinstance(data, list)
        else scalar_declared_type
    )
    wrapped = entry_formatter(data, value)
    return f"val {name} : {decl_type} = {wrapped}"


@beartype
def _build_sml_declaration(
    *,
    sequence_declared_type: str,
    scalar_declared_type: str,
    entry_formatter: Callable[[Value, str], str],
) -> Callable[[str, str, Value], str]:
    """Build an SML variable declaration formatter."""

    def _format(name: str, value: str, data: Value) -> str:
        """Delegate to module-level implementation."""
        return _apply_sml_declaration(
            name=name,
            value=value,
            data=data,
            sequence_declared_type=sequence_declared_type,
            scalar_declared_type=scalar_declared_type,
            entry_formatter=entry_formatter,
        )

    return _format


def _format_sml_preamble_lines(
    lines: list[str],
    *,
    indent: str,
) -> tuple[str, ...]:
    """Format deduplicated preamble lines with SML ``datatype`` syntax.

    The first constructor is indented; subsequent constructors are
    prefixed with ``|``.
    """
    pipe_prefix = " " * max(0, len(indent) - 2) + "| "
    return (
        lines[0],
        indent + lines[1],
        *(f"{pipe_prefix}{line}" for line in lines[2:]),
    )


def _sml_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    /,
) -> tuple[str, ...]:
    """Return SML stub declarations for a call name.

    For dotted names like ``app.client.fetch``, nested SML structures
    are emitted so that ``app.client.fetch arg`` is valid at the call
    site.  The innermost name becomes a ``fun`` declaration that accepts
    any argument and returns unit.
    """
    method = parts[-1]
    lines: list[str] = [f"fun {method} _ = ()"]
    for part in reversed(parts[:-1]):
        lines = [f"structure {part} = struct", *lines, "end"]
    return tuple(lines)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
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
    supports_special_floats = True
    supports_variable_names = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset({"op"})
    allows_bare_call_statement = True
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_zero_parameter_calls = True
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_commented_dict_call_args = True
    supports_module_name = False

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

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
        """Sequence type options for Standard ML."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="SList ["),
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
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Standard ML."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="SSet ["),
            close="]",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
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
            formatter=variable_declaration_formatter(
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

        DOUBLE = enum.auto()

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

        SEMICOLON = enum.auto()

    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """Sml call style options."""

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
        """Version options for SML."""

        SML_97 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.CAMEL,
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
        """Wrap an SML val declaration at top level."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        force_line = f"\nval _ = {variable_name}" if variable_name else ""
        return content + force_line

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Unsupported: literalize() rejects BothVariableForms
        upstream.
        """
        del declaration, assignment, variable_name, body_preamble
        raise WrapCombinedInFileNotSupportedError

    date_format: DateFormats = DateFormats.SML
    datetime_format: DatetimeFormats = DatetimeFormats.SML
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.PAREN_STAR
    declaration_style: DeclarationStyles = DeclarationStyles.VAL
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
    trailing_comma: TrailingCommas = TrailingCommas.NO
    line_ending: LineEndings = LineEndings.SEMICOLON
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    language_version: VersionFormats = VersionFormats.SML_97
    indent: str = "    "
    type_name: str = "val_t"
    constructor_prefix: str = "S"
    call_style: CallStyles = CallStyles.POSITIONAL

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
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""

        def _format(value: str) -> str:
            """Format a string as an SML quoted literal."""
            return format_string_backslash_control(
                value=value,
                control_char_fmt="\\{:03d}",
            )

        return _format

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
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return stub declarations for a call expression."""
        return _sml_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return file-scope stubs for a call expression."""
        return no_call_stub

    @cached_property
    def format_call_statement(self) -> Callable[[str], str]:
        """Wrap a call expression as a val binding so it is a valid SML
        declaration inside a structure block.
        """
        return lambda statement: f"val _ = {statement}"

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
    def format_call_arg_ref_identifier(self) -> Callable[[str], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier in a call-argument
        context.

        Delegates to :attr:`format_call_ref_identifier`.  Override this to
        allow call-argument ``$ref`` values that would otherwise be rejected.
        """
        return self.format_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier_consumable(
        self,
    ) -> Callable[[str], str]:
        """Format a ``$ref`` the caller authorized as consumable.

        Delegates to :attr:`format_call_arg_ref_identifier`.  Override
        this to opt into a consuming form (e.g. C++ ``std::move``).
        """
        return self.format_call_arg_ref_identifier

    scalar_preamble: ClassVar[dict[type, tuple[str, ...]]] = {}

    @cached_property
    def null_literal(self) -> str:
        """Literal for the null value."""
        return f"{self.constructor_prefix}Null"

    @cached_property
    def true_literal(self) -> str:
        """Literal for the true value."""
        return f"{self.constructor_prefix}Bool true"

    @cached_property
    def false_literal(self) -> str:
        """Literal for the false value."""
        return f"{self.constructor_prefix}Bool false"

    @cached_property
    def _entry_formatter(self) -> Callable[[Value, str], str]:
        """Shared entry formatter parameterized by constructor prefix."""
        return _build_sml_entry_formatter(prefix=self.constructor_prefix)

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return dataclasses.replace(
            self.sequence_format.value,
            sequence_open=fixed_open(
                open_str=f"{self.constructor_prefix}List [",
            ),
        )

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return fixed_open(
            open_str=f"{self.constructor_prefix}List [",
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return dataclasses.replace(
            self.set_format.value,
            set_open=fixed_open(
                open_str=f"{self.constructor_prefix}Set [",
            ),
        )

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=fixed_open(
                open_str=f"{self.constructor_prefix}Map [",
            ),
            close="]",
            format_entry=tuple_dict_entry(
                format_value=self._entry_formatter,
            ),
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
        if self.date_format.name == "SML":
            return date_ymd_formatter(
                template=(
                    f"{self.constructor_prefix}Date "
                    f"({{year}}, {{month}}, {{day}})"
                ),
            )
        return self.date_format

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        if self.datetime_format.name == "SML":
            return datetime_ymdhms_formatter(
                template=(
                    f"{self.constructor_prefix}Datetime "
                    f"(({{year}}, {{month}}, {{day}}), "
                    f"({{hour}}, {{minute}}, {{second}}))"
                ),
            )
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
            fallback=raise_for_unrepresentable_int(language_name="SML"),
        )

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Callable that formats a set entry."""
        return self._entry_formatter

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Callable that formats a sequence entry."""
        return self._entry_formatter

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(
                open_str=f"{self.constructor_prefix}Map [",
            ),
            close="]",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return tuple_dict_entry(format_value=self._entry_formatter)

    @cached_property
    def _sml_decl(self) -> Callable[[str, str, Value], str]:
        """Shared SML variable declaration formatter."""
        _raw_declared = self.sequence_format.value.declared_type
        _sequence_declared_type = (
            _raw_declared.replace("val_t", self.type_name)
            if _raw_declared is not None
            else self.type_name
        )
        return _build_sml_declaration(
            sequence_declared_type=_sequence_declared_type,
            scalar_declared_type=self.type_name,
            entry_formatter=self._entry_formatter,
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return declaration_formatter_ignoring_modifiers(
            formatter=self._sml_decl
        )

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        return self._sml_decl

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble for SML datatype declarations."""
        p = self.constructor_prefix
        _h = f"datatype {self.type_name} ="
        _date_constructor = (
            f"{p}Str of string"
            if self.date_format.value.type_produced is str
            else f"{p}Date of (int * int * int)"
        )
        _datetime_constructor = (
            f"{p}Int of LargeInt.int"
            if self.datetime_format.value.type_produced is int
            else (
                f"{p}Str of string"
                if self.datetime_format.value.type_produced is str
                else f"{p}Datetime of ((int * int * int) * (int * int * int))"
            )
        )
        return {
            type(None): (_h, f"{p}Null"),
            bool: (_h, f"{p}Bool of bool"),
            int: (_h, f"{p}Int of LargeInt.int"),
            float: (_h, f"{p}Real of real"),
            str: (_h, f"{p}Str of string"),
            bytes: (_h, f"{p}Str of string"),
            datetime.date: (_h, _date_constructor),
            datetime.datetime: (_h, _datetime_constructor),
            list: (_h, f"{p}List of {self.type_name} list"),
            dict: (_h, f"{p}Map of (string * {self.type_name}) list"),
            ordereddict: (
                _h,
                f"{p}Map of (string * {self.type_name}) list",
            ),
            set: (_h, f"{p}Set of {self.type_name} list"),
        }

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines from the scalar map."""
        return body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=partial(
                _format_sml_preamble_lines,
                indent=self.indent,
            ),
        )
