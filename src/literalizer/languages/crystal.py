"""Crystal language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Mapping, Sequence
from functools import cached_property, partial
from types import MappingProxyType
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
    make_element_to_type,
    make_narrowed_empty_form,
)
from literalizer._formatters.format_dates import (
    datetime_epoch_seconds,
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
from literalizer._formatters.format_factories import (
    dict_format_factory,
    set_format_factory,
)
from literalizer._formatters.format_floats import (
    data_has_special_float,
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    I64_MAX,
    I64_MIN,
    format_integer_underscore,
    make_overflow_fallback_formatter,
)
from literalizer._formatters.format_strings import (
    format_string_backslash_hash_nul_hex,
)
from literalizer._formatters.record_strategy import (
    RecordDeclarationField,
    RecordFieldType,
    RecordLiteralField,
    RecordRenderer,
    RecordStrategy,
    build_record_strategy,
)
from literalizer._formatters.type_inference import record_shape_for_dict
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
    JsonType,
    KeywordCallStyle,
    LanguageCls,
    ModifierCombination,
    NestedMapWideningVariant,
    NewVariableNameSyntax,
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
    no_format_integer_beyond_i64,
    no_format_integer_widened,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    prepend_body_preamble,
)
from literalizer._types import OrderedMap, Scalar, Value
from literalizer.exceptions import (
    UnrepresentableInputError,
    UnrepresentableSpecialFloatError,
)

_CRYSTAL_JSON_ANY = "JSON::Any"
_CRYSTAL_RECORD_MAP_VALUE = "LiteralizerRecordValue"
_CRYSTAL_RECORD_MAP_TYPE = f"Hash(String, {_CRYSTAL_RECORD_MAP_VALUE})"
_CRYSTAL_RECORD_MAP_ALIAS = (
    f"alias {_CRYSTAL_RECORD_MAP_VALUE} = "
    "Bool | Float64 | Int128 | Int32 | Int64 | String | Nil"
)


@beartype
def _wrap_in_json_parse(value: str, /) -> str:
    """Wrap a rendered JSON literal in ``JSON.parse(%(...))``.

    The inner *value* is already a valid JSON document; the
    ``%(...)`` percent literal embeds it as a Crystal string so it can
    be parsed at runtime into a ``JSON::Any``.
    """
    return f"JSON.parse(%({value}))"


@beartype
def _format_crystal_json_call_arg(_raw_value: Value, formatted: str) -> str:
    """Format a Crystal call argument as ``JSON::Any``.

    The argument is wrapped in ``JSON.parse(%(...))`` so the receiving
    proc gets a ``JSON::Any`` regardless of the underlying scalar or
    container type.
    """
    return _wrap_in_json_parse(formatted)


@beartype
def _format_crystal_json_assignment(
    name: str,
    value: str,
    _data: Value,
) -> str:
    """Assign a JSON-rendered literal to a ``JSON::Any`` binding."""
    return f"{name} = {_wrap_in_json_parse(value)}"


@beartype
def _crystal_json_declaration_formatter(
    name: str,
    value: str,
    _data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a Crystal ``JSON::Any`` variable declaration.

    Crystal exposes only the ``ASSIGN`` declaration style, so the
    formatter does not need to branch on the declaration keyword.
    """
    return f"{name} = {_wrap_in_json_parse(value)}"


@beartype
def _to_pascal_case(name: str) -> str:
    """Convert *name* to PascalCase."""
    return IdentifierCase.PASCAL.convert(name=name)


@beartype
def _format_constructor_target(class_name: str, /) -> str:
    """Return a Crystal ``ClassName.new`` constructor call target."""
    return f"{class_name}.new"


_constructor_target: Callable[[str], str] = _format_constructor_target


_crystal_narrowed_empty_form = make_narrowed_empty_form(
    element_to_type=make_element_to_type(
        str_type="String",
        bool_type="Bool",
        int_type="Int32",
        float_type="Float64",
        mixed_numeric_type="String",
        bytes_type="String",
        date_type="String",
        datetime_type="String",
        time_type="String",
        list_template="Array({inner})",
        enable_list_type=True,
        dict_type_template="Hash(String, {inner})",
        fallback_value_type="String",
        wide_int_type=None,
        beyond_i64_type=None,
    ),
    template="[] of {type}",
    fallback_type="String",
)


