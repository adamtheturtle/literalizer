"""Roc language specification."""

import dataclasses
import datetime as dt
import enum
import math
import re
from collections.abc import Callable, Mapping, Sequence
from functools import cached_property
from typing import ClassVar

from beartype import beartype

from literalizer._comments import TabFreeCommentPrefix
from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    datetime_epoch_formatter,
    format_date_iso,
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
from literalizer._formatters.format_integers import (
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    make_overflow_fallback_formatter,
    raise_for_unrepresentable_int,
)
from literalizer._formatters.format_strings import (
    escape_control_chars,
)
from literalizer._formatters.type_inference import (
    RecordShape,
    collect_record_shapes,
)
from literalizer._language import (
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
    BareIntegerWidthStrategies,
    CallParameterShadowing,
    CallStubResult,
    CallStyle,
    CommentConfig,
    DateFormatConfig,
    DateFormatEnum,
    DatetimeFormatConfig,
    DatetimeFormatEnum,
    DeclarationStyleConfig,
    DictFormatConfig,
    FileWrapperContext,
    FloatSpecialsMixin,
    FormatValueMixin,
    HeterogeneousBehavior,
    IdentifierCase,
    JsonType,
    LanguageCls,
    ModifierCombination,
    NewVariableNameSyntax,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    RenderedRecordLiteral,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    VariantMetadata,
    default_call_data_dependent_preamble,
    default_consumable_ref_value_inhibits_consuming_form,
    default_format_call_arg_ref_identifier,
    default_format_call_arg_ref_identifier_consumable,
    default_format_call_ref_identifier,
    default_format_call_statement,
    default_format_call_stub,
    default_format_call_variable_assignment,
    default_sequence_binding_declarations,
    default_type_hint_collection_preamble_lines,
    default_validate_call_arg,
    empty_scalar_preamble,
    identity_constructor_target,
    no_call_binding_body_preamble,
    no_call_binding_file_pragmas,
    no_data_preamble,
    no_format_integer_beyond_i64,
    no_format_integer_widened,
    no_leading_preamble,
    unsupported_wrap_combined_in_file_static,
)
from literalizer._statements import (
    insert_before_line_comment,
    split_statements,
)
from literalizer._types import OrderedMap, Scalar, Value
from literalizer.exceptions import (
    UnrepresentableInputError,
)


