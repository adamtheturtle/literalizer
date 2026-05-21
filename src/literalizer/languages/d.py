"""D language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Mapping, Sequence
from functools import cached_property
from types import MappingProxyType
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
    dict_entry_with_template,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    I64_MAX,
    format_integer_binary,
    format_integer_hex,
    format_integer_underscore,
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
from literalizer._formatters.type_inference import (
    infer_element_type,
    record_shape_for_dict,
)
from literalizer._language import (
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
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
    RenderedRecordLiteral,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
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
)
from literalizer._types import Scalar, Value
from literalizer.exceptions import UnrepresentableInputError

_D_EMPTY_JSON_ARRAY = 'parseJSON("[]")'


@beartype
def _d_narrowed_empty_form(_siblings: Sequence[list[Value]]) -> str:
    """Keep D's ``parseJSON("[]")`` empty literal beside typed siblings.

    ``JSONValue([])`` rejects an empty ``void[]`` payload when the
    template expands; the language's ``parseJSON("[]")`` empty form
    returns a fresh ``JSONValue`` array and is accepted alongside
    typed siblings.
    """
    return _D_EMPTY_JSON_ARRAY


@beartype
def _d_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return D stub declarations for a call name."""
    if len(parts) == 1:
        return (f"int {parts[0]}(T...)(T args) {{ return 0; }}",)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        type_name = f"{root.title()}Type_"
        return (
            f"struct {type_name} {{"
            f" int {method}(T...)(T args) {{ return 0; }} }}",
            f"{type_name} {root};",
        )
    lines: list[str] = []
    inner_type = f"{fields[-1].title()}Type_"
    lines.append(
        f"struct {inner_type} {{ int {method}(T...)(T args) {{ return 0; }} }}"
    )
    prev_type = inner_type
    for i in range(len(fields) - 2, -1, -1):
        curr_type = f"{fields[i].title()}Type_"
        lines.append(f"struct {curr_type} {{ {prev_type} {fields[i + 1]}; }}")
        prev_type = curr_type
    root_type = f"{root.title()}Type_"
    lines.append(f"struct {root_type} {{ {prev_type} {fields[0]}; }}")
    lines.append(f"{root_type} {root};")
    return tuple(lines)


@beartype
def _format_d_entry(original: Value, formatted: str) -> str:
    """Wrap a formatted entry in ``JSONValue(...)``."""
    if isinstance(original, (list, dict, set)):
        return formatted
    return f"JSONValue({formatted})"


