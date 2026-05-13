"""Kotlin language specification."""

import dataclasses
import datetime
import enum
import functools
from collections import OrderedDict
from collections.abc import Callable, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar, assert_never

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._formatters.collection_openers import (
    TypedOpenerConfig,
    fixed_open,
    make_type_to_opener,
    typed_collection_open,
    typed_dict_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    datetime_ymdhms_formatter,
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
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
from literalizer._formatters.format_factories import set_format_factory
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    data_has_out_of_range_int,
    format_integer_binary,
    format_integer_hex,
    format_integer_underscore,
    make_overflow_fallback_formatter,
)
from literalizer._formatters.format_strings import (
    format_string_backslash_dollar,
)
from literalizer._formatters.type_inference import (
    DictType,
    ListType,
)
from literalizer._language import (
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
    KeywordCallStyle,
    LanguageCls,
    ModifierCombination,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    date_scalar_preamble,
    default_wrap_calls_with_declarations,
    identity_call_arg,
    identity_call_ref_identifier,
    identity_call_statement,
    identity_call_target,
    never_inhibits_consuming_form,
    no_call_stub,
    no_type_hint_preamble,
    no_validate_call_arg,
    no_validate_spec_for_data,
    wrap_combined_in_file_noop,
    wrap_in_file_noop,
)
from literalizer._types import Value


@beartype
def _format_kotlin_biginteger_literal(value: int) -> str:
    """Format a value outside signed 64-bit range as a Kotlin
    ``java.math.BigInteger`` constructor call.

    The Kotlin ``Long`` type is signed 64-bit; values outside that
    range must use ``java.math.BigInteger`` (with a matching ``import``
    statement emitted via the data-dependent preamble).
    """
    return f'BigInteger("{value}")'


@beartype
def _kotlin_biginteger_preamble(data: Value, /) -> tuple[str, ...]:
    """Return ``import java.math.BigInteger`` if *data* contains a
    very-large integer.
    """
    if data_has_out_of_range_int(data=data):
        return ("import java.math.BigInteger",)
    return ()


@beartype
def _kotlin_tuple_open(items: list[Value]) -> str:
    """Return the Kotlin tuple opener based on element count."""
    openers: dict[int, str] = {
        2: "Pair(",
        3: "Triple(",
    }
    return openers.get(len(items), "listOf<Any?>(")


@beartype
def _kotlin_list_sequence_open(
    *,
    cfg: TypedOpenerConfig,
    date_type: str | None,
    datetime_type: str | None,
    dict_key_type: str = "",
) -> Callable[[list[Value]], str]:
    """Build a typed sequence opener for the Kotlin List format.

    Delegates to ``_kotlin_type_to_opener`` for scalars and lists
    (preserving specialized openers like ``intArrayOf``), and falls
    through to the config resolver for ``DictType`` so that nested
    types and date/datetime formats are handled correctly.
    """
    dict_resolver = cfg.element_to_type(
        list_template="List<{inner}>",
        date_type=date_type,
        datetime_type=datetime_type,
        enable_dict_type=True,
        dict_key_type=dict_key_type,
    )

    def _combined_opener(
        element_type: type | ListType | DictType,
    ) -> str | None:
        """Delegate to module-level implementation."""
        return _apply_kotlin_combined_opener(
            element_type=element_type, dict_resolver=dict_resolver
        )

    return typed_collection_open(
        type_to_opener=_combined_opener,
        fallback="listOf<Any?>(",
    )


@beartype
def _apply_kotlin_combined_opener(
    element_type: type | ListType | DictType,
    dict_resolver: Callable[[type | ListType | DictType], str | None],
) -> str | None:
    """Resolve element type, preferring specialized Kotlin openers."""
    if isinstance(element_type, DictType):
        return f"listOf<{dict_resolver(element_type)}>("
    return _kotlin_type_to_opener(element_type=element_type)


