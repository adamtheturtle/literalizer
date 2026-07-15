"""Scala language specification."""

import dataclasses
import datetime
import enum
import re
from collections.abc import Callable, Mapping, Sequence
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
    datetime_epoch_formatter,
    datetime_epoch_seconds,
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
    format_time_iso,
    format_time_local_time_of,
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
    format_integer_hex,
    format_integer_underscore,
    make_overflow_fallback_formatter,
    make_overflow_suffix_formatter,
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
from literalizer._formatters.tuple_strategy import (
    TupleRenderer,
    build_tuple_strategy,
)
from literalizer._formatters.type_inference import (
    DictType,
    ListType,
    WideInt,
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
    RenderedRecordLiteral,
    RenderedTupleLiteral,
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
)
from literalizer._types import OrderedMap, Value
from literalizer.exceptions import (
    InvalidRecordNameError,
    NullInCollectionError,
    UnrepresentableInputError,
)

_CIRCE_JSON_TYPE = "io.circe.Json"
_CIRCE_NULL = "Json.Null"
_CIRCE_TRUE = "Json.True"
_CIRCE_FALSE = "Json.False"


@beartype
def _scala_circe_wrap_scalar(raw_value: Value, formatted: str) -> str:  # noqa: PLR0911
    """Wrap a formatted scalar literal in the matching Circe constructor.

    The literal already produced by the per-type formatter is the inner
    argument; this lifts it to a :class:`io.circe.Json` expression so
    every value embedded in a Circe ``Json.obj`` / ``Json.arr`` is a
    well-typed ``Json``.
    """
    match raw_value:
        case bool():
            return _CIRCE_TRUE if raw_value else _CIRCE_FALSE
        case None:
            return _CIRCE_NULL
        case int() if formatted.startswith("BigInt"):
            return f"Json.fromBigInt({formatted})"
        case int() if formatted.endswith("L"):
            return f"Json.fromLong({formatted})"
        case int():
            return f"Json.fromInt({formatted})"
        case float():
            return f"Json.fromDoubleOrNull({formatted})"
        case _:
            return f"Json.fromString({formatted})"


@beartype
def _scala_circe_wrap_value(raw_value: Value, formatted: str) -> str:
    """Wrap a formatted value as a Circe ``Json``; pass container
    literals through unchanged (they already render as ``Json.obj`` /
    ``Json.arr``).
    """
    if isinstance(raw_value, (list, dict, set, OrderedMap)):
        return formatted
    return _scala_circe_wrap_scalar(raw_value=raw_value, formatted=formatted)


@beartype
def _scala_circe_declaration_formatter(
    *,
    declaration_style: enum.Enum,
    json_type_name: str,
) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
    """Return a declaration formatter for Circe ``Json`` output."""

    def _formatter(
        name: str,
        value: str,
        data: Value,
        modifiers: frozenset[enum.Enum],
    ) -> str:
        """Format a Circe-backed declaration."""
        del modifiers
        wrapped = _scala_circe_wrap_value(raw_value=data, formatted=value)
        keyword = "var" if declaration_style.name == "VAR" else "val"
        return f"{keyword} {name}: {json_type_name} = {wrapped}"

    return _formatter


@beartype
def _scala_circe_assignment_formatter(
    name: str,
    value: str,
    data: Value,
) -> str:
    """Format an assignment to an existing Circe-backed binding."""
    wrapped = _scala_circe_wrap_value(raw_value=data, formatted=value)
    return f"{name} = {wrapped}"


@beartype
def _format_scala_bigint_literal(value: int) -> str:
    """Format a value outside signed 64-bit range as a Scala
    ``BigInt(...)`` expression.

    Scala's ``Long`` is signed 64-bit; values outside that range must
    use ``BigInt``, which is available in the default scope.
    """
    return f'BigInt("{value}")'


@beartype
def _format_datetime_scala(value: datetime.datetime) -> str:
    """Format a datetime as a Scala ``ZonedDateTime.of(...)`` call."""
    timezone_name = value.tzname() or "UTC"
    nanoseconds = value.microsecond * 1000
    return (
        f"ZonedDateTime.of({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second}, "
        f'{nanoseconds}, ZoneId.of("{timezone_name}"))'
    )


@beartype
def _list_sequence_open(
    *,
    cfg: TypedOpenerConfig,
    date_type: str | None,
    datetime_type: str | None,
) -> Callable[[list[Value]], str]:
    """Build a typed sequence opener for the List format."""
    return typed_collection_open(
        type_to_opener=make_type_to_opener(
            element_to_type=cfg.element_to_type(
                list_template="List[{inner}]",
                enable_list_type=True,
                date_type=date_type,
                datetime_type=datetime_type,
                enable_dict_type=True,
                dict_key_type="",
            ),
            opener_template="List[{type_name}](",
        ),
        fallback="List(",
    )