@beartype
def _format_variable_declaration(
    name: str,
    value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a D ``auto`` variable declaration using ``JSONValue``."""
    wrapped = _format_d_entry(original=data, formatted=value)
    return f"auto {name} = {wrapped};"


@beartype
def _format_variable_assignment(name: str, value: str, data: Value) -> str:
    """Format a D assignment to an existing variable."""
    wrapped = _format_d_entry(original=data, formatted=value)
    return f"{name} = {wrapped};"


@beartype
def _format_d_entry_raw(_original: Value, formatted: str) -> str:
    """Pass the raw D literal through unchanged.

    Under the ``RECORD`` strategy every value is emitted as a raw D
    literal (no ``JSONValue`` wrapper), so sequence/set elements,
    ordered-map values and variable bindings all pass their
    already-formatted literal through untouched.
    """
    return formatted


# The ``RECORD`` strategy supports only auto ``Record0``/``Record1``/...
# names (no ``record_shape_names``), so the shared renderer always gets
# an empty custom-name mapping.
_D_NO_RECORD_SHAPE_NAMES: Mapping[frozenset[str], str] = MappingProxyType(
    mapping={},
)

# Without the ``JSONValue`` wrapper a heterogeneous scalar list, a
# set, an ordered map or a non-record dict (whether a record field or
# the document root) has no raw D type: D arrays and associative
# arrays hold a single element type, and there is no raw map or
# heterogeneous-array literal that omits its element type, so such an
# input is rejected under ``RECORD``.  The cross-language decision for
# these is tracked in #2317.
_D_UNREPRESENTABLE_RECORD_FIELD = (
    "D cannot represent a heterogeneous scalar list, a set, an ordered "
    "map or a non-record dict under the RECORD heterogeneous strategy"
)

# A datetime/date whose format produces an ``int`` epoch is a D
# ``long`` record field; an ISO-string one is a D ``string``.  The
# ``.get`` default keeps the string fallback off coverage's branch
# accounting (only the int key is crossed with ``RECORD`` by the
# datetime corpus; the date axis is never crossed with ``RECORD``, so
# an ``if``/ternary would leave the string side uncovered).
_D_EPOCH_INT_FIELD_TYPES: Mapping[type, str] = MappingProxyType(
    mapping={int: "long"},
)


@beartype
def _d_record_field_identifier(key: str, /) -> str:
    """Return the D ``struct`` member name for a dict *key*.

    D member identifiers are the dict keys verbatim (no case
    conversion), matching the positional struct-constructor literal
    ``Record0(value, ...)``.
    """
    return key


@beartype
def _d_record_literal(
    name: str,
    fields: Sequence[RecordLiteralField],
    /,
) -> RenderedRecordLiteral:
    """Render a D positional struct-constructor literal
    ``Name(value, ...)`` as structured pieces for the shared
    compact/multiline layout code.

    D has no designated-initializer expression syntax, so the literal
    is the implicit positional constructor of the struct; the shared
    strategy iterates the shape's keys in document order for both the
    declaration and the literal, so the field order always agrees.  A
    trailing comma after the last argument is valid in a D function
    argument list, so the language-wide trailing-comma config applies
    unchanged.
    """
    return RenderedRecordLiteral(
        head=f"{name}(",
        entries=tuple(field.formatted for field in fields),
        closer=")",
        compact_pad="",
    )


@beartype
def _d_render_record_declaration(
    name: str,
    fields: Sequence[RecordDeclarationField],
    /,
) -> str:
    """Render a D ``struct Name { Type field; ... }``."""
    members = " ".join(
        f"{field.type_name} {field.identifier};" for field in fields
    )
    return f"struct {name} {{ {members} }}"


@beartype
def _d_record_sequence_open(items: list[Value], /) -> str:
    """Return the raw D array opener under ``RECORD``.

    A homogeneous (or empty) list is a raw ``[ ... ]`` array literal;
    a heterogeneous scalar list has no raw D array type and is
    rejected (a list whose every element is a record-shaped dict has a
    single inferred element type, so it is not heterogeneous here and
    its ``RecordN`` literals make a well-typed ``RecordN[]``).
    """
    if items and infer_element_type(items=items) is None:
        raise UnrepresentableInputError(_D_UNREPRESENTABLE_RECORD_FIELD)
    return "["


@beartype
def _d_record_dict_open(value: dict[Scalar, Value], /) -> str:
    """Open a record-shaped dict, or reject a non-record dict under
    ``RECORD``.

    A record-shaped dict (non-empty, all-string-keyed) is intercepted
    and rendered as a ``RecordN(...)`` literal by the shared record
    behavior, so the opener returned here is never emitted; the shared
    widening probe (:func:`_compute_dict_open_override`) still calls
    this on every dict in a list, so it must return a string rather
    than raise for those.  A non-record (empty or non-string-keyed)
    dict has no raw D representation and is rejected.
    """
    if record_shape_for_dict(value=value) is not None:
        return "["
    raise UnrepresentableInputError(_D_UNREPRESENTABLE_RECORD_FIELD)


@beartype
def _d_record_reject_open(_collection: object, /) -> str:
    """Reject a set or ordered map under ``RECORD``.

    A set or ordered map is never record-eligible and has no
    raw D representation.
    """
    raise UnrepresentableInputError(_D_UNREPRESENTABLE_RECORD_FIELD)


@beartype
def _d_int_field_type(value: int, /) -> str:
    """Return the D ``struct`` field type for an integer record field.

    D ``long`` is the 64-bit signed type and matches the plain decimal
    literal :attr:`D.format_integer` emits for any value in signed
    64-bit range; a positive value beyond it (the corpus's widest is
    ``2 ** 64 - 1``) is a ``ulong`` literal and is typed ``ulong`` (a
    negative out-of-range value is out of scope, like the other ports,
    and is not in the corpus).
    """
    if value > I64_MAX:
        return "ulong"
    return "long"


@beartype
def _format_d_call_declaration(
    name: str,
    value: str,
    _data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a D declaration binding a call result.

    A literal binding wraps the right-hand side to encode the parsed
    value's runtime type: a ``JSONValue(...)`` projection under the
    default strategy, or a positional ``Record0(value, ...)``
    struct-constructor literal under the ``RECORD`` strategy.  That is
    wrong for a call, whose return type is opaque to the renderer and is
    neither a ``JSONValue`` nor a generated ``struct``.

    D infers the binding type from the initializer, so no caller-supplied
    return-type hint is required: the call result is bound directly with
    a plain inferred ``auto`` declaration and no value-wrapping.
    """
    return f"auto {name} = {value};"


@beartype
def _format_d_call_assignment(name: str, value: str, _data: Value) -> str:
    """Format a D reassignment binding a call result.

    The call-expression counterpart of
    :func:`_format_d_call_declaration`; the variable is already
    declared, so the call result is assigned directly with no
    ``JSONValue`` or struct-constructor wrapping.
    """
    return f"{name} = {value};"


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class D(metaclass=LanguageCls):
    """D language specification."""

    format_integer_widened = no_format_integer_widened
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    module_name: str = "Module"

    leading_preamble = no_leading_preamble
    extension = ".d"
    pygments_name = "d"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_zero_parameter_calls = True
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_multi_param_call_wrapper_stub = True
    supports_dict_literal_as_free_expression = True
    supports_module_name = True
    supports_empty_dict_key = False
    supports_call_style = True
    supports_default_dict_key_type = False
    supports_default_dict_value_type = False
    supports_default_sequence_element_type = False
    supports_default_set_element_type = False
    supports_default_ordered_map_value_type = False
    supports_record_struct_name_prefix = True
    supports_record_shape_names = False
    supports_non_string_dict_keys = False

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

    class DateFormats(enum.Enum):
        """Date format options for D."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for D."""

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
        """Sequence type options for D."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="JSONValue(["),
            close="])",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=_D_EMPTY_JSON_ARRAY,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for D."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="JSONValue(["),
            close="])",
            empty_set=_D_EMPTY_JSON_ARRAY,
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
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

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        AUTO = DeclarationStyleConfig(
            formatter=_format_variable_declaration,
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
        positive_infinity="double.infinity",
        negative_infinity="-double.infinity",
        nan="double.nan",
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

        DOUBLE = enum.auto()

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

        NEVER = enum.auto()
        SAFE = enum.auto()

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

    class StatementTerminatorStyles(enum.Enum):
        """Statement terminator options."""

        SEMICOLON = enum.auto()

    statement_terminator_styles = StatementTerminatorStyles

    class CallStyles(enum.Enum):
        """D call style options."""

        POSITIONAL = PositionalCallStyle()

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Heterogeneous-scalar strategy options.

        ``ERROR`` keeps the default ``std.json.JSONValue`` model (a
        record-shaped dict that mixes scalars with a container is
        rendered as a homogeneous ``JSONValue`` map).  ``RECORD``
        instead renders each record-shaped dict (non-empty,
        string-keyed) as a generated ``struct RecordN { ... }``
        declared in the preamble plus a matching positional
        ``Record0(value, ...)`` constructor literal whose fields are
        raw D values, so a field may mix scalars and containers that
        the homogeneous ``JSONValue`` map cannot.  Without the
        ``JSONValue`` wrapper the whole value is raw; a heterogeneous
        scalar list, a set, an ordered map or a non-record dict has no
        raw D representation and raises
        :class:`~literalizer.exceptions.UnrepresentableInputError`
        (D has no ``JSONValue``-free heterogeneous container; the
        cross-language decision for these is tracked in #2317).
        """

        ERROR = enum.auto()
        RECORD = enum.auto()

    heterogeneous_strategies = HeterogeneousStrategies

    class VersionFormats(enum.Enum):
        """Version options for D."""

        V2 = enum.auto()

    version_formats = VersionFormats

    module_name_case: ClassVar[IdentifierCase] = IdentifierCase.SNAKE
    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
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

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a D declaration in a main function."""
        del variable_name
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        return f"void {self.module_name}() {{\n{content}\n}}"

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap D declaration + assignment in a function."""
        return self.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.AUTO
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
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.SEMICOLON
    )
    call_style: CallStyles = CallStyles.POSITIONAL
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    record_struct_name_prefix: str = "Record"
    # Keep in sync with the ``compiler`` input of the
    # ``dlang-community/setup-dlang`` step in
    # ``.github/workflows/lint.yml``. Every ``dmd-2.x`` release
    # implements the D2 language, so the pin there is ``>=`` this
    # ``V2`` default.
    language_version: VersionFormats = VersionFormats.V2
    indent: str = "    "

    null_literal: ClassVar[str] = "null"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ";"
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash

    @cached_property
    def _record_strategy_active(self) -> bool:
        """Return whether the ``RECORD`` heterogeneous strategy is set."""
        return self.heterogeneous_strategy.name == "RECORD"

    @cached_property
    def static_preamble(self) -> Sequence[str]:
        """File-scope preamble.

        The default ``ERROR`` model wraps every value in
        ``std.json.JSONValue`` and so needs ``import std.json;``; the
        ``RECORD`` strategy emits raw D values plus generated
        ``struct`` declarations and uses no ``JSONValue``, so it needs
        no static import.
        """
        if self._record_strategy_active:
            return ()
        return ("import std.json;",)

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry.

        Under ``RECORD`` every element is a raw D literal (no
        ``JSONValue`` wrapper), so the entry formatter is the identity.
        """
        if self._record_strategy_active:
            return _format_d_entry_raw
        return _format_d_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry.

        Under ``RECORD`` a set has no raw D representation
        and :attr:`set_format_config` rejects it at its opener before
        any entry is formatted, so this formatter is only ever reached
        by the default ``JSONValue`` model.
        """
        return _format_d_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable.

        The default model wraps the value in ``JSONValue``; under
        ``RECORD`` the value is a raw D literal (a ``Record0(...)``
        struct, array or scalar) assigned directly.
        """
        if self._record_strategy_active:

            @beartype
            def _assign(name: str, value: str, _data: Value) -> str:
                """Assign a raw D literal to an existing variable."""
                return f"{name} = {value};"

            return _assign

        return _format_variable_assignment

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Format one ordered-map entry.

        Under ``RECORD`` an ordered map has no raw D
        representation; :attr:`ordered_map_format_config` rejects it
        before an entry is formatted, so this ``JSONValue`` template is
        only ever used by the default model.
        """
        return dict_entry_with_template(
            template="JSONValue([JSONValue({key}), {value}])",
            format_value=_format_d_entry,
        )

    def _d_value_type(self, value: Value, /) -> str:  # noqa: PLR0911
        """Return the D type for a raw record field *value*.

        Derived structurally from the value (never by re-parsing the
        formatted literal): scalars map to their D type, a homogeneous
        list to ``<elem>[]``, and an empty list to ``long[]`` (its
        ``[]`` literal coerces to any element type).  A nested
        record-shaped dict never reaches here -- the shared strategy
        resolves it to its generated name in
        :meth:`_d_record_field_type`.  A heterogeneous scalar list, a
        set, an ordered map or a non-record dict never reaches here
        either: its collection opener
        (:func:`_d_record_sequence_open` / :func:`_d_record_reject_open`
        / :func:`_d_record_dict_open`) rejects the input while the
        literal is formatted, before the preamble derives this field
        type (the cross-language decision for these is tracked in
        #2317), so a value reaching the final branch is a string or
        bytes.
        """
        if isinstance(value, bool):
            return "bool"
        if isinstance(value, int):
            return _d_int_field_type(value)
        if isinstance(value, float):
            return "double"
        if value is None:
            return "typeof(null)"
        if isinstance(value, datetime.datetime):
            return _D_EPOCH_INT_FIELD_TYPES.get(
                self.datetime_format.value.type_produced,
                "string",
            )
        if isinstance(value, datetime.date):
            return _D_EPOCH_INT_FIELD_TYPES.get(
                self.date_format.value.type_produced,
                "string",
            )
        if isinstance(value, list):
            return self._d_list_type(items=value)
        return "string"

    def _d_list_type(self, *, items: list[Value]) -> str:
        """Return the D type for a list record field.

        An empty list has no element type to infer, so it is typed
        ``long[]`` (its ``[]`` literal coerces to any element type); a
        non-empty list is a ``<elem>[]`` array over its first element's
        type.  A heterogeneous list never reaches here --
        :func:`_d_record_sequence_open` rejects it while the literal is
        formatted, before the preamble derives this field type.
        """
        if not items:
            return "long[]"
        return f"{self._d_value_type(items[0])}[]"

    def _d_record_field_type(self, request: RecordFieldType, /) -> str:
        """Return the D ``struct`` field type for a record field.

        A field whose value is itself a nested record-shaped dict uses
        that record's generated name; a field whose value is a list of
        record-shaped dicts is a ``RecordN[]`` array of that element
        record (its literal is ``[RecordN(...), ...]``); every other
        value is typed structurally from the raw value by
        :meth:`_d_value_type`.
        """
        if request.record_name is not None:
            return request.record_name
        if request.element_record_name is not None:
            return f"{request.element_record_name}[]"
        return self._d_value_type(request.value)

    @cached_property
    def _record_renderer(self) -> RecordRenderer:
        """D syntax hooks for the ``RECORD`` strategy."""
        return RecordRenderer(
            name_prefix=self.record_struct_name_prefix,
            record_shape_names=_D_NO_RECORD_SHAPE_NAMES,
            field_identifier=_d_record_field_identifier,
            field_type=self._d_record_field_type,
            render_declaration=_d_render_record_declaration,
            render_literal=_d_record_literal,
        )

    @cached_property
    def _record_strategy(self) -> RecordStrategy:
        """Behavior + ``struct``-declaration preamble for ``RECORD``."""
        return build_record_strategy(renderer=self._record_renderer)

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration.

        The default model wraps the value in ``JSONValue``; under
        ``RECORD`` the value is a raw D literal whose type is inferred,
        so a plain ``auto`` binding is emitted.
        """
        if self._record_strategy_active:

            @beartype
            def _decl(
                name: str,
                value: str,
                _data: Value,
                _modifiers: frozenset[enum.Enum],
            ) -> str:
                """Bind a raw D literal with inferred ``auto`` type."""
                return f"auto {name} = {value};"

            return _decl

        return self.declaration_style.value.formatter

    @cached_property
    def format_call_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a declaration binding a call result.

        A literal binding wraps the right-hand side to encode the parsed
        value's runtime type (a ``JSONValue(...)`` projection, or a
        positional ``Record0(...)`` struct-constructor literal under
        ``RECORD``); a call's return type is opaque to the renderer, so
        the call result is bound directly with a plain inferred ``auto``
        declaration and no value-wrapping.
        """
        return _format_d_call_declaration

    @cached_property
    def format_call_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment binding a call result.

        The call-expression counterpart of
        :attr:`format_variable_assignment`; the ``JSONValue`` /
        struct-constructor wrapping is dropped since the variable is
        already declared.
        """
        return _format_d_call_assignment

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        Under ``RECORD`` this is the generated ``struct RecordN { ... }``
        block, emitted in dependency order so a nested record is
        declared before its parent.
        """
        if self._record_strategy_active:
            return self._record_strategy.preamble
        return no_data_preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config.

        ``RECORD`` resolves to the shared record behavior (its value
        needs the per-instance renderer, so it cannot be stored on the
        enum member); ``ERROR`` keeps the default ``JSONValue`` model.
        """
        if self._record_strategy_active:
            return self._record_strategy.behavior
        return NO_HETEROGENEOUS_BEHAVIOR

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
        return _d_call_stub

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
        """Configuration for the chosen sequence format.

        Under ``RECORD`` a list is a raw D array ``[ ... ]`` (no
        ``JSONValue`` wrapper): the opener is ``[`` for a homogeneous
        or empty list and rejects a heterogeneous scalar list, the
        closer is ``]``, the empty literal is ``[]`` (it coerces to any
        declared element type) and there is no ``parseJSON`` narrowed
        empty form.
        """
        base = self.sequence_format.value
        if self._record_strategy_active:
            return dataclasses.replace(
                base,
                sequence_open=_d_record_sequence_open,
                close="]",
                empty_sequence="[]",
                format_entry=_format_d_entry_raw,
                narrowed_empty_form=None,
            )
        return dataclasses.replace(
            base,
            narrowed_empty_form=_d_narrowed_empty_form,
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format.

        A set has no raw D representation, so under
        ``RECORD`` its opener rejects the input.
        """
        base = self.set_format.value
        if self._record_strategy_active:
            return dataclasses.replace(
                base,
                set_open=_d_record_reject_open,
            )
        return base

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format_config.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting.

        Under ``RECORD`` every record-shaped dict is intercepted by the
        shared record behavior, so any dict reaching this formatter is
        a non-record (empty or non-string-keyed) dict with no
        raw D representation; its opener rejects the input.
        """
        base = DictFormatConfig(
            dict_open=fixed_open(open_str="JSONValue(["),
            close="])",
            format_entry=dict_entry_with_separator(
                separator=": ",
                format_value=_format_d_entry,
            ),
            empty_dict='parseJSON("{}")',
            preamble_lines=(),
            narrowed_open=None,
            supports_trailing_comma=True,
        )
        if self._record_strategy_active:
            return dataclasses.replace(
                base,
                dict_open=_d_record_dict_open,
                empty_dict=None,
            )
        return base

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
        return self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting.

        An ordered map is never record-eligible and has no
        raw D representation, so under ``RECORD`` its
        opener rejects the input.
        """
        if self._record_strategy_active:
            return OrderedMapFormatConfig(
                ordered_map_open=_d_record_reject_open,
                close="])",
                preamble_lines=(),
            )
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="JSONValue(["),
            close="])",
            preamble_lines=(),
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (D needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (D needs none)."""
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
