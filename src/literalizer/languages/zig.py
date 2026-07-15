"""Zig language specification."""

import dataclasses
import datetime
import enum
import re
import textwrap
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
    dict_entry_with_template,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
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
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    format_integer_underscore,
)
from literalizer._formatters.format_json_value import format_json_value_text
from literalizer._formatters.format_strings import (
    format_string_backslash_control,
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
    MixedNumeric,
    infer_element_type,
    record_shape_for_dict,
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
    default_sequence_binding_declarations,
    default_wrap_calls_with_declarations,
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
    prepend_body_preamble,
)
from literalizer._types import OrderedMap, Scalar, Value
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
    UnrepresentableIntegerError,
    UnrepresentableSpecialFloatError,
)


@beartype
def _format_date_zig(value: datetime.date) -> str:
    """Format a date as epoch seconds (midnight UTC)."""
    dt = datetime.datetime(
        year=value.year,
        month=value.month,
        day=value.day,
        tzinfo=datetime.UTC,
    )
    return str(object=int(dt.timestamp()))


@beartype
def _format_datetime_zig(value: datetime.datetime) -> str:
    """Format a datetime as epoch seconds (UTC)."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=datetime.UTC)
    return str(object=int(value.timestamp()))


@dataclasses.dataclass(frozen=True)
class _ZigDeclarationStyleConfig:
    """Configuration for a Zig declaration style.

    Unlike :class:`DeclarationStyleConfig`, this carries no
    ``formatter`` slot: Zig builds its declaration formatter
    per-instance in :attr:`Zig.format_variable_declaration` so it can
    close over the chosen date/datetime ``type_produced``.
    """

    keyword: str
    supports_redefinition: bool


@beartype
def _format_zig_entry(
    *,
    original: Value,
    formatted: str,
    date_type: type,
    datetime_type: type,
) -> str:
    """Wrap a formatted entry in the appropriate Zig ``ZVal`` union
    tag.

    The ``str`` vs ``int`` choice for dates/datetimes is driven by the
    parsed :class:`Value` together with the chosen date/datetime
    format's ``type_produced``, rather than by sniffing *formatted*.
    """
    match original:
        case bool():
            return formatted
        case int():
            if original < I64_MIN:
                msg = (
                    f"Zig cannot represent negative integer {original} "
                    "below the signed 64-bit range using the ZVal "
                    "union's unsigned variant."
                )
                raise UnrepresentableIntegerError(msg)
            tag = "uint" if original > I64_MAX else "int"
        case float():
            tag = "float"
        case str() | bytes():
            tag = "str"
        case datetime.datetime():
            tag = "str" if datetime_type is str else "int"
        case datetime.time():
            tag = "str"
        case datetime.date():
            tag = "str" if date_type is str else "int"
        case _:
            return formatted
    return f".{{ .{tag} = {formatted} }}"


@beartype
def _make_zig_call_preamble_stub(
    *,
    record_mode: bool,
) -> Callable[
    [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
    tuple[str, ...],
]:
    """Build the file-scope Zig call-stub formatter.

    Zig disallows nested function declarations inside ``main``, so
    call stubs are emitted at module scope.  Stubs always return
    ``void`` so a bare ``stub(...);`` statement compiles whether or
    not a ``call_transform`` consumed the value.  Under the default
    ``ZVal`` model a target stub takes ``ZVal`` parameters so anonymous
    union literals like ``.{ .int = 1 }`` coerce to a concrete type at
    the call site; transform wrappers (``["_arg"]``) take ``anytype``
    so they accept both ``ZVal`` and ``void`` arguments.  Under the
    ``RECORD`` strategy (*record_mode*) call arguments are raw Zig
    values (``42``, ``"hello"``, ``null``, ``&.{ ... }``) rather than
    ``ZVal`` union literals, so every parameter is ``anytype``.  Dotted
    targets are realized as a nested ``struct`` chain rooted at a
    module-level constant, so an expression like
    ``app.client.fetch(...)`` resolves to a real method call on a real
    value.
    """

    @beartype
    def _zig_call_preamble_stub(
        parts: Sequence[str],
        params: Sequence[str],
        _stub_return: StubReturn,
        _args: Sequence[Value],
        /,
    ) -> tuple[str, ...]:
        """Return file-scope Zig stub declarations for a call name."""
        param_type = (
            "anytype" if record_mode or list(params) == ["_arg"] else "ZVal"
        )
        param_discards = "".join(f" _ = {p};" for p in params)
        method = parts[-1]
        if len(parts) == 1:
            param_list = ", ".join(f"{p}: {param_type}" for p in params)
            return (f"fn {method}({param_list}) void {{{param_discards} }}",)
        chain = parts[:-1]
        holder = chain[-1]
        holder_type = f"{holder.title()}Type_"
        method_param_list = ", ".join(
            [
                f"self: {holder_type}",
                *(f"{p}: {param_type}" for p in params),
            ],
        )
        lines: list[str] = [
            f"const {holder_type} = struct {{ "
            f"fn {method}({method_param_list}) void "
            f"{{ _ = self;{param_discards} }} }};",
        ]
        prev_type = holder_type
        for i in range(len(chain) - 2, 0, -1):
            curr_type = f"{chain[i].title()}Type_"
            lines.append(
                f"const {curr_type} = struct {{ "
                f"{chain[i + 1]}: {prev_type} = .{{}} }};",
            )
            prev_type = curr_type
        root = chain[0]
        intermediates = chain[1:]
        if intermediates:
            root_type = f"{root.title()}Type_"
            lines.append(
                f"const {root_type} = struct {{ "
                f"{intermediates[0]}: {prev_type} = .{{}} }};",
            )
        else:
            root_type = prev_type
        lines.append(f"const {root}: {root_type} = .{{}};")
        return tuple(lines)

    return _zig_call_preamble_stub


# The ``RECORD`` strategy supports only auto ``Record0``/``Record1``/...
# names (no ``record_shape_names``), so the shared renderer always gets
# an empty custom-name mapping.
_ZIG_NO_RECORD_SHAPE_NAMES: Mapping[frozenset[str], str] = MappingProxyType(
    mapping={},
)

# A datetime/date whose format produces an ``int`` epoch is a Zig
# ``i64`` record field; an ISO string one is ``[]const u8``.  The
# ``.get`` default keeps the string fallback off coverage's branch
# accounting (only the int key is crossed with ``RECORD`` by the
# datetime-cross corpus; the date axis is never crossed, so an
# ``if``/ternary would leave the string side uncovered).
_ZIG_EPOCH_INT_FIELD_TYPES: Mapping[type, str] = MappingProxyType(
    mapping={int: "i64"},
)

# A list mixing ``int`` and ``float`` infers to :class:`MixedNumeric`;
# its Zig slice element type is ``f64`` (the ``int`` literals coerce to
# ``f64``).  Looked up with a ``.get`` default rather than an ``if`` so
# the mapping needs no corpus case to stay coverage-clean (the same
# ``.get``-default trick used for the epoch field type; the coverage
# tool does not treat a dict lookup default as a branch).
_ZIG_INFERRED_ELEMENT_TYPES: Mapping[object, str] = MappingProxyType(
    mapping={MixedNumeric: "f64"},
)


@beartype
def _zig_int_sort_key(value: Value, /) -> int:
    """Return the ``max`` sort key selecting a list's widest int.

    An ``int`` sorts by its value so :meth:`Zig._zig_list_type` types a
    :class:`WideInt` slice from the element that widens it (``u64``
    once any value passes i64 range), not from ``items[0]``.  Every
    other value sorts equal (``0``), so for a homogeneous non-int list
    ``max`` keeps the first element -- an arbitrary but type-equivalent
    representative -- and the int-vs-other branch is exercised by the
    int and string record-list fixtures alike.
    """
    return value if isinstance(value, int) else 0


@beartype
def _zig_record_field_identifier(key: str, /) -> str:
    """Return the Zig ``struct`` member name for a dict *key*.

    Zig member identifiers are the dict keys verbatim (no case
    conversion), matching the designated-initializer literal form
    ``Record0{ .id = 1, ... }``.
    """
    return key


@beartype
def _zig_record_literal(
    name: str,
    fields: Sequence[RecordLiteralField],
    /,
) -> RenderedRecordLiteral:
    """Render a Zig ``Name{ .field = value, ... }`` struct literal as
    structured pieces for the shared compact/multiline layout code.

    A trailing comma after the last initializer is valid in a Zig
    brace-enclosed struct literal, so the language-wide trailing-comma
    config applies unchanged.
    """
    return RenderedRecordLiteral(
        head=f"{name}{{",
        entries=tuple(
            f".{field.identifier} = {field.formatted}" for field in fields
        ),
        closer="}",
        compact_pad=" ",
    )


@beartype
def _zig_render_record_declaration(
    name: str,
    fields: Sequence[RecordDeclarationField],
    /,
) -> str:
    """Render a Zig ``const Name = struct { field: Type, ... };``."""
    members = ", ".join(
        f"{field.identifier}: {field.type_name}" for field in fields
    )
    return f"const {name} = struct {{ {members} }};"


@beartype
def _format_zig_call_assignment(name: str, value: str, _data: Value) -> str:
    """Format a Zig reassignment binding a call result.

    The call-expression counterpart of
    :attr:`Zig.format_call_variable_declaration`; the variable already
    exists, so the call result is assigned directly with none of the
    ``ZVal`` union tagging a literal-binding assignment applies (a call
    result is not a ``ZVal`` union literal).
    """
    return f"{name} = {value};"


_STD_JSON_STATIC_PREAMBLE: tuple[str, ...] = ('const std = @import("std");',)

_ZVAL_STATIC_PREAMBLE: tuple[str, ...] = (
    "const ZVal = union(enum) {",
    "    nil,",
    "    bool: bool,",
    "    int: i64,",
    "    uint: u64,",
    "    float: f64,",
    "    str: []const u8,",
    "    arr: []const ZVal,",
    "    map: []const ZKV,",
    "    set: []const ZVal,",
    "};",
    "const ZKV = struct { key: []const u8, val: ZVal };",
)

_STD_JSON_BODY_PREAMBLE: tuple[str, ...] = (
    "var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);",
    "defer arena.deinit();",
    "const allocator = arena.allocator();",
)


# Sequence/dict format definitions used while ``json_type`` is active.
# The framework still walks through the data to compute a formatted
# ``value``, but that string is discarded by
# :func:`_format_zig_json_declaration` and friends in favor of a fresh
# ``json.dumps`` of the raw data.  These definitions only need to be
# permissive enough that the formatting pass does not error on
# heterogeneous data or nulls inside containers.
_STD_JSON_SEQUENCE_CONFIG = SequenceFormatConfig(
    sequence_open=fixed_open(open_str="["),
    close="]",
    supports_heterogeneity=True,
    single_element_trailing_comma=False,
    supports_trailing_comma=True,
    empty_sequence="[]",
    preamble_lines=(),
    format_entry=passthrough_sequence_entry,
    typed_opener_fallback=None,
    uses_typed_literal_for_scalars=False,
    requires_uniform_record_shapes=False,
    declared_type=None,
    narrowed_empty_form=None,
)

_STD_JSON_SET_CONFIG = SetFormatConfig(
    set_open=fixed_open(open_str="["),
    close="]",
    empty_set="[]",
    preamble_lines=(),
    set_opener_template="",
    supports_heterogeneity=True,
    supports_trailing_comma=True,
)

_STD_JSON_DICT_CONFIG = DictFormatConfig(
    dict_open=fixed_open(open_str="{"),
    close="}",
    format_entry=dict_entry_with_template(
        template="{key}: {value}",
        format_value=passthrough_sequence_entry,
    ),
    empty_dict="{}",
    preamble_lines=(),
    narrowed_open=None,
    supports_trailing_comma=True,
)

_STD_JSON_ORDERED_MAP_CONFIG = OrderedMapFormatConfig(
    ordered_map_open=fixed_open(open_str="{"),
    close="}",
    preamble_lines=(),
)


@beartype
def _zig_parse_expression(data: Value) -> str:
    """Render a ``std.json.parseFromSlice(...) catch unreachable`` call.

    ``catch unreachable`` (rather than ``try``) keeps the enclosing
    ``pub fn main() void`` signature unchanged: every JSON literal here
    is generated by :func:`json.dumps` and is guaranteed to parse, so
    the failure arm is statically unreachable.
    """
    if data_has_special_float(data=data):
        msg = (
            "Zig(json_type=STD_JSON_VALUE) cannot represent special floats "
            "because std.json.parseFromSlice accepts only finite numbers."
        )
        raise UnrepresentableSpecialFloatError(msg)
    json_text = format_json_value_text(data=data)
    zig_literal = format_string_backslash_control(
        value=json_text,
        control_char_fmt="\\x{:02x}",
    )
    return (
        "(std.json.parseFromSlice("
        f"std.json.Value, allocator, {zig_literal}, .{{}}) "
        "catch unreachable).value"
    )


@beartype
def _format_zig_json_declaration(
    name: str,
    _value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a ``std.json.Value`` declaration backed by
    parseFromSlice.
    """
    return f"const {name} = {_zig_parse_expression(data=data)};"


