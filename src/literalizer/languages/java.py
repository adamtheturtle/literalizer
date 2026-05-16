"""Java language specification."""

import dataclasses
import datetime
import enum
import functools
from collections.abc import Callable, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import Any, ClassVar, assert_never

from beartype import beartype

from literalizer._formatters.collection_openers import (
    TypedOpenerConfig,
    fixed_open,
    typed_collection_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    datetime_epoch_formatter,
    datetime_epoch_seconds,
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
    format_time_local_time_of,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_template,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    I64_MAX,
    I64_MIN,
    data_has_out_of_range_int,
    format_integer_binary,
    format_integer_hex,
    format_integer_octal_c_style,
    format_integer_underscore,
    make_long_suffix_formatter,
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
from literalizer._formatters.type_inference import DictType, ListType
from literalizer._language import (
    NO_CALL_PARAMETER_LIMIT,
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
    LanguageCls,
    ModifierCombination,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    RenderedRecordLiteral,
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
    no_data_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    prepend_body_preamble,
)
from literalizer._types import OrderedMap, Scalar, Value
from literalizer.exceptions import (
    IncompatibleFormatsError,
    NullInCollectionError,
)


class _JavaModifiers(enum.Enum):
    """Declaration modifiers supported by Java.

    Each member's value is the Java keyword it renders to.  Declaration
    order matches canonical Java modifier order
    (visibility, storage, finality).

    Exposed as :attr:`Java.Modifiers` / :attr:`Java.modifiers`.
    """

    PUBLIC = "public"
    """Visibility: publicly accessible."""

    PRIVATE = "private"
    """Visibility: private to the enclosing class."""

    PROTECTED = "protected"
    """Visibility: protected (accessible from subclasses)."""

    STATIC = "static"
    """Storage: associated with the enclosing class rather than an
    instance.
    """

    FINAL = "final"
    """Immutability: cannot be reassigned."""


def _java_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Java stub declarations for a call name."""
    if len(parts) == 1:
        return (
            f"static Object {parts[0]}(Object... args) {{ return null; }}",
        )
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        type_name = f"{root.title()}Type_"
        return (
            f"static class {type_name} {{"
            f" Object {method}(Object... args) {{ return null; }} }}",
            f"static {type_name} {root} = new {type_name}();",
        )
    lines: list[str] = []
    inner_type = f"{fields[-1].title()}Type_"
    lines.append(
        f"static class {inner_type} {{"
        f" Object {method}(Object... args) {{ return null; }} }}"
    )
    prev_type = inner_type
    for i in range(len(fields) - 2, -1, -1):
        curr_type = f"{fields[i].title()}Type_"
        lines.append(
            f"static class {curr_type} {{"
            f" {prev_type} {fields[i + 1]} = new {prev_type}(); }}"
        )
        prev_type = curr_type
    root_type = f"{root.title()}Type_"
    lines.append(
        f"static class {root_type} {{"
        f" {prev_type} {fields[0]} = new {prev_type}(); }}"
    )
    lines.append(f"static {root_type} {root} = new {root_type}();")
    return tuple(lines)


@beartype
def _format_java_biginteger_literal(value: int) -> str:
    """Format a value outside signed 64-bit range as a Java
    ``new BigInteger(...)`` expression.

    Java's ``long`` is signed 64-bit; values outside that range must
    use ``java.math.BigInteger``.
    """
    return f'new BigInteger("{value}")'


@beartype
def _java_biginteger_preamble(data: Value, /) -> tuple[str, ...]:
    """Return ``import java.math.BigInteger;`` if *data* contains a
    very-large integer.
    """
    if data_has_out_of_range_int(data=data):
        return ("import java.math.BigInteger;",)
    return ()


@beartype
def _format_datetime_java_zoned(value: datetime.datetime) -> str:
    """Format a datetime as a Java ``ZonedDateTime.of(...)`` call."""
    timezone_name = value.tzname() or "UTC"
    nanoseconds = value.microsecond * 1000
    return (
        f"ZonedDateTime.of({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second}, "
        f'{nanoseconds}, ZoneId.of("{timezone_name}"))'
    )


@beartype
def _format_datetime_java_instant(value: datetime.datetime) -> str:
    """Format a datetime as a Java ``Instant.parse(...)`` call.

    ``Instant.parse`` rejects strings without a timezone offset, so a
    naive datetime (no :attr:`~datetime.datetime.tzinfo`) is rendered
    with a trailing ``Z`` — Python's :meth:`~datetime.datetime.isoformat`
    emits no offset for naive datetimes, which Java reads as invalid.
    Treating naive values as UTC matches the ISO 8601 convention for
    unqualified timestamps.
    """
    iso = value.isoformat()
    if value.tzinfo is None:
        iso += "Z"
    return f'Instant.parse("{iso}")'


@beartype
def _list_of_open(items: list[Any]) -> str:
    """Return ``List.of(`` after checking for null elements.

    Java's ``List.of()`` throws ``NullPointerException`` on null elements.
    """
    if any(item is None for item in items):
        msg = (
            f"Java's List.of() does not accept null elements"
            f" (got {len(items)} items, including null). "
            "Use sequence_format=ARRAY instead."
        )
        raise NullInCollectionError(msg)
    return "List.of("


@beartype
def _java_box(type_name: str) -> str:
    """Return the boxed wrapper type for a Java primitive, or the type
    itself for reference types.
    """
    match type_name:
        case "boolean":
            return "Boolean"
        case "int":
            return "Integer"
        case "long":
            return "Long"
        case "double":
            return "Double"
        case _:
            return type_name


@beartype
def _java_common_element_type(
    *,
    elements: list[Value],
    boxed: bool,
    int_type: str,
    date_hint: str,
    datetime_hint: str,
    seq_is_array: bool,
    dict_outer: str,
    set_outer: str,
) -> str:
    """Find the common Java type for a collection's elements.

    Returns ``"Object"`` when elements are empty or have mixed types.
    """
    if not elements:
        return "Object"
    recurse = functools.partial(
        _java_type_hint,
        int_type=int_type,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        seq_is_array=seq_is_array,
        dict_outer=dict_outer,
        set_outer=set_outer,
    )
    types: list[str] = [recurse(data=e) for e in elements]
    unique = set(types)
    if len(unique) == 1:
        result = unique.pop()
        return _java_box(type_name=result) if boxed else result
    # int + double → double (widening)
    double_t = "double"
    if unique == {int_type, double_t}:
        return "Double" if boxed else "double"
    # int + long → long (integer-width widening for mixed-magnitude
    # int collections, e.g. ``{1, 1099511627776}``)
    if unique == {"int", "long"}:
        return "Long" if boxed else "long"
    return "Object"


_JAVA_I32_MIN = -(2**31)
_JAVA_I32_MAX = 2**31 - 1


@beartype
def _java_scalar_hint(  # pylint: disable=too-complex
    *,
    data: Scalar,
    int_type: str,
    date_hint: str,
    datetime_hint: str,
) -> str:
    """Derive the Java annotation for a scalar value."""
    match data:
        case bool():
            hint = "boolean"
        case int():
            if int_type == "int" and not (
                _JAVA_I32_MIN <= data <= _JAVA_I32_MAX
            ):
                hint = "long"
            else:
                hint = int_type
        case float():
            hint = "double"
        case str() | bytes():
            hint = "String"
        case datetime.datetime():
            hint = datetime_hint
        case datetime.date():
            hint = date_hint
        case datetime.time():
            hint = "LocalTime"
        case None:
            hint = "Object"
        case _ as unreachable:
            assert_never(unreachable)
    return hint


@beartype
def _java_type_hint(
    *,
    data: Value,
    int_type: str,
    date_hint: str,
    datetime_hint: str,
    seq_is_array: bool,
    dict_outer: str,
    set_outer: str,
) -> str:
    """Derive a Java type from *data*."""
    common = functools.partial(
        _java_common_element_type,
        int_type=int_type,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        seq_is_array=seq_is_array,
        dict_outer=dict_outer,
        set_outer=set_outer,
    )
    match data:
        case dict():
            val_type = common(elements=list(data.values()), boxed=True)
            outer = "Map" if isinstance(data, OrderedMap) else dict_outer
            hint = f"{outer}<String, {val_type}>"
        case set():
            elem_type = common(elements=list(data), boxed=True)
            hint = f"{set_outer}<{elem_type}>"
        case list() if seq_is_array:
            elem_type = common(elements=data, boxed=False)
            # Java cannot create arrays of generic types, so fall back
            # to Object[] when the element type is generic.
            if "<" in elem_type:
                elem_type = "Object"
            hint = f"{elem_type}[]"
        case list():
            elem_type = common(elements=data, boxed=True)
            hint = f"List<{elem_type}>"
        case _:
            hint = _java_scalar_hint(
                data=data,
                int_type=int_type,
                date_hint=date_hint,
                datetime_hint=datetime_hint,
            )
    return hint


@beartype
def _java_modifier_prefix(modifiers: frozenset[enum.Enum]) -> str:
    """Return the ``public static final `` prefix for a Java
    declaration, including a trailing space when non-empty.

    Values that are not :class:`_JavaModifiers` members are ignored.
    """
    keywords = [m.value for m in _JavaModifiers if m in modifiers]
    if not keywords:
        return ""
    return " ".join(keywords) + " "


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class _JavaTerminatedValue:
    r"""A Java value rewritten so a terminating ``;`` lands on the code
    line, not on a trailing ``//`` line comment.

    Attributes:
        code: The portion of the original value preceding any trailing
            ``//`` line comments.  The terminating ``;`` is appended
            here.
        trailing: The trailing ``//`` line comments (including the
            leading ``\n`` separator) that follow the terminator.  Empty
            when the value did not end with a line comment.
    """

    code: str
    trailing: str


@beartype
def _java_split_trailing_line_comments(value: str) -> _JavaTerminatedValue:
    """Split *value* at the boundary before any trailing ``//`` line
    comments so a terminating ``;`` can be placed on the code line
    rather than inside the comment.
    """
    lines = value.split(sep="\n")
    split_index = next(
        (
            index + 1
            for index, line in reversed(list(enumerate(iterable=lines)))
            if not line.lstrip().startswith("//")
        ),
        0,
    )
    if split_index == len(lines):
        return _JavaTerminatedValue(code=value, trailing="")
    code = "\n".join(lines[:split_index])
    trailing = "\n" + "\n".join(lines[split_index:])
    return _JavaTerminatedValue(code=code, trailing=trailing)


@beartype
def _format_java_var_declaration(
    name: str,
    value: str,
    _data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a ``var`` declaration, terminating before any trailing
    ``//`` line comment in *value*.
    """
    terminated = _java_split_trailing_line_comments(value=value)
    return f"var {name} = {terminated.code};{terminated.trailing}"


@beartype
def _format_java_assignment(
    name: str,
    value: str,
    _data: Value,
) -> str:
    """Format a Java assignment, terminating before any trailing ``//``
    line comment in *value*.
    """
    terminated = _java_split_trailing_line_comments(value=value)
    return f"{name} = {terminated.code};{terminated.trailing}"


@beartype
def _java_inference_widens_unsafely(*, data: Value) -> bool:
    """Return True if Java ``var`` inference for *data* would widen to a
    permissive type (e.g. ``Object[]`` for ``new Object[]{}``).

    Empty collection literals trigger this fallback in
    :func:`_java_common_element_type`, so they are the canonical case
    for which a ``SAFE`` annotation is preferable to inference.
    """
    match data:
        case list() | set() | dict():
            return not data
        case _:
            return False


@beartype
def _format_java_typed_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    modifiers: frozenset[enum.Enum],
    int_type: str,
    date_hint: str,
    datetime_hint: str,
    seq_is_array: bool,
    dict_outer: str,
    set_outer: str,
) -> str:
    """Format a Java variable declaration with an explicit type."""
    hint = _java_type_hint(
        data=data,
        int_type=int_type,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        seq_is_array=seq_is_array,
        dict_outer=dict_outer,
        set_outer=set_outer,
    )
    prefix = _java_modifier_prefix(modifiers=modifiers)
    terminated = _java_split_trailing_line_comments(value=value)
    return f"{prefix}{hint} {name} = {terminated.code};{terminated.trailing}"


