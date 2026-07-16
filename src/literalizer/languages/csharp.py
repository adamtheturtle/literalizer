"""C# language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    TypedOpenerConfig,
    TypeOpeners,
    fixed_open,
    make_type_to_opener,
    typed_collection_open,
    typed_dict_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    datetime_epoch_seconds,
    datetime_ymdhms_formatter,
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
    format_time_csharp,
    format_time_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_template,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    variable_declaration_formatter,
    variable_formatter,
)
from literalizer._formatters.format_factories import (
    ordered_map_format_factory,
    sequence_format_factory,
    set_format_factory,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    I64_MAX,
    I64_MIN,
    format_integer_binary,
    format_integer_hex,
    format_integer_underscore,
    make_overflow_fallback_formatter,
    raise_for_unrepresentable_int,
)
from literalizer._formatters.format_strings import (
    format_string_backslash,
    format_string_verbatim_csharp,
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
    KeywordCallStyle,
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
    new_constructor_target,
    no_call_binding_body_preamble,
    no_call_binding_file_pragmas,
    no_call_stub,
    no_data_preamble,
    no_format_integer_widened,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    prepend_body_preamble,
    wrap_combined_in_file_noop,
    wrap_in_file_noop,
)
from literalizer._types import OrderedMap, Scalar, Value
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
)


class _CSharpModifiers(enum.Enum):
    """Declaration modifiers supported by C#.

    Each member's value is the C# keyword it renders to.  Declaration
    order matches canonical C# modifier order.

    Exposed as :attr:`CSharp.Modifiers` / :attr:`CSharp.modifiers`.
    """

    PUBLIC = "public"
    """Visibility: publicly accessible."""

    PRIVATE = "private"
    """Visibility: private to the enclosing type."""

    PROTECTED = "protected"
    """Visibility: protected (accessible from subclasses)."""

    STATIC = "static"
    """Storage: associated with the enclosing type rather than an
    instance.
    """

    CONST = "const"
    """Immutability: compile-time constant."""

    READONLY = "readonly"
    """Immutability: cannot be reassigned after initialization."""


@beartype
def _csharp_modifier_prefix(modifiers: frozenset[enum.Enum]) -> str:
    """Return the ``public static readonly `` prefix for a C#
    declaration, including a trailing space when non-empty.

    Values that are not :class:`_CSharpModifiers` members are ignored.
    """
    keywords = [m.value for m in _CSharpModifiers if m in modifiers]
    if not keywords:
        return ""
    return " ".join(keywords) + " "


@beartype
def _csharp_scalar_type(
    *,
    value: Value,
    date_hint: str,
    datetime_hint: str,
) -> str:
    """Return the C# type name for a scalar value."""
    match value:
        case datetime.datetime():
            return datetime_hint
        case datetime.date():
            return date_hint
        case datetime.time():
            return "TimeOnly"
        case bool():
            result = "bool"
        case int():
            result = "int"
        case float():
            result = "double"
        case str() | bytes():
            result = "string"
        case _:
            result = "object"
    return result


@beartype
def _csharp_common_element_type(
    *,
    items: list[Value],
    date_hint: str,
    datetime_hint: str,
    dict_value_type: str,
) -> str:
    """Return the common C# type for a list of elements."""
    if not items:
        return "object"
    types = {
        _csharp_type_hint(
            data=item,
            date_hint=date_hint,
            datetime_hint=datetime_hint,
            dict_value_type=dict_value_type,
        )
        for item in items
    }
    if len(types) == 1:
        return next(iter(types))
    if types == {"int", "double"}:
        return "double"
    return "object"


@beartype
def _csharp_type_hint(
    *,
    data: Value,
    date_hint: str,
    datetime_hint: str,
    dict_value_type: str,
) -> str:
    """Return the C# declared type for *data*."""
    match data:
        case dict():
            val_type = _csharp_common_element_type(
                items=list(data.values()),
                date_hint=date_hint,
                datetime_hint=datetime_hint,
                dict_value_type=dict_value_type,
            )
            return f"Dictionary<string, {val_type}>"
        case set():
            elem = _csharp_common_element_type(
                items=list(data),
                date_hint=date_hint,
                datetime_hint=datetime_hint,
                dict_value_type=dict_value_type,
            )
            return f"HashSet<{elem}>"
        case list():
            elem = _csharp_common_element_type(
                items=data,
                date_hint=date_hint,
                datetime_hint=datetime_hint,
                dict_value_type=dict_value_type,
            )
            return f"{elem}[]"
        case _:
            return _csharp_scalar_type(
                value=data,
                date_hint=date_hint,
                datetime_hint=datetime_hint,
            )


@beartype
def _format_csharp_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    modifiers: frozenset[enum.Enum],
    date_hint: str,
    datetime_hint: str,
    dict_value_type: str,
) -> str:
    """Format a C# variable declaration, applying modifiers when set.

    Falls back to ``var {name} = {value};`` when *modifiers* is empty.
    """
    if _CSharpModifiers.CONST in modifiers and isinstance(
        data,
        list | dict | set | datetime.date | datetime.datetime,
    ):
        msg = (
            "C# 'const' requires a compile-time constant initializer, "
            "but collection and date/datetime literals are not constant "
            "expressions. Use 'readonly' or remove the 'const' modifier."
        )
        raise IncompatibleFormatsError(msg)
    prefix = _csharp_modifier_prefix(modifiers=modifiers)
    if not prefix:
        return f"var {name} = {value};"
    hint = _csharp_type_hint(
        data=data,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        dict_value_type=dict_value_type,
    )
    return f"{prefix}{hint} {name} = {value};"


@dataclasses.dataclass(frozen=True)
class _CSharpDictSpec:
    """Per-format dict config pieces resolved at init time."""

    opener_template: str