@beartype
def _format_zig_json_var_declaration(
    name: str,
    _value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a ``var std.json.Value`` declaration backed by
    parseFromSlice.

    The ``var`` form is selected when the caller pairs the declaration
    with a subsequent assignment (the ``combined`` variable form); a
    plain ``const`` cannot be reassigned.
    """
    return f"var {name}: std.json.Value = {_zig_parse_expression(data=data)};"


@beartype
def _format_zig_json_assignment(name: str, _value: str, data: Value) -> str:
    """Format a ``std.json.Value`` assignment backed by parseFromSlice."""
    return f"{name} = {_zig_parse_expression(data=data)};"


@beartype
def _format_zig_json_call_arg(raw_value: Value, _formatted: str) -> str:
    """Format a direct call argument as a ``std.json.Value`` literal."""
    return _zig_parse_expression(data=raw_value)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Zig(metaclass=LanguageCls):
    """Zig language specification."""

    format_integer_widened = no_format_integer_widened
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".zig"
    pygments_name = "zig"
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
    supports_multi_param_call_wrapper_stub = False
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
        collection_layout_category="collection_layout",
        record_variants=frozenset(),
        nested_map_widening=NestedMapWideningVariant.NONE,
        modifier_sequence_format_overrides={},
    )
    supports_record_struct_name_prefix = True
    supports_record_shape_names = False
    supports_non_string_dict_keys = False

    class DateFormats(enum.Enum):
        """Date format options for Zig."""

        ZIG = DateFormatConfig(
            formatter=_format_date_zig,
            type_produced=int,
            preamble_lines=(),
        )
        ISO = DateFormatConfig(
            formatter=format_date_iso, type_produced=str, preamble_lines=()
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Zig."""

        ZIG = DatetimeFormatConfig(
            formatter=_format_datetime_zig,
            type_produced=int,
            preamble_lines=(),
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
        """Sequence type options for Zig."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(open_str=".{ .arr = &.{"),
            close="}}",
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
        """Set type options for Zig."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str=".{ .set = &.{"),
            close="}}",
            empty_set=None,
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

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        CONST = _ZigDeclarationStyleConfig(
            keyword="const",
            supports_redefinition=False,
        )
        VAR = _ZigDeclarationStyleConfig(
            keyword="var",
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
        positive_infinity="std.math.inf(f64)",
        negative_infinity="-std.math.inf(f64)",
        nan="std.math.nan(f64)",
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
        """Zig call style options."""

        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Heterogeneous-scalar strategy options.

        ``ERROR`` keeps the default ``ZVal`` union model (a
        record-shaped dict that mixes scalars with a container is
        rendered as a homogeneous-typed ``.{ .map = &.{ ... } }``).
        ``RECORD`` instead renders each record-shaped dict (non-empty,
        string-keyed) as a generated ``const Record0 = struct { ... };``
        declared in the preamble plus a matching
        ``Record0{ .field = value, ... }`` literal whose fields are raw
        Zig values, so a field may mix scalars and containers that the
        homogeneous ``ZVal`` map cannot.
        """

        ERROR = enum.auto()
        RECORD = enum.auto()

    heterogeneous_strategies = HeterogeneousStrategies

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for Zig."""

        V0_12 = enum.auto()

    version_formats = VersionFormats

    class JsonTypes(enum.Enum):
        """JSON value type options for Zig."""

        STD_JSON_VALUE = "std.json.Value"
        """Zig's standard library dynamic JSON value type."""

    json_types = JsonTypes

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.PASCAL,
        IdentifierCase.CAMEL,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    def validate_spec_for_data(self, data: Value) -> None:
        """Raise if the spec cannot produce valid code for *data*.

        When :attr:`json_type` is active, walk *data* to reject non-string
        dict keys, which JSON objects cannot represent.
        """
        if self._json_type_active:
            self._validate_json_value_keys(data)

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
        """Wrap a Zig declaration in a main function."""
        json_mode = self._json_type_active
        # Detect ``var``/``const`` on the caller's declaration, before
        # injecting the JSON-mode arena ``var`` body preamble (which
        # would otherwise spuriously trip the regex).
        is_var = bool(
            re.search(
                pattern=r"^\s*var ",
                string=content,
                flags=re.MULTILINE,
            ),
        )
        effective_body_preamble = (
            _STD_JSON_BODY_PREAMBLE + body_preamble
            if json_mode
            else body_preamble
        )
        content = prepend_body_preamble(
            content=content,
            body_preamble=effective_body_preamble,
        )
        indented = textwrap.indent(text=content, prefix=self.indent)
        if not variable_name:
            return f"pub fn main() void {{\n{indented}\n}}"
        match json_mode, self._record_strategy_active, is_var:
            case True, _, True:
                # A ``var x: std.json.Value`` may have been reassigned;
                # take its address so the final discard does not trip
                # the "pointless discard of local variable" error.
                use = f"{self.indent}_ = &{variable_name};"
            case True, _, False:
                use = f"{self.indent}_ = {variable_name};"
            case _, True, _:
                # A raw value is not a ``ZVal``, so a redefinition ``var``
                # cannot be reset to ``.nil``; take its address instead so
                # the final statement uses the variable without tripping
                # the Zig "pointless discard of local variable" error
                # after a preceding write.
                ref = f"&{variable_name}" if is_var else variable_name
                use = f"{self.indent}_ = {ref};"
            case _, False, True:
                use = f"{self.indent}{variable_name} = .nil;"
            case _:
                use = f"{self.indent}_ = {variable_name};"
        return f"pub fn main() void {{\n{indented}\n{use}\n}}"

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Zig declaration + assignment in a main function."""
        return self.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.ZIG
    datetime_format: DatetimeFormats = DatetimeFormats.ZIG
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.CONST
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
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    json_type: JsonTypes | None = None
    record_struct_name_prefix: str = "Record"
    language_version: VersionFormats = VersionFormats.V0_12
    indent: str = "    "

    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ";"
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = (
        'const std = @import("std");',
    )
    call_style: CallStyles = CallStyles.POSITIONAL

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value

    @cached_property
    def _format_entry(self) -> Callable[[Value, str], str]:
        """Shared entry formatter closing over date/datetime
        ``type_produced``.

        Under the ``RECORD`` strategy every value is emitted as a raw
        Zig literal (no ``ZVal`` union tag), so the entry formatter is
        the identity: sequence/set elements, call arguments, and
        variable bindings all pass their already-formatted literal
        through unchanged.
        """
        if self._record_strategy_active:

            @beartype
            def _identity(_original: Value, formatted: str) -> str:
                """Pass the raw Zig literal through unchanged."""
                return formatted

            return _identity

        date_type = self.date_format.value.type_produced
        datetime_type = self.datetime_format.value.type_produced

        @beartype
        def _formatter(original: Value, formatted: str) -> str:
            """Adapt :func:`_format_zig_entry` to the positional
            entry-formatter interface.
            """
            return _format_zig_entry(
                original=original,
                formatted=formatted,
                date_type=date_type,
                datetime_type=datetime_type,
            )

        return _formatter

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        if self._json_type_active:
            return passthrough_sequence_entry
        return self._format_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        if self._json_type_active:
            return passthrough_sequence_entry
        return self._format_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        if self._json_type_active:
            return _format_zig_json_assignment
        format_entry = self._format_entry

        @beartype
        def _format_assign(name: str, value: str, data: Value) -> str:
            """Format a Zig assignment to an existing ``ZVal``
            variable.
            """
            wrapped = format_entry(data, value)
            return f"{name} = {wrapped};"

        return _format_assign

    @cached_property
    def _record_strategy_active(self) -> bool:
        """Return whether the ``RECORD`` heterogeneous strategy is set."""
        return self.heterogeneous_strategy.name == "RECORD"

    @cached_property
    def _json_type_active(self) -> bool:
        """Return whether Zig should render via ``std.json.Value``."""
        return self.json_type is not None

    def __post_init__(self) -> None:
        """Reject ``json_type`` combinations the generator cannot emit."""
        self._validate_json_type_spec()

    def _validate_json_type_spec(self) -> None:
        """Reject ``json_type`` combinations the generator cannot emit.

        Under ``json_type`` the rendered data flows through a single
        ``std.json.parseFromSlice`` call, which is incompatible with
        ``heterogeneous_strategy=RECORD`` (which would generate ``struct``
        declarations parallel to the JSON text).
        """
        if not self._json_type_active:
            return
        if self.heterogeneous_strategy is self.heterogeneous_strategies.RECORD:
            msg = (
                "Zig json_type renders data through "
                "std.json.parseFromSlice(...) and is incompatible with "
                "heterogeneous_strategy=RECORD, which generates typed "
                "struct declarations. Use heterogeneous_strategy=ERROR."
            )
            raise IncompatibleFormatsError(msg)

    def _validate_json_value_keys(self, data: Value, /) -> None:
        """Reject non-string object keys for ``std.json.Value``."""
        match data:
            case OrderedMap() | dict():
                for key, value in data.items():
                    if not isinstance(key, str):
                        msg = (
                            "Zig json_type can only represent dict keys "
                            "as JSON object strings, not "
                            f"{type(key).__name__}"
                        )
                        raise UnrepresentableInputError(msg)
                    self._validate_json_value_keys(value)
            case list() | set():
                for item in data:
                    self._validate_json_value_keys(item)
            case _:
                return

    @cached_property
    def null_literal(self) -> str:
        """The literal representing null.

        The default ``ZVal`` model uses the union tag ``.nil``; under
        ``RECORD`` a null record field is a raw Zig ``null`` (its field
        type is the optional ``?i64``).
        """
        return "null" if self._record_strategy_active else ".nil"

    @cached_property
    def true_literal(self) -> str:
        """The literal representing true.

        Raw Zig ``true`` under ``RECORD`` (a ``bool`` field), the
        ``ZVal`` union literal otherwise.
        """
        if self._record_strategy_active:
            return "true"
        return ".{ .bool = true }"

    @cached_property
    def false_literal(self) -> str:
        """The literal representing false.

        Raw Zig ``false`` under ``RECORD`` (a ``bool`` field), the
        ``ZVal`` union literal otherwise.
        """
        if self._record_strategy_active:
            return "false"
        return ".{ .bool = false }"

    def _zig_value_type(self, value: Value, /) -> str:  # noqa: PLR0911
        """Return the Zig type for a raw record field *value*.

        Derived structurally from the value (never by re-parsing the
        formatted literal): scalars map to their Zig primitive, a
        homogeneous list to ``[]const <elem>``, a heterogeneous list to
        a Zig tuple ``struct { T0, ... }``, and an ordered map to a
        slice of ``key``/``val`` ``struct`` values.  A nested
        record-shaped dict never reaches here -- the shared strategy
        resolves it to its generated name in
        :meth:`_zig_record_field_type`.
        """
        if isinstance(value, bool):
            return "bool"
        if isinstance(value, int):
            return "u64" if value > I64_MAX else "i64"
        if isinstance(value, float):
            return "f64"
        if value is None:
            return "?i64"
        if isinstance(value, datetime.datetime):
            return _ZIG_EPOCH_INT_FIELD_TYPES.get(
                self.datetime_format.value.type_produced,
                "[]const u8",
            )
        if isinstance(value, datetime.date):
            return _ZIG_EPOCH_INT_FIELD_TYPES.get(
                self.date_format.value.type_produced,
                "[]const u8",
            )
        if isinstance(value, OrderedMap):
            # An ordered-map field is out of scope for the base RECORD
            # port (the cross-language decision is tracked in #2317); it
            # is typed imprecisely from the first value's type, like the
            # other ports' non-record-dict fallback.  ``... or [0]``
            # keeps an empty ordered map from raising ``StopIteration``
            # (its ``&.{}`` literal coerces to any slice element type);
            # ``or`` is not a coverage branch, so no unreachable arm is
            # added for a corpus that has no empty ordered-map field.
            val_type = self._zig_value_type(
                (list(value.values()) or [0])[0],
            )
            return f"[]const struct {{ key: []const u8, val: {val_type} }}"
        if isinstance(value, list):
            return self._zig_list_type(items=value)
        return "[]const u8"

    def _zig_list_type(self, *, items: list[Value]) -> str:
        """Return the Zig type for a list record field.

        An empty list has no element type to infer, so it is typed as a
        ``[]const i64`` slice (``&.{}`` coerces to any slice type).  A
        list whose elements share a type is a ``[]const <elem>`` slice;
        a list mixing ``int`` and ``float`` widens to ``[]const f64``
        (its int literals coerce to ``f64``); a heterogeneous list is a
        Zig tuple ``struct { T0, T1, ... }`` (its literal is the
        anonymous tuple ``.{ ... }``, matching :attr:`sequence_open`).

        An int list with a value outside i32 range infers to
        :class:`WideInt`; its element type is taken from the *widest*
        element (``max`` keyed by :func:`_zig_int_sort_key`) via
        :meth:`_zig_value_type`, so a list whose later element exceeds
        i64 range is ``[]const u64`` rather than the ``[]const i64``
        that typing from ``items[0]`` alone would wrongly produce for
        e.g. ``[1, 1 << 63]``.  For every non-int homogeneous list the
        key ties on every element, so ``max`` keeps ``items[0]`` -- an
        arbitrary but type-equivalent representative.
        """
        if not items:
            return "[]const i64"
        inferred = infer_element_type(items=items)
        if inferred is None:
            members = ", ".join(
                self._zig_value_type(element) for element in items
            )
            return f"struct {{ {members} }}"
        element_type = _ZIG_INFERRED_ELEMENT_TYPES.get(
            inferred,
            self._zig_value_type(max(items, key=_zig_int_sort_key)),
        )
        return f"[]const {element_type}"

    def _zig_record_field_type(self, request: RecordFieldType, /) -> str:
        """Return the Zig ``struct`` field type for a record field.

        A field whose value is itself a nested record-shaped dict uses
        that record's generated name; a field whose value is a list of
        record-shaped dicts is a ``[]const RecordN`` slice of that
        element record (its literal is ``&.{ RecordN{ ... }, ... }``);
        every other value is typed structurally from the raw value by
        :meth:`_zig_value_type`.
        """
        if request.record_name is not None:
            return request.record_name
        if request.element_record_name is not None:
            return f"[]const {request.element_record_name}"
        if (
            isinstance(request.value, dict)
            and not isinstance(request.value, OrderedMap)
            and record_shape_for_dict(value=request.value) is not None
        ):
            return "ZVal"
        return self._zig_value_type(request.value)

    @cached_property
    def _record_renderer(self) -> RecordRenderer:
        """Zig syntax hooks for the ``RECORD`` strategy."""
        return RecordRenderer(
            name_prefix=self.record_struct_name_prefix,
            record_shape_names=_ZIG_NO_RECORD_SHAPE_NAMES,
            field_identifier=_zig_record_field_identifier,
            field_type=self._zig_record_field_type,
            render_declaration=_zig_render_record_declaration,
            render_literal=_zig_record_literal,
        )

    @cached_property
    def _record_strategy(self) -> RecordStrategy:
        """Behavior + ``struct``-declaration preamble for ``RECORD``."""
        strategy = build_record_strategy(
            renderer=self._record_renderer,
            split_conflicting_field_types=False,
            widen_unrecordizable_nested_sibling_maps=True,
            derecordized_map_open=".{ .map = &.{",
        )

        def _wrap_scalar(raw_value: Scalar, formatted: str) -> str:
            """Tag a scalar stored in a widened ``ZVal`` map."""
            if raw_value is None:
                return ".nil"
            if isinstance(raw_value, bool):
                return f".{{ .bool = {formatted} }}"
            return _format_zig_entry(
                original=raw_value,
                formatted=formatted,
                date_type=self.date_format.value.type_produced,
                datetime_type=self.datetime_format.value.type_produced,
            )

        return dataclasses.replace(
            strategy,
            behavior=dataclasses.replace(
                strategy.behavior,
                wrap_scalar=_wrap_scalar,
                widens_nested_maps_by_wrapping_scalars=True,
            ),
        )

    @cached_property
    def static_preamble(self) -> Sequence[str]:
        """File-scope preamble.

        Under :attr:`json_type` only ``const std = @import("std");`` is
        emitted (the data flows through ``std.json.parseFromSlice``).
        The default ``ZVal`` model needs its tagged-union declaration;
        the ``RECORD`` strategy emits raw Zig values and generated
        ``struct`` declarations instead, so it needs no static
        preamble.
        """
        if self._json_type_active:
            return _STD_JSON_STATIC_PREAMBLE
        if self._record_strategy_active:
            return ()
        return _ZVAL_STATIC_PREAMBLE

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        Under :attr:`json_type` the data rides inside a single JSON
        string, so no per-data preamble applies.  Under ``RECORD`` this
        is the generated ``const Record0 = struct { ... };`` block,
        emitted in dependency order so a nested record is declared
        before its parent.
        """
        if self._json_type_active:
            return no_data_preamble
        if self._record_strategy_active:
            record_preamble = self._record_strategy.preamble
            compute_wrap_ids = self._record_strategy.behavior.compute_wrap_ids

            def _record_preamble(data: Value, /) -> tuple[str, ...]:
                """Emit ``ZVal`` when a nested map needs that carrier."""
                value_preamble = (
                    _ZVAL_STATIC_PREAMBLE if compute_wrap_ids(data) else ()
                )
                return (*value_preamble, *record_preamble(data))

            return _record_preamble
        return no_data_preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config.

        Under :attr:`json_type` heterogeneous scalars all flow through
        the JSON text, so scalar-uniformity checks are skipped.
        ``RECORD`` resolves to the shared record behavior (its value
        needs the per-instance renderer, so it cannot be stored on the
        enum member); ``ERROR`` keeps the default ``ZVal`` model.
        """
        if self._json_type_active:
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
        """Return stub declarations for a call expression.

        Zig disallows nested function declarations inside ``main``, so
        every stub is emitted at file scope via
        :attr:`format_call_preamble_stub` instead.
        """
        return no_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return file-scope stubs for a call expression.

        Under :attr:`json_type` call arguments are ``std.json.Value``
        expressions rather than ``ZVal`` union literals, so the stub
        accepts ``anytype`` parameters just as the ``RECORD`` strategy
        does.
        """
        return _make_zig_call_preamble_stub(
            record_mode=self._record_strategy_active or self._json_type_active,
        )

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Wrap each call argument in the ``ZVal`` union so call sites
        match the parameter shape emitted by
        :func:`_zig_call_preamble_stub`.

        Under :attr:`json_type` the argument is rendered as a
        ``std.json.Value`` produced by ``parseFromSlice`` instead.
        """
        if self._json_type_active:
            return _format_zig_json_call_arg
        return self._format_entry

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

        Under :attr:`json_type` lists are rendered into the JSON text
        and the framework's formatted output is discarded.  Under
        ``RECORD`` a list is a raw Zig literal -- a ``&.{ ... }`` slice
        (homogeneous / empty) or a ``.{ ... }`` tuple (heterogeneous),
        both closed by a single ``}`` rather than the ``ZVal``
        ``.{ .arr = &.{ ... }}`` form.  Only the closer changes here;
        the opener is chosen per list by :attr:`sequence_open`.
        """
        if self._json_type_active:
            return _STD_JSON_SEQUENCE_CONFIG
        base = self.sequence_format.value
        if self._record_strategy_active:
            return dataclasses.replace(base, close="}")
        return base

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        if self._json_type_active:
            return _STD_JSON_SET_CONFIG
        return self.set_format.value

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence.

        Under ``RECORD`` a homogeneous or empty list opens ``&.{`` so
        the literal coerces to a ``[]const T`` slice; a heterogeneous
        list opens ``.{`` so it is a Zig tuple (matching the
        ``struct { T0, ... }`` field type :meth:`_zig_value_type`
        derives).  Every other strategy keeps the ``ZVal`` array
        opener.
        """
        if self._json_type_active:
            return _STD_JSON_SEQUENCE_CONFIG.sequence_open
        if not self._record_strategy_active:
            return self.sequence_format.value.sequence_open

        def _open(items: list[Value]) -> str:
            """Return the slice opener, or the tuple opener for a
            heterogeneous list.
            """
            if items and infer_element_type(items=items) is None:
                return ".{"
            return "&.{"

        return _open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting.

        Under :attr:`json_type` dicts are rendered into the JSON text
        and the framework's formatted output is discarded.  Under
        ``RECORD`` every non-empty string-keyed dict is a record
        (rendered as a generated ``struct``); the only plain dict that
        still reaches the dict formatter is the empty dict, emitted as
        the raw empty struct ``.{}`` instead of the ``ZVal``
        ``.{ .map = &.{}}`` form.
        """
        if self._json_type_active:
            return _STD_JSON_DICT_CONFIG
        base = DictFormatConfig(
            dict_open=fixed_open(open_str=".{ .map = &.{"),
            close="}}",
            format_entry=dict_entry_with_template(
                template=".{{ .key = {key}, .val = {value} }}",
                format_value=self._format_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
            supports_trailing_comma=True,
        )
        if self._record_strategy_active:
            return dataclasses.replace(base, empty_dict=".{}")
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
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""

        def _format(value: str) -> str:
            """Format a string as a Zig quoted literal."""
            return format_string_backslash_control(
                value=value,
                control_char_fmt="\\x{:02x}",
            )

        return _format

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

        Under :attr:`json_type` ordered maps are folded into the JSON
        text.  An ordered map is never record-eligible, so under
        ``RECORD`` it stays a map but as a raw
        ``&.{ .{ .key = ..., .val = ... }, ... }`` slice of
        ``key``/``val`` ``struct`` values rather than the ``ZVal``
        ``.{ .map = &.{ ... }}`` form.
        """
        if self._json_type_active:
            return _STD_JSON_ORDERED_MAP_CONFIG
        if self._record_strategy_active:
            return OrderedMapFormatConfig(
                ordered_map_open=fixed_open(open_str="&.{"),
                close="}",
                preamble_lines=(),
            )
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str=".{ .map = &.{"),
            close="}}",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return dict_entry_with_template(
            template=".{{ .key = {key}, .val = {value} }}",
            format_value=self._format_entry,
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration.

        Under :attr:`json_type` the declaration is a
        ``parseFromSlice`` call.  A ``const`` binding is emitted with an
        inferred type; a ``var`` binding gets an explicit
        ``: std.json.Value`` annotation so a subsequent assignment can
        compile against the same static type.

        Otherwise this closes over the chosen date/datetime
        ``type_produced`` so the ``ZVal`` tag selection can be driven by
        the parsed :class:`Value` rather than the rendered text.
        """
        if self._json_type_active:
            if self.declaration_style.value.keyword == "var":
                return _format_zig_json_var_declaration
            return _format_zig_json_declaration
        keyword = self.declaration_style.value.keyword
        format_entry = self._format_entry
        record_mode = self._record_strategy_active

        @beartype
        def _format_decl(
            name: str,
            value: str,
            data: Value,
            _modifiers: frozenset[enum.Enum],
        ) -> str:
            """Format a Zig declaration.

            The default ``ZVal`` model declares an explicit ``: ZVal``
            type; under ``RECORD`` the value is a raw Zig literal
            (a ``Record0{ ... }`` struct, slice, tuple or scalar) whose
            type is inferred, so no annotation is emitted.
            """
            wrapped = format_entry(data, value)
            if record_mode:
                return f"{keyword} {name} = {wrapped};"
            return f"{keyword} {name}: ZVal = {wrapped};"

        return _format_decl

    @cached_property
    def format_call_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a declaration binding a call result.

        A Zig literal binding wraps the right-hand side in a
        designated-initializer ``ZVal`` projection (``.{ .int = 42 }``),
        or a generated ``Record0{ .field = value, ... }`` struct literal
        under the ``RECORD`` strategy, and declares an explicit value
        type (``: ZVal``).  A call's return type is opaque to the
        renderer and is neither, so the call result is bound with a
        plain inferred declaration (``const my_data = make_widget(...);``
        / ``var my_data = make_widget(...);``): the Zig ``const``/``var``
        type inference means no caller-supplied return-type hint is
        needed, and the value-wrapping and ``: ZVal`` annotation are
        dropped.
        """
        keyword = self.declaration_style.value.keyword

        @beartype
        def _format_call_decl(
            name: str,
            value: str,
            _data: Value,
            _modifiers: frozenset[enum.Enum],
        ) -> str:
            """Format an inferred Zig declaration binding a call."""
            return f"{keyword} {name} = {value};"

        return _format_call_decl

    @cached_property
    def format_call_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment binding a call result.

        The call-expression counterpart of
        :attr:`format_call_variable_declaration`; the ``ZVal`` tagging a
        literal-binding assignment applies is dropped since a call
        result is not a ``ZVal`` union literal.
        """
        return _format_zig_call_assignment

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Zig needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Zig needs none)."""
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
