"""Nim language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Mapping, Sequence
from functools import cached_property, partial
from types import MappingProxyType
from typing import ClassVar, assert_never

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    datetime_ymdhms_formatter,
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
from literalizer._formatters.format_integers import (
    I64_MAX,
    I64_MIN,
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    format_integer_underscore,
    make_overflow_fallback_formatter,
    raise_for_unrepresentable_int,
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
from literalizer._formatters.type_inference import record_shape_for_dict
from literalizer._heterogeneous import (
    collect_heterogeneous_container_ids,
    collect_sibling_map_wrap_ids,
    iter_wrapped_scalars,
)
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
    no_compute_call_slot_wrap_ids,
    no_data_preamble,
    no_format_integer_widened,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    no_validate_spec_for_data,
    wrap_combined_in_file_noop,
    wrap_in_file_noop,
)
from literalizer._types import OrderedMap, Scalar, Value
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
)

_NIM_JSON_MACRO = "%*"


@beartype
def _nim_json_value_expression(value: str, /) -> str:
    """Wrap *value* in ``%*`` unless it is already a ``JsonNode``
    expression.

    Values produced by the JSON-mode container openers already begin
    with ``%*`` and explicit ``newJArray()`` / ``newJObject()`` /
    ``newJNull()`` builders begin with ``newJ``; both are
    ``JsonNode`` typed and skip the extra wrap so the output does not
    accumulate redundant macros.
    """
    if value.startswith((_NIM_JSON_MACRO, "newJ")):
        return value
    return f"{_NIM_JSON_MACRO}({value})"


@beartype
def _format_nim_json_call_arg(_raw_value: Value, formatted: str) -> str:
    """Format a direct Nim call argument as ``JsonNode``."""
    return _nim_json_value_expression(formatted)


@beartype
def _nim_json_non_scalar_child(  # pragma: no cover
    _raw_value: Value,
    formatted: str,
) -> str:
    """Identity wrapper signaling JSON can hold non-scalar children."""
    return formatted


@beartype
def _format_nim_json_assignment(name: str, value: str, _data: Value) -> str:
    """Assign a rendered literal to a Nim ``JsonNode`` binding."""
    return f"{name} = {_nim_json_value_expression(value)}"


@beartype
def _nim_json_declaration_formatter(
    *,
    declaration_style: enum.Enum,
    json_type: str,
) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
    """Return a declaration formatter for ``JsonNode`` output."""

    def _formatter(
        name: str,
        value: str,
        _data: Value,
        _modifiers: frozenset[enum.Enum],
    ) -> str:
        """Format a JSON-backed declaration."""
        expr = _nim_json_value_expression(value)
        keyword = declaration_style.name.lower()
        return f"{keyword} {name}: {json_type} = {expr}"

    return _formatter


@beartype
def _apply_nim_variable_declaration(
    *,
    name: str,
    value: str,
    _data: Value,
    uses_typed_literal_for_scalars: bool,
    keyword: str,
    force_sequence: bool,
    uses_json_wrap: bool,
) -> str:
    """Format a declaration, using ``@`` for flat sequences of
    simple scalars.
    """
    use_sequence = (
        isinstance(_data, list)
        and _data
        and (
            force_sequence
            or (
                uses_typed_literal_for_scalars
                and all(
                    isinstance(item, (str, int, float, bool, bytes))
                    for item in _data
                )
            )
        )
    )
    if use_sequence:
        return f"{keyword} {name} = @{value}"
    if force_sequence or not uses_json_wrap:
        return f"{keyword} {name} = {value}"
    return f"{keyword} {name} = %* {value}"


@beartype
def _make_variable_declaration(
    *,
    uses_typed_literal_for_scalars: bool,
    keyword: str,
    force_sequence: bool,
    uses_json_wrap: bool,
) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
    """Create a Nim variable declaration formatter."""

    def _format(
        name: str,
        value: str,
        _data: Value,
        _modifiers: frozenset[enum.Enum],
    ) -> str:
        """Delegate to module-level implementation."""
        return _apply_nim_variable_declaration(
            name=name,
            value=value,
            _data=_data,
            uses_typed_literal_for_scalars=uses_typed_literal_for_scalars,
            keyword=keyword,
            force_sequence=force_sequence,
            uses_json_wrap=uses_json_wrap,
        )

    return _format


@beartype
def _apply_nim_variable_assignment(
    *,
    name: str,
    value: str,
    _data: Value,
    uses_typed_literal_for_scalars: bool,
    uses_json_wrap: bool,
) -> str:
    """Format an assignment, using ``@`` for flat sequences of
    simple scalars.
    """
    if (
        uses_typed_literal_for_scalars
        and isinstance(_data, list)
        and _data
        and all(
            isinstance(item, (str, int, float, bool, bytes)) for item in _data
        )
    ):
        return f"{name} = @{value}"
    if not uses_json_wrap:
        return f"{name} = {value}"
    return f"{name} = %* {value}"


@beartype
def _make_variable_assignment(
    *,
    uses_typed_literal_for_scalars: bool,
    uses_json_wrap: bool,
) -> Callable[[str, str, Value], str]:
    """Create a Nim variable assignment formatter."""

    def _format(name: str, value: str, _data: Value) -> str:
        """Delegate to module-level implementation."""
        return _apply_nim_variable_assignment(
            name=name,
            value=value,
            _data=_data,
            uses_typed_literal_for_scalars=uses_typed_literal_for_scalars,
            uses_json_wrap=uses_json_wrap,
        )

    return _format


@dataclasses.dataclass(frozen=True)
class _VariantSignature:
    """Name and optional field info for one Nim object variant branch.

    ``field_name`` and ``field_type`` are ``None`` for unit variants
    (e.g. ``vkNull``); for payload-carrying variants they're the field
    identifier and Nim type used inside the ``of`` branch.
    """

    kind_name: str
    field_name: str | None
    field_type: str | None


@beartype
def _nim_variant_for_scalar(  # pylint: disable=too-complex
    *,
    value: Scalar,
    date_type: str,
    datetime_type: str,
) -> _VariantSignature:
    """Return the Nim object-variant signature for *value*."""
    match value:
        case bool():
            signature = _VariantSignature(
                kind_name="vkBool",
                field_name="boolVal",
                field_type="bool",
            )
        case int():
            signature = _VariantSignature(
                kind_name="vkInt",
                field_name="intVal",
                field_type="int",
            )
        case float():
            signature = _VariantSignature(
                kind_name="vkFloat",
                field_name="floatVal",
                field_type="float",
            )
        case str():
            signature = _VariantSignature(
                kind_name="vkStr",
                field_name="strVal",
                field_type="string",
            )
        case bytes():
            signature = _VariantSignature(
                kind_name="vkBytes",
                field_name="bytesVal",
                field_type="string",
            )
        case datetime.datetime():
            signature = _VariantSignature(
                kind_name="vkDateTime",
                field_name="dateTimeVal",
                field_type=datetime_type,
            )
        case datetime.date():
            signature = _VariantSignature(
                kind_name="vkDate",
                field_name="dateVal",
                field_type=date_type,
            )
        case datetime.time():
            signature = _VariantSignature(
                kind_name="vkTime",
                field_name="timeVal",
                field_type="string",
            )
        case None:
            signature = _VariantSignature(
                kind_name="vkNull",
                field_name=None,
                field_type=None,
            )
        case _ as unreachable:
            assert_never(unreachable)
    return signature


@dataclasses.dataclass(frozen=True, eq=False)
class _HeterogeneousStrategyConfig:
    """Configuration for one Nim heterogeneous-values strategy.

    ``build_behavior`` produces the
    :class:`~literalizer._language.HeterogeneousBehavior` exposed on a
    Nim instance.  ``build_preamble`` produces the data-dependent
    preamble callable (e.g. the object-variant type declaration).  Both
    receive the Nim instance's configurable variant-type name and
    scalar type names so the resulting functions can close over them.

    ``eq=False`` keeps identity equality so two strategies that happen
    to share builder functions (``ERROR`` and ``RECORD`` both reuse the
    no-op error builders -- ``RECORD``'s real behavior/preamble are
    resolved per-instance) stay distinct enum members instead of Python
    folding the second into an alias of the first.
    """

    build_behavior: Callable[[str, str, str], HeterogeneousBehavior]
    build_preamble: Callable[
        [str, str, str, str],
        Callable[[Value], tuple[str, ...]],
    ]


@beartype
def _build_error_behavior(
    _variant_name: str,
    _date_type: str,
    _datetime_type: str,
    /,
) -> HeterogeneousBehavior:
    """ERROR strategy: no wrapping, no skipping of checks."""
    return NO_HETEROGENEOUS_BEHAVIOR


@beartype
def _build_error_preamble(
    _variant_name: str,
    _date_type: str,
    _datetime_type: str,
    _indent: str,
    /,
) -> Callable[[Value], tuple[str, ...]]:
    """ERROR strategy: no data-dependent preamble."""
    return no_data_preamble


@beartype
def _needs_json_wrap_for_field(field_type: str | None) -> bool:
    """Return whether *field_type* requires ``%*`` to convert a
    formatted scalar into the variant payload.

    The Nim ``NIM`` date / datetime formats emit a table-literal string
    like ``{"year": ..., ...}`` that only becomes a value when
    ``%*``-converted to a :class:`json.JsonNode`.
    """
    return field_type == "JsonNode"


@beartype
def _build_object_variant_behavior(
    variant_name: str,
    date_type: str,
    datetime_type: str,
    /,
) -> HeterogeneousBehavior:
    """OBJECT_VARIANT strategy: wrap scalars and skip scalar checks."""

    def _compute(data: Value) -> frozenset[int]:
        """Return container ids whose scalar children should wrap."""
        return collect_heterogeneous_container_ids(
            data=data
        ) | collect_sibling_map_wrap_ids(data=data)

    def _wrap(raw_value: Scalar, formatted: str) -> str:
        """Wrap a scalar as ``{variant_name}(kind: ..., ...Val: ...)``."""
        signature = _nim_variant_for_scalar(
            value=raw_value,
            date_type=date_type,
            datetime_type=datetime_type,
        )
        if signature.field_name is None:
            return f"{variant_name}(kind: {signature.kind_name})"
        payload = (
            f"%*{formatted}"
            if _needs_json_wrap_for_field(field_type=signature.field_type)
            else formatted
        )
        return (
            f"{variant_name}(kind: {signature.kind_name}, "
            f"{signature.field_name}: {payload})"
        )

    return HeterogeneousBehavior(
        skip_scalar_checks=True,
        compute_wrap_ids=_compute,
        wrap_scalar=_wrap,
        wrap_non_scalar=None,
        compute_call_slot_wrap_ids=no_compute_call_slot_wrap_ids,
        dict_open_for_wrap_ids=None,
        widens_nested_maps_by_wrapping_scalars=True,
        widens_unrecordizable_nested_sibling_maps=False,
        render_record_literal=None,
        compute_record_shapes=None,
        render_tuple_literal=None,
        compute_tuple_list_ids=None,
    )


@beartype
def _build_object_variant_preamble(
    variant_name: str,
    date_type: str,
    datetime_type: str,
    indent: str,
    /,
    *,
    compute_wrap_ids: Callable[[Value], frozenset[int]],
) -> Callable[[Value], tuple[str, ...]]:
    """Emit an object-variant ``type`` block for wrapped scalars.

    ``OBJECT_VARIANT`` supplies its broad collector, while ``RECORD``
    uses the same value carrier only for maps excluded from record
    rendering by its shared nested-map fallback and supplies that
    narrower collector.
    """

    def _preamble(data: Value, /) -> tuple[str, ...]:
        """Build the object-variant type declaration for *data*."""
        wrap_ids = compute_wrap_ids(data)
        if not wrap_ids:
            return ()
        scalars = iter_wrapped_scalars(data=data, wrap_ids=wrap_ids)
        variants: list[_VariantSignature] = []
        seen: set[str] = set()
        for scalar in scalars:
            signature = _nim_variant_for_scalar(
                value=scalar,
                date_type=date_type,
                datetime_type=datetime_type,
            )
            if signature.kind_name in seen:
                continue
            seen.add(signature.kind_name)
            variants.append(signature)
        half_indent = " " * (len(indent) // 2)
        kind_type = f"{variant_name}Kind"
        lines: list[str] = [
            "type",
            f"{half_indent}{kind_type} = enum",
            f"{indent}{', '.join(v.kind_name for v in variants)}",
            f"{half_indent}{variant_name} = object",
            f"{indent}case kind: {kind_type}",
        ]
        for variant in variants:
            if variant.field_name is None:
                lines.append(f"{indent}of {variant.kind_name}: discard")
            else:
                lines.append(
                    f"{indent}of {variant.kind_name}: "
                    f"{variant.field_name}: {variant.field_type}"
                )
        return tuple(lines)

    return _preamble


@beartype
def _build_default_object_variant_preamble(
    variant_name: str,
    date_type: str,
    datetime_type: str,
    indent: str,
    /,
) -> Callable[[Value], tuple[str, ...]]:
    """Build the broad ``OBJECT_VARIANT`` preamble."""

    def _compute_wrap_ids(data: Value, /) -> frozenset[int]:
        """Collect every heterogeneous container requiring a variant."""
        return collect_heterogeneous_container_ids(
            data=data,
        ) | collect_sibling_map_wrap_ids(data=data)

    return _build_object_variant_preamble(
        variant_name,
        date_type,
        datetime_type,
        indent,
        compute_wrap_ids=_compute_wrap_ids,
    )


# The ``RECORD`` strategy supports only auto ``Record0``/``Record1``/...
# names (no ``record_shape_names``, consistent with the other non-Rust
# ports), so the shared renderer always gets an empty custom-name
# mapping.
_NIM_NO_RECORD_SHAPE_NAMES: Mapping[frozenset[str], str] = MappingProxyType(
    mapping={},
)


@beartype
def _nim_record_field_identifier(key: str, /) -> str:
    """Return the Nim ``object`` field name for a dict *key*.

    Nim has style-insensitive identifiers that accept the original
    key, but the generated declaration and ``Record0(field: value,
    ...)`` literal read most naturally in the conventional Nim
    ``camelCase`` (e.g. ``is_done`` -> ``isDone``); the same conversion
    is applied to both so they always agree.
    """
    return IdentifierCase.CAMEL.convert(name=key)


@beartype
def _nim_render_record_declaration(
    name: str,
    fields: Sequence[RecordDeclarationField],
    /,
    *,
    indent: str,
) -> str:
    """Render a Nim ``type Name = object`` declaration with one
    indented ``field: Type`` member per resolved field.

    Emitted at module scope by the data-dependent preamble (each
    fixture is its own compilation unit, so file-scope ``type``
    sections never collide); the matching record *literal* stays in
    the value position via the normal value path.
    """
    lines = [f"type {name} = object"]
    lines += [
        f"{indent}{field.identifier}: {field.type_name}" for field in fields
    ]
    return "\n".join(lines)


@beartype
def _nim_record_literal(
    name: str,
    fields: Sequence[RecordLiteralField],
    /,
) -> RenderedRecordLiteral:
    """Render a Nim ``Name(field: value, ...)`` object-construction
    literal as structured pieces for the shared compact/multiline
    layout code.

    A trailing comma after the last field is valid in a Nim object
    constructor, so the language-wide trailing-comma config applies
    unchanged in the multiline form.
    """
    return RenderedRecordLiteral(
        head=f"{name}(",
        entries=tuple(
            f"{field.identifier}: {field.formatted}" for field in fields
        ),
        closer=")",
        compact_pad="",
    )


@beartype
def _nim_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    stub_return: StubReturn,
    _args: Sequence[Value],
    /,
    *,
    indent: str,
) -> tuple[str, ...]:
    """Return Nim stub declarations for a call name.

    VOID stubs use templates with ``varargs[untyped]``.  VALUE stubs use
    generic ``proc`` definitions with ``{.discardable.}`` because the
    ``{.discardable.}`` pragma is not valid on templates in Nim 2.x, and
    calling a value-returning template at statement level raises a
    compiler error without it.

    For single-part names the stub is emitted at module scope.  For
    dotted names object types are built bottom-up so that the Uniform
    Function Call Syntax of Nim lets the caller write
    ``app.client.fetch(x)`` as sugar for ``fetch(app.client, x)``.
    """
    method = parts[-1]

    if stub_return is StubReturn.VOID:
        if len(parts) == 1:
            return (f"template {method}(args: varargs[untyped]) = discard",)
        chain = list(parts[:-1])
        holder = chain[-1]
        holder_type = f"{holder.title()}Type"
        lines: list[str] = [f"type {holder_type} = object"]
        for i in range(len(chain) - 2, -1, -1):
            outer = chain[i]
            inner = chain[i + 1]
            inner_type = f"{inner.title()}Type"
            outer_type = f"{outer.title()}Type"
            lines.extend(
                [
                    f"type {outer_type} = object",
                    f"{indent}{inner}: {inner_type}",
                ]
            )
        lines.append(
            f"template {method}(self: {holder_type};"
            f" args: varargs[untyped]) = discard"
        )
        root = chain[0]
        root_type = f"{root.title()}Type"
        lines.append(f"var {root}: {root_type}")
        return tuple(lines)

    # VALUE: use a generic proc instead of a template
    type_params = [f"T{i}" for i in range(len(_params))]
    type_clause = f"[{', '.join(type_params)}]" if type_params else ""
    if len(parts) == 1:
        params_str = "; ".join(
            f"{p}: {t}" for p, t in zip(_params, type_params, strict=True)
        )
        return (
            f"proc {method}{type_clause}"
            f"({params_str}): int {{.discardable.}} = 0",
        )
    chain = list(parts[:-1])
    holder = chain[-1]
    holder_type = f"{holder.title()}Type"
    lines = [f"type {holder_type} = object"]
    for i in range(len(chain) - 2, -1, -1):
        outer = chain[i]
        inner = chain[i + 1]
        inner_type = f"{inner.title()}Type"
        outer_type = f"{outer.title()}Type"
        lines.extend(
            [
                f"type {outer_type} = object",
                f"{indent}{inner}: {inner_type}",
            ]
        )
    params_str = "; ".join(
        f"{p}: {t}" for p, t in zip(_params, type_params, strict=True)
    )
    self_and_params = (
        f"self: {holder_type}; {params_str}"
        if params_str
        else f"self: {holder_type}"
    )
    lines.append(
        f"proc {method}{type_clause}"
        f"({self_and_params}): int {{.discardable.}} = 0"
    )
    root = chain[0]
    root_type = f"{root.title()}Type"
    lines.append(f"var {root}: {root_type}")
    return tuple(lines)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Nim(metaclass=LanguageCls):
    """Nim language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.NIM`` — table literal,
              e.g. ``{"year": 2024, "month": 1, "day": 15}``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.NIM`` — table literal,
              e.g. ``{"year": 2024, "month": 1, "day": 15,
              "hour": 12, "minute": 30, "second": 0}``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.
    """

    format_integer_widened = no_format_integer_widened
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".nim"
    pygments_name = "nim"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    dict_supports_heterogeneous_values = False
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
    supports_default_dict_key_type = False
    supports_default_dict_value_type = False
    supports_default_sequence_element_type = False
    supports_default_set_element_type = False
    supports_default_ordered_map_value_type = False
    non_default_kwargs: ClassVar[dict[str, str]] = {
        "heterogeneous_value_variant_name": "JsonValue"
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
        record_variants=frozenset({RecordVariant.NONRECORD_DICT_FIELD}),
        nested_map_widening=NestedMapWideningVariant.NONE,
        modifier_sequence_format_overrides={},
    )
    supports_record_struct_name_prefix = True
    supports_record_shape_names = False
    supports_non_string_dict_keys = False

    class DateFormats(enum.Enum):
        """Date format options for Nim."""

        NIM = DateFormatConfig(
            formatter=date_ymd_formatter(
                template='{{"year": {year}, "month": {month}, "day": {day}}}',
            ),
            preamble_lines=(),
            type_produced=datetime.date,
        )
        ISO = DateFormatConfig(
            formatter=format_date_iso,
            preamble_lines=(),
            type_produced=str,
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Nim."""

        NIM = DatetimeFormatConfig(
            formatter=datetime_ymdhms_formatter(
                template='{{"year": {year}, "month": {month}, '
                '"day": {day}, "hour": {hour}, '
                '"minute": {minute}, "second": {second}}}',
            ),
            preamble_lines=(),
            type_produced=datetime.datetime,
        )
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            preamble_lines=(),
            type_produced=str,
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
        """Sequence type options for Nim."""

        SEQ = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="["),
            close="]",
            supports_heterogeneity=False,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=True,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )
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
        """Set type options for Nim."""

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
            prefix="#[",
            suffix=" ]#",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        VAR = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="var {name} = {value}"
            ),
            supports_redefinition=True,
        )
        LET = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="let {name} = {value}"
            ),
            supports_redefinition=False,
        )
        CONST = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="const {name} = {value}"
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
        positive_infinity="Inf",
        negative_infinity="-Inf",
        nan="NaN",
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

    class JsonTypes(enum.Enum):
        """JSON value type options for Nim."""

        JSON_NODE = "JsonNode"
        """Standard-library ``json.JsonNode`` value constructed via
        the ``%*`` macro.
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
        """Nim call style options."""

        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Strategy for representing dicts or lists whose scalar values
        span more than one Nim type.
        """

        ERROR = _HeterogeneousStrategyConfig(
            build_behavior=_build_error_behavior,
            build_preamble=_build_error_preamble,
        )
        """Raise
        :exc:`~literalizer.exceptions.HeterogeneousScalarCollectionError`
        (or
        :exc:`~literalizer.exceptions.HeterogeneousSiblingListsError`)
        when scalar values of mixed types appear in a container that
        cannot represent them.  This is the default, matching the
        strict-typing convention of Nim when tables and sequences are
        used without JSON wrapping.
        """

        OBJECT_VARIANT = _HeterogeneousStrategyConfig(
            build_behavior=_build_object_variant_behavior,
            build_preamble=_build_default_object_variant_preamble,
        )
        """Auto-generate a Nim object variant in the preamble containing
        only the branches actually present in the data, and wrap each
        heterogeneous scalar value as
        ``{VariantName}(kind: vkX, xVal: value)``.

        Switches the dict rendering from ``%* {key: value}`` (which
        relies on the ``json`` module) to ``{key: value}.toTable`` so
        that the object-variant values can be stored directly.  Nested
        sequences emit ``@[...]`` at every level, and the ``json``
        import is dropped unless a date or datetime format still
        produces a ``JsonNode`` payload.

        The variant-type name is configurable via
        :attr:`Nim.heterogeneous_value_variant_name` (default
        ``"Value"``).  Incompatible with ``DeclarationStyles.CONST``:
        ``.toTable`` and ``@[]`` are runtime constructors, so
        ``CONST`` requires a compile-time-expressible initializer.
        """

        # RECORD intentionally reuses the inert ERROR builders (its
        # real behavior/preamble are resolved per-instance, see
        # ``heterogeneous_behavior`` / ``data_dependent_preamble``);
        # ``_HeterogeneousStrategyConfig`` uses identity equality so
        # this stays a distinct member rather than an alias of ERROR,
        # which ``PIE796`` cannot tell apart.
        RECORD = _HeterogeneousStrategyConfig(  # noqa: PIE796
            build_behavior=_build_error_behavior,
            build_preamble=_build_error_preamble,
        )
        """Render each record-shaped dict (non-empty, string-keyed) as a
        generated module-scope ``type Record0 = object`` declaration plus
        a matching ``Record0(field: value, ...)`` literal, so a dict
        mixing scalars with a container is representable even though a
        Nim ``Table`` requires a homogeneous value type.

        Like ``OBJECT_VARIANT`` this switches collections to their
        native Nim constructors (``@[...]``, ``{...}.toTable``) so a
        ``seq``/``Table`` field is well-typed, but it wraps no scalars
        and emits no ``json``/``%*`` rendering.  Auto names
        ``Record0``, ``Record1``, ... (prefix configurable via
        :attr:`Nim.record_struct_name_prefix`); **no**
        ``record_shape_names``, **no** ``record_unify_optional_fields``,
        consistent with the other non-Rust ports.  Its behavior and
        struct preamble need the per-instance renderer, so they are
        resolved in :attr:`heterogeneous_behavior` /
        :attr:`data_dependent_preamble` rather than from the enum
        member's config builders (it reuses the no-op ``ERROR``
        builders, kept a distinct member by
        :class:`_HeterogeneousStrategyConfig`'s identity equality).
        Incompatible with ``DeclarationStyles.CONST`` for the same
        reason as ``OBJECT_VARIANT``: ``@[...]`` / ``.toTable`` are
        runtime constructors.
        """

    heterogeneous_strategies = HeterogeneousStrategies

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for Nim."""

        V2 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.CAMEL,
        IdentifierCase.PASCAL,
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

    date_format: DateFormats = DateFormats.NIM
    datetime_format: DatetimeFormats = DatetimeFormats.NIM
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.SEQ
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.HASH
    declaration_style: DeclarationStyles = DeclarationStyles.VAR
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
    trailing_comma: TrailingCommas = TrailingCommas.NO
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.SEMICOLON
    )
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    json_type: JsonTypes | None = None
    heterogeneous_value_variant_name: str = "Value"
    record_struct_name_prefix: str = "Record"
    call_style: CallStyles = CallStyles.POSITIONAL
    # Keep in sync with the ``NIM_VERSION`` pin in the ``lint-nim`` job
    # of ``.github/workflows/lint.yml``; the pinned compiler must be
    # ``>=`` this ``V2`` (Nim 2.x) default.
    language_version: VersionFormats = VersionFormats.V2
    indent: str = "    "

    def __post_init__(self) -> None:
        """Validate that incompatible formats are not combined.

        ``OBJECT_VARIANT`` and ``RECORD`` replace the JSON-based
        rendering for Nim with runtime ``.toTable`` / ``@[]``
        constructors, so ``CONST`` (which requires a
        compile-time-expressible initializer) cannot be combined with
        either.  ``json_type`` uses the runtime ``%*`` macro for the
        same reason and is likewise incompatible with ``CONST``.
        """
        _decl_cls = type(self.declaration_style)
        _strategy_cls = type(self.heterogeneous_strategy)
        if self.declaration_style is _decl_cls.CONST and (
            self.heterogeneous_strategy
            in {_strategy_cls.OBJECT_VARIANT, _strategy_cls.RECORD}
        ):
            msg = (
                "Nim CONST requires a constant-expression initializer, "
                f"but {self.heterogeneous_strategy.name} produces runtime "
                ".toTable / @[] calls which are not constant expressions. "
                "Use VAR or LET instead."
            )
            raise IncompatibleFormatsError(msg)
        if (
            self.json_type is not None
            and self.declaration_style is _decl_cls.CONST
        ):
            msg = (
                "Nim json_type uses the runtime %* macro, which is not a "
                "constant-expression initializer. Use VAR or LET instead."
            )
            raise IncompatibleFormatsError(msg)

    null_literal: ClassVar[str] = "nil"
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
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value

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
        return passthrough_set_entry

    @cached_property
    def _heterogeneous_variant_date_type(self) -> str:
        """Nim type used for :class:`datetime.date` variant payloads."""
        return (
            "string"
            if self.date_format.value.type_produced is str
            else "JsonNode"
        )

    @cached_property
    def _heterogeneous_variant_datetime_type(self) -> str:
        """Nim type used for :class:`datetime.datetime` variant
        payloads.
        """
        produced = self.datetime_format.value.type_produced
        if produced is str:
            return "string"
        if produced is int:
            return "int"
        return "JsonNode"

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        For ``HeterogeneousStrategies.RECORD`` emits one
        ``type Record0 = object`` block per distinct record shape in
        the data, preceded by ``import tables`` and the
        ``UnusedImport`` opt-out: a non-record dict (the empty dict, or
        an ordered map) renders as a runtime ``Table`` that needs the
        import, while a pure-record fixture leaves it unused, so the
        pragma keeps the always-present import warning-free rather than
        making the import data-dependent.  For
        ``HeterogeneousStrategies.OBJECT_VARIANT`` emits
        a Nim ``type`` block declaring the object variant used to wrap
        heterogeneous scalars.  For ``HeterogeneousStrategies.ERROR``
        emits ``("import json",)`` when the rendered output will use
        the ``%*`` JSON-construction operator (every variable
        declaration / assignment except ``const`` declarations and
        ``@``-prefixed sequences of simple scalars); importing
        ``json`` unconditionally would trigger the Nim compiler's
        ``UnusedImport`` warning.  Under ``json_type`` the rendered
        output always uses ``%*`` (and ``newJ*`` builders), so the
        import is emitted unconditionally and takes precedence over
        any configured heterogeneous strategy.
        """
        if self._uses_json_node:

            def _json_preamble(_data: Value, /) -> tuple[str, ...]:
                """Always import std/json for ``JsonNode`` output."""
                return ("import json",)

            return _json_preamble
        if self._uses_record:
            record_preamble = self._record_strategy.preamble
            variant_preamble = _build_object_variant_preamble(
                self.heterogeneous_value_variant_name,
                self._heterogeneous_variant_date_type,
                self._heterogeneous_variant_datetime_type,
                self.indent,
                compute_wrap_ids=(
                    self._record_strategy.behavior.compute_wrap_ids
                ),
            )

            def _record_preamble(data: Value, /) -> tuple[str, ...]:
                """Emit value-variant and record ``object`` type blocks,
                preceded by the ``UnusedImport`` opt-out and ``import
                tables``.
                """
                return (
                    "{.warning[UnusedImport]:off.}",
                    "import tables",
                    *variant_preamble(data),
                    *record_preamble(data),
                )

            return _record_preamble
        strategy_preamble = self.heterogeneous_strategy.value.build_preamble(
            self.heterogeneous_value_variant_name,
            self._heterogeneous_variant_date_type,
            self._heterogeneous_variant_datetime_type,
            self.indent,
        )
        if self._uses_object_variant:
            return strategy_preamble
        is_const = self.declaration_style is self.declaration_styles.CONST
        uses_typed_literal = (
            self.sequence_format.value.uses_typed_literal_for_scalars
        )

        def _preamble(data: Value, /) -> tuple[str, ...]:
            """Decide whether ``import json`` is required for *data*."""
            if is_const:
                return ()
            renders_as_at_sequence = (
                isinstance(data, list)
                and bool(data)
                and uses_typed_literal
                and all(
                    isinstance(item, (str, int, float, bool, bytes))
                    for item in data
                )
            )
            if renders_as_at_sequence:
                return ()
            return ("import json",)

        return _preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the behavior for the chosen heterogeneous strategy.

        ``json_type`` relaxes scalar-type checks unconditionally,
        because the ``%*`` macro accepts heterogeneous JSON values.
        ``RECORD`` resolves to the shared record behavior (its value
        needs the per-instance renderer, so it cannot be stored on the
        enum member); ``ERROR`` and ``OBJECT_VARIANT`` use their
        config-built behaviors.
        """
        if self._uses_json_node:
            return dataclasses.replace(
                NO_HETEROGENEOUS_BEHAVIOR,
                skip_scalar_checks=True,
                wrap_non_scalar=_nim_json_non_scalar_child,
            )
        if self._uses_record:
            return self._record_strategy.behavior
        return self.heterogeneous_strategy.value.build_behavior(
            self.heterogeneous_value_variant_name,
            self._heterogeneous_variant_date_type,
            self._heterogeneous_variant_datetime_type,
        )

    @cached_property
    def _uses_json_node(self) -> bool:
        """Whether the instance is configured to render values as
        ``JsonNode`` via the ``%*`` macro.
        """
        return self.json_type is not None

    @cached_property
    def _uses_object_variant(self) -> bool:
        """Whether the instance is configured for the OBJECT_VARIANT
        heterogeneous strategy.
        """
        cls = type(self.heterogeneous_strategy)
        return self.heterogeneous_strategy is cls.OBJECT_VARIANT

    @cached_property
    def _uses_record(self) -> bool:
        """Whether the instance is configured for the RECORD
        heterogeneous strategy.
        """
        cls = type(self.heterogeneous_strategy)
        return self.heterogeneous_strategy is cls.RECORD

    @cached_property
    def _uses_native_nim_collections(self) -> bool:
        """Whether collections render with their native Nim
        constructors (``@[...]`` / ``{...}.toTable``) rather than the
        ``%*`` JSON form.

        Both ``OBJECT_VARIANT`` (its wrapped values are native objects)
        and ``RECORD`` (its struct fields must be well-typed ``seq`` /
        ``Table`` values) need this; the default ``ERROR`` strategy
        keeps the JSON rendering.
        """
        return self._uses_object_variant or self._uses_record

    def _nim_value_field_type(  # noqa: C901, PLR0911  # pylint: disable=too-complex
        self,
        value: Value,
        /,
    ) -> str:
        """Return the Nim ``object`` field type for a raw
        (non-nested-record) record field value, derived structurally.

        ``None`` maps to the Nim ``pointer`` type, whose only value is
        ``nil`` (the null literal this port emits), matching how the
        other ports give a null field their top type.  Other scalars
        map to their Nim type and a homogeneous list maps to
        ``seq[<element type>]`` (an empty list keeps the
        ``newSeq[string]()`` placeholder element type the value
        formatter widens it to).  A ``date`` / ``datetime`` is the
        spec-driven Nim type only when the active format renders it as
        a plain ``string`` (ISO) or ``int`` (epoch); under the default
        ``NIM`` table-literal format it would need a ``%*``
        :class:`json.JsonNode` the record literal cannot carry, so it
        is rejected.  A set, an ordered map or a non-record dict as a
        record field is out of scope for the base ``RECORD`` port (the
        cross-language decision is tracked in #2317; Rust rejects these
        too) and is rejected with :exc:`UnrepresentableInputError` so
        the case is skipped rather than emitting non-compiling Nim.
        """
        match value:
            case None:
                return "pointer"
            case bool():
                return "bool"
            case int():
                return "int"
            case float():
                return "float"
            case str() | bytes() | datetime.time():
                return "string"
            case datetime.datetime():
                resolved = self._heterogeneous_variant_datetime_type
            case datetime.date():
                resolved = self._heterogeneous_variant_date_type
            case list():
                if not value:
                    return "seq[string]"
                return f"seq[{self._nim_value_field_type(value[0])}]"
            case _:
                msg = (
                    "Nim cannot represent a set or non-record-dict "
                    "field under the RECORD heterogeneous strategy"
                )
                raise UnrepresentableInputError(msg)
        if resolved == "JsonNode":
            msg = (
                "Nim cannot represent a NIM-table-literal date/datetime "
                "field under the RECORD heterogeneous strategy; use the "
                "ISO or EPOCH format"
            )
            raise UnrepresentableInputError(msg)
        return resolved

    def _nim_record_field_type(self, request: RecordFieldType, /) -> str:
        """Return the Nim ``object`` field type for a record field.

        A field whose value is itself a nested record-shaped dict uses
        that record's generated name; a list whose every element is a
        record-shaped dict of one shared shape is typed
        ``seq[<that name>]`` (a Nim ``seq`` is element-typed, unlike
        the ``[]any`` Go widens such a list to).  Every other value is
        typed structurally from the raw value via
        :meth:`_nim_value_field_type`.
        """
        if request.record_name is not None:
            return request.record_name
        if request.element_record_name is not None:
            return f"seq[{request.element_record_name}]"
        if (
            isinstance(request.value, dict)
            and not isinstance(request.value, OrderedMap)
            and record_shape_for_dict(value=request.value) is not None
        ):
            return f"Table[string, {self.heterogeneous_value_variant_name}]"
        return self._nim_value_field_type(request.value)

    @cached_property
    def _record_renderer(self) -> RecordRenderer:
        """Nim syntax hooks for the ``RECORD`` strategy."""
        return RecordRenderer(
            name_prefix=self.record_struct_name_prefix,
            record_shape_names=_NIM_NO_RECORD_SHAPE_NAMES,
            field_identifier=_nim_record_field_identifier,
            field_type=self._nim_record_field_type,
            render_declaration=partial(
                _nim_render_record_declaration,
                indent=self.indent,
            ),
            render_literal=_nim_record_literal,
        )

    @cached_property
    def _record_strategy(self) -> RecordStrategy:
        """Behavior + ``type``-declaration preamble for ``RECORD``."""
        strategy = build_record_strategy(
            renderer=self._record_renderer,
            split_conflicting_field_types=False,
            widen_unrecordizable_nested_sibling_maps=True,
            derecordized_map_open=None,
        )
        variant_behavior = _build_object_variant_behavior(
            self.heterogeneous_value_variant_name,
            self._heterogeneous_variant_date_type,
            self._heterogeneous_variant_datetime_type,
        )
        return dataclasses.replace(
            strategy,
            behavior=dataclasses.replace(
                strategy.behavior,
                wrap_scalar=variant_behavior.wrap_scalar,
                widens_nested_maps_by_wrapping_scalars=True,
            ),
        )

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
        return partial(_nim_call_stub, indent=self.indent)

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
    def call_data_dependent_preamble(
        self,
    ) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines for a call context.

        For ``HeterogeneousStrategies.RECORD`` emits the
        ``type Record0 = object`` blocks a record-shaped call argument's
        literal references, preceded -- exactly as the non-call
        :attr:`data_dependent_preamble` -- by the ``UnusedImport``
        opt-out and ``import tables`` (``dict_format_config`` no longer
        contributes it under ``RECORD``).  The opt-out is needed both
        for a record-only call (the import is then unused) and because
        a ``varargs[untyped]`` stub never evaluates its arguments, so
        even a non-record dict argument's ``{...}.toTable`` would leave
        the import unused.  For
        ``HeterogeneousStrategies.OBJECT_VARIANT`` emits the Nim
        ``type`` block declaring the object variant used to wrap
        heterogeneous scalars; the call rendering references that type
        by name, so the declaration must be present.  For other
        strategies, call arguments are inline literals that never use
        ``%*``, so ``import json`` is never needed in a call context.

        ``json_type`` wraps every call argument in ``%*``, so the
        ``import json`` line is contributed unconditionally here too.
        """
        if self._uses_json_node:

            def _json_call_preamble(_data: Value, /) -> tuple[str, ...]:
                """Always import std/json for ``JsonNode`` call
                arguments.

                Suppress ``UnusedImport`` because the stub uses
                ``varargs[untyped]`` and never evaluates the wrapped
                ``%*(...)`` expressions, so the Nim compiler treats the
                ``json`` import as unused.
                """
                return (
                    "{.warning[UnusedImport]:off.}",
                    "import json",
                )

            return _json_call_preamble
        if self._uses_record:
            record_preamble = self._record_strategy.preamble
            variant_preamble = _build_object_variant_preamble(
                self.heterogeneous_value_variant_name,
                self._heterogeneous_variant_date_type,
                self._heterogeneous_variant_datetime_type,
                self.indent,
                compute_wrap_ids=(
                    self._record_strategy.behavior.compute_wrap_ids
                ),
            )

            def _record_call_preamble(data: Value, /) -> tuple[str, ...]:
                """Suppress UnusedImport for ``tables`` and emit it plus
                the generated ``object`` type blocks (identical to the
                non-call :attr:`data_dependent_preamble`: a non-record
                dict argument needs the import, a record-only call
                leaves it harmlessly suppressed).
                """
                return (
                    "{.warning[UnusedImport]:off.}",
                    "import tables",
                    *variant_preamble(data),
                    *record_preamble(data),
                )

            return _record_call_preamble
        if self._uses_object_variant:
            strategy_preamble = (
                self.heterogeneous_strategy.value.build_preamble(
                    self.heterogeneous_value_variant_name,
                    self._heterogeneous_variant_date_type,
                    self._heterogeneous_variant_datetime_type,
                    self.indent,
                )
            )

            def _preamble(data: Value, /) -> tuple[str, ...]:
                """Suppress UnusedImport for ``tables`` and emit the
                object-variant type block.

                The ``import tables`` line is contributed by
                :attr:`dict_format_config` so that ``{...}.toTable``
                renders correctly, but the call stub uses
                ``varargs[untyped]`` and never evaluates its arguments,
                so the Nim compiler treats the import as unused.
                """
                return (
                    "{.warning[UnusedImport]:off.}",
                    *strategy_preamble(data),
                )

            return _preamble
        return no_data_preamble

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

        ``json_type`` wraps every sequence literal in the ``%*`` macro so
        it renders as a ``JsonNode`` array, and widens an empty sequence
        to ``newJArray()`` (the explicit JSON array builder).
        ``OBJECT_VARIANT`` and ``RECORD`` replace the JSON-array opener
        with ``@[`` so nested sequences render as Nim-native ``seq``
        literals at every level (the declaration formatter no longer
        adds a leading ``@`` because ``uses_typed_literal_for_scalars``
        is turned off).  Empty sequences widen to ``newSeq[string]()`` so
        the compiler does not reject ``var x = @[]`` with "cannot
        infer the type of the sequence" -- and, under ``RECORD``, so the
        widened element type matches the ``seq[string]`` an empty-list
        record field is declared.
        """
        base = self.sequence_format.value
        if self._uses_json_node:
            return dataclasses.replace(
                base,
                sequence_open=fixed_open(open_str=f"{_NIM_JSON_MACRO}(["),
                close="])",
                supports_heterogeneity=True,
                uses_typed_literal_for_scalars=False,
                preamble_lines=(),
                empty_sequence="newJArray()",
            )
        if not self._uses_native_nim_collections:
            return base
        return dataclasses.replace(
            base,
            sequence_open=fixed_open(open_str="@["),
            uses_typed_literal_for_scalars=False,
            preamble_lines=(),
            empty_sequence="newSeq[string]()",
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format.

        ``json_type`` renders a set as a JSON array via ``%*([...])``
        because JSON has no native set type; empty sets widen to
        ``newJArray()`` for the same reason empty sequences do.
        """
        if self._uses_json_node:
            return dataclasses.replace(
                self.set_format.value,
                set_open=fixed_open(open_str=f"{_NIM_JSON_MACRO}(["),
                close="])",
                empty_set="newJArray()",
                preamble_lines=(),
            )
        return self.set_format.value

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format_config.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting.

        ``OBJECT_VARIANT`` and ``RECORD`` append ``.toTable`` to the
        closing brace so every rendered (non-record) dict becomes a
        runtime :class:`tables.Table`.  An empty dict widens to
        ``initTable[string, string]()`` so the compiler does not reject
        ``{}.toTable``: an empty ``{}`` literal is an empty set rather
        than a table, so the call does not resolve and the key/value
        types cannot be inferred.  This mirrors the ``newSeq[string]()``
        widening for empty sequences.

        ``OBJECT_VARIANT`` always wraps its dicts as tables, so it
        carries the ``import tables`` preamble here.  Under ``RECORD`` a
        record-shaped dict never reaches this config (it is intercepted
        by the record renderer and emitted as a ``Record0(...)``
        literal), so ``import tables`` would be an ``UnusedImport`` for
        the common record-only fixture; the import is instead added by
        :attr:`data_dependent_preamble` only when the data still carries
        a genuinely non-record dict that renders as a table.

        ``json_type`` takes precedence: every dict literal is wrapped in
        ``%*({...})`` so it renders as a JSON object, and an empty dict
        widens to ``newJObject()`` (the explicit builder).  The
        ``import json`` line that powers ``%*`` is contributed by
        :attr:`data_dependent_preamble`, not by this config, so a
        heterogeneous-strategy-free fixture still imports it exactly
        once.
        """
        if self._uses_json_node:
            return DictFormatConfig(
                dict_open=fixed_open(open_str=f"{_NIM_JSON_MACRO}({{"),
                close="})",
                format_entry=dict_entry_with_separator(
                    separator=": ",
                    format_value=passthrough_sequence_entry,
                ),
                empty_dict="newJObject()",
                preamble_lines=(),
                narrowed_open=None,
                supports_trailing_comma=True,
            )
        if self._uses_native_nim_collections:
            return DictFormatConfig(
                dict_open=fixed_open(open_str="{"),
                close="}.toTable",
                format_entry=dict_entry_with_separator(
                    separator=": ",
                    format_value=passthrough_sequence_entry,
                ),
                empty_dict="initTable[string, string]()",
                preamble_lines=(
                    () if self._uses_record else ("import tables",)
                ),
                narrowed_open=None,
                supports_trailing_comma=True,
            )
        return DictFormatConfig(
            dict_open=fixed_open(open_str="{"),
            close="}",
            format_entry=dict_entry_with_separator(
                separator=": ",
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
        """Callable that formats a date as a string literal.

        ``json_type`` overrides the configured ``date_format`` with the
        ISO 8601 string form because the ``NIM`` table-literal form
        would not round-trip through JSON.
        """
        if self._uses_json_node:
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
            self._uses_json_node
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
        """Callable that formats an int value as a literal."""
        return make_overflow_fallback_formatter(
            base=self.integer_format.get_formatter(
                numeric_separator=self.numeric_separator,
            ),
            fallback=raise_for_unrepresentable_int(language_name="Nim"),
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

        ``OBJECT_VARIANT`` and ``RECORD`` render an ordered map with its
        native ``{...}.toOrderedTable`` constructor (an ordered map is
        never record-shaped, so ``RECORD`` leaves it on this path).
        ``json_type`` renders an ordered map as a JSON object (the
        ``%*`` macro preserves object-key insertion order in the
        rendered output).
        """
        if self._uses_json_node:
            return OrderedMapFormatConfig(
                ordered_map_open=fixed_open(open_str=f"{_NIM_JSON_MACRO}({{"),
                close="})",
                preamble_lines=(),
            )
        if self._uses_native_nim_collections:
            return OrderedMapFormatConfig(
                ordered_map_open=fixed_open(open_str="{"),
                close="}.toOrderedTable",
                preamble_lines=("import tables",),
            )
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="{"),
            close="}",
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
        """Callable that formats a new variable declaration.

        Under ``json_type`` the declaration carries an explicit
        ``: JsonNode`` type annotation and the right-hand side is wrapped
        by ``%*`` only when the value is not already a ``JsonNode``
        expression (the wrapping check in
        :func:`_nim_json_value_expression` skips re-wrapping ``%*(...)``
        and ``newJ*`` builders so the rendered output stays flat).
        """
        if self._uses_json_node:
            assert self.json_type is not None  # noqa: S101
            return _nim_json_declaration_formatter(
                declaration_style=self.declaration_style,
                json_type=self.json_type.value,
            )
        is_const = self.declaration_style is self.declaration_styles.CONST
        return _make_variable_declaration(
            uses_typed_literal_for_scalars=(
                self.sequence_format_config.uses_typed_literal_for_scalars
            ),
            keyword=self.declaration_style.name.lower(),
            force_sequence=is_const,
            uses_json_wrap=not self._uses_native_nim_collections,
        )

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable.

        Under ``json_type`` the assigned expression is wrapped by ``%*``
        through the same helper as the declaration form so the two
        halves of a combined declaration / assignment stay consistent.
        """
        if self._uses_json_node:
            return _format_nim_json_assignment
        return _make_variable_assignment(
            uses_typed_literal_for_scalars=(
                self.sequence_format_config.uses_typed_literal_for_scalars
            ),
            uses_json_wrap=not self._uses_native_nim_collections,
        )

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Callable that rewrites a formatted direct call argument.

        Under ``json_type`` every call argument is wrapped in ``%*`` so
        the underlying proc receives a ``JsonNode``; under any other
        mode call arguments pass through unchanged.
        """
        if self._uses_json_node:
            return _format_nim_json_call_arg
        return identity_call_arg

    @cached_property
    def format_call_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a declaration binding a call result.

        The literal-binding declaration prefixes the right-hand side
        with the ``%*`` json macro (or ``@`` for sequences) chosen from
        the parsed literal's type; that JSON-constructs a literal and is
        invalid for a call result.  The plain ``<keyword> <name> =
        <value>`` declaration-style formatter binds the call result
        directly with no wrapping.
        """
        return self.declaration_style.value.formatter

    @cached_property
    def format_call_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment binding a call result.

        The call-expression counterpart of
        :attr:`format_variable_assignment`; the ``%*``/``@`` wrapping is
        dropped since a call result is bound directly.  Unlike the
        declaration form this carries no ``var``/``let``/``const``
        keyword, so it does not reuse the declaration-style formatter.
        """
        return variable_formatter(template="{name} = {value}")

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble for Nim scalar types.

        Under the default ``ERROR`` heterogeneous strategy
        ``import json`` is added by :attr:`data_dependent_preamble`
        only when the rendered output uses ``%*``.  Under
        ``OBJECT_VARIANT`` scalars are emitted as native Nim values,
        except that the ``NIM`` date / datetime formats still
        produce a :class:`json.JsonNode` payload and require
        ``import json`` whenever a date or datetime is present.
        Under ``json_type`` the ``import json`` line is contributed
        unconditionally by :attr:`data_dependent_preamble`, so this
        method returns an empty per-scalar map to avoid duplicating it.
        """
        if self._uses_json_node:
            return {}
        if self._uses_object_variant:
            json_import = ("import json",)
            date_preamble = (
                ()
                if self.date_format.value.type_produced is str
                else json_import
            )
            datetime_preamble = (
                ()
                if self.datetime_format.value.type_produced in {str, int}
                else json_import
            )
            return {
                datetime.date: date_preamble,
                datetime.datetime: datetime_preamble,
            }
        return {
            datetime.date: self.date_format.value.preamble_lines,
            datetime.datetime: self.datetime_format.value.preamble_lines,
        }

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Nim needs none)."""
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