@beartype
def _kotlin_type_to_opener(
    element_type: type | ListType | DictType,
) -> str | None:
    """Map a Python element type to a Kotlin collection opener.

    Used as the scalar/list fallback for the LIST format (via
    :func:`_kotlin_list_sequence_open`).  Returns ``None`` for
    ``DictType`` — the LIST format handles dicts via the config
    resolver before calling this function.
    """
    scalar_openers: dict[type, str] = {
        str: "arrayOf(",
        bool: "booleanArrayOf(",
        int: "intArrayOf(",
        float: "doubleArrayOf(",
        bytes: "arrayOf(",
        datetime.date: "arrayOf(",
        datetime.datetime: "arrayOf(",
    }
    match element_type:
        case DictType():
            return None
        case ListType():
            inner = _kotlin_type_to_opener(element_type=element_type.inner)
            return "arrayOf(" if inner is not None else None
        case _:
            return scalar_openers.get(element_type)


@beartype
def _kotlin_type_hint(  # pylint: disable=too-complex,too-many-branches  # noqa: C901, PLR0911, PLR0912
    *,
    data: Value,
    date_hint: str,
    datetime_hint: str,
    default_set_element_type: str,
    default_dict_key_type: str,
    default_dict_value_type: str,
    dict_outer: str,
    set_outer: str,
    sequence_format_name: str,
) -> str:
    """Derive a Kotlin type annotation from *data*."""
    recurse = functools.partial(
        _kotlin_type_hint,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        default_set_element_type=default_set_element_type,
        default_dict_key_type=default_dict_key_type,
        default_dict_value_type=default_dict_value_type,
        dict_outer=dict_outer,
        set_outer=set_outer,
        sequence_format_name=sequence_format_name,
    )
    match data:
        case bool():
            return "Boolean"
        case int():
            return "Int"
        case float():
            return "Double"
        case str():
            return "String"
        case bytes():
            return "String"
        case datetime.datetime():
            return datetime_hint
        case datetime.date():
            return date_hint
        case None:
            return "Nothing?"
        case dict():
            if not data:
                outer = (
                    dict_outer
                    if not isinstance(data, (ordereddict, OrderedDict))
                    else "LinkedHashMap"
                )
                return (
                    f"{outer}<{default_dict_key_type}"
                    f", {default_dict_value_type}>"
                )
            val_types = [recurse(data=v) for v in data.values()]
            unique = list(dict.fromkeys(val_types))
            match unique:
                case [single]:
                    val_type = single
                case _:
                    val_type = "Any?"
            outer = (
                dict_outer
                if not isinstance(data, (ordereddict, OrderedDict))
                else "LinkedHashMap"
            )
            return f"{outer}<{default_dict_key_type}, {val_type}>"
        case set():
            if not data:
                return f"{set_outer}<{default_set_element_type}>"
            elem_types = sorted({recurse(data=e) for e in data})
            match elem_types:
                case [single]:
                    elem_type = single
                case _:
                    elem_type = "Any?"
            return f"{set_outer}<{elem_type}>"
        case list():
            if not data:
                if sequence_format_name == "ARRAY":
                    return "Array<Any?>"
                return "List<Any?>"
            if sequence_format_name == "TUPLE":
                elem_types = [recurse(data=e) for e in data]
                match data:
                    case [_, _]:
                        return f"Pair<{', '.join(elem_types)}>"
                    case [_, _, _]:
                        return f"Triple<{', '.join(elem_types)}>"
                    case _:
                        return "List<Any?>"
            if sequence_format_name == "ARRAY":
                return "Array<Any?>"
            # LIST format — use typed arrays matching the opener
            elem_types = [recurse(data=e) for e in data]
            unique = list(dict.fromkeys(elem_types))
            if len(unique) != 1:
                return "List<Any?>"
            elem_type = unique[0]
            kotlin_prim = {
                "Boolean": "BooleanArray",
                "Int": "IntArray",
                "Double": "DoubleArray",
            }
            if elem_type in kotlin_prim:
                return kotlin_prim[elem_type]
            # Generic element types (e.g. Map<…>) use listOf, not
            # arrayOf, so the container type is List, not Array.
            if "<" in elem_type:
                return f"List<{elem_type}>"
            return f"Array<{elem_type}>"
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _format_kotlin_typed_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
    keyword: str,
    date_hint: str,
    datetime_hint: str,
    default_set_element_type: str,
    default_dict_key_type: str,
    default_dict_value_type: str,
    dict_outer: str,
    set_outer: str,
    sequence_format_name: str,
) -> str:
    """Format a Kotlin variable declaration with an explicit type."""
    hint = _kotlin_type_hint(
        data=data,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        default_set_element_type=default_set_element_type,
        default_dict_key_type=default_dict_key_type,
        default_dict_value_type=default_dict_value_type,
        dict_outer=dict_outer,
        set_outer=set_outer,
        sequence_format_name=sequence_format_name,
    )
    return f"{keyword} {name}: {hint} = {value}"