@beartype
def _format_crystal_i128_literal(value: int) -> str:
    """Format an out-of-range integer with a Crystal ``_i128`` suffix.

    Crystal rejects bare integer literals outside the signed 64-bit
    range; the ``_i128`` suffix selects ``Int128``, which covers
    ``-2^127`` to ``2^127 - 1``.
    """
    return f"{value}_i128"


# Crystal infers a bare integer literal as ``Int32`` when it fits the
# signed 32-bit range and ``Int64`` when it only fits the signed 64-bit
# range, so a ``RECORD`` integer field is typed by the same thresholds
# to match the rendered literal.  Keep these bounds in sync with
# ``_I32_MIN`` / ``_I32_MAX`` in
# :mod:`literalizer._formatters.type_inference` (the widening threshold
# the value formatter uses for homogeneous lists, which has a
# back-reference to here).
_CRYSTAL_I32_MIN = -(2**31)
_CRYSTAL_I32_MAX = 2**31 - 1

# The ``RECORD`` strategy supports only auto ``Record0``/``Record1``/...
# names (no ``record_shape_names``), so the shared renderer always gets
# an empty custom-name mapping.
_CRYSTAL_NO_RECORD_SHAPE_NAMES: Mapping[frozenset[str], str] = (
    MappingProxyType(mapping={})
)

# Crystal scalar type for a record field, keyed by the value's exact
# Python type.  ``bool`` and ``int`` are not here (they have dedicated
# width-aware handling); a ``bytes`` value renders as a hex/base64
# string and every date/datetime/time format Crystal supports renders
# a string, so they all map to ``String``.  An ``EPOCH`` datetime is
# converted to its epoch integer before the lookup, so the ``datetime``
# entry only ever resolves an ISO datetime.
_CRYSTAL_SCALAR_FIELD_TYPE: Mapping[type, str] = MappingProxyType(
    mapping={
        type(None): "Nil",
        float: "Float64",
        str: "String",
        bytes: "String",
        datetime.date: "String",
        datetime.datetime: "String",
        datetime.time: "String",
    },
)


@beartype
def _crystal_union(parts: set[str], /) -> str:
    """Join Crystal type names into a union the way the compiler prints
    one for an inferred container literal.

    The compiler orders union members by ascending type name with
    ``Nil`` forced last (``Int32 | String``, ``Bool | Int32 |
    String``, ``Int32 | String | Nil``), and a single member is printed
    without a ``|``.  An ``Array``/``Hash`` field is invariant in its
    element type, so the declared element union must match the
    literal's inferred one exactly.
    """
    return " | ".join(
        sorted(parts, key=lambda part: (part == "Nil", part)),
    )


@beartype
def _crystal_int_field_type(*, value: int) -> str:
    """Return the Crystal ``record`` field type for an integer value.

    Mirrors the literal :attr:`Crystal.format_integer` emits: a value
    inside signed 32-bit range is a bare ``Int32`` literal, one only
    inside signed 64-bit range is a bare ``Int64`` literal, and a value
    beyond signed 64-bit range carries the ``_i128`` overflow-fallback
    suffix and is therefore ``Int128``.
    """
    if _CRYSTAL_I32_MIN <= value <= _CRYSTAL_I32_MAX:
        return "Int32"
    if I64_MIN <= value <= I64_MAX:
        return "Int64"
    return "Int128"


@beartype
def _crystal_record_field_identifier(key: str, /) -> str:
    """Return the Crystal ``record`` field name for a dict *key*.

    Crystal field identifiers are the dict keys verbatim (no case
    conversion); the literal is the positional ``Record0.new(...)``
    constructor the ``record`` macro generates, so the field names
    appear only in the declaration.
    """
    return key


@beartype
def _crystal_record_literal(
    name: str,
    fields: Sequence[RecordLiteralField],
    /,
) -> RenderedRecordLiteral:
    """Render a Crystal ``Name.new(value, ...)`` constructor call as
    structured pieces for the shared compact/multiline layout code.

    The ``record`` macro generates a positional initializer in
    declaration order; the shared strategy iterates the shape's keys in
    document order for both the declaration and the literal, so the
    argument order always matches the field order.  A trailing comma
    after the last argument is valid in a Crystal call, so the
    language-wide trailing-comma config applies unchanged.
    """
    return RenderedRecordLiteral(
        head=f"{name}.new(",
        entries=tuple(field.formatted for field in fields),
        closer=")",
        compact_pad="",
    )