_CSHARP_JSON_USING = "using System.Text.Json.Nodes;"
_CSHARP_JSON_OBJECT_OPEN = "new JsonObject {"
_CSHARP_JSON_ARRAY_OPEN = "new JsonArray {"
_CSHARP_JSON_EMPTY_OBJECT = "new JsonObject()"
_CSHARP_JSON_EMPTY_ARRAY = "new JsonArray()"


@beartype
def _csharp_json_value_expression(value: str, /) -> str:
    """Cast a rendered literal to ``JsonNode?`` unless it already
    evaluates to a ``JsonNode`` (a ``new JsonObject``/``new JsonArray``
    expression) or has already been cast.

    The cast triggers ``System.Text.Json.Nodes``'s implicit operators
    that convert primitives (``int``, ``string``, ``bool``, ``double``)
    to ``JsonValue`` so scalars become ``JsonNode``-typed without an
    explicit ``JsonValue.Create(...)`` call.
    """
    if value.startswith(
        (
            _CSHARP_JSON_OBJECT_OPEN,
            _CSHARP_JSON_ARRAY_OPEN,
            _CSHARP_JSON_EMPTY_OBJECT,
            _CSHARP_JSON_EMPTY_ARRAY,
            "(JsonNode",
        )
    ):
        return value
    return f"(JsonNode?)({value})"


@beartype
def _format_csharp_json_call_arg(_raw_value: Value, formatted: str) -> str:
    """Format a direct C# call argument as ``JsonNode?``."""
    return _csharp_json_value_expression(formatted)


@beartype
def _csharp_json_non_scalar_child(  # pragma: no cover
    _raw_value: Value,
    formatted: str,
) -> str:
    """Identity wrapper for non-scalar JSON children."""
    return formatted


@beartype
def _format_csharp_json_assignment(name: str, value: str, _data: Value) -> str:
    """Assign a rendered literal to a C# ``JsonNode?`` binding."""
    return f"{name} = {_csharp_json_value_expression(value)};"


@beartype
def _csharp_json_declaration_formatter(
    *,
    json_type: str,
) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
    """Return a declaration formatter for ``JsonNode?`` output.

    A ``const`` modifier is rejected because ``new JsonObject``/
    ``new JsonArray`` expressions and the ``(JsonNode?)`` cast applied
    to scalars are runtime constructors / user-defined conversions,
    not C# compile-time constant expressions.
    """

    def _formatter(
        name: str,
        value: str,
        _data: Value,
        modifiers: frozenset[enum.Enum],
    ) -> str:
        """Format a JSON-backed declaration."""
        if _CSharpModifiers.CONST in modifiers:
            msg = (
                "C# 'const' requires a compile-time constant initializer, "
                f"but {json_type} expressions are not constant. Use "
                "'readonly' or remove the 'const' modifier."
            )
            raise IncompatibleFormatsError(msg)
        prefix = _csharp_modifier_prefix(modifiers=modifiers)
        expr = _csharp_json_value_expression(value)
        return f"{prefix}{json_type}? {name} = {expr};"

    return _formatter