@dataclasses.dataclass(frozen=True)
class _KotlinDictSpec:
    """Per-format dict config pieces resolved at init time."""

    opener_template: str


def _kotlin_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Kotlin stub declarations for a call name."""
    param_list = ", ".join(f"{p}: Any? = null" for p in params)
    if len(parts) == 1:
        return (f"fun {parts[0]}({param_list}): Any? = null",)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        cls = f"_{root.title()}Type"
        return (
            f"class {cls} {{ fun {method}({param_list}): Any? = null }}",
            f"val {root} = {cls}()",
        )
    lines: list[str] = []
    inner_cls = f"_{fields[-1].title()}Type"
    lines.append(
        f"class {inner_cls} {{ fun {method}({param_list}): Any? = null }}"
    )
    prev_cls = inner_cls
    for i in range(len(fields) - 2, -1, -1):
        cls = f"_{fields[i].title()}Type"
        lines.append(f"class {cls} {{ val {fields[i + 1]} = {prev_cls}() }}")
        prev_cls = cls
    root_cls = f"_{root.title()}Type"
    lines.append(f"class {root_cls} {{ val {fields[0]} = {prev_cls}() }}")
    lines.append(f"val {root} = {root_cls}()")
    return tuple(lines)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Kotlin(metaclass=LanguageCls):
    """Kotlin language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.KOTLIN`` — ``LocalDate.of(...)`` call,
              e.g. ``LocalDate.of(2024, 1, 15)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.KOTLIN`` — ``LocalDateTime.of(...)`` call,
              e.g. ``LocalDateTime.of(2024, 1, 15, 12, 30, 0)``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.

        sequence_format: Which Kotlin sequence type to use.

            * ``sequence_formats.LIST`` — typed array calls
              (e.g. ``intArrayOf(1, 2, 3)``).  Heterogeneous
              sequences fall back to ``listOf<Any?>(…)``.
            * ``sequence_formats.TUPLE`` — ``Pair(…)`` for two-element
              sequences, ``Triple(…)`` for three-element sequences,
              e.g. ``Pair("a", 1)``.  Other sizes fall back to
              ``listOf<Any?>(…)``.
    """

    extension = ".kts"
    pygments_name = "kotlin"
    supports_special_floats = True
    supports_variable_names = True
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_zero_parameter_calls = True
    max_call_parameters: ClassVar[int | None] = None
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_module_name = False

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

    _opener_config = TypedOpenerConfig(
        str_type="String",
        bool_type="Boolean",
        int_type="Int",
        float_type="Double",
        bytes_type="String",
        mixed_numeric_type=None,
        date_type="LocalDate",
        datetime_type="LocalDateTime",
        list_template="Array<{inner}>",
        sequence_opener_template="arrayOf(",
        dict_opener_template="mapOf<{key_type}, {type_name}>(",
        set_opener_template="setOf<{type_name}>(",
        dict_type_template="Map<{key_type}, {inner}>",
        fallback_value_type="Any?",
    )

    class DateFormats(enum.Enum):
        """Date format options for Kotlin."""

        KOTLIN = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="LocalDate.of({year}, {month}, {day})",
            ),
            preamble_lines=("import java.time.LocalDate",),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Kotlin."""

        KOTLIN = DatetimeFormatConfig(
            formatter=datetime_ymdhms_formatter(
                template="LocalDateTime.of({year}, {month}, {day}, "
                "{hour}, {minute}, {second})",
            ),
            preamble_lines=("import java.time.LocalDateTime",),
        )
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
        """Sequence type options for Kotlin."""

        LIST = SequenceFormatConfig(
            sequence_open=typed_collection_open(
                type_to_opener=_kotlin_type_to_opener,
                fallback="listOf<Any?>(",
            ),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback="listOf<Any?>(",
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )
        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="arrayOf<Any?>("),
            close=")",
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
        TUPLE = SequenceFormatConfig(
            sequence_open=_kotlin_tuple_open,
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Kotlin."""

        SET = enum.member(
            value=set_format_factory(
                open_template="setOf<{type}>(",
                close=")",
                empty_template=None,
                preamble_lines=(),
                set_opener_template="",
                supports_heterogeneity=True,
                supports_trailing_comma=True,
            )
        )
        SORTED_SET = enum.member(
            value=set_format_factory(
                open_template="sortedSetOf<{type}>(",
                close=")",
                empty_template=None,
                preamble_lines=(),
                set_opener_template="sortedSetOf<{type_name}>(",
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

        VAL = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="val {name} = {value}"
            ),
            supports_redefinition=False,
        )
        VAR = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="var {name} = {value}"
            ),
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        MAP = _KotlinDictSpec(
            opener_template="mapOf<{key_type}, {type_name}>(",
        )
        HASH_MAP = _KotlinDictSpec(
            opener_template="hashMapOf<{key_type}, {type_name}>(",
        )

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="Double.POSITIVE_INFINITY",
        negative_infinity="Double.NEGATIVE_INFINITY",
        nan="Double.NaN",
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
            default_dict_key_type: str,
            default_dict_value_type: str,
            dict_outer: str,
            set_outer: str,
            sequence_format_name: str,
        ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
            """Return the variable declaration formatter."""
            if self.name in {"NEVER", "SAFE"}:
                return auto_formatter

            def _typed_formatter(
                name: str,
                value: str,
                data: Value,
                modifiers: frozenset[enum.Enum],
            ) -> str:
                """Adapt :func:`_format_kotlin_typed_declaration` to the
                positional formatter interface.
                """
                return _format_kotlin_typed_declaration(
                    name=name,
                    value=value,
                    data=data,
                    _modifiers=modifiers,
                    keyword=keyword,
                    date_hint=date_hint,
                    datetime_hint=datetime_hint,
                    default_set_element_type=default_set_element_type,
                    default_dict_key_type=default_dict_key_type,
                    default_dict_value_type=default_dict_value_type,
                    dict_outer=dict_outer,
                    set_outer=set_outer,
                    sequence_format_name=sequence_format_name,
                )

            return _typed_formatter

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
        """Kotlin call style options."""

        KEYWORD = KeywordCallStyle(separator=" = ")
        POSITIONAL = PositionalCallStyle()

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

    class VersionFormats(enum.Enum):
        """Version options for Kotlin."""

        V1_9 = enum.auto()

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

    date_format: DateFormats = DateFormats.KOTLIN
    datetime_format: DatetimeFormats = DatetimeFormats.KOTLIN
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    default_set_element_type: str = "Any?"
    default_dict_key_type: str = "String"
    default_dict_value_type: str = "Any?"
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.VAL
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.MAP
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
    call_style: CallStyles = CallStyles.KEYWORD
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    language_version: VersionFormats = VersionFormats.V1_9
    indent: str = "    "

    null_literal: ClassVar[str] = "null"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
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
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash_dollar

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
        return variable_formatter(template="{name} = {value}")

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines."""
        return _kotlin_biginteger_preamble

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
        return _kotlin_call_stub

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
    def format_call_ref_identifier(self) -> Callable[[str], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier into the
        language's call expression syntax.
        """
        return identity_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier(self) -> Callable[[str], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier in a call-argument
        context.

        Delegates to :attr:`format_call_ref_identifier`.  Override this to
        allow call-argument ``$ref`` values that would otherwise be rejected.
        """
        return self.format_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier_consumable(
        self,
    ) -> Callable[[str], str]:
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
    def _date_type_name(self) -> str | None:
        """Resolved Kotlin type name for the chosen date format."""
        return self._opener_config.type_name(
            py_type=self.date_format.value.type_produced,
        )

    @cached_property
    def _dt_type_name(self) -> str | None:
        """Resolved Kotlin type name for the chosen datetime format."""
        return self._opener_config.type_name(
            py_type=self.datetime_format.value.type_produced,
        )

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return self.sequence_format.value

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        fmt = self.sequence_format.value
        if fmt.typed_opener_fallback is None:
            return fmt.sequence_open
        return _kotlin_list_sequence_open(
            cfg=self._opener_config,
            date_type=self._date_type_name,
            datetime_type=self._dt_type_name,
            dict_key_type=self.default_dict_key_type,
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        base = self.set_format(default_type=self.default_set_element_type)
        openers = self._opener_config.build(
            date_type=self._date_type_name,
            datetime_type=self._dt_type_name,
            set_opener_template=base.set_opener_template or None,
            narrow_dict_values=False,
            dict_key_type=self.default_dict_key_type,
        )
        return base.with_typed_opener(
            type_to_opener=openers.set,
            fallback=base.set_open([]),
        )

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        resolved_dict_opener = self.dict_format.value.opener_template.replace(
            "{key_type}",
            self.default_dict_key_type,
        )
        return DictFormatConfig(
            dict_open=typed_dict_open(
                type_to_opener=make_type_to_opener(
                    element_to_type=self._opener_config.element_to_type(
                        list_template=None,
                        date_type=self._date_type_name,
                        datetime_type=self._dt_type_name,
                        enable_dict_type=False,
                        dict_key_type=self.default_dict_key_type,
                    ),
                    opener_template=resolved_dict_opener,
                ),
                fallback=resolved_dict_opener.format(
                    type_name=self.default_dict_value_type,
                ),
            ),
            narrowed_open=None,
            supports_trailing_comma=True,
            close=")",
            format_entry=dict_entry_with_separator(
                separator=" to ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
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
            fallback=_format_kotlin_biginteger_literal,
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(
                open_str=(
                    f"linkedMapOf<{self.default_dict_key_type}"
                    f", {self.default_dict_value_type}>("
                )
            ),
            close=")",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return dict_entry_with_separator(
            separator=" to ",
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
            date_hint=(
                "String"
                if self.date_format.value.type_produced is str
                else "LocalDate"
            ),
            datetime_hint=(
                "Long"
                if self.datetime_format.value.type_produced is int
                else (
                    "String"
                    if self.datetime_format.value.type_produced is str
                    else "LocalDateTime"
                )
            ),
            default_set_element_type=self.default_set_element_type,
            default_dict_key_type=self.default_dict_key_type,
            default_dict_value_type=self.default_dict_value_type,
            dict_outer=(
                "HashMap" if self.dict_format.name == "HASH_MAP" else "Map"
            ),
            set_outer=(
                "MutableSet" if self.set_format.name == "SORTED_SET" else "Set"
            ),
            sequence_format_name=self.sequence_format.name,
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble computed from date/datetime format."""
        return date_scalar_preamble(
            date_format=self.date_format,
            datetime_format=self.datetime_format,
        )

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Kotlin needs none)."""
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