@beartype
def _apply_java_object_nil_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    modifiers: frozenset[enum.Enum],
    base_formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
    typed_formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
) -> str:
    """Format a Java variable declaration, guarding top-level ``null``
    and switching to the typed form whenever modifiers are present.
    """
    if modifiers:
        return typed_formatter(name, value, data, modifiers)
    if data is None:
        terminated = _java_split_trailing_line_comments(value=value)
        return f"Object {name} = {terminated.code};{terminated.trailing}"
    return base_formatter(name, value, data, modifiers)


@beartype
def _object_nil_declaration(
    *,
    base_formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
    typed_formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
    """Wrap *base_formatter* so top-level ``null`` gets a typed form.

    Java cannot infer a type from ``null``, so ``var {name} = null;``
    fails to compile.  Emit ``Object {name} = null;`` when the value is
    ``None``.  Modifiers force the typed form because Java class-field
    syntax (e.g. ``public static final``) cannot be combined with
    ``var``.
    """

    def _format(
        name: str,
        value: str,
        data: Value,
        modifiers: frozenset[enum.Enum],
    ) -> str:
        """Delegate to module-level implementation."""
        return _apply_java_object_nil_declaration(
            name=name,
            value=value,
            data=data,
            modifiers=modifiers,
            base_formatter=base_formatter,
            typed_formatter=typed_formatter,
        )

    return _format


@beartype
def _java_record_field_identifier(key: str, /) -> str:
    """Return the Java record component name for a dict *key*.

    Java record components keep the original key (identity); the
    literal is positional so the name only labels the declaration.
    """
    return key


@beartype
def _java_record_literal(
    name: str,
    fields: Sequence[RecordLiteralField],
    /,
) -> RenderedRecordLiteral:
    """Render a Java ``new Name(value, ...)`` positional record literal
    as structured pieces for the shared compact/multiline layout code.

    Java records are positional, so the field identifiers label only
    the declaration; the literal emits arguments in declaration order
    with no field names.
    """
    return RenderedRecordLiteral(
        head=f"new {name}(",
        entries=tuple(field.formatted for field in fields),
        closer=")",
        compact_pad="",
    )


@beartype
def _java_render_declaration(
    name: str,
    fields: Sequence[RecordDeclarationField],
    /,
) -> str:
    """Render a Java ``record Name(type id, ...) {}`` declaration."""
    components = ", ".join(
        f"{field.type_name} {field.identifier}" for field in fields
    )
    return f"record {name}({components}) {{}}"


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Java(metaclass=LanguageCls):
    """Java language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.JAVA`` — ``LocalDate.of(...)`` call,
              e.g. ``LocalDate.of(2024, 1, 15)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.INSTANT`` — ``Instant.parse(...)`` call,
              e.g. ``Instant.parse("2024-01-15T12:30:00")``.
            * ``datetime_formats.ZONED`` — ``ZonedDateTime.of(...)`` call,
              e.g. ``ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0,
              ZoneId.of("UTC"))``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.

        sequence_format: How to format sequences.

            * ``sequence_formats.ARRAY`` — Java array literal,
              e.g. ``new Object[]{1, 2, 3}``.
            * ``sequence_formats.LIST`` — ``List.of(...)`` call,
              e.g. ``List.of(1, 2, 3)``.
    """

    module_name: str = "Module"

    extension = ".java"
    pygments_name = "java"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    supports_call_variable_binding = True
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
    supports_module_name = True
    supports_empty_dict_key = False
    supports_call_style = True
    supports_default_dict_key_type = False
    supports_default_dict_value_type = False
    supports_default_sequence_element_type = False
    supports_default_set_element_type = False
    supports_default_ordered_map_value_type = False
    supports_record_struct_name_prefix = True
    supports_record_shape_names = False
    supports_non_string_dict_keys = True

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

    _opener_config = TypedOpenerConfig(
        str_type="String",
        bool_type="boolean",
        int_type="int",
        float_type="double",
        mixed_numeric_type="double",
        bytes_type="String",
        date_type="LocalDate",
        datetime_type=None,
        time_type="LocalTime",
        list_template="{inner}[]",
        sequence_opener_template="new {type_name}[]{{",
        dict_opener_template="new {type_name}[]{{",
        set_opener_template="Set.of(",
        dict_type_template=None,
        fallback_value_type=None,
    )

    _opener_config_long = TypedOpenerConfig(
        str_type="String",
        bool_type="boolean",
        int_type="long",
        float_type="double",
        mixed_numeric_type="double",
        bytes_type="String",
        date_type="LocalDate",
        datetime_type=None,
        time_type="LocalTime",
        list_template="{inner}[]",
        sequence_opener_template="new {type_name}[]{{",
        dict_opener_template="new {type_name}[]{{",
        set_opener_template="Set.of(",
        dict_type_template=None,
        fallback_value_type=None,
    )

    class DateFormats(enum.Enum):
        """Date formatting options for Java."""

        JAVA = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="LocalDate.of({year}, {month}, {day})",
            ),
            preamble_lines=("import java.time.LocalDate;",),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime formatting options for Java."""

        INSTANT = DatetimeFormatConfig(
            formatter=_format_datetime_java_instant,
            preamble_lines=("import java.time.Instant;",),
        )
        ZONED = DatetimeFormatConfig(
            formatter=_format_datetime_java_zoned,
            preamble_lines=(
                "import java.time.ZoneId;",
                "import java.time.ZonedDateTime;",
            ),
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
        """Sequence type options for Java."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="new Object[]{"),
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback="new Object[]{",
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )
        LIST = SequenceFormatConfig(
            sequence_open=_list_of_open,
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=False,
            empty_sequence="List.of()",
            preamble_lines=("import java.util.List;",),
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Java."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="Set.of("),
            close=")",
            empty_set=None,
            preamble_lines=("import java.util.Set;",),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=False,
        )
        TREE_SET = SetFormatConfig(
            set_open=fixed_open(open_str="new TreeSet<>(Set.of("),
            close="))",
            empty_set="new TreeSet<>()",
            preamble_lines=(
                "import java.util.Set;",
                "import java.util.TreeSet;",
            ),
            set_opener_template="",
            supports_heterogeneity=False,
            supports_trailing_comma=False,
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

        VAR = DeclarationStyleConfig(
            formatter=_format_java_var_declaration,
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        MAP_OF_ENTRIES = DictFormatConfig(
            dict_open=fixed_open(open_str="Map.ofEntries("),
            close=")",
            format_entry=dict_entry_with_template(
                template="Map.entry({key}, {value})",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=("import java.util.Map;",),
            narrowed_open=None,
            supports_trailing_comma=False,
        )
        HASH_MAP = DictFormatConfig(
            dict_open=fixed_open(open_str="new HashMap<>(Map.ofEntries("),
            close="))",
            format_entry=dict_entry_with_template(
                template="Map.entry({key}, {value})",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict="new HashMap<>()",
            preamble_lines=(
                "import java.util.HashMap;",
                "import java.util.Map;",
            ),
            narrowed_open=None,
            supports_trailing_comma=False,
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
        OCTAL = MappingProxyType(
            mapping={
                "NONE": format_integer_octal_c_style,
                "UNDERSCORE": format_integer_octal_c_style,
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
        AUTO = enum.auto()

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

    Modifiers = _JavaModifiers

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats
    modifiers = _JavaModifiers

    class HeterogeneousStrategies(enum.Enum):
        """Strategy for dicts whose values span more than one Java type.

        ``ERROR`` keeps Java's strict-typing behavior (mixed-value dicts
        that cannot be represented raise).  ``RECORD`` renders each
        record-shaped dict (non-empty, string-keyed) as a generated
        ``record`` declared in the preamble plus a matching positional
        ``new Record0(...)`` literal, so fields may legitimately mix
        scalars and containers.
        """

        ERROR = enum.auto()
        RECORD = enum.auto()

    heterogeneous_strategies = HeterogeneousStrategies

    class VersionFormats(enum.Enum):
        """Version options for Java.

        * ``VersionFormats.JDK_11``: target Java 11.
        * ``VersionFormats.JDK_16``: target Java 16.

        The ``RECORD`` ``heterogeneous_strategy`` emits ``record``
        declarations, which require Java 16 or newer, so a
        ``RECORD`` spec pins ``language_version`` to ``JDK_16``.
        """

        JDK_11 = enum.auto()
        JDK_16 = enum.auto()

    version_formats = VersionFormats

    module_name_case: ClassVar[IdentifierCase] = IdentifierCase.PASCAL
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.CAMEL,
        IdentifierCase.PASCAL,
        IdentifierCase.UPPER_SNAKE,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = (
        ModifierCombination(
            name="public_static_final",
            modifiers=frozenset(
                {
                    _JavaModifiers.PUBLIC,
                    _JavaModifiers.STATIC,
                    _JavaModifiers.FINAL,
                },
            ),
        ),
    )

    def __post_init__(self) -> None:
        """Pin ``language_version`` to ``JDK_16`` for the ``RECORD``
        strategy.

        The ``RECORD`` ``heterogeneous_strategy`` emits ``record``
        declarations, which require Java 16; ``JDK_11`` output would
        fail to compile.  Coercing here (rather than rejecting a
        ``JDK_11`` + ``RECORD`` spec) keeps the golden harness simple:
        every ``RECORD`` spec, however constructed, renders and is
        tagged ``@jdk_16``.
        """
        jdk_16 = self.version_formats.JDK_16
        if (
            self.heterogeneous_strategy is self.heterogeneous_strategies.RECORD
            and self.language_version is not jdk_16
        ):
            object.__setattr__(self, "language_version", jdk_16)

    def validate_spec_for_data(self, data: Value) -> None:
        """Raise if the spec cannot produce valid code for *data*.

        Under the ``RECORD`` heterogeneous strategy a list-valued
        record component is typed from the array opener
        (``new <type>[]{``) the value formatter emits, so its declared
        type matches the rendered literal.  Only
        ``sequence_format=ARRAY`` produces that opener; every other
        sequence format (e.g. ``LIST`` -> ``List.of(...)``) carries no
        element type in its opener and is outside the ``RECORD``
        strategy's MVP (cf. the set / non-record-dict boundary in
        #2317), so the combination is rejected here rather than
        emitting a ``record`` declaration that fails to compile.  This
        check is spec-only; *data* is unused.
        """
        del data
        strategies = type(self.heterogeneous_strategy)
        formats = type(self.sequence_format)
        if (
            self.heterogeneous_strategy is strategies.RECORD
            and self.sequence_format is not formats.ARRAY
        ):
            msg = (
                "Java heterogeneous_strategy=RECORD requires "
                "sequence_format=ARRAY: a list-valued record component "
                "is typed from the array opener the value formatter "
                "emits, and other sequence formats (e.g. LIST -> "
                "List.of(...)) carry no element type. "
                "Use sequence_format=ARRAY."
            )
            raise IncompatibleFormatsError(msg)

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
        ALWAYS = enum.auto()
        SAFE = enum.auto()

        def formatter(
            self,
            *,
            auto_formatter: Callable[
                [str, str, Value, frozenset[enum.Enum]], str
            ],
            int_type: str,
            date_hint: str,
            datetime_hint: str,
            seq_is_array: bool,
            dict_outer: str,
            set_outer: str,
        ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
            """Return the variable declaration formatter."""

            def typed(
                name: str,
                value: str,
                data: Value,
                modifiers: frozenset[enum.Enum],
            ) -> str:
                """Adapt :func:`_format_java_typed_declaration` to the
                positional formatter interface.
                """
                return _format_java_typed_declaration(
                    name=name,
                    value=value,
                    data=data,
                    modifiers=modifiers,
                    int_type=int_type,
                    date_hint=date_hint,
                    datetime_hint=datetime_hint,
                    seq_is_array=seq_is_array,
                    dict_outer=dict_outer,
                    set_outer=set_outer,
                )

            if self is type(self).NEVER:
                return _object_nil_declaration(
                    base_formatter=auto_formatter,
                    typed_formatter=typed,
                )
            if self.name == "SAFE":
                auto_with_nil = _object_nil_declaration(
                    base_formatter=auto_formatter,
                    typed_formatter=typed,
                )

                def _safe_formatter(
                    name: str,
                    value: str,
                    data: Value,
                    modifiers: frozenset[enum.Enum],
                ) -> str:
                    """Annotate when inference would widen unsafely
                    (empty collection).
                    """
                    if _java_inference_widens_unsafely(data=data):
                        return typed(
                            name=name,
                            value=value,
                            data=data,
                            modifiers=modifiers,
                        )
                    return auto_with_nil(name, value, data, modifiers)

                return _safe_formatter
            return typed

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
        """Java call style options."""

        POSITIONAL = PositionalCallStyle()

    call_styles = CallStyles

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a Java declaration in a ``class`` scope named after
        the configured module name.

        When *content* starts with a class-field modifier keyword
        (``public``, ``private``, ``protected``, ``static``) the
        declaration is placed at class-field scope, which is the only
        context where those modifiers are valid.  Otherwise the
        declaration goes inside a ``public static void`` method named
        after the configured module name so that local-only forms like
        ``var x = 42;`` compile.
        """
        del variable_name
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
        }
        # Lines starting with "static " are class-level declarations
        # (call stubs); everything else goes inside the method body.
        class_lines = [
            line for line in body_preamble if line.startswith("static ")
        ]
        method_lines = tuple(
            line for line in body_preamble if not line.startswith("static ")
        )
        class_block = "\n".join(class_lines) + "\n" if class_lines else ""
        method_name = IdentifierCase.CAMEL.convert(name=self.module_name)
        if is_class_field:
            field_preamble = (
                "\n".join(method_lines) + "\n" if method_lines else ""
            )
            return (
                f"class {self.module_name} {{\n"
                f"{class_block}{field_preamble}{content}\n}}"
            )
        content = prepend_body_preamble(
            content=content,
            body_preamble=method_lines,
        )
        return (
            f"class {self.module_name} {{\n"
            f"{class_block}"
            f"{self.indent}public static void {method_name}() {{\n"
            f"{content}\n"
            f"{self.indent}}}\n"
            "}"
        )

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Java declaration + assignment in a static method."""
        return self.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.JAVA
    datetime_format: DatetimeFormats = DatetimeFormats.INSTANT
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.VAR
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.MAP_OF_ENTRIES
    float_format: FloatFormats = FloatFormats.REPR
    integer_format: IntegerFormats = IntegerFormats.DECIMAL
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
    # The `Lint Java` step in `.github/workflows/lint.yml` compiles each
    # `@jdk_<release>` golden with the `--release` literal matching its
    # `VersionFormats` member (`11` for `JDK_11`, `16` for `JDK_16`).
    # Keep those literals in sync with `VersionFormats` above.
    language_version: VersionFormats = VersionFormats.JDK_11
    record_struct_name_prefix: str = "Record"
    indent: str = "    "

    null_literal: ClassVar[str] = "null"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = True
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ";"
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

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
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        return _format_java_assignment

    @cached_property
    def _java_record_int_type(self) -> str:
        """Java integer type for a record-component scalar."""
        return "long" if self._suffix_is_auto else "int"

    def _java_record_datetime_type(self, value: datetime.datetime, /) -> str:
        """Java type for a :class:`datetime.datetime` record component.

        Unlike a top-level variable annotation, a record component must
        match the literal :meth:`format_datetime` emits.  ``ISO``
        renders a quoted string (``String``); ``EPOCH`` renders the
        epoch seconds through :attr:`format_integer`, which appends an
        ``L`` (so the type is ``long``) once the value leaves Java's
        32-bit ``int`` range -- epoch seconds after 2038-01-19 overflow
        it.  The component type therefore reuses the exact plain
        ``int`` record-field formula (``AUTO`` suffix forces ``long``
        for every epoch); it stays value-driven rather than a pure
        ``cached_property``.  Otherwise the type is format-driven
        (``ZonedDateTime`` / ``Instant``).
        """
        produced = self.datetime_format.value.type_produced
        if produced is str:
            return "String"
        if produced is int:
            epoch = datetime_epoch_seconds(value=value)
            int_type = self._java_record_int_type
            in_i32 = _JAVA_I32_MIN <= epoch <= _JAVA_I32_MAX
            return "long" if int_type == "int" and not in_i32 else int_type
        if self.datetime_format.name == "ZONED":
            return "ZonedDateTime"
        return "Instant"

    @cached_property
    def _java_record_scalar_resolver(
        self,
    ) -> Callable[[type | ListType | DictType], str | None]:
        """Type-only scalar resolver (the mapping the typed openers are
        built on); returns ``None`` for an unmapped type so callers can
        fall back to the top type.
        """
        return self._opener_config.element_to_type(
            list_template=None,
            enable_list_type=False,
            date_type=None,
            datetime_type=None,
            enable_dict_type=False,
        )

    def _java_record_field_type(  # noqa: PLR0911
        self,
        request: RecordFieldType,
        /,
    ) -> str:
        """Return the Java record-component type for a field.

        Derives the type from the raw value (and any resolved
        nested-record name), mirroring Go's structural port rather than
        re-parsing the formatted literal.  ``int`` magnitude (``int``
        vs ``long``) and the format-dependent ``datetime`` type
        (``Instant`` / ``ZonedDateTime`` / ``String`` / magnitude-aware
        epoch ``int`` or ``long``) are value- and spec-driven, so they
        are resolved explicitly;
        every other scalar (including ``date`` -> ``LocalDate``) goes
        through the shared type-only resolver.

        An ordered-map field is the concrete ``java.util.ArrayList``
        the ordered-map opener constructs.  A list field is typed from
        the array opener ``self.sequence_open`` emits for it (no
        sibling override, so the opener equals the one rendered):
        ``new int[]{`` -> ``int[]``, ``new Object[]{`` -> ``Object[]``.
        Only ``sequence_format=ARRAY`` produces that opener;
        :meth:`validate_spec_for_data` rejects ``RECORD`` with any
        other sequence format up front, so no opener without an
        encoded element type (e.g. ``List.of(``) reaches this branch.

        A set or a non-record dict (an empty or non-string-keyed dict)
        as a record field is outside the ``RECORD`` strategy's MVP --
        the same shapes Rust's ``_rust_record_field_type`` is imprecise
        for (#2317) -- so it folds into the ``Object`` top type, which
        the rendered literal still assigns into.
        """
        if request.record_name is not None:
            return request.record_name
        value = request.value
        int_type = self._java_record_int_type
        match value:
            case bool():
                return "boolean"
            case int() if not I64_MIN <= value <= I64_MAX:
                return "BigInteger"
            case int():
                in_i32 = _JAVA_I32_MIN <= value <= _JAVA_I32_MAX
                return "long" if int_type == "int" and not in_i32 else int_type
            case datetime.datetime():
                return self._java_record_datetime_type(value)
            case OrderedMap():
                field_type = "java.util.ArrayList"
            case list():
                opener = self.sequence_open(value)
                field_type = opener.removeprefix("new ").removesuffix("{")
            case _:
                return self._java_record_scalar_resolver(type(value)) or (
                    "Object"
                )
        return field_type

    @cached_property
    def _record_renderer(self) -> RecordRenderer:
        """Java syntax hooks for the ``RECORD`` strategy."""
        return RecordRenderer(
            name_prefix=self.record_struct_name_prefix,
            # Java does not yet expose a ``record_shape_names``
            # constructor field (ported with its own RECORD work); an
            # empty mapping keeps every shape on the auto
            # ``{prefix}{N}`` names.
            record_shape_names=MappingProxyType(mapping={}),
            field_identifier=_java_record_field_identifier,
            field_type=self._java_record_field_type,
            render_declaration=_java_render_declaration,
            render_literal=_java_record_literal,
        )

    @cached_property
    def _record_strategy(self) -> RecordStrategy:
        """Resolve the active strategy to its behavior + preamble."""
        cls = type(self.heterogeneous_strategy)
        if self.heterogeneous_strategy is cls.RECORD:
            return build_record_strategy(renderer=self._record_renderer)
        return RecordStrategy(
            behavior=NO_HETEROGENEOUS_BEHAVIOR,
            preamble=no_data_preamble,
        )

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        Always emits ``import java.math.BigInteger;`` when the data
        needs it; under ``HeterogeneousStrategies.RECORD`` also emits
        one ``record`` declaration per record shape present in the
        data.
        """
        record_preamble = self._record_strategy.preamble

        @beartype
        def _preamble(data: Value, /) -> tuple[str, ...]:
            """Combine the BigInteger import with record declarations."""
            return _java_biginteger_preamble(data) + record_preamble(data)

        return _preamble

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
        return _java_call_stub

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
    def _suffix_is_auto(self) -> bool:
        """Whether the numeric-literal suffix is AUTO (long suffix)."""
        return self.numeric_literal_suffix.name == "AUTO"

    @cached_property
    def _java_dict_entry(self) -> Callable[[str, Value, str], str]:
        """Shared dict-entry formatter used by dict and ordered-map."""
        return dict_entry_with_template(
            template="Map.entry({key}, {value})",
            format_value=passthrough_sequence_entry,
        )

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
        fmt = self.sequence_format.value
        if fmt.typed_opener_fallback is None:
            return fmt.sequence_open
        cfg = (
            self._opener_config_long
            if self._suffix_is_auto
            else self._opener_config
        )
        openers = cfg.build(
            date_type=cfg.type_name(
                py_type=self.date_format.value.type_produced
            ),
            datetime_type=(
                "long"
                if self.datetime_format.value.type_produced is int
                else cfg.type_name(
                    py_type=self.datetime_format.value.type_produced,
                )
            ),
            set_opener_template=None,
            narrow_dict_values=False,
        )
        return typed_collection_open(
            type_to_opener=openers.seq,
            fallback=fmt.typed_opener_fallback,
        )

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return self.dict_format.value

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
        a post-2038 value carries the ``L`` suffix Java requires for an
        integer literal outside 32-bit range: a bare ``4085195400``
        fails to compile as an ``int`` literal even when assigned to a
        ``long``.  In-range epoch seconds format identically to the
        plain integer, so every checked-in golden file stays
        byte-identical.
        """
        if self.datetime_format.name == "EPOCH":
            return datetime_epoch_formatter(format_integer=self.format_integer)
        return self.datetime_format

    @cached_property
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        return format_time_local_time_of

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer_widened(self) -> Callable[[int], str]:
        """Always-``L``-suffixed integer formatter for widened
        collections (mixed-magnitude int sets/lists).
        """
        base_int_formatter = self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )
        return make_overflow_fallback_formatter(
            base=make_long_suffix_formatter(base=base_int_formatter),
            fallback=_format_java_biginteger_literal,
        )

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        base_int_formatter = self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )
        suffixed: Callable[[int], str] = (
            make_long_suffix_formatter(base=base_int_formatter)
            if self._suffix_is_auto
            else make_overflow_suffix_formatter(
                base=base_int_formatter,
                min_value=-(2**31),
                max_value=2**31 - 1,
                suffix="L",
            )
        )
        return make_overflow_fallback_formatter(
            base=suffixed,
            fallback=_format_java_biginteger_literal,
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
                    "new java.util.ArrayList<>(java.util.Arrays.asList("
                ),
            ),
            close="))",
            preamble_lines=("import java.util.Map;",),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return self._java_dict_entry

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        datetime_produced = self.datetime_format.value.type_produced
        if datetime_produced is str:
            datetime_hint = "String"
        elif datetime_produced is int:
            datetime_hint = "long"
        elif self.datetime_format.name == "ZONED":
            datetime_hint = "ZonedDateTime"
        else:
            datetime_hint = "Instant"
        return self.variable_type_hints.formatter(
            auto_formatter=self.declaration_style.value.formatter,
            int_type="long" if self._suffix_is_auto else "int",
            date_hint=(
                "String"
                if self.date_format.value.type_produced is str
                else "LocalDate"
            ),
            datetime_hint=datetime_hint,
            seq_is_array=(self.sequence_format.name == "ARRAY"),
            dict_outer=(
                "HashMap" if self.dict_format.name == "HASH_MAP" else "Map"
            ),
            set_outer=(
                "TreeSet" if self.set_format.name == "TREE_SET" else "Set"
            ),
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble computed from date/datetime format."""
        return date_scalar_preamble(
            date_format=self.date_format,
            datetime_format=self.datetime_format,
            extra={datetime.time: ("import java.time.LocalTime;",)},
        )

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Java needs none)."""
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
        return self.call_style.value
