"""Swift language specification."""

import dataclasses
import datetime
import enum
import functools
from collections.abc import Callable, Mapping, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar, assert_never

from beartype import beartype

from literalizer._formatters.collection_openers import fixed_open
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
from literalizer._formatters.format_factories import (
    dict_format_factory,
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
    format_integer_octal,
    format_integer_underscore,
    make_overflow_fallback_formatter,
    raise_for_unrepresentable_int,
)
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
    wrap_combined_in_file_noop,
    wrap_in_file_noop,
)
from literalizer._types import OrderedMap, Scalar, Value


@beartype
def _format_date_swift(value: datetime.date) -> str:
    """Format a date as a Swift ``DateComponents`` expression."""
    return (
        "DateComponents("
        "calendar: Calendar(identifier: .gregorian), "
        f"year: {value.year}, month: {value.month}, day: {value.day}"
        ").date!"
    )


@beartype
def _format_datetime_swift(value: datetime.datetime) -> str:
    """Format a datetime as a Swift ``DateComponents`` expression."""
    parts = (
        "DateComponents("
        "calendar: Calendar(identifier: .gregorian), "
        f"year: {value.year}, month: {value.month}, day: {value.day}, "
        f"hour: {value.hour}, minute: {value.minute}, second: {value.second}"
    )
    if value.microsecond:
        nanosecond = value.microsecond * 1000
        parts += f", nanosecond: {nanosecond}"
    return parts + ").date!"


@beartype
def _tuple_sequence_entry(original: Value, entry: str) -> str:
    """Format a tuple sequence entry, casting nil to Any? for Swift."""
    if original is None:
        return "nil as Any?"
    return entry


@beartype
def _swift_param(*, name: str, accepts_nil: bool) -> str:
    """Format a single Swift parameter for a stub signature.

    When *accepts_nil* is ``True`` the parameter type is ``Any?`` with
    a ``nil`` default so a caller may pass ``nil``; otherwise it is
    ``Any`` with a ``0`` default.
    """
    type_and_default = "Any? = nil" if accepts_nil else "Any = 0"
    if name.startswith("_"):
        return f"_ {name}: {type_and_default}"
    return f"{name}: {type_and_default}"


@beartype
def _swift_args_contain_nil(*, args: Sequence[Value]) -> bool:
    """Return ``True`` when any top-level or per-element call argument is
    ``None``.

    Accepts either the flat per-call argument list or a list of
    per-element call argument lists; both shapes are inspected so a
    ``None`` at any call's slot is detected.
    """
    inner: list[Value] = []
    for arg in args:
        match arg:
            case list():
                inner.extend(arg)
            case _:
                inner.append(arg)
    return any(v is None for v in inner)