@beartype
def _csharp_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return C# stub declarations for a call name.

    For a single-name target the stub is a static method whose
    parameter list matches the given names; for a dotted target a
    chain of nested stub classes is emitted so ``a.b.c.d(...)``
    dispatches to a real method whose body returns ``null``.  Every
    argument is spelled out by name with a ``null`` default so
    named-argument call styles bind to real parameters instead of
    failing at runtime.
    """
    param_list = ", ".join(f"object {p} = null" for p in params)
    if len(parts) == 1:
        return (f"static object {parts[0]}({param_list}) => null;",)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        type_name = f"{root.title()}Type_"
        return (
            f"class {type_name} {{"
            f" public object {method}({param_list}) => null; }}",
            f"static {type_name} {root} = new {type_name}();",
        )
    lines: list[str] = []
    inner_type = f"{fields[-1].title()}Type_"
    lines.append(
        f"class {inner_type} {{"
        f" public object {method}({param_list}) => null; }}"
    )
    prev_type = inner_type
    for i in range(len(fields) - 2, -1, -1):
        curr_type = f"{fields[i].title()}Type_"
        lines.append(
            f"class {curr_type} {{"
            f" public {prev_type} {fields[i + 1]} = new {prev_type}(); }}"
        )
        prev_type = curr_type
    root_type = f"{root.title()}Type_"
    lines.append(
        f"class {root_type} {{"
        f" public {prev_type} {fields[0]} = new {prev_type}(); }}"
    )
    lines.append(f"static {root_type} {root} = new {root_type}();")
    return tuple(lines)


# Signed 32-bit range.  An integer record field inside it is declared
# ``int``; a wider one is declared ``long`` to match the literal C#
# infers for the same value.  Keep these bounds in sync with
# ``_I32_MIN`` / ``_I32_MAX`` in
# :mod:`literalizer._formatters.type_inference` (the widening threshold
# the value formatter uses, which has a back-reference to here).
_CSHARP_I32_MIN = -(2**31)
_CSHARP_I32_MAX = 2**31 - 1

# The ``RECORD`` strategy supports only auto ``Record0``/``Record1``/...
# names (no ``record_shape_names``), so the shared renderer always gets
# an empty custom-name mapping.
_CSHARP_NO_RECORD_SHAPE_NAMES: MappingProxyType[frozenset[str], str] = (
    MappingProxyType(mapping={})
)


@beartype
def _csharp_record_field_identifier(key: str, /) -> str:
    """Return the C# record component name for a dict *key*.

    C# conventions name record components in PascalCase; the literal is
    positional so the name only labels the declaration.
    """
    return IdentifierCase.PASCAL.convert(name=key)


@beartype
def _csharp_record_literal(
    name: str,
    fields: Sequence[RecordLiteralField],
    /,
) -> RenderedRecordLiteral:
    """Render a C# ``new Name(value, ...)`` positional record literal as
    structured pieces for the shared compact/multiline layout code.

    C# positional records are constructed by their primary constructor,
    so the literal emits arguments in declaration order with no field
    names (the PascalCase identifiers label only the declaration).
    """
    return RenderedRecordLiteral(
        head=f"new {name}(",
        entries=tuple(field.formatted for field in fields),
        closer=")",
        compact_pad="",
    )


@beartype
def _csharp_render_record_declaration(
    name: str,
    fields: Sequence[RecordDeclarationField],
    /,
) -> str:
    """Render a C# ``record Name(Type Id, ...);`` positional record.

    A positional ``record`` (reference type, value equality, mirroring
    the Java port) is used rather than a ``struct``; its primary
    constructor matches the positional literal
    :func:`_csharp_record_literal` emits.
    """
    components = ", ".join(
        f"{field.type_name} {field.identifier}" for field in fields
    )
    return f"record {name}({components});"


@beartype
def _csharp_int_field_type(*, value: int) -> str:
    """Return the C# record-component type for an integer.

    A value inside signed 32-bit range is declared ``int``; a wider one
    is declared ``long``.  C# types a literal that carries no type
    suffix by magnitude (signed 32-bit, then unsigned 32-bit, then
    signed 64-bit), and each of those converts implicitly to the chosen
    field type, so the declared type accepts the rendered literal.  A
    value beyond signed 64-bit range uses the unsigned 64-bit type,
    matching the literal C# infers there.
    """
    if not I64_MIN <= value <= I64_MAX:
        return "ulong"
    if _CSHARP_I32_MIN <= value <= _CSHARP_I32_MAX:
        return "int"
    return "long"


@beartype
def _csharp_record_dict_field_type(value: dict[Scalar, Value], /) -> str:
    """Return the component type for a dict not rendered as a record."""
    if record_shape_for_dict(value=value) is not None:
        return "Dictionary<string, object>"
    return "object"


@beartype
def _all_record_shaped(items: list[Value], /) -> bool:
    """Return whether *items* is a non-empty list whose every element is
    a record-shaped dict (non-empty, all-string-keyed, not an ordered
    map).

    Under the ``RECORD`` strategy such a list renders each element as a
    generated ``RecordN`` literal, so the C# sequence opener widens to
    an implicitly-typed array (``new[] { ... }``) whose element type C#
    infers from those literals, rather than the
    ``Dictionary<string, object>[]`` the typed opener would otherwise
    emit.

    Uniformity of shape need not be checked here: a sibling list whose
    record-shaped dicts do not all share one shape is rejected for every
    ``RECORD`` language by the shared
    :func:`literalizer._checks.check_data` guard before any value is
    formatted, so a list reaching this predicate is always single-shape
    and the inferred ``RecordN[]`` is well-formed.
    """
    if not items:
        return False
    return all(
        isinstance(item, dict)
        and not isinstance(item, OrderedMap)
        and record_shape_for_dict(value=item) is not None
        for item in items
    )


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class CSharp(metaclass=LanguageCls):
    """C# language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.CSHARP`` — ``new DateOnly(...)`` call,
              e.g. ``new DateOnly(2024, 1, 15)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.CSHARP`` — ``new DateTime(...)`` call,
              e.g. ``new DateTime(2024, 1, 15, 12, 30, 0)``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.

        json_type: When set to
            ``json_types.SYSTEM_TEXT_JSON_NODE``, render values through
            ``System.Text.Json.Nodes.JsonNode`` (``JsonObject`` /
            ``JsonArray`` / typed scalars) instead of C#'s narrow
            collection types.  Dates / datetimes / times switch to ISO
            8601 strings (unless ``datetime_format`` is ``EPOCH``) and
            the ``const`` modifier is rejected because the JSON
            constructors are not constant expressions.
    """

    format_integer_widened = no_format_integer_widened
    format_call_variable_declaration = default_format_call_variable_declaration
    format_call_variable_assignment = default_format_call_variable_assignment
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(new_constructor_target)
    )
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".cs"
    pygments_name = "csharp"
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
    supports_module_name = False
    supports_empty_dict_key = False
    supports_call_style = True
    supports_default_dict_key_type = True
    supports_default_dict_value_type = True
    supports_default_sequence_element_type = True
    supports_default_set_element_type = True
    supports_default_ordered_map_value_type = False
    non_default_kwargs: ClassVar[dict[str, str]] = {
        "default_set_element_type": "string",
        "default_sequence_element_type": "string",
        "default_dict_value_type": "object?",
        "default_dict_key_type": "object",
    }
    json_type_variant_name_suffix = "json_node"
    declaration_style_sequence_format_overrides: ClassVar[dict[str, str]] = {}
    supports_non_ascii_string_literals = True
    variant_metadata: ClassVar[VariantMetadata] = VariantMetadata(
        pre_indent_comment_scalar_variant=False,
        fixture_module_name_template=None,
        fixture_module_name_lowercase=False,
        golden_filename_lowercase=False,
        collection_layout_category="collection_layout",
        record_variants=frozenset({RecordVariant.NONRECORD_DICT_FIELD}),
        nested_map_widening=NestedMapWideningVariant.NONE,
        modifier_sequence_format_overrides={"READONLY": "ARRAY"},
    )
    supports_record_struct_name_prefix = False
    supports_record_shape_names = False
    supports_non_string_dict_keys = False

    _opener_config = TypedOpenerConfig(
        str_type="string",
        bool_type="bool",
        int_type="int",
        wide_int_type="long",
        float_type="double",
        mixed_numeric_type="double",
        bytes_type="string",
        date_type="DateOnly",
        datetime_type="DateTime",
        time_type="TimeOnly",
        list_template="{inner}[]",
        sequence_opener_template="new {type_name}[] {{",
        dict_opener_template="new Dictionary<{key_type}, {type_name}> {{",
        set_opener_template="new HashSet<{type_name}> {{",
        dict_type_template="Dictionary<{key_type}, {inner}>",
        fallback_value_type="object",
    )

    class DateFormats(enum.Enum):
        """Date format options for C#."""

        CSHARP = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="new DateOnly({year}, {month}, {day})",
            ),
            preamble_lines=("using System;",),
            type_produced=datetime.date,
        )
        ISO = DateFormatConfig(
            formatter=format_date_iso, type_produced=str, preamble_lines=()
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for C#."""

        CSHARP = DatetimeFormatConfig(
            formatter=datetime_ymdhms_formatter(
                template="new DateTime({year}, {month}, {day}, "
                "{hour}, {minute}, {second})",
            ),
            preamble_lines=("using System;",),
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
        """Sequence type options for C#."""

        TUPLE = enum.member(
            value=sequence_format_factory(
                open_template="(",
                close=")",
                supports_heterogeneity=True,
                single_element_trailing_comma=False,
                supports_trailing_comma=False,
                empty_template="ValueTuple.Create()",
                preamble_lines=("using System;",),
                format_entry=passthrough_sequence_entry,
                typed_opener_fallback_template=None,
            )
        )
        ARRAY = enum.member(
            value=sequence_format_factory(
                open_template="new {type}[] {{",
                close="}",
                supports_heterogeneity=True,
                single_element_trailing_comma=False,
                supports_trailing_comma=True,
                empty_template="new {type}[] {{}}",
                preamble_lines=(),
                format_entry=passthrough_sequence_entry,
                typed_opener_fallback_template=("new {type}[] {{"),
            )
        )

        def __call__(self, default_type: str) -> SequenceFormatConfig:
            """Create a sequence format config for the given type."""
            return self.value(default_type)

    class SetFormats(enum.Enum):
        """Set type options for C#."""

        HASH_SET = enum.member(
            value=set_format_factory(
                open_template="new HashSet<{type}> {{",
                close="}}",
                empty_template="new HashSet<{type}>()",
                preamble_lines=("using System.Collections.Generic;",),
                set_opener_template="",
                supports_heterogeneity=True,
                supports_trailing_comma=True,
            )
        )
        SORTED_SET = enum.member(
            value=set_format_factory(
                open_template="new SortedSet<{type}> {{",
                close="}}",
                empty_template="new SortedSet<{type}>()",
                preamble_lines=("using System.Collections.Generic;",),
                set_opener_template="new SortedSet<{type_name}> {{",
                supports_heterogeneity=False,
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

        VAR = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="var {name} = {value};",
            ),
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DICTIONARY = _CSharpDictSpec(
            opener_template="new Dictionary<{key_type}, {type_name}> {{",
        )
        SORTED_DICTIONARY = _CSharpDictSpec(
            opener_template="new SortedDictionary<{key_type}, {type_name}> {{",
        )

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="double.PositiveInfinity",
        negative_infinity="double.NegativeInfinity",
        nan="double.NaN",
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

        DOUBLE = enum.member(value=format_string_backslash)
        VERBATIM = enum.member(value=format_string_verbatim_csharp)

        def __call__(self, value: str, /) -> str:
            """Format a string."""
            return self.value(value=value)

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        YES = TrailingCommaConfig(multiline_trailing_comma=True)
        NO = TrailingCommaConfig(multiline_trailing_comma=False)

    Modifiers = _CSharpModifiers

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats
    modifiers = _CSharpModifiers

    class HeterogeneousStrategies(enum.Enum):
        """Heterogeneous-scalar strategy options.

        ``ERROR`` raises on any value that cannot be represented.
        ``RECORD`` renders each record-shaped dict (non-empty,
        string-keyed) as a generated positional ``record`` declared in
        the preamble plus a matching positional literal, rather than a
        homogeneous ``Dictionary``.
        """

        ERROR = enum.auto()
        RECORD = enum.auto()

    heterogeneous_strategies = HeterogeneousStrategies

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for C#."""

        V10 = enum.auto()

    version_formats = VersionFormats

    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.PASCAL,
        IdentifierCase.CAMEL,
        IdentifierCase.UPPER_SNAKE,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = (
        ModifierCombination(
            name="public_static_readonly",
            modifiers=frozenset(
                {
                    _CSharpModifiers.PUBLIC,
                    _CSharpModifiers.STATIC,
                    _CSharpModifiers.READONLY,
                },
            ),
        ),
    )

    def validate_spec_for_data(self, data: Value) -> None:
        """Validate C#-specific data / format combinations.

        Under ``json_type`` only dict keys that are strings can be
        represented as JSON object keys, so a non-string dict key is
        rejected up-front rather than emitted as a ``[<non-string>]
        = ...`` initializer that the C# compiler would reject.
        """
        if self._json_type_active:
            self._validate_json_value_keys(data)

    def _validate_json_value_keys(self, data: Value, /) -> None:
        """Reject non-string object keys for ``JsonNode`` output."""
        match data:
            case dict():
                for key, value in data.items():
                    if not isinstance(key, str):
                        msg = (
                            "C# json_type can only represent dict keys "
                            f"as JSON object strings, not {type(key).__name__}"
                        )
                        raise UnrepresentableInputError(msg)
                    self._validate_json_value_keys(value)
            case list() | set():
                for item in data:
                    self._validate_json_value_keys(item)
            case _:
                return

    def __post_init__(self) -> None:
        """Force ``sequence_format=ARRAY`` for the ``RECORD`` strategy.

        Under ``RECORD`` a list-valued record component is declared from
        the array opener (``new <Type>[] {``) the value formatter emits,
        so its declared type matches the rendered literal.  The default
        tuple sequence format carries no element type in its opener and
        no fixed-length component type, so it cannot back a generated
        record component.  Coercing here (rather than rejecting a
        non-array spec) keeps the golden harness simple: every ``RECORD``
        spec, however constructed, renders.
        """
        strategies = type(self.heterogeneous_strategy)
        formats = type(self.sequence_format)
        if (
            self.heterogeneous_strategy is strategies.RECORD
            and self.sequence_format is not formats.ARRAY
        ):
            object.__setattr__(
                self,
                "sequence_format",
                formats.ARRAY,
            )

    @cached_property
    def validate_call_arg(self) -> Callable[[Value], None]:
        """Return call-argument validation for this language."""
        return no_validate_call_arg

    @cached_property
    def format_call_statement(self) -> Callable[[str], str]:
        """Return call-statement formatting for this language."""
        return identity_call_statement

    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    class VariableTypeHints(enum.Enum):
        """Variable type hint options."""

        NEVER = enum.auto()
        SAFE = enum.auto()

    variable_type_hints_formats = VariableTypeHints

    class JsonTypes(enum.Enum):
        """JSON value type options for C#."""

        SYSTEM_TEXT_JSON_NODE = "JsonNode"
        """``System.Text.Json.Nodes.JsonNode``, the built-in .NET JSON
        document object model.
        """

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
        """CSharp call style options."""

        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )
        NAMED = KeywordCallStyle(separator=": ")

    call_styles = CallStyles

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap code in a valid file.

        When *content* starts with a class-field modifier keyword (one
        of the visibility or storage keywords that C# only accepts on
        class members) the declaration is placed inside a ``class
        Check`` body with a ``Main`` entry point.

        When *body_preamble* carries call-stub declarations (``class
        Foo_ { ... }`` and ``static Foo_ foo = new Foo_();``) the whole
        file is wrapped in ``class Check { ...stubs... static void
        Main() { ...content... } }``.  C# requires type declarations to
        follow top-level statements, so stubs cannot sit before
        top-level calls — wrapping them as class members sidesteps
        that ordering rule.

        Under the ``RECORD`` strategy a record literal's ``var``
        declaration would otherwise be a bare top-level statement, but
        the generated ``record`` declarations are emitted at file scope
        (by the data-dependent preamble) ahead of this output and C#
        forbids a top-level statement after a type declaration; such
        content is therefore wrapped as a ``Main`` method body inside
        ``class Check`` rather than left as a top-level statement (call
        stubs and class-field declarations keep their own wrapping).

        Otherwise the content is emitted as a top-level statement,
        which is the only context where ``var`` declarations are valid.
        """
        first_token = (
            content.lstrip().split(sep=" ", maxsplit=1)[0]
            if content.strip()
            else ""
        )
        is_class_field = first_token in {
            "public",
            "private",
            "protected",
            "static",
            "readonly",
        }
        if is_class_field:
            preamble_block = (
                "\n".join(body_preamble) + "\n" if body_preamble else ""
            )
            return (
                f"{preamble_block}class Check {{\n"
                f"{content}\n"
                f"{self.indent}public static void Main() {{}}\n"
                "}"
            )
        stub_prefixes = ("class ", "static ")
        stub_lines = tuple(
            line for line in body_preamble if line.startswith(stub_prefixes)
        )
        other_lines = tuple(
            line
            for line in body_preamble
            if not line.startswith(stub_prefixes)
        )
        if stub_lines:
            stub_block = "\n".join(stub_lines) + "\n"
            body = prepend_body_preamble(
                content=content,
                body_preamble=other_lines,
            )
            return (
                f"class Check {{\n"
                f"{stub_block}"
                f"{self.indent}public static void Main() {{\n"
                f"{body}\n"
                f"{self.indent}}}\n"
                f"}}"
            )
        if self._record_strategy_active:
            body = prepend_body_preamble(
                content=content,
                body_preamble=body_preamble,
            )
            return (
                f"class Check {{\n"
                f"{self.indent}public static void Main() {{\n"
                f"{body}\n"
                f"{self.indent}}}\n"
                f"}}"
            )
        return wrap_in_file_noop(
            content=content,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap declaration and assignment in a valid file.

        Under the ``RECORD`` strategy the declaration and assignment are
        top-level statements that must follow the file-scope ``record``
        declarations, so they are wrapped as a ``Main`` method body via
        :meth:`wrap_in_file`; otherwise this is a no-op.
        """
        if self._record_strategy_active:
            return self.wrap_in_file(
                content=declaration + "\n" + assignment,
                variable_name=variable_name,
                body_preamble=body_preamble,
            )
        return wrap_combined_in_file_noop(
            declaration=declaration,
            assignment=assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.CSHARP
    datetime_format: DatetimeFormats = DatetimeFormats.CSHARP
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.TUPLE
    set_format: SetFormats = SetFormats.HASH_SET
    default_set_element_type: str = "object"
    default_sequence_element_type: str = "object"
    default_dict_key_type: str = "string"
    default_dict_value_type: str = "object"
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.VAR
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.DICTIONARY
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
    trailing_comma: TrailingCommas = TrailingCommas.NO
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.SEMICOLON
    )
    call_style: CallStyles = CallStyles.POSITIONAL
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    json_type: JsonTypes | None = None
    # Keep in sync with the `LanguageVersion` passed to the C# lint host
    # in `scripts/lint-csharp/Program.cs`.
    language_version: VersionFormats = VersionFormats.V10
    indent: str = "    "

    _default_null_literal: ClassVar[str] = "(object?)null"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ";"
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def _json_type_active(self) -> bool:
        """Return whether C# should render through ``JsonNode``."""
        return self.json_type is not None

    @cached_property
    def null_literal(self) -> str:
        """Null literal for the active C# representation.

        Under ``json_type`` an explicitly-typed ``(JsonNode?)null``
        keeps a top-level ``null`` from ambiguously binding to a method
        overload (``System.Text.Json.Nodes`` exposes implicit operators
        from many primitive types that a bare ``null`` literal would
        also match).
        """
        if self._json_type_active:
            return "(JsonNode?)null"
        return self._default_null_literal

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Callable that rewrites a formatted direct call argument.

        Under ``json_type`` every call argument is cast to ``JsonNode?``
        so the underlying stub receives a JSON value; under any other
        mode call arguments pass through unchanged.
        """
        if self._json_type_active:
            return _format_csharp_json_call_arg
        return identity_call_arg

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
        """Format an assignment to an existing variable.

        Under ``json_type`` the assigned expression is cast to
        ``JsonNode?`` through the same helper as the declaration form
        so the two halves of a combined declaration / assignment stay
        consistent.
        """
        if self._json_type_active:
            return _format_csharp_json_assignment
        return variable_formatter(template="{name} = {value};")

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Format one ordered-map entry.

        Under ``json_type`` an ordered map renders as a ``JsonObject``,
        whose collection initializer takes ``KeyValuePair`` entries via
        the indexer ``["key"] = value`` form (matching the dict
        renderer).
        """
        return dict_entry_with_template(
            template="[{key}] = {value}",
            format_value=passthrough_sequence_entry,
        )

    @cached_property
    def _record_strategy_active(self) -> bool:
        """Return whether the ``RECORD`` heterogeneous strategy is set."""
        return self.heterogeneous_strategy.name == "RECORD"

    @cached_property
    def _csharp_record_scalar_resolver(
        self,
    ) -> Callable[[type], str | None]:
        """Map a scalar field's Python type to its C# type name.

        Built from the same scalar mapping the collection openers use,
        with the date/datetime names resolved from the configured
        formats (so an ``ISO`` datetime field is typed ``string``,
        matching the rendered literal).  A type with no entry in that
        mapping (e.g. ``NoneType``) yields ``None`` so the caller can
        fall back to the top type ``object``.
        """
        cfg = self._opener_config
        return cfg.element_to_type(
            list_template=None,
            enable_list_type=False,
            date_type=cfg.type_name(py_type=self._date_tp),
            datetime_type=cfg.type_name(py_type=self._dt_tp),
            enable_dict_type=False,
            dict_key_type="",
        )

    def _csharp_record_field_type(  # noqa: PLR0911
        self,
        request: RecordFieldType,
        /,
    ) -> str:
        """Return the C# record-component type for a field, derived
        structurally from the raw value (the Go/Java/Scala pattern).

        A field whose value is itself a nested record-shaped dict uses
        that record's generated name.  A field whose value is a list of
        record-shaped dicts (one shared shape) is typed ``RecordN[]`` to
        match the implicitly-typed array opener
        :attr:`sequence_open` widens it to (C# infers the element type
        from the ``RecordN`` literals).  An integer is sized to match
        the literal C# infers for the same value (``int``/``long``, or
        ``ulong`` beyond signed 64-bit range, the bare-decimal overflow
        fallback).  An ``EPOCH`` datetime renders as its epoch integer,
        so it is sized like that integer.  A list or ordered-map field
        is typed from the very opener the value formatter uses for that
        value (a record field is formatted with no sibling override, so
        the opener equals the one rendered): the ``new `` prefix and the
        trailing `` {`` are stripped (``new int[] {`` -> ``int[]``,
        ``new Dictionary<string, object> {`` ->
        ``Dictionary<string, object>``).  Every other scalar uses the
        shared scalar resolver (``date`` -> ``DateOnly``).

        A record-eligible dict with no ``record_name`` was widened out
        of record inference because its nested sibling maps cannot
        share one shape.  Type that field as ``Dictionary<string,
        object>`` so the uniform enclosing record survives (#2913).  A
        set or a genuinely non-record dict (empty or non-string-keyed)
        still has no precise component type; per the cross-language
        decision in #2317, C# folds it into the ``object`` top type.
        """
        if request.record_name is not None:
            return request.record_name
        if request.element_record_name is not None:
            return f"{request.element_record_name}[]"
        value = request.value
        # An ``EPOCH`` datetime renders as its epoch integer, so size
        # the field exactly like that integer; other datetime formats
        # stay datetime-typed via the scalar resolver below.
        if (
            isinstance(value, datetime.datetime)
            and self.datetime_format.value.type_produced is int
        ):
            value = datetime_epoch_seconds(value=value)
        match value:
            case bool():
                return "bool"
            case int():
                return _csharp_int_field_type(value=value)
            case OrderedMap():
                opener = self.ordered_map_format_config.ordered_map_open(
                    value,
                )
            case dict():
                return _csharp_record_dict_field_type(value)
            case list():
                opener = self.sequence_open(value)
            case _:
                return (
                    self._csharp_record_scalar_resolver(type(value))
                    or "object"
                )
        return opener.removeprefix("new ").removesuffix(" {")

    @cached_property
    def _record_renderer(self) -> RecordRenderer:
        """C# syntax hooks for the ``RECORD`` strategy."""
        return RecordRenderer(
            name_prefix="Record",
            record_shape_names=_CSHARP_NO_RECORD_SHAPE_NAMES,
            field_identifier=_csharp_record_field_identifier,
            field_type=self._csharp_record_field_type,
            render_declaration=_csharp_render_record_declaration,
            render_literal=_csharp_record_literal,
        )

    @cached_property
    def _record_strategy(self) -> RecordStrategy:
        """Behavior + ``record``-declaration preamble for ``RECORD``."""
        return build_record_strategy(
            renderer=self._record_renderer,
            split_conflicting_field_types=False,
            widen_unrecordizable_nested_sibling_maps=True,
            derecordized_map_open="new Dictionary<string, object> {",
        )

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        Under ``json_type`` every rendered file pulls in
        ``System.Text.Json.Nodes`` unconditionally; the per-collection
        format configurations leave their ``preamble_lines`` empty so
        the ``using`` line is emitted here exactly once regardless of
        which container shapes appear in the data.

        Under ``HeterogeneousStrategies.RECORD`` this emits one
        positional ``record`` declaration per record shape present in
        the data; otherwise C# needs no data-dependent preamble.
        """
        if self._json_type_active:

            def _json_preamble(_data: Value, /) -> tuple[str, ...]:
                """Always contribute the JsonNode ``using`` directive."""
                return (_CSHARP_JSON_USING,)

            return _json_preamble
        if self._record_strategy_active:
            return self._record_strategy.preamble
        return no_data_preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config.

        ``json_type`` relaxes scalar-type checks unconditionally,
        because ``JsonObject`` / ``JsonArray`` accept heterogeneous
        ``JsonNode`` children by construction.

        ``RECORD`` resolves to the shared record behavior (its value
        needs the per-instance renderer, so it cannot be stored on the
        enum member); ``ERROR`` uses the static raising behavior.
        """
        if self._json_type_active:
            return dataclasses.replace(
                NO_HETEROGENEOUS_BEHAVIOR,
                skip_scalar_checks=True,
                wrap_non_scalar=_csharp_json_non_scalar_child,
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
        return _csharp_call_stub

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
    def _date_tp(self) -> type:
        """Python type produced by the chosen date format."""
        return self.date_format.value.type_produced

    @cached_property
    def _dt_tp(self) -> type:
        """Python type produced by the chosen datetime format."""
        return self.datetime_format.value.type_produced

    @cached_property
    def _base_set_format_config(self) -> SetFormatConfig:
        """Base set format config before typed-opener application."""
        return self.set_format(
            default_type=self.default_set_element_type,
        )

    @cached_property
    def _openers(self) -> TypeOpeners:
        """Typed openers built from the opener config."""
        cfg = self._opener_config
        return cfg.build(
            date_type=cfg.type_name(py_type=self._date_tp),
            datetime_type=cfg.type_name(py_type=self._dt_tp),
            set_opener_template=(
                self._base_set_format_config.set_opener_template or None
            ),
            narrow_dict_values=False,
            dict_key_type=self.default_dict_key_type,
        )

    @cached_property
    def _resolved_dict_opener(self) -> str:
        """Opener template with the key type resolved."""
        return self.dict_format.value.opener_template.replace(
            "{key_type}",
            self.default_dict_key_type,
        )

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format.

        Under ``json_type`` every sequence is rendered as ``new
        JsonArray { ... }`` (and ``new JsonArray()`` for the empty
        case), which accepts heterogeneous ``JsonNode`` children via
        the implicit conversion operators on
        ``System.Text.Json.Nodes``.  The ``using`` directive is
        contributed by :attr:`data_dependent_preamble`, so this config
        leaves its ``preamble_lines`` empty.

        ``()`` parses as an invalid expression in C#; the language's
        ``ValueTuple.Create()`` (or a typed empty array literal
        ``new T[] {}`` for the array format) is the syntactically valid
        empty form, so prefer it whenever an empty inner list sits
        beside non-empty siblings.  The array empty form is a plain
        language-level array literal, never ``Array.Empty<T>()``, so the
        array path needs no ``using System;``.
        """
        if self._json_type_active:
            return SequenceFormatConfig(
                sequence_open=fixed_open(open_str=_CSHARP_JSON_ARRAY_OPEN),
                close="}",
                supports_heterogeneity=True,
                single_element_trailing_comma=False,
                supports_trailing_comma=True,
                empty_sequence=_CSHARP_JSON_EMPTY_ARRAY,
                preamble_lines=(),
                format_entry=passthrough_sequence_entry,
                typed_opener_fallback=None,
                uses_typed_literal_for_scalars=False,
                requires_uniform_record_shapes=False,
                declared_type=(
                    self.json_type.value
                    if self.json_type is not None
                    else None
                ),
                narrowed_empty_form=None,
            )
        element_type = self.default_sequence_element_type
        base = self.sequence_format(default_type=element_type)
        empty = (
            f"new {element_type}[] {{}}"
            if self.sequence_format.name == "ARRAY"
            else "ValueTuple.Create()"
        )

        def _narrowed_empty_form(
            _siblings: Sequence[list[Value]],
        ) -> str:
            """Return the C# typed empty literal for this format."""
            return empty

        return dataclasses.replace(
            base,
            narrowed_empty_form=_narrowed_empty_form,
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format (with typed opener).

        Under ``json_type`` a set renders as a ``new JsonArray { ... }``
        because JSON has no native set type; the empty form widens to
        ``new JsonArray()`` for the same reason an empty sequence does.
        """
        if self._json_type_active:
            return SetFormatConfig(
                set_open=fixed_open(open_str=_CSHARP_JSON_ARRAY_OPEN),
                close="}",
                empty_set=_CSHARP_JSON_EMPTY_ARRAY,
                preamble_lines=(),
                set_opener_template="",
                supports_heterogeneity=True,
                supports_trailing_comma=True,
            )
        base = self._base_set_format_config
        return base.with_typed_opener(
            type_to_opener=self._openers.set,
            fallback=base.set_open([]),
        )

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence.

        Under the ``RECORD`` strategy a list whose every element is a
        record-shaped dict renders each element as a generated
        ``RecordN`` literal; the typed opener would type such a list
        ``Dictionary<string, object>[]`` (the homogeneous-map element
        type) which the record literals cannot initialize.  Such a list
        is instead opened with an implicitly-typed array ``new[] {`` so
        C# infers ``RecordN[]`` from the literals.  Every other list
        keeps the typed array opener.

        ``json_type`` takes precedence over the ``RECORD`` strategy:
        record-shaped dicts under json mode render as ``new JsonObject
        { ... }`` (not as ``RecordN`` literals), so their parent list
        must keep the json ``new JsonArray {`` opener rather than the
        implicitly-typed ``new[] {`` form, which would otherwise infer
        a ``JsonObject[]`` array that is not what json mode promises.
        """
        fmt = self.sequence_format_config
        if fmt.typed_opener_fallback is not None:
            base_open = typed_collection_open(
                type_to_opener=self._openers.seq,
                fallback=fmt.typed_opener_fallback,
            )
        else:
            base_open = fmt.sequence_open
        if self._json_type_active or not self._record_strategy_active:
            return base_open

        def _open(items: list[Value]) -> str:
            """Return the implicitly-typed array opener for an
            all-record list, else the typed array opener.
            """
            if _all_record_shaped(items):
                return "new[] {"
            return base_open(items)

        return _open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting.

        Under ``json_type`` every dict literal is wrapped in ``new
        JsonObject { ["key"] = value, ... }`` so it renders as a JSON
        object, and an empty dict widens to ``new JsonObject()``.  The
        ``using System.Text.Json.Nodes;`` line that powers
        ``JsonObject`` is contributed by :attr:`data_dependent_preamble`
        rather than from this config, so a json-mode fixture imports it
        exactly once regardless of how many dict literals appear.
        """
        if self._json_type_active:
            return DictFormatConfig(
                dict_open=fixed_open(open_str=_CSHARP_JSON_OBJECT_OPEN),
                close="}",
                format_entry=dict_entry_with_template(
                    template="[{key}] = {value}",
                    format_value=passthrough_sequence_entry,
                ),
                empty_dict=_CSHARP_JSON_EMPTY_OBJECT,
                preamble_lines=(),
                narrowed_open=None,
                supports_trailing_comma=True,
            )
        cfg = self._opener_config
        resolved = self._resolved_dict_opener
        return DictFormatConfig(
            dict_open=typed_dict_open(
                type_to_opener=make_type_to_opener(
                    element_to_type=cfg.element_to_type(
                        list_template=None,
                        enable_list_type=(
                            self.sequence_format is self.sequence_formats.ARRAY
                        ),
                        date_type=cfg.type_name(py_type=self._date_tp),
                        datetime_type=cfg.type_name(py_type=self._dt_tp),
                        enable_dict_type=False,
                        dict_key_type=self.default_dict_key_type,
                    ),
                    opener_template=resolved,
                ),
                fallback=resolved.format(
                    type_name=self.default_dict_value_type,
                ),
            ),
            close="}",
            format_entry=dict_entry_with_template(
                template="[{key}] = {value}",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=("using System.Collections.Generic;",),
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
        """Callable that formats a date as a string literal.

        ``json_type`` overrides the configured ``date_format`` with the
        ISO 8601 string form because the C# native ``DateOnly`` literal
        would not round-trip through JSON.
        """
        if self._json_type_active:
            return format_date_iso
        return self.date_format

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal.

        ``json_type`` overrides the configured ``datetime_format`` with
        the ISO 8601 string form unless the user has explicitly chosen
        the ``EPOCH`` integer form, which remains a valid JSON number.
        """
        if (
            self._json_type_active
            and self.datetime_format.value.type_produced is not int
        ):
            return format_datetime_iso
        return self.datetime_format

    @cached_property
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal.

        ``json_type`` overrides the native ``TimeOnly`` literal with the
        ISO 8601 string form because there is no implicit conversion
        from ``TimeOnly`` to ``JsonNode`` and JSON has no native time
        type.
        """
        if self._json_type_active:
            return format_time_iso
        return format_time_csharp

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
        """Callable that formats an int value as a literal.

        Positive values above ``long.MaxValue`` are accepted as bare
        literals because C# infers ``ulong`` for literals without a
        type suffix up to ``ulong.MaxValue``.  Values below
        ``long.MinValue`` have no clean literal form (unary minus
        cannot apply to ``ulong``), so they raise
        ``UnrepresentableIntegerError``.
        """
        base = self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )
        return make_overflow_fallback_formatter(
            base=base,
            fallback=raise_for_unrepresentable_int(language_name="C#"),
            min_value=I64_MIN,
            max_value=2**64 - 1,
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting.

        Under ``json_type`` an ordered map renders as a ``JsonObject``;
        the ``System.Text.Json.Nodes`` library preserves the indexer
        insertion order in the rendered output, so the JSON object
        opener is interchangeable with the dict opener here.
        """
        if self._json_type_active:
            return OrderedMapFormatConfig(
                ordered_map_open=fixed_open(
                    open_str=_CSHARP_JSON_OBJECT_OPEN,
                ),
                close="}",
                preamble_lines=(),
            )
        return ordered_map_format_factory(
            open_template="new Dictionary<{key_type}, {type}> {{",
            close="}",
            preamble_lines=("using System.Collections.Generic;",),
        )(
            self.default_dict_value_type,
            default_key_type=self.default_dict_key_type,
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration.

        Under ``json_type`` the declaration carries an explicit
        ``JsonNode?`` type annotation (never ``var``) and the
        right-hand side is wrapped in a ``(JsonNode?)`` cast unless the
        value is already a ``JsonObject`` / ``JsonArray`` literal.  The
        per-declaration formatter rejects the ``const`` modifier
        because every json-mode initializer (the cast or the
        constructor) is a runtime expression.
        """
        if self._json_type_active:
            assert self.json_type is not None  # noqa: S101
            return _csharp_json_declaration_formatter(
                json_type=self.json_type.value,
            )
        date_hint = (
            "string"
            if self.date_format.value.type_produced is str
            else "DateOnly"
        )
        datetime_hint = (
            "long"
            if self.datetime_format.value.type_produced is int
            else (
                "string"
                if self.datetime_format.value.type_produced is str
                else "DateTime"
            )
        )
        dict_value_type = self.default_dict_value_type

        def _formatter(
            name: str,
            value: str,
            data: Value,
            modifiers: frozenset[enum.Enum],
        ) -> str:
            """Adapt :func:`_format_csharp_declaration` to the positional
            formatter interface.
            """
            return _format_csharp_declaration(
                name=name,
                value=value,
                data=data,
                modifiers=modifiers,
                date_hint=date_hint,
                datetime_hint=datetime_hint,
                dict_value_type=dict_value_type,
            )

        return _formatter

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble computed from date/datetime format.

        Under ``json_type`` the ``using System.Text.Json.Nodes;`` line
        is contributed by :attr:`data_dependent_preamble` instead, so
        this method returns an empty per-scalar map to avoid
        duplicating it; dates / datetimes / times all render as ISO
        8601 strings (or an epoch integer for the explicit ``EPOCH``
        datetime format) and need no per-scalar import of their own.
        """
        if self._json_type_active:
            return {}
        return date_scalar_preamble(
            date_format=self.date_format,
            datetime_format=self.datetime_format,
            extra={datetime.time: ("using System;",)},
        )

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (C# needs none)."""
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
