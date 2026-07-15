"""V language specification."""

import dataclasses
import datetime
import enum
import textwrap
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
    datetime_epoch_formatter,
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
    make_unsigned_overflow_fallback,
)
from literalizer._formatters.format_strings import (
    format_string_backslash_dollar_single,
)
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
from literalizer._heterogeneous import (
    collect_heterogeneous_container_ids,
    collect_sibling_map_wrap_ids,
)
from literalizer._language import (
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
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
    identity_constructor_target,
    never_inhibits_consuming_form,
    no_call_binding_body_preamble,
    no_call_binding_file_pragmas,
    no_compute_call_slot_wrap_ids,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import OrderedMap, Scalar, Value

_V_I32_MIN = -(2**31)  # -2147483648
_V_I32_MAX = 2**31 - 1  # 2147483647

_V_IFACE_NAME = "IVal"
_V_IFACE_DECL = f"interface {_V_IFACE_NAME} {{}}"
_V_NULL_WRAPPED = f"{_V_IFACE_NAME}(unsafe {{ nil }})"

_v_element_to_type = make_element_to_type(
    str_type="string",
    bool_type="bool",
    int_type="int",
    wide_int_type="i64",
    float_type="f64",
    bytes_type="string",
    mixed_numeric_type="string",
    date_type="string",
    datetime_type="string",
    time_type="string",
    list_template="[]{inner}",
    enable_list_type=True,
    dict_type_template=None,
    fallback_value_type=_V_IFACE_NAME,
)

_v_narrowed_empty_form = make_narrowed_empty_form(
    element_to_type=_v_element_to_type,
    template="[]{type}{{}}",
    fallback_type=_V_IFACE_NAME,
)


@beartype
def _format_v_u64_positive(value: int) -> str:
    """Format a positive value outside signed 64-bit range as a V
    ``u64`` typed conversion.
    """
    return f"u64({value})"


@beartype
def _make_v_i64_formatter(
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Return a formatter that wraps *base*-formatted values in
    ``i64(...)``.

    Used for values that overflow V's 32-bit ``int`` but fit in ``i64``.
    The inner representation preserves the requested integer format (hex,
    octal, binary, etc.) rather than forcing decimal.
    """

    def _format(value: int) -> str:
        """Format *value* as ``i64(<base(value)>)``."""
        return f"i64({base(value)})"

    return _format


@beartype
def _v_collect_ids_needing_wrap(  # pylint: disable=too-complex
    data: Value,
) -> frozenset[int]:
    """Return container ids that need interface-type wrapping in V.

    Extends :func:`collect_heterogeneous_container_ids` with a
    bottom-up traversal that also catches:

    * Empty containers (V requires explicit typed empty literals).
    * Containers with any ``None`` values (V cannot store ``none`` in
      typed collections).
    * Sets with mixed Python types.
    * Containers whose children have mixed V types because some
      children are in wrap_ids and others are not.
    * Maps that are individually homogeneous yet must widen because a
      sibling map at the same slot does
      (:func:`collect_sibling_map_wrap_ids`, issue #2896).
    """
    base_ids = collect_heterogeneous_container_ids(
        data=data
    ) | collect_sibling_map_wrap_ids(data=data)
    wrap_ids: set[int] = set(base_ids)

    def _visit(item: Value) -> None:
        """Recursively mark *item* and its containers if wrapping
        needed.
        """
        match item:
            case dict():
                children: list[Value] = list(item.values())
            case list() | set():
                children = list(item)
            case _:
                return
        for child in children:
            _visit(item=child)
        if id(item) in wrap_ids:
            return
        if not children or any(v is None for v in children):
            wrap_ids.add(id(item))
            return
        python_types = {type(v) for v in children if v is not None}
        if len(python_types) > 1:
            wrap_ids.add(id(item))
            return
        container_children = [
            v for v in children if isinstance(v, (list, dict, set))
        ]
        if container_children:
            wrapped = [v for v in container_children if id(v) in wrap_ids]
            if wrapped and len(wrapped) < len(container_children):
                wrap_ids.add(id(item))

    _visit(item=data)
    return frozenset(wrap_ids)


@beartype
def _build_v_interface_behavior() -> HeterogeneousBehavior:
    """INTERFACE strategy: wrap scalars in ``IVal(...)``."""

    def _compute(data: Value) -> frozenset[int]:
        """Return container ids whose scalar children should be
        wrapped.
        """
        return _v_collect_ids_needing_wrap(data=data)

    def _wrap_scalar(raw_value: Scalar, formatted: str) -> str:
        """Wrap a scalar as ``IVal(formatted)`` or the null sentinel."""
        if raw_value is None:
            return _V_NULL_WRAPPED
        return f"{_V_IFACE_NAME}({formatted})"

    def _wrap_non_scalar(_raw_value: Value, formatted: str) -> str:
        """Wrap a ref marker or container's formatted form as
        ``IVal(formatted)``.
        """
        return f"{_V_IFACE_NAME}({formatted})"

    return HeterogeneousBehavior(
        skip_scalar_checks=True,
        compute_wrap_ids=_compute,
        wrap_scalar=_wrap_scalar,
        wrap_non_scalar=_wrap_non_scalar,
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
def _build_v_interface_preamble(
    *,
    compute_wrap_ids: Callable[[Value], frozenset[int]],
) -> Callable[[Value], tuple[str, ...]]:
    """Emit ``interface IVal {}`` when an interface-wrapped map is used.

    ``INTERFACE`` supplies its broad collector, while ``RECORD`` passes
    the narrower set of maps excluded from record rendering by its
    shared nested-map fallback.
    """

    def _preamble(data: Value, /) -> tuple[str, ...]:
        """Emit ``interface IVal {}`` when any container needs
        wrapping.
        """
        wrap_ids = compute_wrap_ids(data)
        if not wrap_ids:
            return ()
        return (_V_IFACE_DECL,)

    return _preamble


@beartype
def _build_v_empty_container_preamble() -> Callable[[Value], tuple[str, ...]]:
    """ERROR strategy: emit ``interface IVal {}`` when empty containers
    will render as ``[]IVal{}`` / ``map[string]IVal{}``.
    """

    def _has_empty_container(item: Value) -> bool:
        """Return True if *item* or any descendant is an empty list,
        dict, or set.
        """
        match item:
            case dict():
                return not item or any(
                    _has_empty_container(item=v) for v in item.values()
                )
            case list() | set():
                return not item or any(
                    _has_empty_container(item=v) for v in item
                )
            case _:
                return False

    def _preamble(data: Value, /) -> tuple[str, ...]:
        """Emit ``interface IVal {}`` when an empty collection literal
        will reference it.
        """
        if not _has_empty_container(item=data):
            return ()
        return (_V_IFACE_DECL,)

    return _preamble


@beartype
def _v_call_preamble_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    stub_return: StubReturn,
    _args: Sequence[Value],
    /,
    *,
    indent: str,
) -> tuple[str, ...]:
    """Return V preamble stub declarations for a call name.

    Includes ``interface ICallArg_ {}`` in every result so that
    duplicate copies can be dropped when multiple stubs are combined.
    For dotted targets like ``app.client.fetch``, one struct per
    prefix level is emitted together with the method declaration.
    """
    iface = "interface ICallArg_ {}"

    if len(parts) == 1:
        if stub_return is StubReturn.VOID:
            return (iface, f"fn {parts[0]}(args ...ICallArg_) {{}}")
        return (
            iface,
            f"fn {parts[0]}(args ...ICallArg_) ICallArg_ {{ return 0 }}",
        )

    def _cap_type(name: str, /) -> str:
        """Return *name* with an upper-case first letter and ``Type_``
        suffix.
        """
        return name[0].upper() + name[1:] + "Type_"

    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    receiver_type = _cap_type(fields[-1]) if fields else _cap_type(root)

    if stub_return is StubReturn.VOID:
        method_line = (
            f"fn (r {receiver_type}) {method}(args ...ICallArg_) {{}}"
        )
    else:
        method_line = (
            f"fn (r {receiver_type}) {method}(args ...ICallArg_)"
            f" ICallArg_ {{ return 0 }}"
        )

    lines: list[str] = [iface, f"struct {receiver_type} {{}}", method_line]

    if fields:
        prev_type = receiver_type
        for i in range(len(fields) - 2, -1, -1):
            curr_type = _cap_type(fields[i])
            field = fields[i + 1]
            lines.append(
                f"struct {curr_type} {{\n{indent}{field} {prev_type}\n}}"
            )
            prev_type = curr_type
        root_type = _cap_type(root)
        lines.append(
            f"struct {root_type} {{\n{indent}{fields[0]} {prev_type}\n}}"
        )

    return tuple(lines)


@beartype
def _v_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return V body-level variable stubs for a call name.

    For dotted targets the root variable is declared inside ``fn main``
    so it is in scope when the call expression is evaluated.  Simple
    one-part targets are declared at file level (preamble) and need no
    body stub.
    """
    if len(parts) == 1:
        return ()
    root = parts[0]
    root_type = root[0].upper() + root[1:] + "Type_"
    return (f"{root} := {root_type}{{}}",)


# The ``RECORD`` strategy supports only auto ``Record0``/``Record1``/...
# names (no ``record_shape_names``, consistent with the other non-Rust
# ports), so the shared renderer always gets an empty custom-name
# mapping.
_V_NO_RECORD_SHAPE_NAMES: Mapping[frozenset[str], str] = MappingProxyType(
    mapping={},
)

# V scalar type for a record field, keyed by the value's exact Python
# type.  ``bool`` and ``int`` are not here (they have dedicated handling
# -- ``bool`` matches before ``int`` and an integer is sized by its own
# magnitude).  ``None`` renders as ``unsafe { nil }``, whose V type is
# ``voidptr``.  A ``bytes`` value renders as a hex/base64 string and
# every date/datetime/time format V supports renders a string, so they
# all map to ``string``; an ``EPOCH`` datetime is converted to its
# epoch integer before this lookup is reached, so the ``datetime`` entry
# only ever resolves an ISO datetime.
_V_SCALAR_FIELD_TYPE: Mapping[type, str] = MappingProxyType(
    mapping={
        type(None): "voidptr",
        float: "f64",
        str: "string",
        bytes: "string",
        datetime.date: "string",
        datetime.datetime: "string",
        datetime.time: "string",
    },
)


@beartype
def _v_int_field_type(value: int, /) -> str:
    """Return the V ``struct`` field type for an integer record field.

    Mirrors the literal :attr:`V.format_integer` emits: a value inside
    signed 32-bit range is a bare literal typed ``int``; a value only
    inside signed 64-bit range is wrapped ``i64(...)`` and is therefore
    ``i64``; a positive value beyond signed 64-bit range is wrapped
    ``u64(...)`` and is therefore ``u64`` (a negative value beyond
    signed 64-bit range raises at format time, so that side is never
    reached here).
    """
    if _V_I32_MIN <= value <= _V_I32_MAX:
        return "int"
    if I64_MIN <= value <= I64_MAX:
        return "i64"
    return "u64"


@beartype
def _v_inner_type(items: list[Value], /) -> str:
    """Return the V element type a homogeneous *items* list compiles
    to.

    A non-empty homogeneous list is the only kind that reaches here: a
    heterogeneous one raises before the preamble is built (V has no
    unwrapped heterogeneous container under ``RECORD``).  The shared
    element-type inference resolves the common Python element type (an
    ``int`` outside signed 32-bit range widens to the ``i64`` the value
    formatter casts every element to), and an empty list -- the one
    ``None`` case still reachable here (e.g. ``record_sequence``'s
    empty ``tags``) -- falls back to the empty-collection element type
    ``IVal``, exactly matching the ``[]IVal{}`` literal the value
    formatter emits.
    """
    inner = infer_element_type(items=items)
    resolved = _v_element_to_type(inner) if inner is not None else None
    return resolved or _V_IFACE_NAME


@beartype
def _v_record_field_identifier(key: str, /) -> str:
    """Return the V ``struct`` member name for a dict *key*.

    V member identifiers are the dict keys verbatim (no case
    conversion), matching the ``Record0{ id: 1, ... }`` literal form.
    """
    return key


@beartype
def _v_record_literal(
    name: str,
    fields: Sequence[RecordLiteralField],
    /,
) -> RenderedRecordLiteral:
    """Render a V ``Name{ field: value, ... }`` struct literal as
    structured pieces for the shared compact/multiline layout code.

    A trailing comma after the last field is valid in a V struct
    literal, so the language-wide trailing-comma config applies
    unchanged in the multiline form.
    """
    return RenderedRecordLiteral(
        head=f"{name}{{",
        entries=tuple(
            f"{field.identifier}: {field.formatted}" for field in fields
        ),
        closer="}",
        compact_pad=" ",
    )


@beartype
def _build_v_record_preamble(
    *,
    record_preamble: Callable[[Value], tuple[str, ...]],
    interface_preamble: Callable[[Value], tuple[str, ...]],
) -> Callable[[Value], tuple[str, ...]]:
    """Build the ``RECORD``-strategy ``data_dependent_preamble``.

    Composes the ``interface IVal {}`` line (emitted for an empty
    collection or a nested map excluded from record rendering) followed by
    generated
    ``struct`` declarations.  The interface precedes declarations so a
    declared field may name ``[]IVal`` or ``map[string]IVal``.
    """
    empty_container_preamble = _build_v_empty_container_preamble()

    def _record_pre(data: Value, /) -> tuple[str, ...]:
        """Return the ``interface IVal {}`` line (when needed) plus the
        ``struct`` declarations.
        """
        return tuple(
            dict.fromkeys(
                (
                    *empty_container_preamble(data),
                    *interface_preamble(data),
                    *record_preamble(data),
                ),
            ),
        )

    return _record_pre


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class V(metaclass=LanguageCls):
    """V language specification.

    Args:
        declaration_style: How to declare variables.

            * ``declaration_styles.ASSIGN`` — immutable short
              declaration, e.g. ``x := value``.
            * ``declaration_styles.MUT`` — mutable short
              declaration, e.g. ``mut x := value``.
    """

    format_call_variable_declaration = default_format_call_variable_declaration
    format_call_variable_assignment = default_format_call_variable_assignment
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".v"
    pygments_name = "v"
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
    non_default_kwargs: ClassVar[dict[str, str]] = {}
    declaration_style_sequence_format_overrides: ClassVar[dict[str, str]] = {}
    json_type_variant_name_suffix: ClassVar[str | None] = None
    supports_non_ascii_string_literals = True
    variant_metadata: ClassVar[VariantMetadata] = VariantMetadata(
        pre_indent_comment_scalar_variant=False,
        fixture_module_name_template=None,
        fixture_module_name_lowercase=False,
        golden_filename_lowercase=False,
        collection_layout_category="collection_layout",
        record_variants=frozenset(),
        nested_map_widening=NestedMapWideningVariant.NONE,
        modifier_sequence_format_overrides={},
    )
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
        """Date format options for V."""

        ISO = DateFormatConfig(
            formatter=format_date_iso, type_produced=str, preamble_lines=()
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for V."""

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
        """Sequence type options for V."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="["),
            close="]",
            supports_heterogeneity=False,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=f"[]{_V_IFACE_NAME}{{}}",
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=_v_narrowed_empty_form,
        )

    class SetFormats(enum.Enum):
        """Set type options for V."""

        ARRAY = SetFormatConfig(
            set_open=fixed_open(open_str="["),
            close="]",
            empty_set=f"[]{_V_IFACE_NAME}{{}}",
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=False,
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

        ASSIGN = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="{name} := {value}"
            ),
            supports_redefinition=False,
        )
        MUT = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="mut {name} := {value}"
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
        positive_infinity="math.inf(1)",
        negative_infinity="math.inf(-1)",
        nan="math.nan()",
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

        SINGLE = enum.auto()

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

        NEWLINE = enum.auto()

    statement_terminator_styles = StatementTerminatorStyles

    class CallStyles(enum.Enum):
        """V call style options."""

        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Heterogeneous-scalar strategy options for V."""

        ERROR = enum.auto()
        """Raise on heterogeneous scalar collections (default).

        V is statically typed and rejects unwrapped heterogeneous
        collections, so the default refuses to render them rather than
        emit code the V compiler will not accept.  Callers that want
        to materialize such data must opt in to ``INTERFACE`` or
        ``RECORD``.

        Still emits ``interface IVal {}`` when the data contains an
        empty list, dict, or set, because the empty-literal rendering
        (``[]IVal{}`` / ``map[string]IVal{}``) references it regardless
        of strategy.
        """

        INTERFACE = enum.auto()
        """Wrap heterogeneous scalars and null values with ``IVal(...)``
        and emit ``interface IVal {}`` in the file preamble.
        """

        RECORD = enum.auto()
        """Render each record-shaped dict (non-empty, string-keyed) as a
        generated file-scope ``struct`` plus a matching
        ``Record0{ field: value, ... }`` literal, so a dict may mix
        scalars and containers that a homogeneous ``map[string]V``
        cannot.

        The behavior and preamble are resolved per instance from
        :attr:`_record_strategy` (the shared record behavior needs the
        per-instance renderer, so it cannot be stored on the enum
        member).
        """

    heterogeneous_strategies = HeterogeneousStrategies

    class JsonTypes(enum.Enum):
        """Empty: this language has no JSON value-type variants."""

    json_types = JsonTypes

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for V."""

        V0_4 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = frozenset(
        {IdentifierCase.SNAKE}
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
        """Wrap a V declaration in ``fn main()``."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        indented = textwrap.indent(text=content, prefix=self.indent)
        use_line = (
            f"\n{self.indent}_ = {variable_name}" if variable_name else ""
        )
        return f"\nfn main() {{\n{indented}{use_line}\n}}"

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap V declaration + assignment in ``fn main()``."""
        return self.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.ARRAY
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
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
    string_format: StringFormats = StringFormats.SINGLE
    trailing_comma: TrailingCommas = TrailingCommas.YES
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.NEWLINE
    )
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    record_struct_name_prefix: str = "Record"
    # Keep in sync with the pinned V release downloaded by the
    # ``Install V`` step of the ``lint-v`` job in
    # ``.github/workflows/lint.yml``: the pinned ``weekly.2026.08``
    # release is ``>=`` this ``V0_4`` default, so the fixture gate
    # runs under a compiler that accepts the declared language
    # version.  (The ``0.5.1`` stable is too old: it emits broken C
    # for the interface-strategy float fixtures.)
    language_version: VersionFormats = VersionFormats.V0_4
    indent: str = "\t"
    call_style: CallStyles = CallStyles.POSITIONAL

    null_literal: ClassVar[str] = "unsafe { nil }"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = True
    statement_terminator: ClassVar[str] = ";"
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ("import math",)

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Return the active call-style configuration."""
        return self.call_style.value

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash_dollar_single

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        return variable_formatter(template="{name} = {value}")

    def _v_epoch_normalized(self, value: Value, /) -> Value:
        """Return *value* with every ``datetime.datetime`` replaced by
        its epoch-second integer when the active datetime format renders
        epochs (``EPOCH``), descending through lists so a datetime
        element is typed like the integer literal the value formatter
        emits for it rather than as the ``string`` the generic resolver
        would map ``datetime.datetime`` to.

        A plain ``datetime.date`` / ``datetime.time`` (which always
        renders as a string) and every non-datetime value pass through
        unchanged; the list walk runs for every list field, so the
        branch is exercised independently of the datetime format.
        """
        match value:
            case datetime.datetime() if (
                self.datetime_format.value.type_produced is int
            ):
                return datetime_epoch_seconds(value=value)
            case list():
                return [self._v_epoch_normalized(item) for item in value]
            case _:
                return value

    def _v_type_for_value(self, value: Value, /) -> str:
        """Return the V type the rendered literal for *value* compiles
        to.

        A scalar maps to its V type, with an integer sized by its own
        magnitude to match the rendered literal (``int`` / the
        ``i64(...)``-wrapped ``i64`` / the ``u64(...)``-wrapped ``u64``)
        and an ``EPOCH`` datetime rendered as -- and sized like -- its
        epoch integer (a list of ``EPOCH`` datetimes likewise compiles
        to ``[]int`` / ``[]i64``), while every other
        date/datetime/time/bytes format renders a string and ``None``
        renders ``unsafe { nil }`` (a ``voidptr``).  A list compiles to
        ``[]`` of its element type (an empty list to ``[]IVal``,
        matching the ``[]IVal{}`` empty literal).

        An ordered map remains out of scope for the base ``RECORD``
        port (the cross-language decision is tracked in #2317).  A
        plain nested map excluded from record rendering by the shared
        sibling-map fallback is instead typed as ``map[string]IVal`` by
        :meth:`_v_record_field_type`.
        """
        value = self._v_epoch_normalized(value)
        match value:
            case bool():
                return "bool"
            case int():
                return _v_int_field_type(value)
            case list():
                return f"[]{_v_inner_type(value)}"
            case _:
                return _V_SCALAR_FIELD_TYPE.get(type(value)) or _V_IFACE_NAME

    def _v_record_field_type(self, request: RecordFieldType, /) -> str:
        """Return the V ``struct`` field type for a record field.

        A field whose value is itself a nested record-shaped dict uses
        that record's generated name; a field whose value is a
        non-empty list of record-shaped dicts of one shared shape is
        typed ``[]RecordN`` (the element struct name the shared strategy
        resolves, which V infers from the ``[RecordN{...}, ...]``
        literal).  Every other value is typed structurally by
        :meth:`_v_type_for_value`.
        """
        if request.record_name is not None:
            return request.record_name
        if request.element_record_name is not None:
            return f"[]{request.element_record_name}"
        if (
            isinstance(request.value, dict)
            and not isinstance(request.value, OrderedMap)
            and record_shape_for_dict(value=request.value) is not None
        ):
            return f"map[string]{_V_IFACE_NAME}"
        return self._v_type_for_value(request.value)

    def _v_render_record_declaration(
        self,
        name: str,
        fields: Sequence[RecordDeclarationField],
        /,
    ) -> str:
        """Render a V ``struct Name { ... }`` with one
        newline-separated ``field Type`` per line.

        V struct fields are newline-separated (no terminator), matching
        the file-scope ``struct`` declarations
        :func:`_v_call_preamble_stub` already emits.  The block is
        emitted at file scope by the data-dependent preamble (each V
        fixture is compiled on its own, so file-scope ``struct``
        declarations never collide across cases).
        """
        lines = [f"struct {name} {{"]
        lines += [
            f"{self.indent}{field.identifier} {field.type_name}"
            for field in fields
        ]
        lines.append("}")
        return "\n".join(lines)

    @cached_property
    def _record_renderer(self) -> RecordRenderer:
        """V syntax hooks for the ``RECORD`` strategy."""
        return RecordRenderer(
            name_prefix=self.record_struct_name_prefix,
            record_shape_names=_V_NO_RECORD_SHAPE_NAMES,
            field_identifier=_v_record_field_identifier,
            field_type=self._v_record_field_type,
            render_declaration=self._v_render_record_declaration,
            render_literal=_v_record_literal,
        )

    @cached_property
    def _record_strategy(self) -> RecordStrategy:
        """Behavior + ``struct``-declaration preamble for ``RECORD``."""
        strategy = build_record_strategy(
            renderer=self._record_renderer,
            split_conflicting_field_types=False,
            widen_unrecordizable_nested_sibling_maps=True,
            derecordized_map_open=None,
            allow_same_key_record_variants_in_sequences=False,
        )
        interface_behavior = _build_v_interface_behavior()
        return dataclasses.replace(
            strategy,
            behavior=dataclasses.replace(
                strategy.behavior,
                wrap_scalar=interface_behavior.wrap_scalar,
                wrap_non_scalar=interface_behavior.wrap_non_scalar,
                widens_nested_maps_by_wrapping_scalars=True,
            ),
        )

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines for the chosen strategy.

        ``RECORD`` emits the ``interface IVal {}`` line (when an empty
        container references it) followed by one ``struct`` declaration
        per record shape; ``INTERFACE`` emits the interface when any
        container needs wrapping; ``ERROR`` emits the interface only
        for an empty-collection literal.
        """
        match self.heterogeneous_strategy.name:
            case "RECORD":
                return _build_v_record_preamble(
                    record_preamble=self._record_strategy.preamble,
                    interface_preamble=_build_v_interface_preamble(
                        compute_wrap_ids=(
                            self._record_strategy.behavior.compute_wrap_ids
                        ),
                    ),
                )
            case "INTERFACE":
                return _build_v_interface_preamble(
                    compute_wrap_ids=_v_collect_ids_needing_wrap,
                )
            case _:
                return _build_v_empty_container_preamble()

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config for the chosen
        strategy.

        ``RECORD`` resolves to the shared record behavior (its value
        needs the per-instance renderer, so it cannot be stored on the
        enum member); ``INTERFACE`` wraps scalars in ``IVal(...)``;
        ``ERROR`` raises on unwrapped heterogeneous collections.
        """
        match self.heterogeneous_strategy.name:
            case "RECORD":
                return self._record_strategy.behavior
            case "INTERFACE":
                return _build_v_interface_behavior()
            case _:
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
        return _v_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return file-scope stubs for a call expression."""
        return partial(_v_call_preamble_stub, indent=self.indent)

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
        """Append ``.clone()`` to the ref identifier, except for scalars.

        V's container types (arrays, maps) are not copied by direct
        assignment, so a ``$ref`` marker appearing on the right-hand
        side of an emitted assignment must be cloned to satisfy the
        V compiler.  V's primitive scalars (``int``, ``bool``,
        ``f64``, …) have no ``.clone()`` method - ``int.clone()`` is a
        hard error - so we emit the bare identifier and let V's
        automatic primitive copy do the right thing.  When the caller
        did not supply ``ref_values`` we cannot tell which case applies
        and fall back to ``.clone()``, which is correct for V's
        original use case (map/array refs).
        """

        def _clone(name: str, value: Value | None, /) -> str:
            """Return *name* with ``.clone()`` appended unless *value*
            is a register-trivial scalar that V auto-copies.
            """
            if isinstance(value, bool | int | float):
                return name
            return f"{name}.clone()"

        return _clone

    @cached_property
    def format_call_arg_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Return the ref identifier unchanged in a call-argument context.

        When a ``$ref`` is passed as a function argument (directly or
        nested inside a container argument via
        :func:`~literalizer.literalize_call`), V does not require
        ``.clone()``; V passes the value automatically without copying.
        """
        return identity_call_ref_identifier

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
                separator=": ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=f"map[string]{_V_IFACE_NAME}{{}}",
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
        """Callable that formats a datetime as a string literal.

        ``EPOCH`` seconds are routed through :attr:`format_integer` so
        a post-2038 value carries the ``i64(...)`` cast V requires for
        an integer literal outside signed 32-bit range (a bare
        ``4085195400`` is otherwise an out-of-range ``int`` literal),
        matching the ``i64`` field type the ``RECORD`` strategy derives
        for it.  In-range epoch seconds format identically to the plain
        integer, so every checked-in golden file stays byte-identical.
        """
        if self.datetime_format.name == "EPOCH":
            return datetime_epoch_formatter(
                format_integer=self.format_integer,
            )
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

        Values in 32-bit signed range are formatted with the chosen
        integer format.  Values outside that range but within 64-bit
        signed range use ``i64(...)``.  Values outside 64-bit signed
        range use ``u64(...)`` (or raise for negative overflow).
        """
        base = self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )
        i64_or_u64_fallback = make_overflow_fallback_formatter(
            base=_make_v_i64_formatter(base=base),
            fallback=make_unsigned_overflow_fallback(
                format_positive=_format_v_u64_positive,
                language_name="V",
            ),
            min_value=I64_MIN,
            max_value=I64_MAX,
        )
        return make_overflow_fallback_formatter(
            base=base,
            fallback=i64_or_u64_fallback,
            min_value=_V_I32_MIN,
            max_value=_V_I32_MAX,
        )

    @cached_property
    def format_integer_widened(self) -> Callable[[int], str]:
        """Always-``i64(...)``-cast integer formatter for widened
        collections (mixed-magnitude int sets/lists).
        """
        base = self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )
        return make_overflow_fallback_formatter(
            base=_make_v_i64_formatter(base=base),
            fallback=make_unsigned_overflow_fallback(
                format_positive=_format_v_u64_positive,
                language_name="V",
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
        """Callable that formats a new variable declaration."""
        return self.declaration_style.value.formatter

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (V needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (V needs none)."""
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