@beartype
def _crystal_render_record_declaration(
    name: str,
    fields: Sequence[RecordDeclarationField],
    /,
) -> str:
    """Render a Crystal ``record Name, field : Type, ...`` declaration.

    The ``record`` macro expands to a ``struct`` with a positional
    initializer and one getter per field, which is exactly what the
    generated ``Name.new(...)`` literal needs.
    """
    members = ", ".join(
        f"{field.identifier} : {field.type_name}" for field in fields
    )
    return f"record {name}, {members}"


@beartype
def _crystal_call_stub(
    format_class_name: Callable[[str], str],
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Crystal stub declarations for a call name."""
    param_list = ", ".join(f"{param} = nil" for param in params)
    method_stub = f"def {{name}}({param_list}); 0; end"
    if len(parts) == 1:
        return (method_stub.format(name=parts[0]),)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        cls = format_class_name(root) + "Type_"
        return (
            f"class {cls}; {method_stub.format(name=method)}; end",
            f"{root} = {cls}.new",
        )
    lines: list[str] = []
    inner_cls = format_class_name(fields[-1]) + "Type_"
    lines.append(f"class {inner_cls}; {method_stub.format(name=method)}; end")
    prev_cls = inner_cls
    for i in range(len(fields) - 2, -1, -1):
        cls = format_class_name(fields[i]) + "Type_"
        lines.append(
            f"class {cls}; def {fields[i + 1]}; {prev_cls}.new; end; end"
        )
        prev_cls = cls
    root_cls = format_class_name(root) + "Type_"
    lines.append(
        f"class {root_cls}; def {fields[0]}; {prev_cls}.new; end; end"
    )
    lines.append(f"{root} = {root_cls}.new")
    return tuple(lines)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Crystal(metaclass=LanguageCls):
    """Crystal language specification.

    Args:
        sequence_format: Which Crystal sequence type to use.

            * ``sequence_formats.ARRAY`` — array literal,
              e.g. ``[1, 2, 3]``.
            * ``sequence_formats.TUPLE`` — tuple literal,
              e.g. ``{1, 2, 3}``.
    """

    new_variable_name_syntax: ClassVar[NewVariableNameSyntax] = (
        NewVariableNameSyntax.LOWER_ASCII
    )

    format_integer_widened = no_format_integer_widened
    format_integer_beyond_i64 = no_format_integer_beyond_i64
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(_constructor_target)
    )
    format_call_variable_declaration = default_format_call_variable_declaration
    format_call_variable_assignment = default_format_call_variable_assignment
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".cr"
    pygments_name = "crystal"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = True
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    reserved_variable_identifiers_case_sensitive: bool = True
    reserved_variable_identifiers: frozenset[str] = frozenset(
        {
            "abstract",
            "alias",
            "asm",
            "begin",
            "break",
            "case",
            "class",
            "def",
            "do",
            "else",
            "elsif",
            "end",
            "ensure",
            "extend",
            "false",
            "for",
            "if",
            "in",
            "include",
            "lib",
            "macro",
            "module",
            "next",
            "nil",
            "of",
            "out",
            "private",
            "protected",
            "require",
            "rescue",
            "return",
            "select",
            "self",
            "sizeof",
            "struct",
            "super",
            "then",
            "true",
            "type",
            "typeof",
            "union",
            "unless",
            "until",
            "when",
            "while",
            "with",
            "yield",
        }
    )
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_json_call_result_binding = False
    supports_zero_parameter_calls = True
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_multi_param_call_wrapper_stub = True
    supports_dict_literal_as_free_expression = True
    supports_module_name = True
    supports_empty_dict_key = False
    supports_call_style = True
    supports_default_dict_key_type = True
    supports_default_dict_value_type = True
    supports_default_sequence_element_type = False
    supports_default_set_element_type = True
    supports_default_ordered_map_value_type = False
    non_default_kwargs: ClassVar[dict[str, str]] = {
        "default_set_element_type": "Int32",
        "default_dict_value_type": "Int32",
        "default_dict_key_type": "Int32",
    }
    declaration_style_sequence_format_overrides: ClassVar[dict[str, str]] = {}
    json_type_variant_name_suffix: ClassVar[str | None] = None
    supports_non_ascii_string_literals = True
    variant_metadata: ClassVar[VariantMetadata] = VariantMetadata(
        string_literals_escape_null_byte=True,
        pre_indent_comment_scalar_variant=False,
        fixture_module_name_template="Fixture_{parent}_{stem}",
        fixture_module_name_lowercase=False,
        golden_filename_lowercase=False,
        collection_layout_category="collection_layout",
        record_variants=frozenset({RecordVariant.FIELD_TYPE_SPLIT}),
        nested_map_widening=NestedMapWideningVariant.NONE,
        modifier_sequence_format_overrides={},
    )
    supports_record_struct_name_prefix = True
    supports_record_shape_names = False
    record_shape_names_emit_declarations = False
    supports_non_string_dict_keys = True

    class DateFormats(enum.Enum):
        """Date format options for Crystal."""

        ISO = DateFormatConfig(
            formatter=format_date_iso, type_produced=str, preamble_lines=()
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Crystal."""

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
        """Sequence type options for Crystal."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="["),
            close="]",
            empty_sequence="[] of Nil",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )
        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="{"),
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence="Tuple.new",
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Crystal."""

        SET = enum.member(
            value=set_format_factory(
                open_template="Set{{",
                close="}}",
                empty_template="Set({type}).new",
                preamble_lines=('require "set"',),
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
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = enum.member(
            value=dict_format_factory(
                open_template="{{",
                close="}",
                format_entry=dict_entry_with_separator(
                    separator=" => ",
                    format_value=passthrough_sequence_entry,
                ),
                empty_template="{{}} of {key_type} => {type}",
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
        positive_infinity="Float64::INFINITY",
        negative_infinity="-Float64::INFINITY",
        nan="Float64::NAN",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = MappingProxyType(
            mapping={
                "NONE": lambda value: str(object=value),
                "UNDERSCORE": format_integer_underscore,
            }
        )

        def get_formatter(
            self,
            numeric_separator: enum.Enum,
        ) -> Callable[[int], str]:
            """Return the integer formatter for the given separator."""
            return self.value[numeric_separator.name]

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

    class JsonTypes(JsonType):
        """JSON value type options for Crystal."""

        JSON_ANY = _CRYSTAL_JSON_ANY
        """Standard-library ``JSON::Any`` via ``JSON.parse(%(...))``."""

    json_types = JsonTypes
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
        """Crystal call style options."""

        KEYWORD = KeywordCallStyle(separator=": ")
        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Heterogeneous-scalar strategy options.

        ``ERROR`` raises for any record-shaped dict that mixes scalars
        with a container (``Hash`` requires a homogeneous value type).
        ``RECORD`` instead renders each record-shaped dict (non-empty,
        string-keyed) as a generated ``record`` struct declared in the
        per-fixture module body plus a matching positional
        ``Record0.new(value, ...)`` literal, so such fields are
        representable.
        """

        ERROR = enum.auto()
        RECORD = enum.auto()

    heterogeneous_strategies = HeterogeneousStrategies

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for Crystal."""

        V1 = enum.auto()

    version_formats = VersionFormats

    module_name_case: ClassVar[IdentifierCase] = IdentifierCase.PASCAL
    empty_container_type_hint_variant_kwargs = None

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.UPPER_SNAKE,
        IdentifierCase.PASCAL,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    def validate_spec_for_data(self, data: Value) -> None:
        r"""Validate Crystal-specific data/format combinations.

        Under ``json_type`` every dict key must be a string (a JSON
        object only admits string keys) and every integer must fit the
        ``Int64`` range that Crystal's ``JSON.parse`` exposes through
        ``JSON::Any#as_i``.  Strings embedded in the rendered JSON
        document cannot contain characters the ``%(...)`` percent
        literal interprets specially: ``\\``, ``"``, ``(``, ``)``, or
        ``#{``; we reject those upfront with a clear error rather than
        letting the Crystal compiler or JSON parser fail at runtime.
        """
        if self._uses_json_any:
            if data_has_special_float(data=data):
                msg = (
                    "Crystal(json_type=JSON_ANY) cannot represent special "
                    "floats because JSON.parse accepts only finite numbers."
                )
                raise UnrepresentableSpecialFloatError(msg)
            self._validate_json_any_data(data=data)

    def _validate_json_any_data(self, *, data: Value) -> None:
        """Recursively validate *data* for ``JSON::Any`` rendering."""
        match data:
            case dict():
                self._validate_json_any_dict(data=data)
            case list() | set():
                for item in data:
                    self._validate_json_any_data(data=item)
            case str():
                self._validate_json_any_string(value=data)
            case bool():
                return
            case int():
                self._validate_json_any_int(value=data)
            case _:
                return

    def _validate_json_any_dict(
        self,
        *,
        data: Mapping[Scalar, Value],
    ) -> None:
        """Validate that every dict key is a JSON-compatible string."""
        for key, value in data.items():
            if not isinstance(key, str):
                msg = (
                    "Crystal json_type can only represent dict keys "
                    "as JSON object strings, not "
                    f"{type(key).__name__}"
                )
                raise UnrepresentableInputError(msg)
            self._validate_json_any_string(value=key)
            self._validate_json_any_data(data=value)

    @staticmethod
    def _validate_json_any_int(*, value: int) -> None:
        """Reject integers outside the signed 64-bit ``JSON::Any``
        range.
        """
        if not I64_MIN <= value <= I64_MAX:
            msg = (
                "Crystal json_type cannot represent integer "
                f"{value}: value is outside the signed 64-bit "
                "range that JSON::Any exposes."
            )
            raise UnrepresentableInputError(msg)

    @staticmethod
    def _validate_json_any_string(*, value: str) -> None:
        r"""Reject characters Crystal's ``%(...)`` literal mishandles.

        ``%(...)`` processes the same escapes as a double-quoted
        Crystal string, so a literal ``\\``, ``"``, or ``#{`` inside
        the JSON document would be rewritten before the JSON parser
        sees it; unbalanced ``(`` or ``)`` would terminate the
        percent literal early.  All five cases produce broken Crystal
        source rather than the intended ``JSON::Any``.
        """
        forbidden = {
            "\\": "backslash",
            '"': "double quote",
            "(": "open parenthesis",
            ")": "close parenthesis",
        }
        for char, description in forbidden.items():
            if char in value:
                msg = (
                    f"Crystal json_type cannot embed a {description} in a "
                    "string value: it would break the JSON.parse(%(...)) "
                    "wrapper."
                )
                raise UnrepresentableInputError(msg)
        if "#{" in value:
            msg = (
                "Crystal json_type cannot embed '#{' in a string value: "
                "Crystal's %(...) percent literal would interpret it as "
                "string interpolation."
            )
            raise UnrepresentableInputError(msg)

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
        """Wrap a Crystal declaration in a module."""
        del variable_name
        body = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        return f"module {self.module_name}\nextend self\n{body}\nend"

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Crystal declaration + assignment in a module."""
        return self.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    module_name: str = "Check"
    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.SET
    default_set_element_type: str = "String"
    default_dict_key_type: str = "String"
    default_dict_value_type: str = "String"
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
    call_style: CallStyles = CallStyles.KEYWORD
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    json_type: JsonTypes | None = None
    record_struct_name_prefix: str = "Record"
    # Keep in sync with the ``crystal:`` pin passed to
    # ``crystal-lang/install-crystal`` in the ``lint-crystal`` job of
    # ``.github/workflows/lint.yml``.
    language_version: VersionFormats = VersionFormats.V1
    indent: str = "    "

    _default_null_literal: ClassVar[str] = "nil"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = True
    statement_terminator: ClassVar[str] = ";"
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def _uses_json_any(self) -> bool:
        """Return whether Crystal should render via ``JSON::Any``."""
        return self.json_type is not None

    @cached_property
    def null_literal(self) -> str:
        """Null literal for the active Crystal representation.

        ``JSON::Any`` mode produces JSON documents inside a
        ``JSON.parse(%(...))`` wrapper, so the JSON ``null`` keyword
        replaces Crystal's ``nil``.
        """
        if self._uses_json_any:
            return "null"
        return self._default_null_literal

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash_hash_nul_hex

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        if self._uses_json_any:
            return _format_crystal_json_assignment
        return variable_formatter(template="{name} = {value}")

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Callable that rewrites a formatted direct call argument.

        Under ``json_type`` every call argument is wrapped in
        ``JSON.parse(%(...))`` so the receiving proc gets a
        ``JSON::Any`` regardless of the underlying scalar or container
        shape; otherwise the rendered literal passes through unchanged.
        """
        if self._uses_json_any:
            return _format_crystal_json_call_arg
        return identity_call_arg

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        The ``RECORD`` strategy's generated ``record`` declarations are
        not emitted here (file scope): Crystal compiles every fixture in
        one ``crystal run`` invocation, so a file-scope ``record
        Record0`` would collide across cases.  They are emitted into the
        per-fixture module body instead; see
        :attr:`compute_body_preamble`.

        Under ``json_type`` the rendered output always passes through
        ``JSON.parse``, so ``require "json"`` is contributed
        unconditionally.
        """
        if self._uses_json_any:

            def _json_preamble(_data: Value, /) -> tuple[str, ...]:
                """Always require the standard-library ``json`` module."""
                return ('require "json"',)

            return _json_preamble
        return no_data_preamble

    @cached_property
    def _record_strategy_active(self) -> bool:
        """Return whether the ``RECORD`` heterogeneous strategy is set."""
        return self.heterogeneous_strategy.name == "RECORD"

    def _crystal_type_for_value(self, value: Value, /) -> str:
        """Return the Crystal type the rendered literal for *value*
        compiles to.

        Scalars map to their Crystal type (an integer sized by
        magnitude to match the rendered literal -- ``Int32`` /
        ``Int64`` / the ``_i128``-suffixed ``Int128``; an ``EPOCH``
        datetime renders as its epoch integer and is sized the same
        way, while every other date/datetime/time/bytes format renders
        a string).  A list compiles to ``Array`` of the union of its
        items' types (empty -> ``[] of Nil`` -> ``Array(Nil)``); an
        ordered map compiles to ``Hash`` keyed by
        :attr:`default_dict_key_type` of the union of its value types,
        or -- when empty, matching the ``{} of K => V`` literal the
        formatter emits -- of :attr:`default_dict_value_type`.  The
        union is built to match the compiler's own canonical ordering
        so the invariant ``Array`` / ``Hash`` field type accepts the
        inferred literal.
        """
        if (
            isinstance(value, datetime.datetime)
            and self.datetime_format.value.type_produced is int
        ):
            value = datetime_epoch_seconds(value=value)
        match value:
            case bool():
                return "Bool"
            case int():
                return _crystal_int_field_type(value=value)
            case list() if not value:
                return "Array(Nil)"
            case list():
                parts = {self._crystal_type_for_value(item) for item in value}
                return f"Array({_crystal_union(parts)})"
            case OrderedMap():
                parts = {
                    self._crystal_type_for_value(item)
                    for item in value.values()
                }
                # An empty ordered map renders as ``{} of K => V`` with
                # the configured dict defaults, so the union falls back
                # to ``default_dict_value_type`` (``or`` keeps the
                # never-empty corpus path branch-free).
                value_type = (
                    _crystal_union(parts) or self.default_dict_value_type
                )
                return f"Hash({self.default_dict_key_type}, {value_type})"
            case _:
                # A set or non-record dict field is out of scope for
                # the base ``RECORD`` port (#2317) and is not reached
                # by any record golden; the ``or`` widens it to ``Nil``.
                return _CRYSTAL_SCALAR_FIELD_TYPE.get(type(value)) or "Nil"

    def _crystal_record_field_type(self, request: RecordFieldType, /) -> str:
        """Return the Crystal ``record`` field type for a record field.

        A field whose value is itself a nested record-shaped dict uses
        that record's generated name.  A field whose value is a list of
        single-shape record dicts is an ``Array`` of that record's
        name: Crystal infers the element type from the generated
        ``Name.new(...)`` literals, and ``Array`` is invariant, so the
        declared element type must be the record name (not the widened
        ``Array(Nil)`` :meth:`_crystal_type_for_value` would derive
        from the raw dicts).  Every other value is typed by
        :meth:`_crystal_type_for_value`.  A record-eligible dict with no
        ``record_name`` was widened out of record inference because its
        nested sibling maps cannot share one shape; it uses a ``Hash``
        over the generated native scalar union (#2919).  A set or
        genuinely non-record dict field remains out of scope for the
        base ``RECORD`` port (the cross-language decision is tracked in
        #2317).
        """
        if request.record_name is not None:
            return request.record_name
        if request.element_record_name is not None:
            return f"Array({request.element_record_name})"
        if (
            isinstance(request.value, dict)
            and not isinstance(request.value, OrderedMap)
            and record_shape_for_dict(value=request.value) is not None
        ):
            return _CRYSTAL_RECORD_MAP_TYPE
        return self._crystal_type_for_value(request.value)

    @cached_property
    def _record_renderer(self) -> RecordRenderer:
        """Crystal syntax hooks for the ``RECORD`` strategy."""
        return RecordRenderer(
            name_prefix=self.record_struct_name_prefix,
            record_shape_names=_CRYSTAL_NO_RECORD_SHAPE_NAMES,
            field_identifier=_crystal_record_field_identifier,
            field_type=self._crystal_record_field_type,
            render_declaration=_crystal_render_record_declaration,
            render_literal=_crystal_record_literal,
        )

    @cached_property
    def _record_strategy(self) -> RecordStrategy:
        """Behavior + ``record``-declaration preamble for ``RECORD``."""
        return build_record_strategy(
            renderer=self._record_renderer,
            split_conflicting_field_types=True,
            widen_unrecordizable_nested_sibling_maps=True,
            derecordized_map_open=f"{_CRYSTAL_RECORD_MAP_TYPE}{{",
        )

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config.

        ``json_type`` overrides the configured strategy: JSON arrays
        and objects accept any mix of value types, so scalar-type checks
        are skipped unconditionally.
        ``RECORD`` resolves to the shared record behavior (its value
        needs the per-instance renderer, so it cannot be stored on the
        enum member); ``ERROR`` raises.
        """
        if self._uses_json_any:
            return dataclasses.replace(
                NO_HETEROGENEOUS_BEHAVIOR,
                skip_scalar_checks=True,
            )
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
        return partial(_crystal_call_stub, _to_pascal_case)

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

        ``json_type`` renders sequences as JSON arrays (``[ ... ]``)
        inside the outer ``JSON.parse(%(...))`` wrapper, with no
        Crystal-side typing or trailing comma (the JSON spec rejects
        trailing commas in arrays).
        """
        if self._uses_json_any:
            return SequenceFormatConfig(
                sequence_open=fixed_open(open_str="["),
                close="]",
                empty_sequence="[]",
                supports_heterogeneity=True,
                single_element_trailing_comma=False,
                supports_trailing_comma=False,
                preamble_lines=(),
                format_entry=passthrough_sequence_entry,
                typed_opener_fallback=None,
                uses_typed_literal_for_scalars=False,
                requires_uniform_record_shapes=False,
                declared_type=None,
                narrowed_empty_form=None,
            )
        return dataclasses.replace(
            self.sequence_format.value,
            narrowed_empty_form=_crystal_narrowed_empty_form,
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format.

        ``json_type`` renders a set as a JSON array because JSON has no
        native set type; the empty form widens to ``[]`` for the same
        reason.
        """
        if self._uses_json_any:
            return SetFormatConfig(
                set_open=fixed_open(open_str="["),
                close="]",
                empty_set="[]",
                preamble_lines=(),
                set_opener_template="",
                supports_heterogeneity=True,
                supports_trailing_comma=False,
            )
        return self.set_format(
            default_type=self.default_set_element_type,
        )

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format.value.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting.

        ``json_type`` renders a dict as a JSON object with ``": "`` as
        the entry separator and no trailing comma; the empty form
        widens to ``{}``.
        """
        if self._uses_json_any:
            return DictFormatConfig(
                dict_open=fixed_open(open_str="{"),
                close="}",
                format_entry=dict_entry_with_separator(
                    separator=": ",
                    format_value=passthrough_sequence_entry,
                ),
                empty_dict="{}",
                preamble_lines=(),
                narrowed_open=None,
                supports_trailing_comma=False,
                narrowed_empty_form=None,
            )
        return self.dict_format(
            default_type=self.default_dict_value_type,
            default_key_type=self.default_dict_key_type,
        )

    @cached_property
    def trailing_comma_config(self) -> TrailingCommaConfig:
        """Configuration for trailing-comma behavior.

        ``json_type`` always disables trailing commas because the JSON
        content embedded in ``JSON.parse(%(...))`` is parsed against
        the JSON spec, which rejects trailing commas in arrays and
        objects.
        """
        if self._uses_json_any:
            return TrailingCommaConfig(multiline_trailing_comma=False)
        return self.trailing_comma.value

    @cached_property
    def format_bytes(self) -> Callable[[bytes], str]:
        """Callable that formats a bytes value as a string literal."""
        return self.bytes_format

    @cached_property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a date as a string literal.

        ``json_type`` always emits ISO 8601 dates so the result is a
        JSON string regardless of the configured ``date_format``.
        """
        if self._uses_json_any:
            return format_date_iso
        return self.date_format

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal.

        ``json_type`` always emits ISO 8601 datetimes (JSON strings)
        unless the user has explicitly chosen the ``EPOCH`` form, which
        remains a valid JSON number.
        """
        if (
            self._uses_json_any
            and self.datetime_format.value.type_produced is not int
        ):
            return format_datetime_iso
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
        """Callable that formats an int value as a literal.

        ``json_type`` skips the ``_i128`` overflow fallback because the
        JSON spec has no integer-width annotation; out-of-range values
        are rejected by :meth:`validate_spec_for_data` with a clear
        error before they reach the formatter.
        """
        base = self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )
        if self._uses_json_any:
            return base
        return make_overflow_fallback_formatter(
            base=base,
            fallback=_format_crystal_i128_literal,
            min_value=I64_MIN,
            max_value=I64_MAX,
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting.

        ``json_type`` reuses the JSON object form for ordered maps
        (JSON objects preserve insertion order in the rendered text).
        """
        if self._uses_json_any:
            return OrderedMapFormatConfig(
                ordered_map_open=fixed_open(open_str="{"),
                close="}",
                preamble_lines=(),
            )
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="{"),
            close="}",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry.

        ``json_type`` uses the JSON ``": "`` separator; the native
        Crystal form uses ``" => "``.
        """
        if self._uses_json_any:
            return dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            )
        return dict_entry_with_separator(
            separator=" => ",
            format_value=passthrough_sequence_entry,
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration.

        Under ``json_type`` the rendered literal is wrapped in
        ``JSON.parse(%(...))``; Crystal's only declaration style is
        ``ASSIGN``, so the formatter does not branch on the keyword.
        """
        if self._uses_json_any:
            return _crystal_json_declaration_formatter
        return self.declaration_style.value.formatter

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Crystal needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Crystal needs none)."""
        return {}

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines from the scalar map, prefixed
        with the ``RECORD`` strategy's generated ``record``
        declarations.

        Crystal compiles every fixture in one ``crystal run``
        invocation, so a file-scope ``record Record0`` would collide
        across cases.  Emitting the declarations into the body preamble
        (which :meth:`wrap_in_file` places inside the per-fixture
        module, ahead of the value) scopes each ``RecordN`` to its own
        fixture; the declarations precede the scalar body lines so a
        record type is in scope before its literal.
        """
        scalar_body = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )
        if not self._record_strategy_active:
            return scalar_body
        record_preamble = self._record_strategy.preamble

        def _compute(
            types: frozenset[type],
            data: Value,
            /,
        ) -> tuple[str, ...]:
            """Record declaration lines precede scalar body lines."""
            alias = (
                (_CRYSTAL_RECORD_MAP_ALIAS,)
                if self._record_strategy.behavior.compute_wrap_ids(data)
                else ()
            )
            return alias + record_preamble(data) + scalar_body(types, data)

        return _compute

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        config: CallStyle = self.call_style.value
        return config