@beartype
def _resolve_sequence_open(
    *,
    cfg: TypedOpenerConfig,
    sequence_format: enum.Enum,
    list_member: enum.Enum,
    fmt: SequenceFormatConfig,
    openers: TypeOpeners,
    date_type: str | None,
    datetime_type: str | None,
) -> Callable[[list[Value]], str]:
    """Resolve the sequence opener for a Scala sequence format."""
    if sequence_format is list_member:
        return _list_sequence_open(
            cfg=cfg,
            date_type=date_type,
            datetime_type=datetime_type,
        )
    if fmt.typed_opener_fallback is not None:
        _typed_open = typed_collection_open(
            type_to_opener=openers.seq,
            fallback=fmt.typed_opener_fallback,
        )

        def _null_guarded(items: list[Value]) -> str:
            """Raise if any item is null, else delegate to the typed
            opener.
            """
            if any(item is None for item in items):
                msg = (
                    "Scala's Array cannot contain null elements without an "
                    f"explicit type annotation (got {len(items)} items, "
                    "including null)."
                )
                raise NullInCollectionError(msg)
            return _typed_open(items)

        return _null_guarded
    return fmt.sequence_open


@dataclasses.dataclass(frozen=True)
class _ScalaDictSpec:
    """Per-format dict config pieces resolved at init time."""

    opener_template: str
    fallback: str
    preamble_lines: tuple[str, ...]


