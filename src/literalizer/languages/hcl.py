"""HCL (HashiCorp Configuration Language) language specification."""

import dataclasses
import datetime
import enum
import re
from collections.abc import Callable, Sequence
from functools import cached_property
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
    format_time_iso,
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
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_strings import format_string_backslash_hcl
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
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    VariantMetadata,
    body_preamble_from_scalars,
    default_format_call_variable_assignment,
    default_format_call_variable_declaration,
    default_sequence_binding_declarations,
    default_wrap_calls_with_declarations,
    identity_call_arg,
    identity_call_ref_identifier,
    identity_call_statement,
    identity_call_target,
    identity_constructor_target,
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
    wrap_in_file_noop,
)
from literalizer._types import Value
from literalizer.exceptions import WrapCombinedInFileNotSupportedError

_HCL_DECLARATION_PATTERN = re.compile(pattern=r"^\s*[A-Za-z_]\w*\s*=")


@dataclasses.dataclass
class _HclScanState:
    """Mutable HCL bracket/string scan state across lines."""

    depth: int
    in_string: bool
    escaped: bool


@beartype
def _advance_outside_string(*, char: str, state: _HclScanState) -> None:
    """Update *state* for a character that is not inside a string."""
    match char:
        case '"':
            state.in_string = True
        case "[" | "{" | "(":
            state.depth += 1
        case "]" | "}" | ")":
            state.depth -= 1
        case _:
            pass


@beartype
def _advance_scan_state(*, line: str, state: _HclScanState) -> None:
    r"""Update *state* by scanning brackets and strings in *line*.

    Tracks ``\`` escapes inside strings so a backslash-escaped quote
    (``"a\"b"``) does not flip ``in_string`` at the wrong character.
    Without this, an odd number of escaped quotes would leave the
    scanner stuck inside a phantom string and merge later statements
    into it.
    """
    for char in line:
        if state.escaped:
            state.escaped = False
            continue
        if state.in_string:
            match char:
                case "\\":
                    state.escaped = True
                case '"':
                    state.in_string = False
                case _:
                    pass
            continue
        _advance_outside_string(char=char, state=state)


@beartype
def _split_top_level_statements(*, content: str) -> list[str]:
    r"""Split *content* into top-level HCL statements.

    A statement boundary is a line that returns the bracket and string
    nesting to depth zero.  Multi-line list or object literals stay
    grouped with their opening line so a declaration like ``name = [\n
    ...\n]`` is preserved as a single statement.
    """
    statements: list[str] = []
    current: list[str] = []
    state = _HclScanState(depth=0, in_string=False, escaped=False)
    for line in content.split(sep="\n"):
        current.append(line)
        _advance_scan_state(line=line, state=state)
        if state.depth == 0 and not state.in_string:
            statements.append("\n".join(current))
            current = []
    return statements


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Hcl(metaclass=LanguageCls):
    """HCL (HashiCorp Configuration Language) language specification."""

    format_integer_widened = no_format_integer_widened
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    format_call_variable_declaration = default_format_call_variable_declaration
    format_call_variable_assignment = default_format_call_variable_assignment
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".hcl"
    pygments_name = "hcl"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = True
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = False
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    allows_empty_call_parens = True
    supports_dotted_call_stub = False
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
    supports_default_dict_key_type = False
    supports_default_dict_value_type = False
    supports_default_sequence_element_type = False
    supports_default_set_element_type = False
    supports_default_ordered_map_value_type = False
    non_default_kwargs: ClassVar[dict[str, str]] = {}
    declaration_style_sequence_format_overrides: ClassVar[dict[str, str]] = {}
    json_type_variant_name_suffix: ClassVar[str | None] = None
    variant_metadata: ClassVar[VariantMetadata] = VariantMetadata(
        pre_indent_comment_scalar_variant=False,
        collection_layout_category="collection_layout",
        record_variants=frozenset(),
        nested_map_widening=NestedMapWideningVariant.NONE,
        modifier_sequence_format_overrides={},
    )
    supports_record_struct_name_prefix = False
    supports_record_shape_names = False
    supports_non_string_dict_keys = True

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

    class DateFormats(enum.Enum):
        """Date format options for Hcl."""

        ISO = DateFormatConfig(
            formatter=format_date_iso, type_produced=str, preamble_lines=()
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Hcl."""

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
        """Sequence type options for HCL."""

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
        """Set type options for HCL."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="["),
            close="]",
            empty_set=None,
            preamble_lines=(),
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
        BLOCK = CommentConfig(
            prefix="/*",
            suffix=" */",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        ASSIGN = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="{name} = {value}"
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
        positive_infinity="inf",
        negative_infinity="-inf",
        nan="nan",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.auto()

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

        SEMICOLON = enum.auto()

    statement_terminator_styles = StatementTerminatorStyles

    class CallStyles(enum.Enum):
        """Hcl call style options."""

        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )

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

    class JsonTypes(enum.Enum):
        """Empty: this language has no JSON value-type variants."""

    json_types = JsonTypes

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for HCL."""

        V2 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
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

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap code in a valid HCL file.

        When *variable_name* is empty (call rendering), bare function
        calls are not valid HCL, so each is assigned to a unique local
        ``_N``.  Top-level ``name = value`` statements (including
        multi-line list/object literals) are already valid HCL and pass
        through unchanged so a mixed file of variable declarations and
        calls parses correctly.
        """
        if variable_name:
            return wrap_in_file_noop(
                content=content,
                variable_name=variable_name,
                body_preamble=body_preamble,
            )
        statements = _split_top_level_statements(content=content)
        rendered: list[str] = []
        call_counter = 0
        comment_prefix = self.comment_config.prefix
        for statement in statements:
            first_line = statement.split(sep="\n", maxsplit=1)[0]
            if first_line.lstrip().startswith(
                comment_prefix
            ) or _HCL_DECLARATION_PATTERN.match(string=first_line):
                rendered.append(statement)
            else:
                rendered.append(f"_{call_counter} = {statement}")
                call_counter += 1
        result = "\n".join(rendered)
        return prepend_body_preamble(
            content=result,
            body_preamble=body_preamble,
        )

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

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.HASH
    declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN
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
        StatementTerminatorStyles.SEMICOLON
    )
    call_style: CallStyles = CallStyles.POSITIONAL
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    language_version: VersionFormats = VersionFormats.V2
    indent: str = "    "

    null_literal: ClassVar[str] = "null"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = True
    statement_terminator: ClassVar[str] = ""
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash_hcl

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Format an int value as a literal."""
        return str

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
        return no_call_stub

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
        return DictFormatConfig(
            dict_open=fixed_open(open_str="{"),
            close="}",
            format_entry=dict_entry_with_separator(
                separator=" = ",
                format_value=passthrough_sequence_entry,
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
            separator=" = ",
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
        """Per-instance scalar preamble (HCL needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (HCL needs none)."""
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
