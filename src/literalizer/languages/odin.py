"""Odin language specification."""

import dataclasses
import datetime
import enum
import json
import math
import re
from collections.abc import Callable, Mapping, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
    make_element_to_type,
    make_type_to_opener,
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
    dict_entry_with_template,
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
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
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
    no_data_preamble,
    no_format_integer_beyond_i64,
    no_format_integer_widened,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    prepend_body_preamble,
)
from literalizer._types import OrderedMap, Value
from literalizer.exceptions import (
    IncompatibleFormatsError,
    UnrepresentableInputError,
    WrapCombinedInFileNotSupportedError,
)


@beartype
def _format_set_entry(_original: Value, item: str) -> str:
    """Format an Odin set entry as a map entry with empty struct value.

    Example: ``"apple"`` → ``"apple" = {}``.
    """
    return f"{item} = {{}}"


@beartype
def _apply_odin_nil_safe_declaration(
    name: str,
    value: str,
    data: Value,
    modifiers: frozenset[enum.Enum],
    base_formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
) -> str:
    """Format an Odin variable declaration, guarding top-level ``nil``."""
    if data is None:
        return f"{name}: any = {value}"
    return base_formatter(name, value, data, modifiers)


@beartype
def _nil_safe_declaration(
    base_formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
    """Wrap *base_formatter* so top-level ``nil`` gets a typed form.

    Odin cannot infer a type from ``nil`` alone, so
    ``my_data := nil`` fails to compile.  Emit
    ``{name}: any = nil`` when the value is ``None``.
    """

    def _format(
        name: str,
        value: str,
        data: Value,
        modifiers: frozenset[enum.Enum],
    ) -> str:
        """Delegate to module-level implementation."""
        return _apply_odin_nil_safe_declaration(
            name=name,
            value=value,
            data=data,
            modifiers=modifiers,
            base_formatter=base_formatter,
        )

    return _format


@beartype
def _odin_call_preamble_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return file-scope Odin stub declarations for a call name.

    Emits only type and helper-procedure definitions; the root variable
    initialisation is deferred to :func:`_odin_call_body_stub` so it
    lives inside ``main`` rather than at package scope, avoiding an Odin
    compiler crash on nested struct literals in global scope.
    """
    if len(parts) == 1:
        return (f"{parts[0]} :: proc(args: ..any) -> any {{ return nil }}",)
    root = parts[0]
    method = parts[-1]
    chain = parts[:-1]
    holder = chain[-1]
    holder_type = f"{holder.title()}Type_"
    helper_name = f"_{holder}_{method}_"
    lines: list[str] = [
        f"{helper_name} :: proc(args: ..any) -> any {{ return nil }}",
        f"{holder_type} :: struct {{ {method}: proc(..any) -> any }}",
    ]
    prev_type = holder_type
    for i in range(len(chain) - 2, 0, -1):
        curr = chain[i]
        child = chain[i + 1]
        curr_type = f"{curr.title()}Type_"
        lines.append(f"{curr_type} :: struct {{ {child}: {prev_type} }}")
        prev_type = curr_type
    root_type = f"{root.title()}Type_"
    if len(chain) > 1:
        lines.append(f"{root_type} :: struct {{ {chain[1]}: {prev_type} }}")
    return tuple(lines)


@beartype
def _odin_call_body_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return body-scope Odin variable initialisation for a dotted call.

    For single-part calls the proc is declared at file scope and no local
    variable is needed.  For dotted calls the root variable is declared
    inside ``main`` to avoid the Odin compiler crash triggered by nested
    struct literals declared at global scope.
    """
    if len(parts) == 1:
        return ()
    root = parts[0]
    method = parts[-1]
    chain = parts[:-1]
    holder = chain[-1]
    holder_type = f"{holder.title()}Type_"
    helper_name = f"_{holder}_{method}_"
    root_type = f"{root.title()}Type_"
    init_expr = f"{holder_type}{{ {method} = {helper_name} }}"
    for i in range(len(chain) - 2, -1, -1):
        outer_type = f"{chain[i].title()}Type_"
        inner_field = chain[i + 1]
        init_expr = f"{outer_type}{{ {inner_field} = {init_expr} }}"
    return (f"{root}: {root_type} = {init_expr}",)


# The ``RECORD`` strategy supports only auto ``Record0``/``Record1``/...
# names (no ``record_shape_names``, consistent with the other non-Rust
# ports), so the shared renderer always gets an empty custom-name
# mapping.
_ODIN_NO_RECORD_SHAPE_NAMES: Mapping[frozenset[str], str] = MappingProxyType(
    mapping={},
)


@beartype
def _odin_record_field_identifier(key: str, /) -> str:
    """Return the Odin ``struct`` member name for a dict *key*.

    Odin member identifiers are the dict keys verbatim (no case
    conversion), matching the ``Record0{ id = 1, ... }`` literal form.
    """
    return key


@beartype
def _odin_int_field_type(value: int, /) -> str:
    """Return the Odin ``struct`` field type for an integer record
    field.

    Odin's ``int`` is 64-bit on the targets the fixtures build for, so
    every value within the signed 64-bit range is ``int``.  The only
    out-of-range integer the record corpus carries is the unsigned
    64-bit maximum (``2**64 - 1``); it is typed ``u64`` so the
    decimal/hex/octal/binary literal -- every integer literal is a
    bare constant in Odin with no inherent type -- fits the declared
    field.  A value beyond unsigned 64-bit range is out of scope for
    the base
    ``RECORD`` port (Rust is imprecise here too) and is not reached by
    any record golden.
    """
    if not I64_MIN <= value <= I64_MAX:
        return "u64"
    return "int"


@beartype
def _odin_render_record_declaration(
    name: str,
    fields: Sequence[RecordDeclarationField],
    /,
) -> str:
    """Render an Odin ``Name :: struct { field: Type, ... }``.

    Emitted at package scope by the data-dependent preamble (each
    fixture is its own compilation unit, so file-scope ``struct``
    declarations never collide).  The matching record *literal* stays
    inside ``main`` via the normal value path, avoiding the Odin
    compiler crash on nested struct literals at global scope that
    :func:`_odin_call_preamble_stub` already works around.
    """
    members = ", ".join(
        f"{field.identifier}: {field.type_name}" for field in fields
    )
    return f"{name} :: struct {{ {members} }}"


@beartype
def _odin_record_literal(
    name: str,
    fields: Sequence[RecordLiteralField],
    /,
) -> RenderedRecordLiteral:
    """Render an Odin ``Name{ field = value, ... }`` struct literal as
    structured pieces for the shared compact/multiline layout code.

    A trailing comma after the last field is valid in an Odin compound
    literal, so the language-wide trailing-comma config applies
    unchanged in the multiline form.
    """
    return RenderedRecordLiteral(
        head=f"{name}{{",
        entries=tuple(
            f"{field.identifier} = {field.formatted}" for field in fields
        ),
        closer="}",
        compact_pad=" ",
    )


# Static preamble lines emitted under ``json_type=JSON_VALUE``.  The
# helper procedure normalizes ``json.parse_string`` (which returns a
# ``(Value, Error)`` pair and defaults ``parse_integers`` to ``false``)
# into a single-expression call returning a ``json.Value`` with
# integers parsed as ``Integer`` rather than ``Float``, so every
# declaration/assignment/call-argument site can render as a plain
# ``_json_parse(`...`)``.
_JSON_VALUE_STATIC_PREAMBLE: tuple[str, ...] = (
    "#+feature dynamic-literals",
    "package main",
    'import "core:encoding/json"',
    "_json_parse :: proc(s: string) -> json.Value {",
    "\tv, _ := json.parse_string(s, parse_integers=true)",
    "\treturn v",
    "}",
)


# Permissive format-config records used while ``json_type`` is active.  The
# framework still walks the data to compute a formatted ``value``, but
# that string is discarded by :func:`_format_odin_json_declaration` and
# friends in favor of a fresh ``_json_parse(`...`)`` call against the
# raw data.  These definitions only need to be permissive enough that
# the formatting pass does not error on heterogeneous data or nulls
# inside containers.
_JSON_VALUE_SEQUENCE_CONFIG = SequenceFormatConfig(
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

_JSON_VALUE_SET_CONFIG = SetFormatConfig(
    set_open=fixed_open(open_str="["),
    close="]",
    empty_set="[]",
    preamble_lines=(),
    set_opener_template="",
    supports_heterogeneity=True,
    supports_trailing_comma=True,
)

_JSON_VALUE_DICT_CONFIG = DictFormatConfig(
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

_JSON_VALUE_ORDERED_MAP_CONFIG = OrderedMapFormatConfig(
    ordered_map_open=fixed_open(open_str="{"),
    close="}",
    preamble_lines=(),
)


@beartype
def _temporal_to_iso(data: datetime.date | datetime.time) -> str:
    """Return ISO-8601 text for a date / datetime / time value.

    Naive datetimes are anchored to UTC so the round trip through
    ``json.parse_string`` keeps a definite offset.
    """
    if isinstance(data, datetime.datetime):
        iso = data.isoformat()
        if data.tzinfo is None:
            iso += "Z"
        return iso
    return data.isoformat()


@beartype
def _to_jsonable(data: Value) -> object:
    """Convert *data* into a value that :func:`json.dumps` can serialize.

    Dates, datetimes, and times become ISO-8601 strings (JSON has no
    temporal type).  Bytes become a hex-encoded string.  Sets and
    :class:`OrderedMap` fold into list/dict respectively.  Non-string
    dict keys are not handled here; the caller validates first.
    """
    match data:
        case datetime.datetime() | datetime.date() | datetime.time():
            return _temporal_to_iso(data=data)
        case bytes():
            return data.hex()
        case OrderedMap() | dict():
            return {
                key: _to_jsonable(data=value) for key, value in data.items()
            }
        case set():
            items = [_to_jsonable(data=item) for item in data]
            items.sort(key=repr)
            return items
        case list():
            return [_to_jsonable(data=item) for item in data]
        case _:
            return data


@beartype
def _format_odin_json_value(data: Value) -> str:
    """Serialize *data* as a single-line JSON expression."""
    return json.dumps(obj=_to_jsonable(data=data), ensure_ascii=False)


@beartype
def _odin_parse_expression(data: Value) -> str:
    """Render an ``_json_parse`` call call.

    Odin's raw-string literal (backtick-delimited) carries the JSON
    text verbatim, including embedded double quotes and backslash
    escapes, without needing further escaping.  :func:`json.dumps`
    never produces a literal backtick, so the raw string is safe.
    """
    json_text = _format_odin_json_value(data=data)
    return f"_json_parse(`{json_text}`)"


@beartype
def _format_odin_json_declaration(
    name: str,
    _value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a ``json.Value`` declaration backed by ``_json_parse``."""
    return f"{name} := {_odin_parse_expression(data=data)}"


@beartype
def _format_odin_json_assignment(
    name: str,
    _value: str,
    data: Value,
) -> str:
    """Format a ``json.Value`` assignment backed by ``_json_parse``."""
    return f"{name} = {_odin_parse_expression(data=data)}"


@beartype
def _format_odin_json_call_arg(raw_value: Value, _formatted: str) -> str:
    """Format a direct call argument as a ``json.Value`` literal."""
    return _odin_parse_expression(data=raw_value)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Odin(metaclass=LanguageCls):
    """Odin language specification."""

    format_integer_widened = no_format_integer_widened
    format_integer_beyond_i64 = no_format_integer_beyond_i64
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".odin"
    pygments_name = "odin"
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
            "asm",
            "auto_cast",
            "bit_field",
            "break",
            "case",
            "cast",
            "context",
            "continue",
            "defer",
            "distinct",
            "do",
            "dynamic",
            "else",
            "enum",
            "false",
            "for",
            "for_all",
            "for_any",
            "foreign",
            "if",
            "import",
            "in",
            "inline",
            "map",
            "matrix",
            "or_return",
            "package",
            "proc",
            "return",
            "struct",
            "switch",
            "transmute",
            "true",
            "typeid",
            "union",
            "using",
            "when",
            "where",
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
    supports_default_dict_key_type = False
    supports_default_dict_value_type = False
    supports_default_sequence_element_type = False
    supports_default_set_element_type = True
    supports_default_ordered_map_value_type = False
    non_default_kwargs: ClassVar[dict[str, str]] = {
        "default_set_element_type": "int"
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
        record_variants=frozenset(),
        nested_map_widening=NestedMapWideningVariant.NONE,
        modifier_sequence_format_overrides={},
    )
    supports_record_struct_name_prefix = True
    supports_record_shape_names = False
    supports_non_string_dict_keys = False

    class DateFormats(enum.Enum):
        """Date format options for Odin."""

        ISO = DateFormatConfig(
            formatter=format_date_iso, type_produced=str, preamble_lines=()
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Odin."""

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
        """Sequence type options for Odin."""

        DYNAMIC_ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="[dynamic]any{"),
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
        """Set type options for Odin."""

        SET = enum.member(
            value=set_format_factory(
                open_template="map[{type}]struct{{}}{{",
                close="}}",
                empty_template=None,
                preamble_lines=(),
                set_opener_template="",
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

        SHORT = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="{name} := {value}"
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
        positive_infinity="math.inf_f64(1)",
        negative_infinity="math.inf_f64(-1)",
        nan="math.nan_f64()",
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
        """Odin call style options."""

        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Heterogeneous-scalar strategy options.

        ``ERROR`` raises on a heterogeneous scalar collection.
        ``RECORD`` instead renders each record-shaped dict (non-empty,
        string-keyed) as a generated package-scope ``struct`` plus a
        matching ``Record0{ field = value, ... }`` literal, so a dict
        may mix scalars and containers that the homogeneous
        ``map[string]V`` cannot.
        """

        ERROR = enum.auto()
        RECORD = enum.auto()

    heterogeneous_strategies = HeterogeneousStrategies

    class JsonTypes(enum.Enum):
        """JSON value type options for Odin."""

        JSON_VALUE = "json.Value"
        """Odin's standard ``core:encoding/json`` ``Value`` sum type."""

    json_types = JsonTypes

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for Odin."""

        DEV_2024 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.PASCAL,
        IdentifierCase.UPPER_SNAKE,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    def validate_spec_for_data(self, data: Value) -> None:
        """Raise if the spec cannot produce valid code for *data*.

        When :attr:`json_type` is active, walk *data* to reject
        non-string dict keys (which JSON objects cannot represent) and
        strings (string values or string-typed dict keys) carrying a
        literal backtick (which would terminate the Odin raw-string
        delimiter that wraps the embedded JSON text).
        """
        if self._json_type_active:
            self._validate_json_value(data)

    @cached_property
    def _json_type_active(self) -> bool:
        """Return whether Odin should render via ``json.Value``."""
        return self.json_type is not None

    def __post_init__(self) -> None:
        """Reject ``json_type`` combinations the generator cannot emit."""
        self._validate_json_type_spec()

    def _validate_json_type_spec(self) -> None:
        """Reject ``json_type`` combinations the generator cannot emit.

        Under ``json_type`` the rendered data flows through a single
        ``_json_parse`` call, which is incompatible with
        ``heterogeneous_strategy=RECORD`` (which would generate ``struct``
        declarations parallel to the JSON text).
        """
        if not self._json_type_active:
            return
        if self.heterogeneous_strategy is self.heterogeneous_strategies.RECORD:
            msg = (
                "Odin json_type renders data through "
                "_json_parse(`...`) and is incompatible with "
                "heterogeneous_strategy=RECORD, which generates typed "
                "struct declarations. Use heterogeneous_strategy=ERROR."
            )
            raise IncompatibleFormatsError(msg)

    def _validate_json_value(self, data: Value, /) -> None:
        """Reject inputs ``json.Value`` cannot carry.

        Walks the value tree and rejects non-string object keys (no
        JSON representation), any string value or string-typed key
        containing a literal backtick character (which would terminate
        the Odin raw-string delimiter wrapping the embedded JSON
        text), and non-finite floats (``NaN`` / ``+Infinity`` /
        ``-Infinity``) which JSON has no syntax for and which
        ``json.parse_string`` rejects at runtime.
        """
        match data:
            case OrderedMap() | dict():
                for key, value in data.items():
                    if not isinstance(key, str):
                        msg = (
                            "Odin json_type can only represent dict keys "
                            "as JSON object strings, not "
                            f"{type(key).__name__}"
                        )
                        raise UnrepresentableInputError(msg)
                    self._reject_backtick(value=key)
                    self._validate_json_value(value)
            case list() | set():
                for item in data:
                    self._validate_json_value(item)
            case str():
                self._reject_backtick(value=data)
            case bool():
                return
            case float() if not math.isfinite(data):
                msg = (
                    "Odin json_type renders the literalized value as a "
                    "JSON text; JSON has no representation for non-finite "
                    "floats (NaN / +Infinity / -Infinity) and "
                    "json.parse_string rejects them at runtime."
                )
                raise UnrepresentableInputError(msg)
            case _:
                return

    @staticmethod
    def _reject_backtick(value: str) -> None:
        """Raise if *value* contains an Odin raw-string terminator."""
        if "`" in value:
            msg = (
                "Odin json_type embeds the rendered JSON text inside a "
                "backtick-delimited raw string; a literal backtick in a "
                "string value or dict key would terminate the literal "
                "and yield non-compiling output."
            )
            raise UnrepresentableInputError(msg)

    @cached_property
    def validate_call_arg(self) -> Callable[[Value], None]:
        """Return call-argument validation for this language.

        Under :attr:`json_type` direct call arguments flow through
        the same ``_json_parse`` shortcut as variable bindings, so
        they need the same dict-key / backtick rejection that
        :meth:`validate_spec_for_data` applies on the variable path.
        """
        if self._json_type_active:
            return self._validate_json_value
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
        """Wrap an Odin declaration in a main procedure.

        Under :attr:`json_type` an :class:`ExistingVariable` form
        produces a bare ``my_data = _json_parse(...)`` line, which the
        Odin compiler rejects (the name is undeclared); inject a
        zero-valued ``my_data: any`` declaration ahead of the
        assignment so the wrapped file still compiles.  Typed ``any``
        (not ``json.Value``): the assignment may bind either a
        ``_json_parse`` value or a call result whose stub returns
        ``any``, and only ``any`` accepts both.
        """
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        if (
            self._json_type_active
            and variable_name
            and re.search(
                pattern=rf"^[ \t]*{re.escape(pattern=variable_name)} = ",
                string=content,
                flags=re.MULTILINE,
            )
            and not re.search(
                pattern=rf"^[ \t]*{re.escape(pattern=variable_name)} := ",
                string=content,
                flags=re.MULTILINE,
            )
        ):
            content = f"{variable_name}: any\n{content}"
        use_line = f"\n_ = {variable_name}" if variable_name else ""
        return f"\nmain :: proc() {{\n{content}{use_line}\n}}"

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
    sequence_format: SequenceFormats = SequenceFormats.DYNAMIC_ARRAY
    set_format: SetFormats = SetFormats.SET
    default_set_element_type: str = "string"
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
        StatementTerminatorStyles.SEMICOLON
    )
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    json_type: JsonTypes | None = None
    record_struct_name_prefix: str = "Record"
    language_version: VersionFormats = VersionFormats.DEV_2024
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
    statement_terminator: ClassVar[str] = ";"
    static_body_preamble: ClassVar[Sequence[str]] = ()

    @cached_property
    def static_preamble(self) -> Sequence[str]:
        """File-scope preamble.

        Under :attr:`json_type` the package gains a ``core:encoding/json``
        import plus a tiny ``_json_parse`` helper so every literalized
        value can render as a single ``_json_parse`` call call.
        """
        if self._json_type_active:
            return _JSON_VALUE_STATIC_PREAMBLE
        return (
            "#+feature dynamic-literals",
            "package main",
        )

    special_float_preamble: ClassVar[tuple[str, ...]] = ('import "core:math"',)
    call_style: CallStyles = CallStyles.POSITIONAL

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
        """Format a set entry.

        Under :attr:`json_type` set entries fold into the JSON text
        and the per-entry string is discarded, so the framework just
        needs a permissive identity arm rather than the
        ``"key" = {}`` map-as-set form.
        """
        if self._json_type_active:
            return passthrough_sequence_entry
        return _format_set_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable.

        Under :attr:`json_type` the assignment uses the
        ``_json_parse`` call shortcut instead of the framework's
        formatted value.
        """
        if self._json_type_active:
            return _format_odin_json_assignment
        return variable_formatter(template="{name} = {value}")

    def _odin_record_field_type(  # noqa: PLR0911  # pylint: disable=too-complex
        self,
        request: RecordFieldType,
        /,
    ) -> str:
        """Return the Odin ``struct`` field type for a record field,
        derived structurally from the raw value.

        A field whose value is itself a nested record-shaped dict uses
        that record's generated name.  Every container Odin renders is
        ``any``-boxed -- a list is ``[dynamic]any{...}`` and an ordered
        map or non-record dict is ``map[string]any{...}`` -- so the
        declared field type is the matching ``any`` container; no
        element type is inferred.  A scalar maps to its Odin type, with
        an integer's width following its own value (so a wide-integer
        literal still fits its field) and a datetime typed ``int`` only
        when the active datetime format renders it as an epoch number.
        A set or non-record dict field is out of scope for the base
        ``RECORD`` port (the cross-language decision is tracked in
        #2317); a non-record dict still renders as a plain
        ``map[string]any`` so the catch-all type matches its literal.
        """
        if request.record_name is not None:
            return request.record_name
        value = request.value
        match value:
            case None:
                return "any"
            case bool():
                return "bool"
            case int():
                return _odin_int_field_type(value)
            case float():
                return "f64"
            case str() | bytes():
                return "string"
            case datetime.datetime() if (
                self.datetime_format.value.type_produced is int
            ):
                return _odin_int_field_type(
                    datetime_epoch_seconds(value=value),
                )
            case datetime.date() | datetime.time():
                return "string"
            case list():
                return "[dynamic]any"
            case _:
                return "map[string]any"

    @cached_property
    def _record_renderer(self) -> RecordRenderer:
        """Odin syntax hooks for the ``RECORD`` strategy."""
        return RecordRenderer(
            name_prefix=self.record_struct_name_prefix,
            record_shape_names=_ODIN_NO_RECORD_SHAPE_NAMES,
            field_identifier=_odin_record_field_identifier,
            field_type=self._odin_record_field_type,
            render_declaration=_odin_render_record_declaration,
            render_literal=_odin_record_literal,
        )

    @cached_property
    def _record_strategy(self) -> RecordStrategy:
        """Resolve the active strategy to its behavior + preamble.

        ``RECORD`` resolves to the shared record behavior plus the
        package-scope ``struct``-declaration preamble; ``ERROR`` keeps
        the raising behavior and emits no data preamble.
        """
        cls = type(self.heterogeneous_strategy)
        if self.heterogeneous_strategy is cls.RECORD:
            return build_record_strategy(
                renderer=self._record_renderer,
                split_conflicting_field_types=False,
                widen_unrecordizable_nested_sibling_maps=True,
                derecordized_map_open=None,
            )
        return RecordStrategy(
            behavior=NO_HETEROGENEOUS_BEHAVIOR,
            preamble=no_data_preamble,
        )

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        Under :attr:`json_type` the data rides inside a single JSON
        string, so no per-data preamble applies.  For
        ``HeterogeneousStrategies.RECORD`` emits one ``struct``
        declaration per record shape present in the data; otherwise
        produces no preamble.
        """
        if self._json_type_active:
            return no_data_preamble
        return self._record_strategy.preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the behavior for the chosen heterogeneous strategy.

        Under :attr:`json_type` heterogeneous scalars all flow through
        the JSON text, so scalar-uniformity checks are skipped.
        """
        if self._json_type_active:
            return dataclasses.replace(
                NO_HETEROGENEOUS_BEHAVIOR,
                skip_scalar_checks=True,
            )
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
        return _odin_call_body_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return file-scope stubs for a call expression."""
        return _odin_call_preamble_stub

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
    def format_call_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a declaration binding a call result.

        Always uses the plain ``{name} := {value}`` form regardless of
        :attr:`json_type`: a call's return type is opaque to the
        renderer (the generated proc stub returns ``any``), and the
        json-mode ``_json_parse`` shortcut applied to literal bindings
        would discard the formatted call expression and substitute the
        argument data, which is not the call's return value.
        """

        @beartype
        def _format_call_decl(
            name: str,
            value: str,
            _data: Value,
            _modifiers: frozenset[enum.Enum],
        ) -> str:
            """Format an inferred Odin declaration binding a call."""
            return f"{name} := {value}"

        return _format_call_decl

    @cached_property
    def format_call_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment binding a call result.

        The call-expression counterpart of
        :attr:`format_call_variable_declaration`; the json-mode
        ``_json_parse`` shortcut applied to literal assignments would
        substitute the argument data for the formatted call
        expression and is dropped here.
        """

        @beartype
        def _format_call_assign(name: str, value: str, _data: Value) -> str:
            """Format an Odin assignment binding a call."""
            return f"{name} = {value}"

        return _format_call_assign

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Callable that rewrites a formatted direct call argument.

        Under :attr:`json_type` each argument is a ``json.Value``
        produced by ``_json_parse``; otherwise the framework's
        formatted text passes through unchanged.
        """
        if self._json_type_active:
            return _format_odin_json_call_arg
        return identity_call_arg

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format.

        Under :attr:`json_type` lists fold into the JSON text and the
        framework's formatted output is discarded.
        """
        if self._json_type_active:
            return _JSON_VALUE_SEQUENCE_CONFIG
        return self.sequence_format.value

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        if self._json_type_active:
            return _JSON_VALUE_SEQUENCE_CONFIG.sequence_open
        return self.sequence_format.value.sequence_open

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        if self._json_type_active:
            return _JSON_VALUE_SET_CONFIG
        init_element_to_type = make_element_to_type(
            str_type="string",
            bool_type="bool",
            int_type="int",
            float_type="f64",
            mixed_numeric_type="f64",
            bytes_type="string",
            date_type="string",
            datetime_type="string",
            time_type="string",
            list_template="[dynamic]{inner}",
            enable_list_type=True,
            dict_type_template="map[string]{inner}",
            fallback_value_type="string",
            wide_int_type=None,
        )
        base_set_config: SetFormatConfig = self.set_format(
            default_type=self.default_set_element_type,
        )
        return base_set_config.with_typed_opener(
            type_to_opener=make_type_to_opener(
                element_to_type=init_element_to_type,
                opener_template="map[{type_name}]struct{{}}{{",
            ),
            fallback=base_set_config.set_open([]),
        )

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        if self._json_type_active:
            return _JSON_VALUE_DICT_CONFIG
        return DictFormatConfig(
            dict_open=fixed_open(
                open_str="map[string]any{",
            ),
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
        """Configuration for ordered-map formatting."""
        if self._json_type_active:
            return _JSON_VALUE_ORDERED_MAP_CONFIG
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="map[string]any{"),
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
        """Callable that formats a new variable declaration.

        Under :attr:`json_type` the declaration is a
        ``_json_parse`` call call (the inferred return type is
        ``json.Value``), bypassing both the framework's formatted value
        and the nil-safe ``: any = nil`` shim.
        """
        if self._json_type_active:
            return _format_odin_json_declaration
        return _nil_safe_declaration(
            base_formatter=self.declaration_style.value.formatter,
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Odin needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Odin needs none)."""
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