@beartype
def _scala_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Scala stub declarations for a call name."""
    param_list = ", ".join(f"{p}: Any = null" for p in params)
    if len(parts) == 1:
        return (f"def {parts[0]}({param_list}): Any = null",)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        cls = f"_{root.capitalize()}Type"
        return (
            f"class {cls} {{ def {method}({param_list}): Any = null }}",
            f"val {root} = new {cls}",
        )
    lines: list[str] = []
    inner_cls = f"_{fields[-1].capitalize()}Type"
    lines.append(
        f"class {inner_cls} {{ def {method}({param_list}): Any = null }}"
    )
    prev_cls = inner_cls
    for i in range(len(fields) - 2, -1, -1):
        cls = f"_{fields[i].capitalize()}Type"
        lines.append(f"class {cls} {{ val {fields[i + 1]} = new {prev_cls} }}")
        prev_cls = cls
    root_cls = f"_{root.capitalize()}Type"
    lines.append(f"class {root_cls} {{ val {fields[0]} = new {prev_cls} }}")
    lines.append(f"val {root} = new {root_cls}")
    return tuple(lines)


# A fallback opener carries no element type in the formatted literal
# (Scala infers it for a ``val``, but a ``case class`` field needs an
# explicit annotation).  Widen each to an ``[Any]`` form.  This is
# sound for every opener here, including ``scala.Array`` (which is
# *invariant*, unlike ``List`` / ``Map`` / ``ListMap``, covariant in
# their value parameter): the formatted literal is a collection-factory
# ``apply`` call (``List(...)``, ``Array(...)``, ``ListMap(...)``), and
# Scala infers that factory's element type from the expected (declared
# field) type, so ``Array(rec, rec)`` assigned to an ``Array[Any]``
# field elaborates to ``Array.apply[Any](...)`` and is itself
# ``Array[Any]``, never ``Array[RecordN]``.  Correctness does not rely
# on variance, only on expected-type-directed inference of the
# factory's type argument.
_SCALA_UNTYPED_OPENERS: dict[str, str] = {
    "List": "List[Any]",
    "Seq": "Seq[Any]",
    "Array": "Array[Any]",
    "Set": "Set[Any]",
    "Map": "Map[String, Any]",
    "ListMap": "scala.collection.immutable.ListMap[String, Any]",
    "scala.collection.immutable.ListMap": (
        "scala.collection.immutable.ListMap[String, Any]"
    ),
}

# Scala ``Int`` is signed 32-bit; an integer outside this range is
# formatted with an ``L`` suffix and is therefore a ``Long`` field
# (mapped via :class:`WideInt`).  Keep these bounds in sync with
# ``_I32_MIN`` / ``_I32_MAX`` in
# :mod:`literalizer._formatters.type_inference` (the widening threshold
# the value formatter uses, which has a back-reference to here).
_SCALA_INT32_MIN = -(2**31)
_SCALA_INT32_MAX = 2**31 - 1

_PASCAL_CASE_IDENTIFIER = re.compile(pattern=r"^[A-Z][A-Za-z0-9_]*$")

# Backtick identifiers let case-class parameters retain JSON keys that
# collide with Scala 3 hard or soft keywords.  The set intentionally
# includes contextual keywords: escaping them is harmless in contexts
# where they would otherwise be accepted and prevents parser drift.
_SCALA_KEYWORDS: frozenset[str] = frozenset(
    {
        "abstract",
        "as",
        "case",
        "catch",
        "class",
        "def",
        "derives",
        "do",
        "else",
        "end",
        "enum",
        "export",
        "extends",
        "extension",
        "false",
        "final",
        "finally",
        "for",
        "forSome",
        "given",
        "if",
        "implicit",
        "import",
        "infix",
        "inline",
        "lazy",
        "match",
        "new",
        "null",
        "object",
        "opaque",
        "open",
        "override",
        "package",
        "private",
        "protected",
        "return",
        "sealed",
        "super",
        "then",
        "this",
        "throw",
        "trait",
        "transparent",
        "true",
        "try",
        "type",
        "using",
        "val",
        "var",
        "while",
        "with",
        "yield",
    }
)


@beartype
def _scala_record_field_identifier(key: str, /) -> str:
    """Return the Scala ``case class`` field name for a dict *key*.

    Scala field identifiers are otherwise the dict keys verbatim (no
    case conversion).  Keywords are enclosed in backticks in both the
    declaration and named argument (issue #2968).
    """
    if key in _SCALA_KEYWORDS:
        return f"`{key}`"
    return key


@beartype
def _scala_record_literal(
    name: str,
    fields: Sequence[RecordLiteralField],
    /,
) -> RenderedRecordLiteral:
    """Render a Scala ``Name(field = value, ...)`` literal as structured
    pieces for the shared compact/multiline layout code.
    """
    return RenderedRecordLiteral(
        head=f"{name}(",
        entries=tuple(
            f"{field.identifier} = {field.formatted}" for field in fields
        ),
        closer=")",
        compact_pad="",
    )


@beartype
def _scala_render_declaration(
    name: str,
    fields: Sequence[RecordDeclarationField],
    /,
) -> str:
    """Render a Scala ``case class Name(field: Type, ...)``
    declaration.
    """
    params = ", ".join(
        f"{field.identifier}: {field.type_name}" for field in fields
    )
    return f"case class {name}({params})"


@beartype
def _scala_tuple_arity_representable(arity: int, /) -> bool:
    """Return whether Scala 3 has a native fixed-size tuple of the
    given element count.

    Scala 3 -- the only version this language targets -- imposes no
    tuple-length limit: ``(a, b, ...)`` is a native tuple for any
    element count, with lengths past 22 transparently backed by
    ``TupleXXL`` (Scala 2's ``Tuple22`` cap was removed).  A
    tuple-eligible array always has at least two elements (Scala has
    no one-element tuple sugar, but such a length never reaches here),
    so every length the ``TUPLE`` strategy passes is representable.
    """
    del arity
    return True


@beartype
def _scala_render_tuple_literal(
    value: list[Value],
    elements: Sequence[str],
    /,
) -> RenderedTupleLiteral:
    """Render a heterogeneous scalar array as a Scala tuple literal.

    The shared layout assembler joins *elements* into the compact
    ``(a, b)`` or one-per-line multiline form; *value* is unused
    because every element is already formatted.  Scala permits a
    trailing comma before the closing ``)`` on its own line (the same
    policy its collection literals use), so the language-wide
    trailing-comma config is kept for the multiline form.
    """
    del value
    return RenderedTupleLiteral(
        head="(",
        entries=tuple(elements),
        closer=")",
        compact_pad="",
        multiline_trailing_comma=True,
    )


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Scala(metaclass=LanguageCls):
    """Scala language specification."""

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
    extension = ".scala"
    pygments_name = "scala"
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
    non_default_kwargs: ClassVar[dict[str, str]] = {}
    declaration_style_sequence_format_overrides: ClassVar[dict[str, str]] = {}
    json_type_variant_name_suffix: ClassVar[str | None] = None
    supports_non_ascii_string_literals = True
    variant_metadata: ClassVar[VariantMetadata] = VariantMetadata(
        pre_indent_comment_scalar_variant=False,
        fixture_module_name_template="Fixture_{parent}_{stem}",
        fixture_module_name_lowercase=False,
        golden_filename_lowercase=False,
        collection_layout_category="collection_layout",
        record_variants=frozenset(),
        nested_map_widening=NestedMapWideningVariant.NONE,
        modifier_sequence_format_overrides={},
    )
    supports_record_struct_name_prefix = True
    supports_record_shape_names = True
    supports_non_string_dict_keys = False

    module_name: str = "Check"

    _opener_config = TypedOpenerConfig(
        str_type="String",
        bool_type="Boolean",
        int_type="Int",
        wide_int_type="Long",
        float_type="Double",
        mixed_numeric_type="Double",
        bytes_type="String",
        date_type="LocalDate",
        datetime_type="ZonedDateTime",
        time_type="LocalTime",
        list_template="Array[{inner}]",
        sequence_opener_template="Array[{type_name}](",
        dict_opener_template="Map[String, {type_name}](",
        set_opener_template="Set[{type_name}](",
        dict_type_template="Map[String, {inner}]",
        fallback_value_type="Any",
    )

    class DateFormats(enum.Enum):
        """Date format options for Scala."""

        SCALA = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="LocalDate.of({year}, {month}, {day})",
            ),
            preamble_lines=("import java.time.LocalDate",),
            type_produced=datetime.date,
        )
        ISO = DateFormatConfig(
            formatter=format_date_iso, type_produced=str, preamble_lines=()
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Scala."""

        SCALA = DatetimeFormatConfig(
            formatter=_format_datetime_scala,
            preamble_lines=(
                "import java.time.ZoneId",
                "import java.time.ZonedDateTime",
            ),
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
        """Sequence type options for Scala."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="List("),
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
        SEQ = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="Seq("),
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
        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="Array("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence="Array.empty[Any]",
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback="Array(",
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Scala."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="Set("),
            close=")",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )
        TREE_SET = SetFormatConfig(
            set_open=fixed_open(open_str="TreeSet("),
            close=")",
            empty_set="TreeSet.empty[Int]",
            preamble_lines=("import scala.collection.immutable.TreeSet",),
            set_opener_template="TreeSet[{type_name}](",
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

        MAP = _ScalaDictSpec(
            opener_template="Map[String, {type_name}](",
            fallback="Map(",
            preamble_lines=(),
        )
        LIST_MAP = _ScalaDictSpec(
            opener_template="ListMap[String, {type_name}](",
            fallback="ListMap(",
            preamble_lines=("import scala.collection.immutable.ListMap",),
        )

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="Double.PositiveInfinity",
        negative_infinity="Double.NegativeInfinity",
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
        """Scala call style options."""

        KEYWORD = KeywordCallStyle(separator=" = ")
        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Strategy for dicts whose values span more than one Scala type.

        ``ERROR`` keeps Scala's strict-typing behavior (mixed-value
        dicts that cannot be represented raise).  ``RECORD`` renders
        each record-shaped dict (non-empty, string-keyed) as a
        generated ``case class`` declared in the preamble plus a
        matching ``Record0(field = value, ...)`` literal, so fields may
        legitimately mix scalars and containers.  ``TUPLE`` composes
        ``RECORD`` and additionally renders each fixed-length
        heterogeneous scalar array (a record field, another dict value,
        or the document root) as a native tuple ``(e0, e1, ...)`` typed
        ``(T0, T1, ...)``.  Scala 3 imposes no tuple-length limit
        (lengths past 22 are transparently backed by ``TupleXXL``), so
        any fixed-length heterogeneous scalar array is representable.
        """

        ERROR = enum.auto()
        RECORD = enum.auto()
        TUPLE = enum.auto()

    heterogeneous_strategies = HeterogeneousStrategies

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for Scala."""

        V3 = enum.auto()

    version_formats = VersionFormats

    class JsonTypes(enum.Enum):
        """JSON value type options for Scala."""

        CIRCE = _CIRCE_JSON_TYPE
        """Circe's :class:`io.circe.Json` dynamic JSON value type."""

    json_types = JsonTypes

    module_name_case: ClassVar[IdentifierCase] = IdentifierCase.PASCAL
    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.CAMEL,
        IdentifierCase.PASCAL,
        IdentifierCase.UPPER_SNAKE,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    def validate_spec_for_data(self, data: Value) -> None:
        """Validate Scala-specific data/format combinations."""
        if self._json_type_active:
            self._validate_circe_value_keys(data=data)

    def _validate_circe_value_keys(self, *, data: Value) -> None:
        """Reject non-string object keys for Circe ``Json``."""
        match data:
            case dict():
                for key, value in data.items():
                    if not isinstance(key, str):
                        msg = (
                            "Scala json_type can only represent dict keys "
                            "as JSON object strings, not "
                            f"{type(key).__name__}"
                        )
                        raise UnrepresentableInputError(msg)
                    self._validate_circe_value_keys(data=value)
            case list() | set():
                for item in data:
                    self._validate_circe_value_keys(data=item)
            case _:
                return

    @cached_property
    def _json_type_active(self) -> bool:
        """Return whether Scala should render via Circe ``Json``."""
        return self.json_type is not None

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
        """Wrap a Scala declaration in an object."""
        del variable_name
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        return f"object {self.module_name} {{\n{content}\n}}"

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Scala declaration + assignment in an object."""
        return self.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    json_type: JsonTypes | None = None
    date_format: DateFormats = DateFormats.SCALA
    datetime_format: DatetimeFormats = DatetimeFormats.SCALA
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.VAL
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.MAP
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
    record_shape_names: Mapping[frozenset[str], str] = dataclasses.field(
        default_factory=lambda: MappingProxyType(mapping={}),
        hash=False,
    )
    # Keep in sync with the `-S` flag passed to `scala-cli run` in
    # `.github/workflows/lint.yml` (which only accepts the Scala major
    # version, so `V3` maps to `-S 3`).
    language_version: VersionFormats = VersionFormats.V3
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
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    def __post_init__(self) -> None:
        """Validate ``record_shape_names`` after construction."""
        self._validate_record_naming()

    def _validate_record_naming(self) -> None:
        """Validate ``record_shape_names`` for PascalCase identifier
        shape, collisions with the auto-generated ``{prefix}{N}``
        struct names, and duplicate target names.

        Ported from
        :meth:`literalizer.languages.Rust._validate_record_naming`.
        Scala has no ``heterogeneous_value_enum_name`` so that
        collision check does not apply, and Rust's reserved-keyword
        check is unnecessary here: every Scala keyword is lowercase,
        so the PascalCase requirement already rejects every one of
        them.
        """
        prefix = self.record_struct_name_prefix
        auto_name_pattern = re.compile(
            pattern=rf"^{re.escape(pattern=prefix)}\d+$",
        )
        seen_names: set[str] = set()
        for keys, name in self.record_shape_names.items():
            if not _PASCAL_CASE_IDENTIFIER.match(string=name):
                msg = (
                    f"record_shape_names entry for keys {sorted(keys)!r} "
                    f"maps to {name!r}, which is not a PascalCase Scala "
                    f"identifier."
                )
                raise InvalidRecordNameError(msg)
            if auto_name_pattern.match(string=name):
                msg = (
                    f"record_shape_names entry for keys {sorted(keys)!r} "
                    f"maps to {name!r}, which collides with the "
                    f"auto-generated {prefix!r}-prefixed struct names."
                )
                raise InvalidRecordNameError(msg)
            if name in seen_names:
                msg = (
                    f"record_shape_names maps multiple key-sets to "
                    f"{name!r}; struct names must be unique."
                )
                raise InvalidRecordNameError(msg)
            seen_names.add(name)

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        if self._json_type_active:
            return _scala_circe_wrap_value
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        if self._json_type_active:
            return _scala_circe_wrap_value
        return passthrough_set_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        if self._json_type_active:
            return _scala_circe_assignment_formatter
        return variable_formatter(template="{name} = {value}")

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Callable that rewrites a formatted direct call argument."""
        if self._json_type_active:
            return _scala_circe_wrap_value
        return identity_call_arg

    @cached_property
    def _scalar_field_type_resolver(
        self,
    ) -> Callable[[type | ListType | DictType], str | None]:
        """Map a scalar element type to its Scala type name.

        Built from the same scalar mapping the collection openers use,
        with the date/datetime names resolved from the configured
        formats (so an ``ISO`` datetime field is typed ``String``,
        matching the rendered literal).  ``WideInt`` resolves to
        ``Long``.  An ``EPOCH`` datetime field bypasses the datetime
        mapping here: :meth:`_scala_record_field_type` routes it
        through :meth:`_scala_int_magnitude_field_type` so its width
        tracks the epoch value.
        """
        return self._opener_config.element_to_type(
            list_template=None,
            enable_list_type=False,
            date_type=self._date_type_name,
            datetime_type=self._datetime_type_name,
            enable_dict_type=False,
            dict_key_type="",
        )

    def _scala_int_magnitude_field_type(self, value: int, /) -> str:
        """Resolve an integer's ``case class`` field type by 32-bit
        magnitude.

        An ``Int``-range value stays ``Int``; a wider one maps via
        :class:`WideInt` to ``Long``, matching the ``L``-suffixed
        literal :attr:`format_integer` emits.  Shared by the plain
        integer arm and the ``EPOCH`` datetime arm (epoch seconds after
        2038-01-19 leave 32-bit range) so the declared field type
        always matches the rendered literal; it is therefore
        value-driven, not a pure ``cached_property``.
        """
        element_type: type = (
            int if _SCALA_INT32_MIN <= value <= _SCALA_INT32_MAX else WideInt
        )
        return self._scalar_field_type_resolver(element_type) or "Any"

    def _scala_record_field_type(  # noqa: PLR0911  # pylint: disable=too-complex
        self,
        request: RecordFieldType,
        /,
    ) -> str:
        """Return the Scala ``case class`` field type for a record
        field, derived structurally from the raw value.

        A field whose value is itself a nested record-shaped dict uses
        that record's generated name.  A list or ordered-map field
        derives its type from the very collection opener the value
        formatter uses for that value (a record field is formatted with
        no sibling override, so the opener equals the one emitted); the
        opener's trailing ``(`` is dropped, and a bare fallback opener
        (``List(`` / ``Array(``, or the ordered-map opener) widens to
        its ``...[Any]`` form.  That widening type-checks even for the
        invariant ``Array`` because the literal is a factory ``apply``
        whose element type Scala infers from the declared field type
        (see :data:`_SCALA_UNTYPED_OPENERS`), not by collection
        variance.  A scalar field uses the same scalar mapping the
        openers are built on (a wide ``int`` -> ``Long``); an ``EPOCH``
        datetime is sized like the epoch integer it renders as
        (``Int``, or ``Long`` once it leaves 32-bit range past 2038).

        A record-eligible dict with no ``record_name`` was widened out
        of record inference because its nested sibling maps cannot
        share one shape.  Type that field as ``Map[String, Any]`` so the
        uniform enclosing record survives (#2915).  A set or a genuinely
        non-record dict (empty or non-string-keyed) still has no precise
        component type; per the cross-language decision in #2317, Scala
        widens it to the top type ``Any``.
        """
        if request.record_name is not None:
            return request.record_name
        value = request.value
        # An ``EPOCH`` datetime renders as its epoch integer, so size
        # the field exactly like that integer (``Int`` or, past 2038,
        # ``Long``); other datetime formats stay datetime-typed via the
        # scalar resolver below.
        if (
            isinstance(value, datetime.datetime)
            and self.datetime_format.value.type_produced is int
        ):
            value = datetime_epoch_seconds(value=value)
        match value:
            case None:
                return "Any"
            case OrderedMap():
                opener = self.ordered_map_format_config.ordered_map_open(
                    value,
                )
            case dict() if record_shape_for_dict(value=value) is not None:
                return "Map[String, Any]"
            case list():
                opener = self.sequence_open(value)
            case bool():
                return self._scalar_field_type_resolver(bool) or "Any"
            case int() if not I64_MIN <= value <= I64_MAX:
                return "BigInt"
            case int():
                return self._scala_int_magnitude_field_type(value)
            case _:
                return self._scalar_field_type_resolver(type(value)) or "Any"
        head = opener[: -len("(")]
        return _SCALA_UNTYPED_OPENERS.get(head, head)

    @cached_property
    def _record_renderer(self) -> RecordRenderer:
        """Scala syntax hooks for the ``RECORD`` strategy."""
        return RecordRenderer(
            name_prefix=self.record_struct_name_prefix,
            record_shape_names=self.record_shape_names,
            field_identifier=_scala_record_field_identifier,
            field_type=self._scala_record_field_type,
            render_declaration=_scala_render_declaration,
            render_literal=_scala_record_literal,
        )

    def _scala_tuple_field_type(self, elements: list[Value], /) -> str:
        """Return the Scala tuple type ``(T0, T1, ...)`` for a
        tuple-eligible ``RECORD`` field, one type per position.

        The length is validated at check time, so *elements* is 2..22;
        each position's type reuses :meth:`_scala_record_field_type`
        (the same scalar resolution a plain field value uses), so e.g.
        ``[1, "email"]`` types ``(Int, String)``.
        """
        elem_types = [
            self._scala_record_field_type(
                RecordFieldType(
                    value=element,
                    record_name=None,
                    element_record_name=None,
                ),
            )
            for element in elements
        ]
        return f"({', '.join(elem_types)})"

    @cached_property
    def _scala_tuple_renderer(self) -> TupleRenderer:
        """Scala syntax hooks for the ``TUPLE`` strategy.

        Tuple element types reuse :meth:`_scala_record_field_type`, so
        a tuple-eligible record field is typed exactly like the scalar
        positions it holds; only the tuple literal syntax is
        Scala-specific (Scala 3 has no tuple-length cap, so every
        eligible array is representable).
        """
        return TupleRenderer(
            render_literal=_scala_render_tuple_literal,
            field_type=self._scala_tuple_field_type,
            representable_arity=_scala_tuple_arity_representable,
        )

    @cached_property
    def _record_strategy(self) -> RecordStrategy:
        """Resolve the active strategy to its behavior + preamble.

        ``TUPLE`` composes ``RECORD``; both reuse
        :attr:`_record_renderer` so a tuple-eligible array that is a
        record field becomes a tuple-typed ``case class`` field.
        """
        cls = type(self.heterogeneous_strategy)
        if self.heterogeneous_strategy is cls.RECORD:
            return build_record_strategy(
                renderer=self._record_renderer,
                split_conflicting_field_types=False,
                widen_unrecordizable_nested_sibling_maps=True,
                derecordized_map_open="Map[String, Any](",
                allow_same_key_record_variants_in_sequences=False,
            )
        if self.heterogeneous_strategy is cls.TUPLE:
            return build_tuple_strategy(
                record_renderer=self._record_renderer,
                tuple_renderer=self._scala_tuple_renderer,
            )
        return RecordStrategy(
            behavior=NO_HETEROGENEOUS_BEHAVIOR,
            preamble=no_data_preamble,
        )

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        The ``RECORD`` strategy's ``case class`` declarations are not
        emitted here (file scope): Scala compiles every fixture
        together, so a file-scope ``case class Record0`` would collide
        across cases.  They are emitted into the per-fixture ``object``
        body instead; see :attr:`compute_body_preamble`.
        """
        return no_data_preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the behavior for the chosen heterogeneous strategy."""
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
        return _scala_call_stub

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
    def _date_type_name(self) -> str | None:
        """Scala type name for the configured date format."""
        return self._opener_config.type_name(
            py_type=self.date_format.value.type_produced,
        )

    @cached_property
    def _datetime_type_name(self) -> str | None:
        """Scala type name for the configured datetime format."""
        return self._opener_config.type_name(
            py_type=self.datetime_format.value.type_produced,
        )

    @cached_property
    def _openers(self) -> TypeOpeners:
        """Pre-built typed openers for sequence/set/dict literals."""
        return self._opener_config.build(
            date_type=self._date_type_name,
            datetime_type=self._datetime_type_name,
            set_opener_template=(
                self.set_format.value.set_opener_template or None
            ),
            narrow_dict_values=False,
            dict_key_type="",
        )

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        if self._json_type_active:
            return SequenceFormatConfig(
                sequence_open=fixed_open(open_str="Json.arr("),
                close=")",
                supports_heterogeneity=True,
                single_element_trailing_comma=False,
                supports_trailing_comma=True,
                empty_sequence="Json.arr()",
                preamble_lines=(),
                format_entry=_scala_circe_wrap_value,
                typed_opener_fallback=None,
                uses_typed_literal_for_scalars=False,
                requires_uniform_record_shapes=False,
                declared_type=_CIRCE_JSON_TYPE,
                narrowed_empty_form=None,
            )
        return self.sequence_format.value

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        if self._json_type_active:
            return SetFormatConfig(
                set_open=fixed_open(open_str="Json.arr("),
                close=")",
                empty_set="Json.arr()",
                preamble_lines=(),
                set_opener_template="",
                supports_heterogeneity=True,
                supports_trailing_comma=True,
            )
        return self.set_format.value.with_typed_opener(
            type_to_opener=self._openers.set,
            fallback=self.set_format.value.set_open([]),
        )

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence.

        Under the ``RECORD`` strategy (and ``TUPLE``, which composes
        it) a list whose elements are record-shaped dicts is opened
        with the format's plain, element-type-free opener (``List(``)
        so the elements render as ``RecordN(...)`` literals and Scala
        infers ``List[RecordN]``; the typed opener would otherwise
        infer a ``Map[String, ...]`` element type that the struct
        literals do not satisfy.
        """
        base = _resolve_sequence_open(
            cfg=self._opener_config,
            sequence_format=self.sequence_format,
            list_member=self.sequence_formats.LIST,
            fmt=self.sequence_format.value,
            openers=self._openers,
            date_type=self._date_type_name,
            datetime_type=self._datetime_type_name,
        )
        if self._json_type_active:
            return fixed_open(open_str="Json.arr(")
        cls = type(self.heterogeneous_strategy)
        if self.heterogeneous_strategy not in (cls.RECORD, cls.TUPLE):
            return base
        plain_open = self.sequence_format.value.sequence_open

        def _open(items: list[Value], /) -> str:
            """Use the plain opener for lists of record-shaped dicts.

            ``OrderedMap`` is never record-eligible, so an omap element
            keeps the typed opener.
            """
            if any(
                isinstance(item, dict) and not isinstance(item, OrderedMap)
                for item in items
            ):
                return plain_open(items)
            return base(items)

        return _open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        if self._json_type_active:
            return DictFormatConfig(
                dict_open=fixed_open(open_str="Json.obj("),
                narrowed_open=None,
                supports_trailing_comma=True,
                close=")",
                format_entry=dict_entry_with_separator(
                    separator=" -> ",
                    format_value=_scala_circe_wrap_value,
                ),
                empty_dict="Json.obj()",
                preamble_lines=(),
            )
        dict_spec: _ScalaDictSpec = self.dict_format.value
        return DictFormatConfig(
            dict_open=typed_dict_open(
                type_to_opener=make_type_to_opener(
                    element_to_type=self._opener_config.element_to_type(
                        list_template=(
                            "List[{inner}]"
                            if self.sequence_format
                            is self.sequence_formats.LIST
                            else None
                        ),
                        enable_list_type=True,
                        date_type=self._date_type_name,
                        datetime_type=self._datetime_type_name,
                        enable_dict_type=False,
                        dict_key_type="",
                    ),
                    opener_template=dict_spec.opener_template,
                ),
                fallback=dict_spec.fallback,
            ),
            narrowed_open=None,
            supports_trailing_comma=True,
            close=")",
            format_entry=dict_entry_with_separator(
                separator=" -> ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=dict_spec.preamble_lines,
        )

    @cached_property
    def trailing_comma_config(self) -> TrailingCommaConfig:
        """Configuration for trailing-comma behavior."""
        return self.trailing_comma.value

    @cached_property
    def format_bytes(self) -> Callable[[bytes], str]:
        """Callable that formats a bytes value as a string literal."""
        if self._json_type_active:
            return lambda value: format_bytes_hex(value=value)
        return self.bytes_format

    @cached_property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a date as a string literal."""
        if self._json_type_active:
            return format_date_iso
        return self.date_format

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal.

        ``EPOCH`` seconds are routed through :attr:`format_integer` so
        a post-2038 value carries the ``L`` suffix Scala requires for
        an integer literal outside 32-bit range: a bare ``4085195400``
        is rejected by the compiler as "number too large" even when
        the target type is ``Long``.  In-range epoch seconds format
        identically to the plain integer, so every checked-in golden
        file stays byte-identical.
        """
        if self._json_type_active:
            return format_datetime_iso
        if self.datetime_format.name == "EPOCH":
            return datetime_epoch_formatter(format_integer=self.format_integer)
        return self.datetime_format

    @cached_property
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        if self._json_type_active:
            return format_time_iso
        return format_time_local_time_of

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        return make_overflow_fallback_formatter(
            base=make_overflow_suffix_formatter(
                base=self.integer_format.get_formatter(
                    numeric_separator=self.numeric_separator,
                ),
                min_value=-(2**31),
                max_value=2**31 - 1,
                suffix="L",
            ),
            fallback=_format_scala_bigint_literal,
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
        if self._json_type_active:
            return OrderedMapFormatConfig(
                ordered_map_open=fixed_open(open_str="Json.obj("),
                close=")",
                preamble_lines=(),
            )
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(
                open_str="scala.collection.immutable.ListMap("
            ),
            close=")",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        if self._json_type_active:
            return dict_entry_with_separator(
                separator=" -> ",
                format_value=_scala_circe_wrap_value,
            )
        return dict_entry_with_separator(
            separator=" -> ",
            format_value=passthrough_sequence_entry,
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        if self._json_type_active:
            assert self.json_type is not None  # noqa: S101
            return _scala_circe_declaration_formatter(
                declaration_style=self.declaration_style,
                json_type_name="Json",
            )
        return self.declaration_style.value.formatter

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble computed from date/datetime format."""
        if self._json_type_active:
            return {}
        return date_scalar_preamble(
            date_format=self.date_format,
            datetime_format=self.datetime_format,
            extra={datetime.time: ("import java.time.LocalTime",)},
        )

    @cached_property
    def static_preamble(self) -> Sequence[str]:
        """Static preamble lines emitted once per file.

        Circe-backed Scala output needs ``io.circe.Json`` in scope so
        the ``Json.obj`` / ``Json.arr`` factories the rendered literal
        uses resolve.
        """
        if self._json_type_active:
            return ("import io.circe.Json",)
        return ()

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines from the scalar map, prefixed
        with the ``RECORD`` strategy's generated ``case class``
        declarations.

        Scala compiles every fixture in one invocation, so a
        file-scope ``case class Record0`` would collide across cases.
        Emitting the declarations into the body preamble (which
        :meth:`wrap_in_file` places inside the per-fixture ``object``,
        ahead of the value) scopes each ``RecordN`` to its own fixture;
        the declarations precede the scalar body lines so a record type
        is in scope before its literal.
        """
        scalar_body = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )
        if self._json_type_active:

            def _compute_circe(
                types: frozenset[type],
                data: Value,
                /,
            ) -> tuple[str, ...]:
                """Skip ``case class`` lines under Circe ``Json``."""
                return scalar_body(types, data)

            return _compute_circe
        record_preamble = self._record_strategy.preamble

        def _compute(
            types: frozenset[type],
            data: Value,
            /,
        ) -> tuple[str, ...]:
            """Record ``case class`` lines precede scalar body lines."""
            return record_preamble(data) + scalar_body(types, data)

        return _compute

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        config: CallStyle = self.call_style.value
        return config