@beartype
def _escape_roc_string_body(value: str) -> str:
    r"""Apply Roc string escapes to *value* (no surrounding quotes).

    Escapes ``\\``, ``"``, ``\r``, ``\n``, ``\t``, the interpolation
    sequences ``$(`` and ``${``, and other C0 control characters via
    ``\u(XXXX)``.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("$(", "\\$(")
        .replace("${", "\\${")
    )
    return escape_control_chars(
        value=escaped,
        fmt="\\u({:04x})",
        escape_delete=False,
    )


@beartype
def _format_roc_string_literal(value: str) -> str:
    """Quote and escape strings, including unprintable Unicode."""
    literal = f'"{_escape_roc_string_body(value=value)}"'
    return "".join(
        character if character.isprintable() else f"\\u({ord(character):04x})"
        for character in literal
    )


_I128_MIN = -(2**127)
_I128_MAX = 2**127 - 1


@beartype
def _roc_dict_entry(
    key: str,
    _raw_value: Value,
    formatted_value: str,
) -> str:
    """Format a dict entry with its already-rendered plain-string key."""
    return f"({key}, {formatted_value})"


@beartype
def _build_roc_body_preamble(
    *,
    type_name: str,
    constructor_prefix: str,
    datetime_type_produced: type,
) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
    """Build a callable that computes body-preamble lines for Roc.

    The callable receives the set of types present in the data and
    returns the nominal tag union with only the constructors that
    are actually needed.
    """

    @beartype
    def _compute(types: frozenset[type], data: Value, /) -> tuple[str, ...]:
        """Return the nominal tag union for *types*."""
        del data  # unused
        p = constructor_prefix
        int_types: set[type] = {int}
        str_types: set[type] = {str, bytes, dt.date}
        if datetime_type_produced is int:
            int_types.add(dt.datetime)
        else:
            str_types.add(dt.datetime)

        constructors = [
            constructor
            for type_set, constructor in (
                (frozenset({type(None)}), f"{p}Null"),
                (frozenset({bool}), f"{p}Bool(Bool)"),
                (frozenset(int_types), f"{p}Int(I128)"),
                (frozenset({float}), f"{p}Float(F64)"),
                (frozenset(str_types), f"{p}Str(Str)"),
                (
                    frozenset({list}),
                    f"{p}List(List({type_name}))",
                ),
                (
                    frozenset({dict, OrderedMap}),
                    f"{p}Dict(List((Str, {type_name})))",
                ),
                (
                    frozenset({set}),
                    f"{p}Set(List({type_name}))",
                ),
            )
            if len(types & type_set) > 0
        ]
        body = ",\n".join(f"    {c}" for c in constructors)
        return (f"{type_name} := [\n{body},\n]",)

    return _compute


@beartype
def _roc_record_literal(
    _value: dict[Scalar, Value], formatted_fields: Mapping[str, str]
) -> RenderedRecordLiteral:
    """Render a string-keyed object using native Roc record syntax."""
    return RenderedRecordLiteral(
        head="{",
        entries=tuple(
            f"{key}: {value}" for key, value in formatted_fields.items()
        ),
        closer="}",
        compact_pad=" ",
    )


@beartype
def _roc_record_shapes(data: Value, /) -> Mapping[int, RecordShape]:
    """Collect the record-shaped dictionaries in a native Roc value."""
    return collect_record_shapes(data=data)


_ROC_RECORD_RESERVED_FIELDS = frozenset(
    {
        "app",
        "as",
        "dbg",
        "else",
        "expect",
        "exposing",
        "if",
        "import",
        "is",
        "module",
        "package",
        "platform",
        "return",
        "then",
        "try",
        "when",
    }
)


@beartype
def _roc_native_type_shape(data: Value) -> str:
    """Describe a value's native type for sibling-record validation."""
    result: str
    if isinstance(data, dict):
        fields = tuple(
            sorted(
                (
                    key if isinstance(key, str) else "<invalid>",
                    _roc_native_type_shape(data=value),
                )
                for key, value in data.items()
            )
        )
        result = f"record:{fields!r}"
    elif isinstance(data, list):
        element_types = sorted(
            {_roc_native_type_shape(data=value) for value in data}
        )
        result = f"list:{element_types!r}"
    elif isinstance(data, bool):
        result = "bool"
    elif isinstance(data, int):
        result = "int"
    elif isinstance(data, float):
        result = "float"
    elif isinstance(data, (str, bytes, dt.date, dt.time)):
        result = "str"
    elif data is None:
        result = "null"
    else:
        result = type(data).__name__
    return result


@beartype
def _validate_roc_record_data(data: Value) -> None:
    """Reject shapes that the opt-in native record mode cannot
    preserve.
    """
    if isinstance(data, OrderedMap):
        msg = "Roc native record mode cannot represent ordered maps"
        raise UnrepresentableInputError(msg)
    if isinstance(data, dict):
        for key, value in data.items():
            if (
                not isinstance(key, str)
                or re.fullmatch(pattern=r"[a-z][A-Za-z0-9_]*", string=key)
                is None
                or key in _ROC_RECORD_RESERVED_FIELDS
            ):
                msg = f"Roc native record mode cannot represent field {key!r}"
                raise UnrepresentableInputError(msg)
            _validate_roc_record_data(data=value)
    elif isinstance(data, list):
        record_types = {
            _roc_native_type_shape(data=value)
            for value in data
            if isinstance(value, dict)
        }
        if len(record_types) > 1:
            msg = "Roc native record mode requires uniform record list types"
            raise UnrepresentableInputError(msg)
        for value in data:
            _validate_roc_record_data(data=value)
    elif isinstance(data, set):
        msg = "Roc native record mode cannot represent sets"
        raise UnrepresentableInputError(msg)


