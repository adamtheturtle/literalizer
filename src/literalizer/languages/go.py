"""Go language specification."""

import dataclasses
import datetime
import enum
import re
from collections.abc import Callable, Mapping, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar

from beartype import beartype
from ruamel.yaml.compat import ordereddict as _ordereddict

from literalizer._formatters.collection_openers import (
    fixed_open,
    make_element_to_type,
    make_type_to_opener,
    typed_collection_open,
    typed_dict_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
    format_time_iso,
)
from literalizer._formatters.format_entries import (
    braced_dict_entry,
    dict_entry_with_separator,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    variable_declaration_formatter,
    variable_formatter,
)
from literalizer._formatters.format_factories import set_format_factory
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    I64_MAX,
    I64_MIN,
    U64_MAX,
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    format_integer_underscore,
    make_int64_cast_formatter,
    make_overflow_fallback_formatter,
    make_unsigned_overflow_fallback,
)
from literalizer._formatters.format_strings import format_string_backslash
from literalizer._formatters.record_strategy import (
    RecordDeclarationField,
    RecordFieldType,
    RecordLiteralField,
    RecordRenderer,
    RecordStrategy,
    build_record_strategy,
)
from literalizer._formatters.type_inference import DictType, ListType
from literalizer._language import (
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
    BareIntegerWidthStrategies,
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
    NestedMapWideningVariant,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    RecordVariant,
    RenderedRecordLiteral,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    VariantMetadata,
    body_preamble_from_scalars,
    date_scalar_preamble,
    default_format_call_variable_assignment,
    default_format_call_variable_declaration,
    default_sequence_binding_declarations,
    default_wrap_calls_with_declarations,
    identity_call_arg,
    identity_call_ref_identifier,
    identity_call_statement,
    identity_call_target,
    never_inhibits_consuming_form,
    no_call_binding_body_preamble,
    no_call_binding_file_pragmas,
    no_call_stub,
    no_data_preamble,
    no_format_integer_widened,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import OrderedMap, Value
from literalizer.exceptions import (
    InvalidRecordNameError,
    UnrepresentableIntegerError,
)

_PASCAL_CASE_IDENTIFIER = re.compile(pattern=r"^[A-Z][A-Za-z0-9_]*$")


@beartype
def _format_go_uint64_positive(value: int) -> str:
    """Format a positive value outside signed 64-bit range as a Go
    ``uint64`` typed conversion.

    A Go integer constant without an explicit type can hold arbitrary
    size, but its default promotion to ``int`` overflows.  Wrapping in
    ``uint64(...)`` forces a typed conversion and accepts values up to
    ``math.MaxUint64``.  Values above ``math.MaxUint64`` have no native
    literal type and raise ``UnrepresentableIntegerError`` rather than
    emit a ``uint64(...)`` conversion the compiler will reject.
    """
    if value > U64_MAX:
        msg = (
            f"Go cannot represent integer {value} above the unsigned "
            "64-bit range."
        )
        raise UnrepresentableIntegerError(msg)
    return f"uint64({value})"


@beartype
def _go_call_preamble_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Go stub declarations for a call name."""
    if len(parts) == 1:
        return (f"func {parts[0]}(args ...any) any {{ return nil }}",)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        type_name = f"{root}Type_"
        return (
            f"type {type_name} struct{{}}",
            f"func ({type_name}) {method}(args ...any) any {{ return nil }}",
            f"var {root} {type_name}",
        )
    lines: list[str] = []
    inner_type = f"{fields[-1]}Type_"
    lines.append(f"type {inner_type} struct{{}}")
    lines.append(
        f"func ({inner_type}) {method}(args ...any) any {{ return nil }}"
    )
    prev_type = inner_type
    for i in range(len(fields) - 2, -1, -1):
        curr_type = f"{fields[i]}Type_"
        field = fields[i + 1]
        lines.append(f"type {curr_type} struct{{ {field} {prev_type} }}")
        prev_type = curr_type
    root_type = f"{root}Type_"
    lines.append(f"type {root_type} struct{{ {fields[0]} {prev_type} }}")
    lines.append(f"var {root} {root_type}")
    return tuple(lines)


@beartype
def _go_month_name(month: int) -> str:
    """Return the Go ``time.Month`` constant for a 1-based month
    number.
    """
    return (
        "time.January",
        "time.February",
        "time.March",
        "time.April",
        "time.May",
        "time.June",
        "time.July",
        "time.August",
        "time.September",
        "time.October",
        "time.November",
        "time.December",
    )[month - 1]


@beartype
def _format_date_go(value: datetime.date) -> str:
    """Format a date as a Go ``time.Date(...)`` call."""
    month = _go_month_name(month=value.month)
    return (
        f"time.Date({value.year}, {month}, {value.day}, 0, 0, 0, 0, time.UTC)"
    )


@beartype
def _format_datetime_go(value: datetime.datetime) -> str:
    """Format a datetime as a Go ``time.Date(...)`` call."""
    month = _go_month_name(month=value.month)
    nanoseconds = value.microsecond * 1000
    return (
        f"time.Date({value.year}, {month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second}, "
        f"{nanoseconds}, time.UTC)"
    )


@beartype
def _format_go_set_entry(_original: Value, item: str) -> str:
    """Format a Go set entry as a map entry with empty struct value.

    Example: ``"apple"`` → ``"apple": struct{}{}``.
    """
    return f"{item}: struct{{}}{{}}"


@beartype
def _go_record_field_identifier(key: str, /) -> str:
    """Return the exported Go struct field name for a dict *key*."""
    return IdentifierCase.PASCAL.convert(name=key)


@beartype
def _go_record_literal(
    name: str,
    fields: Sequence[RecordLiteralField],
    /,
) -> RenderedRecordLiteral:
    """Render a Go ``Name{Field: value, ...}`` literal as structured
    pieces for the shared compact/multiline layout code.
    """
    return RenderedRecordLiteral(
        head=f"{name}{{",
        entries=tuple(
            f"{field.identifier}: {field.formatted}" for field in fields
        ),
        closer="}",
        compact_pad="",
    )


@beartype
def _apply_go_nil_safe_declaration(
    name: str,
    value: str,
    data: Value,
    modifiers: frozenset[enum.Enum],
    base_formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
) -> str:
    """Format a Go variable declaration, guarding top-level
    ``nil``.
    """
    if data is None:
        return f"var {name} any = {value}"
    return base_formatter(name, value, data, modifiers)


@beartype
def _nil_safe_declaration(
    base_formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
    """Wrap *base_formatter* so top-level ``nil`` gets a typed form.

    Go cannot infer a type from ``nil`` alone, so
    ``my_data := nil`` and ``var my_data = nil`` both fail to compile.
    Emit ``var {name} any = nil`` when the value is ``None``.
    """

    def _format(
        name: str,
        value: str,
        data: Value,
        modifiers: frozenset[enum.Enum],
    ) -> str:
        """Delegate to module-level implementation."""
        return _apply_go_nil_safe_declaration(
            name=name,
            value=value,
            data=data,
            modifiers=modifiers,
            base_formatter=base_formatter,
        )

    return _format


@beartype
def _format_constructor_target(class_name: str, /) -> str:
    """Return a Go ``NewClassName`` constructor call target."""
    return f"New{class_name}"


_constructor_target: Callable[[str], str] = _format_constructor_target


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Go(metaclass=LanguageCls):
    """Go language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.GO`` — ``time.Date`` call,
              e.g. ``time.Date(2024, time.January, 15, 0, 0, 0, 0,
              time.UTC)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.GO`` — ``time.Date`` call,
              e.g. ``time.Date(2024, time.January, 15, 12, 30, 0, 0,
              time.UTC)``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.
    """

    format_integer_widened = no_format_integer_widened
    format_call_variable_declaration = default_format_call_variable_declaration
    format_call_variable_assignment = default_format_call_variable_assignment
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(_constructor_target)
    )
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".go"
    pygments_name = "go"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    reserved_variable_identifiers_case_sensitive: bool = True
    reserved_variable_identifiers: frozenset[str] = frozenset(
        {
            "break",
            "case",
            "chan",
            "const",
            "continue",
            "default",
            "defer",
            "else",
            "fallthrough",
            "false",
            "for",
            "func",
            "go",
            "goto",
            "if",
            "import",
            "interface",
            "map",
            "nil",
            "package",
            "range",
            "return",
            "select",
            "struct",
            "switch",
            "true",
        }
    )
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_zero_parameter_calls = True
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_multi_param_call_wrapper_stub = True
    supports_dict_literal_as_free_expression = True
    supports_module_name = False
    supports_empty_dict_key = False
    supports_call_style = True
    supports_default_dict_key_type = True
    supports_default_dict_value_type = True
    supports_default_sequence_element_type = True
    supports_default_set_element_type = True
    supports_default_ordered_map_value_type = True
    non_default_kwargs: ClassVar[dict[str, str]] = {
        "default_set_element_type": "string",
        "default_sequence_element_type": "interface{}",
        "default_dict_value_type": "interface{}",
        "default_dict_key_type": "any",
        "default_ordered_map_value_type": "interface{}",
    }
    declaration_style_sequence_format_overrides: ClassVar[dict[str, str]] = {}
    json_type_variant_name_suffix: ClassVar[str | None] = None
    supports_non_ascii_string_literals = True
    variant_metadata: ClassVar[VariantMetadata] = VariantMetadata(
        pre_indent_comment_scalar_variant=False,
        fixture_module_name_template=None,
        fixture_module_name_lowercase=False,
        golden_filename_lowercase=False,
        collection_layout_category="collection_layout",
        record_variants=frozenset({RecordVariant.FIELD_TYPE_SPLIT}),
        nested_map_widening=NestedMapWideningVariant.DEFAULT,
        modifier_sequence_format_overrides={},
    )
    supports_record_struct_name_prefix = True
    supports_record_shape_names = True
    supports_non_string_dict_keys = False

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

    class DateFormats(enum.Enum):
        """Date format options for Go."""

        GO = DateFormatConfig(
            formatter=_format_date_go,
            preamble_lines=('import "time"',),
            type_produced=datetime.date,
        )
        ISO = DateFormatConfig(
            formatter=format_date_iso, type_produced=str, preamble_lines=()
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Go."""

        GO = DatetimeFormatConfig(
            formatter=_format_datetime_go,
            preamble_lines=('import "time"',),
            type_produced=datetime.datetime,
        )
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            type_produced=str,
            preamble_lines=(),
        )

        EPOCH = DatetimeFormatConfig(
            formatter=format_datetime_epoch,
            type_produced=int,
            preamble_lines=(),
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
        """Sequence type options for Go."""

        SLICE = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="[]any{"),
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
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Go."""

        SET = enum.member(
            value=set_format_factory(
                open_template="map[{type}]struct{{}}{{",
                close="}}",
                empty_template=None,
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

        SHORT = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="{name} := {value}"
            ),
            supports_redefinition=True,
        )
        VAR = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="var {name} = {value}"
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
        positive_infinity="math.Inf(1)",
        negative_infinity="math.Inf(-1)",
        nan="math.NaN()",
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
        AUTO = enum.auto()

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = enum.auto()
        UNDERSCORE = enum.auto()

    class NumericStyles(enum.Enum):
        """Numeric literal style options."""

        OVERLOADED = enum.auto()

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.auto()

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        YES = TrailingCommaConfig(multiline_trailing_comma=True)

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats

    class VariableTypeHints(enum.Enum):
        """Variable type hint options."""

        NEVER = enum.auto()
        SAFE = enum.auto()

    variable_type_hints_formats = VariableTypeHints
    declaration_styles = DeclarationStyles
    dict_entry_styles = DictEntryStyles
    dict_formats = DictFormats
    empty_dict_keys = EmptyDictKey
    float_formats = FloatFormats
    integer_formats = IntegerFormats
    integer_width_strategies = BareIntegerWidthStrategies
    numeric_literal_suffixes = NumericLiteralSuffixes
    numeric_separators = NumericSeparators
    numeric_styles = NumericStyles
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class StatementTerminatorStyles(enum.Enum):
        """Statement terminator options."""

        NONE = ""

        @property
        def statement_terminator(self) -> str:
            """Terminator appended to complete call statements."""
            return self.value

    statement_terminator_styles = StatementTerminatorStyles

    class CallStyles(enum.Enum):
        """Go call style options."""

        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Strategy for dicts whose values span more than one Go type.

        ``ERROR`` keeps Go's strict-typing behavior (mixed-value dicts
        that cannot be represented raise).  ``RECORD`` renders each
        record-shaped dict (non-empty, string-keyed) as a generated
        ``struct`` declared in the preamble plus a matching struct
        literal, so fields may legitimately mix scalars and containers.
        """

        ERROR = enum.auto()
        RECORD = enum.auto()

    heterogeneous_strategies = HeterogeneousStrategies

    class JsonTypes(enum.Enum):
        """Empty: this language has no JSON value-type variants."""

    json_types = JsonTypes

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for Go."""

        V1_18 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.PASCAL,
        IdentifierCase.CAMEL,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    validate_spec_for_data = no_validate_spec_for_data

    @cached_property
    def validate_call_arg(self) -> Callable[[Value], None]:
        """Return call-argument validation for this language."""
        return no_validate_call_arg

    @cached_property
    def format_call_statement(self) -> Callable[[str], str]:
        """Return call-statement formatting for this language."""
        return identity_call_statement

    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a Go declaration in ``func main()``."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        use_line = f"\n_ = {variable_name}" if variable_name else ""
        return f"\nfunc main() {{\n{content}{use_line}\n}}"

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Go declaration + assignment in ``func main()``."""
        return Go.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.GO
    datetime_format: DatetimeFormats = DatetimeFormats.GO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.SLICE
    set_format: SetFormats = SetFormats.SET
    default_set_element_type: str = "any"
    default_sequence_element_type: str = "any"
    default_dict_key_type: str = "string"
    default_dict_value_type: str = "any"
    default_ordered_map_value_type: str = "any"
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.SHORT
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.DEFAULT
    float_format: FloatFormats = FloatFormats.REPR
    integer_format: IntegerFormats = IntegerFormats.DECIMAL
    integer_width_strategy: BareIntegerWidthStrategies = (
        BareIntegerWidthStrategies.BARE
    )
    numeric_literal_suffix: NumericLiteralSuffixes = (
        NumericLiteralSuffixes.NONE
    )
    numeric_separator: NumericSeparators = NumericSeparators.NONE
    numeric_style: NumericStyles = NumericStyles.OVERLOADED
    string_format: StringFormats = StringFormats.DOUBLE
    trailing_comma: TrailingCommas = TrailingCommas.YES
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.NONE
    )
    call_style: CallStyles = CallStyles.POSITIONAL
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    record_struct_name_prefix: str = "Record"
    record_shape_names: Mapping[frozenset[str], str] = dataclasses.field(
        default_factory=lambda: MappingProxyType(mapping={}),
        hash=False,
    )
    # Keep in sync with the `go` directive in the generated go.mod in
    # `.github/workflows/lint.yml`.
    language_version: VersionFormats = VersionFormats.V1_18
    indent: str = "\t"

    null_literal: ClassVar[str] = "nil"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = True
    static_preamble: ClassVar[Sequence[str]] = ("package main",)
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ('import "math"',)

    def __post_init__(self) -> None:
        """Validate ``record_shape_names`` after construction."""
        self._validate_record_naming()

    def _validate_record_naming(self) -> None:
        """Validate ``record_shape_names`` for PascalCase identifier
        shape, collisions with the auto-generated ``{prefix}{N}``
        struct names, and duplicate target names.

        Ported from
        :meth:`literalizer.languages.Rust._validate_record_naming`.  Go
        has no ``heterogeneous_value_enum_name`` so that collision
        check does not apply, and Rust's reserved-keyword check is
        unnecessary here: every Go keyword and built-in identifier is
        lowercase, so the PascalCase requirement already rejects every
        one of them.
        """
        prefix = self.record_struct_name_prefix
        auto_name_pattern = re.compile(
            pattern=rf"^{re.escape(pattern=prefix)}\d+$",
        )
        seen_names: set[str] = set()
        for keys, name in self.record_shape_names.items():
            if not _PASCAL_CASE_IDENTIFIER.match(string=name):
                msg = (
                    f"record_shape_names entry for keys {sorted(keys)!r} "
                    f"maps to {name!r}, which is not a PascalCase Go "
                    f"identifier."
                )
                raise InvalidRecordNameError(msg)
            if auto_name_pattern.match(string=name):
                msg = (
                    f"record_shape_names entry for keys {sorted(keys)!r} "
                    f"maps to {name!r}, which collides with the "
                    f"auto-generated {prefix!r}-prefixed struct names."
                )
                raise InvalidRecordNameError(msg)
            if name in seen_names:
                msg = (
                    f"record_shape_names maps multiple key-sets to "
                    f"{name!r}; struct names must be unique."
                )
                raise InvalidRecordNameError(msg)
            seen_names.add(name)

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return _format_go_set_entry

    def _go_record_field_type(self, request: RecordFieldType, /) -> str:
        """Return the Go struct field type for a record field.

        A field whose value is itself a nested record-shaped dict uses
        that record's generated struct name.  A list or ordered-map
        field derives its type from the very collection opener the
        value formatter uses for that value (a record field is
        formatted with no sibling override, so the opener equals the
        one emitted, including a widening to ``[]any``); the opener's
        trailing ``{`` is dropped to leave the bare type, e.g.
        ``[]int{`` -> ``[]int``, ``[][2]any{`` -> ``[][2]any``.  A
        scalar field uses the same scalar mapping the openers are
        built on.  A positive integer beyond the signed 64-bit range is
        the one exception: its literal comes from the ``uint64(...)``
        overflow fallback (see
        :func:`make_unsigned_overflow_fallback`), so the field is typed
        ``uint64`` to match that typed conversion.

        A record-eligible dict with no generated record name was widened
        out of the record-shape mapping because its nested sibling family
        cannot share one shape (issue #2911); it uses ``map[string]any``.
        A set or a non-record dict (an empty or non-string-keyed dict)
        as a record field has no precise component type under the
        ``RECORD`` strategy.  Per the cross-language decision in #2317,
        Rust rejects such a field while Go widens it to the top type
        ``any`` (documented best effort), which the rendered literal
        still assigns into.
        """
        if request.record_name is not None:
            return request.record_name
        value = request.value
        if (
            isinstance(value, dict)
            and not isinstance(value, OrderedMap)
            and bool(value)
            and all(isinstance(key, str) for key in value)
        ):
            return "map[string]any"
        match value:
            case None:
                return "any"
            case OrderedMap():
                opener = self.ordered_map_format_config.ordered_map_open(
                    value,
                )
            case list():
                opener = self.sequence_open(value)
            case int() if not isinstance(value, bool) and value > I64_MAX:
                return "uint64"
            case _:
                return self._init_element_to_type(type(value)) or "any"
        return opener[: -len("{")]

    def _go_render_declaration(
        self,
        name: str,
        fields: Sequence[RecordDeclarationField],
        /,
    ) -> str:
        """Render a Go ``type Name struct { ... }`` declaration."""
        lines = [f"type {name} struct {{"]
        lines += [
            f"{self.indent}{field.identifier} {field.type_name}"
            for field in fields
        ]
        lines.append("}")
        return "\n".join(lines)

    @cached_property
    def _record_renderer(self) -> RecordRenderer:
        """Go syntax hooks for the ``RECORD`` strategy."""
        return RecordRenderer(
            name_prefix=self.record_struct_name_prefix,
            record_shape_names=self.record_shape_names,
            field_identifier=_go_record_field_identifier,
            field_type=self._go_record_field_type,
            render_declaration=self._go_render_declaration,
            render_literal=_go_record_literal,
        )

    @cached_property
    def _record_strategy(self) -> RecordStrategy:
        """Resolve the active strategy to its behavior + preamble."""
        cls = type(self.heterogeneous_strategy)
        if self.heterogeneous_strategy is cls.RECORD:
            return build_record_strategy(
                renderer=self._record_renderer,
                split_conflicting_field_types=True,
                widen_unrecordizable_nested_sibling_maps=True,
                derecordized_map_open="map[string]any{",
            )
        return RecordStrategy(
            behavior=NO_HETEROGENEOUS_BEHAVIOR,
            preamble=no_data_preamble,
        )

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        For ``HeterogeneousStrategies.RECORD`` emits one ``struct``
        declaration per record shape present in the data; otherwise
        produces no preamble.
        """
        return self._record_strategy.preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the behavior for the chosen heterogeneous strategy."""
        return self._record_strategy.behavior

    @cached_property
    def call_data_dependent_preamble(
        self,
    ) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines for call rendering."""
        return self.data_dependent_preamble

    @cached_property
    def type_hint_collection_preamble_lines(
        self,
    ) -> Callable[[frozenset[type]], tuple[str, ...]]:
        """Return preamble lines for empty-collection type hints."""
        return no_type_hint_preamble

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return stub declarations for a call expression."""
        return no_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return file-scope stubs for a call expression."""
        return _go_call_preamble_stub

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into the language's call
        syntax.
        """
        return identity_call_target

    @cached_property
    def format_call_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier into the
        language's call expression syntax.
        """
        return identity_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier in a call-argument
        context.

        Delegates to :attr:`format_call_ref_identifier`.  Override this to
        allow call-argument ``$ref`` values that would otherwise be rejected.
        """
        return self.format_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier_consumable(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Format a ``$ref`` the caller authorized as consumable.

        Delegates to :attr:`format_call_arg_ref_identifier`.  Override
        this to opt into a consuming form (e.g. C++ ``std::move``).
        """
        return self.format_call_arg_ref_identifier

    @cached_property
    def consumable_ref_value_inhibits_consuming_form(
        self,
    ) -> Callable[[Value], bool]:
        """Predicate deciding whether a ref's underlying value type
        inhibits the consume form.

        Delegates to :data:`never_inhibits_consuming_form`.  Languages
        whose consume operator rejects certain value types (notably
        the Mojo ``^`` on register-trivial scalars) override this.
        """
        return never_inhibits_consuming_form

    @cached_property
    def _init_element_to_type(
        self,
    ) -> Callable[[type | ListType | DictType], str | None]:
        """Element-to-type resolver for the configured Go types."""
        _type_names: dict[type, str] = {
            datetime.date: "time.Time",
            datetime.datetime: "time.Time",
            str: "string",
        }
        suffix_is_auto = self.numeric_literal_suffix.name == "AUTO"
        go_int_type = "int64" if suffix_is_auto else "int"
        _type_names[int] = go_int_type
        date_type = _type_names.get(self.date_format.value.type_produced)
        datetime_type = _type_names.get(
            self.datetime_format.value.type_produced,
        )
        return make_element_to_type(
            str_type="string",
            bool_type="bool",
            int_type=go_int_type,
            float_type="float64",
            mixed_numeric_type="float64",
            bytes_type="string",
            date_type=date_type,
            datetime_type=datetime_type,
            time_type="string",
            list_template="[]{inner}",
            enable_list_type=True,
            dict_type_template=f"map[{self.default_dict_key_type}]{{inner}}",
            fallback_value_type="any",
            wide_int_type=None,
        )

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return self.sequence_format.value

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        base_set_config: SetFormatConfig = self.set_format(
            default_type=self.default_set_element_type,
        )
        return base_set_config.with_typed_opener(
            type_to_opener=make_type_to_opener(
                element_to_type=self._init_element_to_type,
                opener_template="map[{type_name}]struct{{}}{{",
            ),
            fallback=base_set_config.set_open([]),
        )

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence.

        Under the ``RECORD`` strategy a list whose elements are
        record-shaped dicts is rendered as ``[]any{ RecordN{...}, ... }``
        (the elements format as struct literals, not as the
        ``map[string]...`` the typed opener would otherwise infer).
        """
        base = typed_collection_open(
            type_to_opener=make_type_to_opener(
                element_to_type=self._init_element_to_type,
                opener_template="[]{type_name}{{",
            ),
            fallback=f"[]{self.default_sequence_element_type}{{",
        )
        record = type(self.heterogeneous_strategy).RECORD
        if self.heterogeneous_strategy is not record:
            return base
        any_open = f"[]{self.default_sequence_element_type}{{"

        def _open(items: list[Value], /) -> str:
            """Use ``[]any{`` for lists of record-shaped dicts."""
            if any(
                isinstance(item, dict) and not isinstance(item, _ordereddict)
                for item in items
            ):
                return any_open
            return base(items)

        return _open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=typed_dict_open(
                type_to_opener=make_type_to_opener(
                    element_to_type=self._init_element_to_type,
                    opener_template=f"map[{self.default_dict_key_type}]{{type_name}}{{{{",
                ),
                fallback=f"map[{self.default_dict_key_type}]{self.default_dict_value_type}{{",
            ),
            close="}",
            format_entry=dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
            narrowed_open="{",
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
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        return format_time_iso

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        base_int_formatter = self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )
        suffix_is_auto = self.numeric_literal_suffix.name == "AUTO"
        base: Callable[[int], str] = (
            make_int64_cast_formatter(base=base_int_formatter)
            if suffix_is_auto
            else base_int_formatter
        )
        return make_overflow_fallback_formatter(
            base=base,
            fallback=make_unsigned_overflow_fallback(
                format_positive=_format_go_uint64_positive,
                language_name="Go",
            ),
            min_value=I64_MIN,
            max_value=I64_MAX,
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(
                open_str=f"[][2]{self.default_ordered_map_value_type}{{"
            ),
            close="}",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return braced_dict_entry(format_value=passthrough_sequence_entry)

    @cached_property
    def statement_terminator(self) -> str:
        """String appended to each call expression."""
        return self.statement_terminator_style.statement_terminator

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return _nil_safe_declaration(
            base_formatter=self.declaration_style.value.formatter,
        )

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
            extra=None,
        )

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Go needs none)."""
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
        return self.call_style.value