@beartype
def _swift_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Swift stub declarations for a call name."""
    accepts_nil = _swift_args_contain_nil(args=args)
    param_list = ", ".join(
        _swift_param(name=p, accepts_nil=accepts_nil) for p in params
    )
    if len(parts) == 1:
        return (
            f"@discardableResult func {parts[0]}({param_list}) -> Any {{ 0 }}",
        )
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    method_decl = (
        f"@discardableResult func {method}({param_list}) -> Any {{ 0 }}"
    )
    if not fields:
        cls = f"_{root}Type"
        return (
            f"class {cls} {{ {method_decl} }}",
            f"let {root} = {cls}()",
        )
    lines: list[str] = []
    inner_cls = f"_{fields[-1]}Type"
    lines.append(f"class {inner_cls} {{ {method_decl} }}")
    prev_cls = inner_cls
    for i in range(len(fields) - 2, -1, -1):
        cls = f"_{fields[i]}Type"
        lines.append(f"class {cls} {{ var {fields[i + 1]} = {prev_cls}() }}")
        prev_cls = cls
    root_cls = f"_{root}Type"
    lines.append(f"class {root_cls} {{ var {fields[0]} = {prev_cls}() }}")
    lines.append(f"let {root} = {root_cls}()")
    return tuple(lines)


@beartype
def _swift_scalar_hint(
    *,
    data: Scalar,
    date_hint: str,
    datetime_hint: str,
) -> str:
    """Derive the Swift annotation for a scalar value."""
    match data:
        case bool():
            hint = "Bool"
        case int():
            hint = "Int"
        case float():
            hint = "Double"
        case str() | bytes():
            hint = "String"
        case datetime.datetime():
            hint = datetime_hint
        case datetime.date():
            hint = date_hint
        case datetime.time():
            hint = "String"
        case None:
            hint = "Any?"
        case _ as unreachable:
            assert_never(unreachable)
    return hint


@beartype
def _swift_collapse(types: list[str]) -> str:
    """Return a single Swift element type or ``Any`` / ``Any?``
    fallback.
    """
    unique = list(dict.fromkeys(types))
    match unique:
        case [single]:
            return single
        case _ if "Any?" in unique:
            return "Any?"
        case _:
            return "Any"


@beartype
def _swift_dict_hint(
    *,
    val_types: list[str],
    is_empty: bool,
    default_dict_value_type: str,
) -> str:
    """Derive a Swift dictionary type annotation."""
    if is_empty:
        return f"[String: {default_dict_value_type}]"
    return f"[String: {_swift_collapse(types=val_types)}]"


@beartype
def _swift_list_hint(
    *,
    elem_types: list[str],
    is_empty: bool,
    sequence_is_tuple: bool,
    default_sequence_element_type: str,
) -> str:
    """Derive a Swift array/tuple type annotation."""
    if is_empty:
        return (
            "()" if sequence_is_tuple else f"[{default_sequence_element_type}]"
        )
    if sequence_is_tuple:
        return f"({', '.join(elem_types)})"
    return f"[{_swift_collapse(types=elem_types)}]"


@beartype
def _swift_type_hint(
    *,
    data: Value,
    date_hint: str,
    datetime_hint: str,
    default_set_element_type: str,
    default_sequence_element_type: str,
    default_dict_value_type: str,
    sequence_is_tuple: bool,
) -> str:
    """Derive a Swift type annotation from *data*."""
    recurse = functools.partial(
        _swift_type_hint,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        default_set_element_type=default_set_element_type,
        default_sequence_element_type=default_sequence_element_type,
        default_dict_value_type=default_dict_value_type,
        sequence_is_tuple=sequence_is_tuple,
    )
    match data:
        case dict():
            hint = _swift_dict_hint(
                val_types=[recurse(data=v) for v in data.values()],
                is_empty=not data,
                default_dict_value_type=default_dict_value_type,
            )
        case set():
            hint = f"Set<{default_set_element_type}>"
        case list():
            hint = _swift_list_hint(
                elem_types=[recurse(data=e) for e in data],
                is_empty=not data,
                sequence_is_tuple=sequence_is_tuple,
                default_sequence_element_type=default_sequence_element_type,
            )
        case _:
            hint = _swift_scalar_hint(
                data=data,
                date_hint=date_hint,
                datetime_hint=datetime_hint,
            )
    return hint


@beartype
def _format_swift_typed_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
    keyword: str,
    date_hint: str,
    datetime_hint: str,
    default_set_element_type: str,
    default_sequence_element_type: str,
    default_dict_value_type: str,
    sequence_is_tuple: bool,
) -> str:
    """Format a Swift variable declaration with a specific type."""
    hint = _swift_type_hint(
        data=data,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        default_set_element_type=default_set_element_type,
        default_sequence_element_type=default_sequence_element_type,
        default_dict_value_type=default_dict_value_type,
        sequence_is_tuple=sequence_is_tuple,
    )
    return f"{keyword} {name}: {hint} = {value}"


@beartype
def _apply_swift_optional_nil_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
    base_formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
    keyword: str,
) -> str:
    """Format a Swift variable declaration, guarding top-level ``nil``."""
    if data is None:
        return f"{keyword} {name}: Any? = {value}"
    return base_formatter(name, value, data, _modifiers)


@beartype
def _optional_nil_declaration(
    *,
    base_formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
    keyword: str,
) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
    """Wrap *base_formatter* so top-level ``nil`` gets an optional type.

    ``Any`` is non-optional in Swift, so ``let my_data: Any = nil`` fails
    to compile.  Emit ``{keyword} {name}: Any? = nil`` when the value is
    ``None``.
    """

    def _format(
        name: str,
        value: str,
        data: Value,
        _modifiers: frozenset[enum.Enum],
    ) -> str:
        """Delegate to module-level implementation."""
        return _apply_swift_optional_nil_declaration(
            name=name,
            value=value,
            data=data,
            _modifiers=_modifiers,
            base_formatter=base_formatter,
            keyword=keyword,
        )

    return _format


# The ``RECORD`` strategy supports only auto ``Record0``/``Record1``/...
# names (no ``record_shape_names``), so the shared renderer always gets
# an empty custom-name mapping.
_SWIFT_NO_RECORD_SHAPE_NAMES: Mapping[frozenset[str], str] = MappingProxyType(
    mapping={},
)


@beartype
def _swift_record_field_identifier(key: str, /) -> str:
    """Return the Swift ``struct`` member name for a dict *key*.

    Swift property identifiers are the dict keys verbatim (no case
    conversion), matching the synthesized-initializer literal form
    ``Record0(id: 1, ...)`` whose argument labels are the property
    names.
    """
    return key


@beartype
def _swift_record_literal(
    name: str,
    fields: Sequence[RecordLiteralField],
    /,
) -> RenderedRecordLiteral:
    """Render a Swift ``Name(field: value, ...)`` initializer literal as
    structured pieces for the shared compact/multiline layout code.

    A ``struct`` with stored properties and no explicit initializer gets
    a synthesized initializer taking one argument per stored property,
    each argument named for its property in declaration order; the
    shared strategy iterates the shape's keys in document order for both
    the declaration and the literal, so the orders always agree.
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
def _swift_render_record_declaration(
    name: str,
    fields: Sequence[RecordDeclarationField],
    /,
) -> str:
    """Render a Swift ``struct Name { let field: Type; ... }``.

    Stored ``let`` properties are emitted on one line separated by
    ``;``; the compiler synthesizes the initializer the literal calls.
    """
    members = "; ".join(
        f"let {field.identifier}: {field.type_name}" for field in fields
    )
    return f"struct {name} {{ {members} }}"


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Swift(metaclass=LanguageCls):
    """Swift language specification."""

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
    extension = ".swift"
    pygments_name = "swift"
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
        "default_set_element_type": "String",
        "default_sequence_element_type": "String",
        "default_dict_value_type": "String",
        "default_dict_key_type": "AnyHashable",
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
    supports_non_string_dict_keys = True

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

    class DateFormats(enum.Enum):
        """Date format options for Swift."""

        SWIFT = DateFormatConfig(
            formatter=_format_date_swift,
            preamble_lines=("import Foundation",),
            type_produced=datetime.date,
        )
        ISO = DateFormatConfig(
            formatter=format_date_iso, type_produced=str, preamble_lines=()
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Swift."""

        SWIFT = DatetimeFormatConfig(
            formatter=_format_datetime_swift,
            preamble_lines=("import Foundation",),
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
        """Sequence type options for Swift."""

        ARRAY = enum.member(
            value=sequence_format_factory(
                open_template="[",
                close="]",
                supports_heterogeneity=True,
                single_element_trailing_comma=False,
                supports_trailing_comma=True,
                empty_template="[{type}]()",
                preamble_lines=(),
                format_entry=passthrough_sequence_entry,
                typed_opener_fallback_template=None,
            )
        )
        TUPLE = enum.member(
            value=sequence_format_factory(
                open_template="(",
                close=")",
                supports_heterogeneity=True,
                single_element_trailing_comma=False,
                supports_trailing_comma=True,
                empty_template=None,
                preamble_lines=(),
                format_entry=_tuple_sequence_entry,
                typed_opener_fallback_template=None,
            )
        )

        def __call__(self, default_type: str) -> SequenceFormatConfig:
            """Create a sequence format config for the given type."""
            return self.value(default_type)

    class SetFormats(enum.Enum):
        """Set type options for Swift."""

        SET = enum.member(
            value=set_format_factory(
                open_template="Set<{type}>([",
                close="])",
                empty_template="Set<{type}>()",
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

        LET = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="let {name}: Any = {value}"
            ),
            supports_redefinition=False,
        )
        VAR = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="var {name}: Any = {value}"
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
                open_template="[",
                close="]",
                format_entry=dict_entry_with_separator(
                    separator=": ",
                    format_value=passthrough_sequence_entry,
                ),
                empty_template="[{key_type}: {type}]()",
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
        positive_infinity="Double.infinity",
        negative_infinity="-Double.infinity",
        nan="Double.nan",
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
        ALWAYS = enum.auto()
        SAFE = enum.auto()

        def formatter(
            self,
            *,
            auto_formatter: Callable[
                [str, str, Value, frozenset[enum.Enum]], str
            ],
            keyword: str,
            date_hint: str,
            datetime_hint: str,
            default_set_element_type: str,
            default_sequence_element_type: str,
            default_dict_value_type: str,
            sequence_is_tuple: bool,
        ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
            """Return the variable declaration formatter."""
            if self.name in {"NEVER", "SAFE"}:
                return _optional_nil_declaration(
                    base_formatter=auto_formatter,
                    keyword=keyword,
                )

            def _typed_formatter(
                name: str,
                value: str,
                data: Value,
                modifiers: frozenset[enum.Enum],
            ) -> str:
                """Adapt :func:`_format_swift_typed_declaration` to the
                positional formatter interface.
                """
                return _format_swift_typed_declaration(
                    name=name,
                    value=value,
                    data=data,
                    _modifiers=modifiers,
                    keyword=keyword,
                    date_hint=date_hint,
                    datetime_hint=datetime_hint,
                    default_set_element_type=default_set_element_type,
                    default_sequence_element_type=(
                        default_sequence_element_type
                    ),
                    default_dict_value_type=default_dict_value_type,
                    sequence_is_tuple=sequence_is_tuple,
                )

            return _typed_formatter

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
        """Swift call style options."""

        KEYWORD = KeywordCallStyle(separator=": ")

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Heterogeneous-scalar strategy options.

        Swift represents heterogeneous collections with ``Any`` by
        default (``ERROR``).  ``RECORD`` instead renders each
        record-shaped dict (non-empty, string-keyed) as a generated
        ``struct`` declared in the preamble plus a matching
        ``Record0(field: value, ...)`` initializer literal, so a
        record-shaped dict that mixes scalars with a container is
        representable as a typed value even though ``Dictionary``
        requires a homogeneous value type.
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
        """Version options for Swift."""

        V5_9 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.CAMEL,
        IdentifierCase.PASCAL,
        IdentifierCase.UPPER_SNAKE,
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

    date_format: DateFormats = DateFormats.SWIFT
    datetime_format: DatetimeFormats = DatetimeFormats.SWIFT
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.SET
    default_set_element_type: str = "AnyHashable"
    default_sequence_element_type: str = "Any"
    default_dict_key_type: str = "String"
    default_dict_value_type: str = "Any"
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.LET
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
    record_struct_name_prefix: str = "Record"
    # Keep in sync with the `-swift-version` flag passed to the Swift
    # linter in `.github/workflows/lint.yml` (which only accepts the
    # major language mode, so `V5_9` maps to `-swift-version 5`).
    language_version: VersionFormats = VersionFormats.V5_9
    indent: str = "    "

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
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""

        def _format(value: str) -> str:
            """Format a string as a Swift quoted literal."""
            return format_string_backslash_control(
                value=value,
                control_char_fmt="\\u{{{:x}}}",
            )

        return _format

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        return variable_formatter(template="{name} = {value}")

    @cached_property
    def _swift_date_hint(self) -> str:
        """Swift type name for the chosen :class:`datetime.date`
        format.
        """
        if self.date_format.value.type_produced is str:
            return "String"
        return "Date"

    @cached_property
    def _swift_datetime_hint(self) -> str:
        """Swift type name for the chosen :class:`datetime.datetime`
        format.
        """
        produced = self.datetime_format.value.type_produced
        if produced is int:
            return "Int"
        if produced is str:
            return "String"
        return "Date"

    def _swift_record_field_type(self, request: RecordFieldType, /) -> str:
        """Return the Swift ``struct`` field type for a record field,
        derived structurally from the raw value.

        A field whose value is itself a nested record-shaped dict uses
        that record's generated name.  A field whose value is a list
        whose every element is a record-shaped dict of one shared shape
        is typed ``[RecordN]`` to match the element type Swift infers
        from the homogeneous array of ``RecordN`` literals.  Every other
        value is typed by the same :func:`_swift_type_hint` machinery
        the typed variable declaration uses.  A record-eligible dict
        with no ``record_name`` was widened out of record inference
        because its nested sibling maps cannot share one shape; type it
        as ``[String: Any]`` so the uniform enclosing record survives
        (#2916).  Other dict and set fields fall through to the shared
        resolver.
        """
        if request.record_name is not None:
            return request.record_name
        if request.element_record_name is not None:
            return f"[{request.element_record_name}]"
        if (
            isinstance(request.value, dict)
            and not isinstance(request.value, OrderedMap)
            and record_shape_for_dict(value=request.value) is not None
        ):
            return "[String: Any]"
        return _swift_type_hint(
            data=request.value,
            date_hint=self._swift_date_hint,
            datetime_hint=self._swift_datetime_hint,
            default_set_element_type=self.default_set_element_type,
            default_sequence_element_type=self.default_sequence_element_type,
            default_dict_value_type=self.default_dict_value_type,
            sequence_is_tuple=(self.sequence_format.name == "TUPLE"),
        )

    @cached_property
    def _record_renderer(self) -> RecordRenderer:
        """Swift syntax hooks for the ``RECORD`` strategy."""
        return RecordRenderer(
            name_prefix=self.record_struct_name_prefix,
            record_shape_names=_SWIFT_NO_RECORD_SHAPE_NAMES,
            field_identifier=_swift_record_field_identifier,
            field_type=self._swift_record_field_type,
            render_declaration=_swift_render_record_declaration,
            render_literal=_swift_record_literal,
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
                derecordized_map_open=None,
                allow_same_key_record_variants_in_sequences=True,
            )
        return RecordStrategy(
            behavior=NO_HETEROGENEOUS_BEHAVIOR,
            preamble=no_data_preamble,
        )

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        Under ``HeterogeneousStrategies.RECORD`` this emits one
        ``struct`` declaration per record shape present in the data;
        otherwise no data-dependent lines.
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
        return _swift_call_stub

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

    scalar_body_preamble: ClassVar[dict[type, tuple[str, ...]]] = {}

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return self.sequence_format(
            default_type=self.default_sequence_element_type,
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return self.set_format(default_type=self.default_set_element_type)

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format_config.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return self.dict_format(
            default_type=self.default_dict_value_type,
            default_key_type=self.default_dict_key_type,
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
        return make_overflow_fallback_formatter(
            base=self.integer_format.get_formatter(
                numeric_separator=self.numeric_separator,
            ),
            fallback=raise_for_unrepresentable_int(language_name="Swift"),
            min_value=I64_MIN,
            max_value=I64_MAX,
        )

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Callable that formats a sequence entry."""
        return self.sequence_format_config.format_entry

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="["),
            close="]",
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
        return self.variable_type_hints.formatter(
            auto_formatter=self.declaration_style.value.formatter,
            keyword=self.declaration_style.name.lower(),
            date_hint=self._swift_date_hint,
            datetime_hint=self._swift_datetime_hint,
            default_set_element_type=self.default_set_element_type,
            default_sequence_element_type=self.default_sequence_element_type,
            default_dict_value_type=self.default_dict_value_type,
            sequence_is_tuple=(self.sequence_format.name == "TUPLE"),
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble computed from date/datetime format."""
        return date_scalar_preamble(
            date_format=self.date_format,
            datetime_format=self.datetime_format,
            extra=None,
        )

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