@beartype
def _roc_format_call_target(parts: Sequence[str]) -> str:
    """Flatten a sequence of call target parts to an underscored Roc
    identifier.

    Roc identifiers cannot contain ``.``, so ``["app", "client",
    "fetch"]`` becomes ``app_client_fetch``.
    """
    return "_".join(parts)


@beartype
def _roc_call_body_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _result: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Declare a polymorphic function with unused parameter bindings."""
    name = _roc_format_call_target(parts=parts)
    wildcards = ", ".join("_" for _ in params)
    return (f"{name} = |{wildcards}| {{}}",)


@beartype
def _roc_closed_call(*, statement: str) -> str:
    """Return *statement* with its ``dbg`` closer before any comment."""
    return insert_before_line_comment(
        statement=statement,
        text=")",
        quotes='"',
        line_comment_prefixes=("#",),
    )


@beartype
def _indent_call_lines(*, content: str, indent: str) -> str:
    """Wrap each call line of *content* in ``dbg (...)`` for a Roc
    ``main`` body.

    *content* is one single-line call expression per line: this is the
    only shape produced by ``literalize_call`` for Roc, which uses
    :attr:`CollectionLayout.COMPACT` for wrapped calls and rejects
    standalone comments in that path.  Wrapping each line in
    ``dbg (...)`` prevents Roc from flagging the discarded
    pure-function result as an ``UNNECESSARY DEFINITION``.
    """
    return "\n".join(
        f"{indent}dbg ({_roc_closed_call(statement=statement)}".replace(
            "\n", f"\n{indent}"
        )
        for statement in split_statements(
            content=content,
            quotes='"',
            line_comment_prefixes=("#",),
        )
    )


@beartype
def _no_record_body_preamble(
    _types: frozenset[type], _data: Value, /
) -> tuple[str, ...]:
    """Native records need no tag-union body preamble."""
    return ()


@beartype
def _roc_nominal_scalar[DataT](
    *, constructor: str | None, formatter: Callable[[DataT], str]
) -> Callable[[DataT], str]:
    """Compose a raw scalar formatter with a new-compiler constructor."""

    @beartype
    def format_value(value: DataT) -> str:
        """Render a scalar, optionally tagging it for the nominal
        union.
        """
        literal = formatter(value)
        if constructor is None:
            return literal
        return f"{constructor}({literal})"

    return format_value


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Roc(metaclass=LanguageCls):
    """Roc language specification.

    The generated output uses custom tag constructors (``RNull``,
    ``RBool``, ``RList``, ``RDict``, ``RSet``) that are wrapped in a
    ``Val`` nominal tag union emitted in the body preamble. For
    example, data consisting solely of an integer yields:

    .. code-block:: text

       Val := [
           RInt(I128),
       ]

    Set ``dict_format=Roc.dict_formats.RECORD`` to emit native Roc
    records with scalar and list values without tags instead.  This mode
    rejects keys that are not Roc field identifiers, ordered maps, and
    sets; the default tagged representation remains available for them.
    Null has no native Roc literal and remains an inferred ``RNull`` tag.

    The default and only target, ``Roc.version_formats.V1``, uses compiler
    nightly ``2026-11-15-f25da45``. It uses nominal value unions,
    parenthesized constructors and calls, and typed numeric literals.
    Wrapped files are complete default-platform apps with a ``main!``
    entry point. The former ``V0`` target is retired.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.ISO`` — ISO 8601 string,
              e.g. ``RStr("2024-01-15")``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.ISO`` — ISO 8601 string,
              e.g. ``RStr("2024-01-15T12:30:00")``.

        type_name: Name of the generated tag-union alias.  Defaults to
            ``"Val"``.

        constructor_prefix: Prefix for generated constructor names.
            Defaults to ``"R"``, producing constructors like ``RNull``,
            ``RBool``, ``RInt``, etc.
        dict_format: ``DEFAULT`` for tagged pairs or ``RECORD`` for
            native records.
    """

    format_call_class_scope_stub = default_format_call_stub

    reserved_module_identifiers: ClassVar[frozenset[str]] = frozenset()
    immutable_variable_modifiers: ClassVar[frozenset[enum.Enum]] = frozenset()
    wrap_in_file_tolerates_pre_indent = True
    module_name_shares_variable_scope = False
    reserved_variable_identifier_pattern: ClassVar[re.Pattern[str] | None] = (
        None
    )
    reserved_call_parameter_identifiers: ClassVar[frozenset[str]] = frozenset()
    reserved_call_parameter_identifier_pattern: ClassVar[
        re.Pattern[str] | None
    ] = None
    uses_data_keyword_for_algebraic_constructors = False
    accepts_type_name_call_target = True
    declares_type_name_call_target = False
    dotted_call_root_shares_entrypoint_namespace = True
    reserved_bare_call_target_identifiers: ClassVar[frozenset[str]] = (
        frozenset()
    )
    reserved_call_target_head_identifiers: ClassVar[frozenset[str]] = (
        frozenset()
    )
    call_parameter_shadowing = CallParameterShadowing.ALLOWED
    reserved_call_target_keywords_case_sensitive = True
    module_name_must_start_uppercase = False
    new_variable_name_syntax = NewVariableNameSyntax.LOWER_LETTER_ASCII
    max_variable_identifier_length: ClassVar[int | None] = None
    call_stub_result: ClassVar[CallStubResult | None] = None
    call_literal_syntax: ClassVar[None] = None
    call_target_name_syntax: ClassVar[NewVariableNameSyntax | None] = None
    supports_multiline_dict_layout = True
    pools_map_integer_width = True

    format_integer_widened = no_format_integer_widened
    format_integer_beyond_i64 = no_format_integer_beyond_i64
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    format_call_variable_assignment = default_format_call_variable_assignment
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".roc"
    pygments_name = "text"
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    wraps_data_dependent_preamble_in_body = False
    dict_supports_heterogeneous_values = True
    supports_local_binding_documents = False
    supports_stateful_free_call_consumers = False
    supports_stateful_receiver_result_checks = False
    supports_native_invocations = False
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    declares_call_parameter_names = True
    reserved_variable_identifiers_case_sensitive: bool = True
    contextual_call_target_identifiers: ClassVar[frozenset[str]] = (
        # The words a module header is spelled from.  They are keywords
        # only there, so a value may still take the name.
        frozenset(
            {
                "app",
                "exposing",
                "interface",
                "module",
                "package",
                "platform",
                "provides",
                "requires",
            }
        )
    )
    reserved_variable_identifiers: frozenset[str] = frozenset(
        {
            "app",
            "as",
            "crash",
            "else",
            "expect",
            "exposing",
            "for",
            "if",
            "import",
            "interface",
            "module",
            "package",
            "platform",
            "provides",
            "requires",
            "returns",
            "then",
            "to",
            "type",
        }
    )
    allows_empty_call_parens = True
    supports_dotted_call_stub = False
    dotted_call_stub_indexes_colliding_helpers = False
    call_returns_expression = True
    supports_json_call_result_binding = False
    supports_zero_parameter_calls = True
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = False
    supports_multi_param_call_wrapper_stub = True
    supports_variadic_calls = False
    supports_dict_literal_as_free_expression = True
    supports_module_name = False
    supports_empty_dict_key = False
    supports_call_style = True
    supports_bare_mapping_documents = False
    supports_json_object_documents = False
    supports_default_dict_key_type = False
    supports_default_dict_value_type = False
    supports_nullable_object_fallbacks = False
    supports_default_sequence_element_type = False
    supports_key_value_assignment_documents = False
    supports_default_set_element_type = False
    supports_default_ordered_map_value_type = False
    json_type_variant_name_suffix: ClassVar[str | None] = None
    supports_non_ascii_string_literals = True
    supports_multiline_string_literals = False
    supports_empty_sibling_sequence_type_hints = True
    supports_typed_dict_open = False
    language_id: ClassVar[str] = "roc"
    variant_metadata: ClassVar[VariantMetadata] = VariantMetadata(
        round_trip_capabilities=frozenset(),
        modifier_sequence_format_overrides={},
        string_literals_escape_null_byte=True,
        supports_ref_elements_in_tuple_strategy=False,
    )
    supports_record_struct_name_prefix = False
    supports_record_shape_names = False
    record_shape_names_emit_declarations = False
    supports_non_string_dict_keys = False
    checks_raw_control_dict_keys_separately = False
    stringifies_nested_collections = False
    supports_special_floats = True

    class DateFormats(DateFormatEnum):
        """Date format options for Roc."""

        ISO = DateFormatConfig(
            formatter=format_date_iso,
            type_produced=str,
            preamble_lines=(),
        )

    class DatetimeFormats(DatetimeFormatEnum):
        """Datetime format options for Roc."""

        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            type_produced=str,
            preamble_lines=(),
        )

        EPOCH = DatetimeFormatConfig(
            formatter=datetime_epoch_formatter(format_integer=str),
            type_produced=int,
            preamble_lines=(),
        )

    class BytesFormats(FormatValueMixin[Callable[[bytes], str]], enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)
        BASE64 = enum.member(value=format_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Roc."""

        LIST = SequenceFormatConfig(
            length_is_part_of_type=False,
            sequence_open=fixed_open(open_str="RList(["),
            close="])",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            single_element_template=None,
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
        """Set type options for Roc."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="RSet(["),
            close="])",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        HASH = CommentConfig(
            prefix=TabFreeCommentPrefix(object="#"),
            suffix="",
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
        """Tagged key-value pairs, preserving arbitrary string keys."""

        RECORD = enum.auto()
        """Native records and untagged scalar/list values where
        possible.
        """

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="RFloat(F64.infinity)",
        negative_infinity="RFloat(-F64.infinity)",
        nan="RFloat(F64.nan)",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(FormatValueMixin[Callable[[int], str]], enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=str)
        HEX = enum.member(value=format_integer_hex)
        OCTAL = enum.member(value=format_integer_octal)
        BINARY = enum.member(value=format_integer_binary)

        def __call__(self, value: int, /) -> str:
            """Format an integer."""
            formatter: Callable[[int], str] = self.value
            return formatter(value)

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
    integer_width_strategies = BareIntegerWidthStrategies
    numeric_literal_suffixes = NumericLiteralSuffixes
    numeric_separators = NumericSeparators
    numeric_styles = NumericStyles
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class StatementTerminatorStyles(enum.Enum):
        """Statement terminator options."""

        NONE = enum.auto()

    statement_terminator_styles = StatementTerminatorStyles

    class CallStyles(enum.Enum):
        """Roc call style options."""

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

    class JsonTypes(JsonType):
        """Empty: this language has no JSON value-type variants."""

    json_types = JsonTypes

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for Roc."""

        V1 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.PASCAL,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    def validate_spec_for_data(self, data: Value) -> None:
        """Ensure native-record output has only representable shapes."""
        if self.dict_format is type(self.dict_format).RECORD:
            _validate_roc_record_data(data=data)

    validate_call_arg = default_validate_call_arg

    format_call_statement = default_format_call_statement

    def wrap_in_file(self, content: str, context: FileWrapperContext) -> str:
        """Wrap a value or pure calls in a complete default-platform app.

        Keep the nominal value type only when a literal declaration uses it.
        Call results use ``dbg (...)`` so the compiler accepts their disposal.
        """
        content = re.sub(
            pattern=r"(?m)^([ \t]+)([A-Za-z_][A-Za-z0-9_]*) : ([^\n]+)\n\2 =",
            repl="\\1\\2 : \\3\\n\\1\\2 =",
            string=content,
        )
        variable_name = context.variable_name
        preamble_str = self._body_preamble_text(context=context)
        if variable_name == "":
            return self._wrap_calls(
                declarations=(), calls=content, preamble=preamble_str
            )
        return (
            f"{preamble_str}{content}\n\n"
            f"main! = |_args| {{\n{self.indent}_ = {variable_name}\n"
            f"{self.indent}Ok({{}})\n}}"
        )

    def _wrap_calls(
        self, *, declarations: tuple[str, ...], calls: str, preamble: str
    ) -> str:
        """Host pure calls in a complete new-compiler default app."""
        decl_block = "\n".join(declarations)
        body = _indent_call_lines(content=calls, indent=self.indent)
        return (
            f"{preamble}{decl_block}\n\nmain! = |_args| {{\n"
            f"{body}\n{self.indent}Ok({{}})\n}}"
        )

    @staticmethod
    def _body_preamble_text(
        *,
        context: FileWrapperContext,
    ) -> str:
        """Keep generated aliases only for literal-binding
        declarations.
        """
        effective_preamble = context.body_preamble
        if not context.has_literal_declarations:
            effective_preamble = tuple(
                entry
                for entry in context.body_preamble
                if entry not in context.generated_body_preamble
            )
        if len(effective_preamble) == 0:
            return ""
        return "\n".join(effective_preamble) + "\n\n"

    def wrap_calls_with_declarations(
        self,
        declarations: tuple[str, ...],
        calls: str,
        context: FileWrapperContext,
    ) -> str:
        """Keep declarations at app scope and execute calls in
        ``main!``.
        """
        preamble_str = self._body_preamble_text(context=context)
        return self._wrap_calls(
            declarations=declarations, calls=calls, preamble=preamble_str
        )

    wrap_combined_in_file: ClassVar[
        "staticmethod[[str, str, FileWrapperContext], str]"
    ] = unsupported_wrap_combined_in_file_static

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
        StatementTerminatorStyles.NONE
    )
    call_style: CallStyles = CallStyles.POSITIONAL
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    # Keep in sync with the pinned ``ROC_NIGHTLY_BUILD`` downloaded in
    # the ``Install Roc`` step of ``.github/workflows/lint.yml``. Roc
    # has no stable release and no ``--langversion``-style flag, so the
    # pinned nightly build is the only mechanism for pinning the
    # version; ``V1`` maps to ``2026-11-15-f25da45``. Keep the platform
    # in scripts/run_roc_roundtrip.py paired with this compiler.
    language_version: VersionFormats = VersionFormats.V1
    indent: str = "    "
    type_name: str = "Val"
    constructor_prefix: str = "R"

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
    @beartype
    def call_style_config(self) -> CallStyle:
        """Configuration for the Roc call style."""
        return self.call_style.value

    @cached_property
    @beartype
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    @beartype
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    @beartype
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Use the nominal type emitted by
        :meth:`compute_body_preamble`.
        """
        return no_data_preamble

    @cached_property
    @beartype
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config."""
        if self.dict_format is type(self.dict_format).RECORD:
            return dataclasses.replace(
                NO_HETEROGENEOUS_BEHAVIOR,
                compute_record_shapes=_roc_record_shapes,
                render_record_literal=_roc_record_literal,
            )
        return self.heterogeneous_strategy.value

    call_data_dependent_preamble = default_call_data_dependent_preamble

    type_hint_collection_preamble_lines = (
        default_type_hint_collection_preamble_lines
    )

    @cached_property
    @beartype
    def format_call_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Declare polymorphic functions before the app's calls."""
        return _roc_call_body_stub

    format_call_preamble_stub = default_format_call_stub

    @cached_property
    @beartype
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Keep arguments unchanged inside positional call parentheses."""
        return passthrough_sequence_entry

    @cached_property
    @beartype
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into a Roc identifier."""
        return _roc_format_call_target

    format_call_ref_identifier = default_format_call_ref_identifier

    format_call_arg_ref_identifier = default_format_call_arg_ref_identifier

    format_call_arg_ref_identifier_consumable = (
        default_format_call_arg_ref_identifier_consumable
    )

    consumable_ref_value_inhibits_consuming_form = (
        default_consumable_ref_value_inhibits_consuming_form
    )

    @cached_property
    @beartype
    def null_literal(self) -> str:
        """Literal representing ``None``."""
        return f"{self.constructor_prefix}Null"

    @cached_property
    @beartype
    def true_literal(self) -> str:
        """Literal representing ``True``."""
        if self.dict_format is type(self.dict_format).RECORD:
            return "Bool.True"
        return f"{self.constructor_prefix}Bool(Bool.True)"

    @cached_property
    @beartype
    def false_literal(self) -> str:
        """Literal representing ``False``."""
        if self.dict_format is type(self.dict_format).RECORD:
            return "Bool.False"
        return f"{self.constructor_prefix}Bool(Bool.False)"

    @cached_property
    @beartype
    def _seq_open(self) -> Callable[[list[Value]], str]:
        """Shared sequence opener with configured constructor prefix."""
        if self.dict_format is type(self.dict_format).RECORD:
            return fixed_open(open_str="[")
        return fixed_open(open_str=f"{self.constructor_prefix}List([")

    @cached_property
    @beartype
    def _dict_entry(self) -> Callable[[str, Value, str], str]:
        """Shared dict-entry formatter used by dict and ordered-map."""
        return _roc_dict_entry

    @cached_property
    @beartype
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return dataclasses.replace(
            self.sequence_format.value,
            sequence_open=self._seq_open,
            close="])"
            if self.dict_format is not type(self.dict_format).RECORD
            else "]",
            supports_heterogeneity=self.dict_format
            is not type(self.dict_format).RECORD,
            requires_uniform_record_shapes=self.dict_format
            is type(self.dict_format).RECORD,
        )

    @cached_property
    @beartype
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self._seq_open

    @cached_property
    @beartype
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return dataclasses.replace(
            self.set_format.value,
            set_open=fixed_open(open_str=f"{self.constructor_prefix}Set(["),
        )

    @cached_property
    @beartype
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        if self.dict_format is type(self.dict_format).RECORD:
            return DictFormatConfig(
                dict_open=fixed_open(open_str="{"),
                close="}",
                format_entry=dict_entry_with_separator(
                    separator=": ", format_value=passthrough_sequence_entry
                ),
                empty_dict=None,
                preamble_lines=(),
                narrowed_open=None,
                supports_trailing_comma=True,
                narrowed_empty_form=None,
            )
        return DictFormatConfig(
            dict_open=fixed_open(open_str=f"{self.constructor_prefix}Dict(["),
            close="])",
            format_entry=self._dict_entry,
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
            supports_trailing_comma=True,
            narrowed_empty_form=None,
        )

    @cached_property
    @beartype
    def trailing_comma_config(self) -> TrailingCommaConfig:
        """Configuration for trailing-comma behavior."""
        return self.trailing_comma.value

    @cached_property
    @beartype
    def format_bytes(self) -> Callable[[bytes], str]:
        """Callable that formats a bytes value as a string literal."""
        return _roc_nominal_scalar(
            constructor=self._constructor(tag="Str"),
            formatter=self.bytes_format,
        )

    @cached_property
    @beartype
    def format_date(self) -> Callable[[dt.date], str]:
        """Callable that formats a date as a string literal."""
        return _roc_nominal_scalar(
            constructor=self._constructor(tag="Str"), formatter=format_date_iso
        )

    @cached_property
    @beartype
    def format_datetime(self) -> Callable[[dt.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        if self.datetime_format is self.datetime_formats.EPOCH:
            return datetime_epoch_formatter(format_integer=self.format_integer)
        return _roc_nominal_scalar(
            constructor=self._constructor(tag="Str"),
            formatter=format_datetime_iso,
        )

    @cached_property
    @beartype
    def format_time(self) -> Callable[[dt.time], str]:
        """Callable that formats a time as a string literal."""
        return _roc_nominal_scalar(
            constructor=self._constructor(tag="Str"), formatter=format_time_iso
        )

    @cached_property
    @beartype
    def format_dict_key(self) -> Callable[[str], str]:
        """Render a string key without a value constructor."""
        return _format_roc_string_literal

    @cached_property
    @beartype
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        return _roc_nominal_scalar(
            constructor=self._constructor(tag="Str"),
            formatter=_format_roc_string_literal,
        )

    @cached_property
    @beartype
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        base = self.integer_format

        @beartype
        def integer(value: int) -> str:
            """Pin a raw integer to the union's I128 payload type."""
            return f"{base(value)}.I128"

        return _roc_nominal_scalar(
            constructor=self._constructor(tag="Int"),
            formatter=make_overflow_fallback_formatter(
                base=integer,
                min_value=_I128_MIN,
                max_value=_I128_MAX,
                fallback=raise_for_unrepresentable_int(language_name="Roc"),
            ),
        )

    @cached_property
    @beartype
    def format_float(self) -> Callable[[float], str]:
        """Format the new compiler's finite and special float values."""
        base = self.float_format

        @beartype
        def floating(value: float) -> str:
            """Pin finite literals and spell the new float constants."""
            if math.isnan(value):
                return "F64.nan"
            if math.isinf(value):
                return "-F64.infinity" if value < 0 else "F64.infinity"
            return f"{base(value).replace('e+', 'e')}.F64"

        return _roc_nominal_scalar(
            constructor=self._constructor(tag="Float"), formatter=floating
        )

    @cached_property
    @beartype
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    @beartype
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(
                open_str=f"{self.constructor_prefix}Dict(["
            ),
            close="])",
            preamble_lines=(),
        )

    @cached_property
    @beartype
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return self._dict_entry

    @cached_property
    @beartype
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        _base_declaration = self.declaration_style.value.formatter
        if self.dict_format is type(self.dict_format).RECORD:
            return _base_declaration
        _type_name = self.type_name

        @beartype
        def _roc_declaration(
            name: str,
            value: str,
            data: Value,
            _modifiers: frozenset[enum.Enum],
        ) -> str:
            """Format a Roc variable declaration with type annotation."""
            base = _base_declaration(name, value, data, _modifiers)
            return f"{name} : {_type_name}\n{base}"

        return _roc_declaration

    @cached_property
    @beartype
    def format_call_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a declaration binding a call expression.

        The literal-binding declaration emits a ``name : Val``
        annotation derived from the bound value's runtime tag-union
        type; a call expression has no such tag, so the annotation is
        omitted and Roc infers the call's return type instead.
        """
        return self.declaration_style.value.formatter

    def assignment_declares_binding(self, _data: Value, /) -> bool:
        """Retain whether the configured literal assignment declares a
        name.
        """
        return self.dict_format is type(self.dict_format).RECORD

    reference_assignment_declares_binding = assignment_declares_binding
    call_assignment_declares_binding = True

    @cached_property
    @beartype
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        return variable_formatter(template="{name} = {value}")

    @cached_property
    @beartype
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Roc needs none)."""
        return {}

    scalar_body_preamble: ClassVar[
        cached_property[dict[type, tuple[str, ...]]]
    ] = cached_property(func=empty_scalar_preamble)

    @cached_property
    @beartype
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Declare the nominal value type for the required data tags."""
        if self.dict_format is type(self.dict_format).RECORD:
            return _no_record_body_preamble
        return _build_roc_body_preamble(
            type_name=self.type_name,
            constructor_prefix=self.constructor_prefix,
            datetime_type_produced=self.datetime_format.value.type_produced,
        )

    def _constructor(self, *, tag: str) -> str | None:
        """Select a nominal payload constructor or a native scalar."""
        if self.dict_format is self.dict_formats.RECORD:
            return None
        return f"{self.constructor_prefix}{tag}"
