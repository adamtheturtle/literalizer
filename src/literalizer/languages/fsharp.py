"""F# language specification."""

import dataclasses
import datetime
import enum
import textwrap
from collections.abc import Callable, Sequence
from functools import cached_property
from typing import ClassVar

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
    format_time_fsharp,
    format_time_iso,
)
from literalizer._formatters.format_entries import (
    declaration_formatter_ignoring_modifiers,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    tuple_dict_entry,
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
    U64_MAX,
    data_has_out_of_range_int,
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    make_overflow_suffix_formatter,
)
from literalizer._formatters.format_strings import format_string_backslash
from literalizer._language import (
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
    BareIntegerWidthStrategies,
    CallStyle,
    CommandCallStyle,
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
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
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
    no_data_preamble,
    no_format_integer_widened,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    prepend_body_preamble,
)
from literalizer._types import OrderedMap, Value
from literalizer.exceptions import (
    UnrepresentableInputError,
    UnrepresentableIntegerError,
)


@beartype
def _apply_fsharp_entry(original: Value, formatted: str, prefix: str) -> str:
    """Wrap a formatted entry in the appropriate F# ``Val``
    constructor.
    """
    match original:
        case bool():
            return formatted
        case int():
            negative = formatted.startswith("-")
            # ``format_integer`` already appends the ``I`` suffix for
            # values outside the signed 64-bit range; here we only add
            # the ``L`` suffix for in-range ``int64`` values.
            literal = (
                f"{formatted}L"
                if I64_MIN <= original <= I64_MAX
                else formatted
            )
            return (
                f"{prefix}Int({literal})"
                if negative
                else f"{prefix}Int {literal}"
            )
        case float():
            negative = formatted.startswith("-")
            return (
                f"{prefix}Float({formatted})"
                if negative
                else f"{prefix}Float {formatted}"
            )
        case datetime.datetime() if formatted.startswith(f"{prefix}Int"):
            return formatted
        case str() | bytes() | datetime.date() | datetime.time():
            return (
                f"{prefix}Str (string ({formatted}))"
                if formatted.startswith("System.")
                else f"{prefix}Str {formatted}"
            )
        case _:
            return formatted


@beartype
def _build_fsharp_entry_formatter(
    prefix: str,
) -> Callable[[Value, str], str]:
    """Build an entry formatter that wraps values in F# constructors."""

    def _format(original: Value, formatted: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_fsharp_entry(
            original=original, formatted=formatted, prefix=prefix
        )

    return _format


_format_fsharp_entry = _build_fsharp_entry_formatter(prefix="F")


_FSHARP_JSON_USING = "open System.Text.Json.Nodes"
_FSHARP_JSON_OBJECT_OPEN = "JsonObject(dict ["
_FSHARP_JSON_OBJECT_CLOSE = "])"
_FSHARP_JSON_ARRAY_OPEN = "JsonArray([|"
_FSHARP_JSON_ARRAY_CLOSE = "|])"
_FSHARP_JSON_EMPTY_OBJECT = "JsonObject()"
_FSHARP_JSON_EMPTY_ARRAY = "JsonArray()"


@beartype
def _fsharp_json_wrap(formatted: str) -> str:
    """Coerce a rendered F# expression to the ``JsonNode`` base class.

    ``JsonObject`` / ``JsonArray`` literals and ``null`` are already
    valid ``JsonNode`` expressions; a scalar literal is wrapped in
    ``JsonValue.Create`` first so it becomes a ``JsonValue`` (a class
    that derives from ``JsonNode``) before the cast.  An explicit
    ``:> JsonNode`` cast is added in every case so heterogeneous
    collections type-infer as ``IDictionary<string, JsonNode>`` /
    ``JsonNode array``.
    """
    if formatted.startswith(
        (
            _FSHARP_JSON_OBJECT_OPEN,
            _FSHARP_JSON_ARRAY_OPEN,
            _FSHARP_JSON_EMPTY_OBJECT,
            _FSHARP_JSON_EMPTY_ARRAY,
        )
    ):
        return f"({formatted} :> JsonNode)"
    if formatted == "null":
        return "(null :> JsonNode)"
    return f"(JsonValue.Create({formatted}) :> JsonNode)"


@beartype
def _format_fsharp_json_entry(_original: Value, formatted: str) -> str:
    """Wrap a sequence / set / dict entry for ``JsonArray`` /
    ``JsonObject``.
    """
    return _fsharp_json_wrap(formatted=formatted)


@beartype
def _format_fsharp_json_call_arg(_original: Value, formatted: str, /) -> str:
    """Wrap a direct F# call argument as ``JsonNode``."""
    return _fsharp_json_wrap(formatted=formatted)


@beartype
def _fsharp_json_top_level(formatted: str) -> str:
    """Render the top-level right-hand side of a ``JsonNode`` binding.

    Collection literals (``JsonObject(...)``, ``JsonArray(...)``) and
    ``null`` assign directly to a ``JsonNode``-annotated binding via
    subsumption; a scalar literal is wrapped in ``JsonValue.Create``
    so the binding holds a ``JsonValue`` (a class derived from
    ``JsonNode``) rather than a raw primitive that F# would refuse to
    widen.
    """
    if formatted.startswith(
        (
            _FSHARP_JSON_OBJECT_OPEN,
            _FSHARP_JSON_ARRAY_OPEN,
            _FSHARP_JSON_EMPTY_OBJECT,
            _FSHARP_JSON_EMPTY_ARRAY,
        )
    ):
        return formatted
    if formatted == "null":
        return "null"
    return f"JsonValue.Create({formatted})"


@beartype
def _format_fsharp_json_assignment(name: str, value: str, _data: Value) -> str:
    """Assign a rendered literal to an F# ``JsonNode`` binding."""
    return f"let {name}: JsonNode = {_fsharp_json_top_level(formatted=value)}"


@beartype
def _build_fsharp_json_declaration_inner(
    *,
    keyword: str,
) -> Callable[[str, str, Value], str]:
    """Build a new F# ``JsonNode`` declaration formatter."""

    def _format(name: str, value: str, _data: Value) -> str:
        """Format a JSON-backed declaration."""
        rhs = _fsharp_json_top_level(formatted=value)
        return f"{keyword} {name}: JsonNode = {rhs}"

    return _format


@beartype
def _build_fsharp_datetime_epoch(
    prefix: str,
) -> Callable[[datetime.datetime], str]:
    """Build a datetime formatter that produces ``{prefix}Int`` from
    Unix epoch seconds.
    """

    def _format(value: datetime.datetime) -> str:
        """Format epoch seconds with the F# integer constructor."""
        formatted = format_datetime_epoch(value=value)
        return _apply_fsharp_entry(
            original=int(formatted),
            formatted=formatted,
            prefix=prefix,
        )

    return _format


_format_fsharp_datetime_epoch = _build_fsharp_datetime_epoch(prefix="F")


@beartype
def _apply_fsharp_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    template: str,
    sequence_declared_type: str,
    scalar_declared_type: str,
    entry_formatter: Callable[[Value, str], str],
) -> str:
    """Format a variable declaration or assignment."""
    decl_type = (
        sequence_declared_type
        if isinstance(data, list)
        else scalar_declared_type
    )
    wrapped = entry_formatter(data, value)
    return template.format(
        name=name,
        declared_type=decl_type,
        wrapped=wrapped,
    )


@beartype
def _build_fsharp_declaration(
    *,
    template: str,
    sequence_declared_type: str,
    scalar_declared_type: str,
    entry_formatter: Callable[[Value, str], str],
) -> Callable[[str, str, Value], str]:
    """Build an F# variable declaration/assignment formatter."""

    def _format(name: str, value: str, data: Value) -> str:
        """Delegate to module-level implementation."""
        return _apply_fsharp_declaration(
            name=name,
            value=value,
            data=data,
            template=template,
            sequence_declared_type=sequence_declared_type,
            scalar_declared_type=scalar_declared_type,
            entry_formatter=entry_formatter,
        )

    return _format


@beartype
def _build_fsharp_call_stub_lines(
    *,
    parts: Sequence[str],
    params: Sequence[str],
    curried: bool,
) -> tuple[str, ...]:
    """Return F# stub declarations for a call name."""
    if curried:
        param_list = " " + " ".join(f"(_{p}: obj)" for p in params)
    else:
        param_list = "(" + ", ".join(f"_{p}: obj" for p in params) + ")"
    let_param_list = param_list if curried else f" {param_list}"
    if len(parts) == 1:
        return (f"let {parts[0]}{let_param_list} : obj = null",)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        cls = f"{root.title()}Type_"
        return (
            f"type {cls}() =",
            f"    member _.{method}{param_list} : obj = null",
            f"let {root} = {cls}()",
        )
    lines: list[str] = []
    inner_cls = f"{fields[-1].title()}Type_"
    lines.append(f"type {inner_cls}() =")
    lines.append(f"    member _.{method}{param_list} : obj = null")
    prev_cls = inner_cls
    for i in range(len(fields) - 2, -1, -1):
        cls = f"{fields[i].title()}Type_"
        lines.append(f"type {cls}() =")
        lines.append(f"    member _.{fields[i + 1]} = {prev_cls}()")
        prev_cls = cls
    root_cls = f"{root.title()}Type_"
    lines.append(f"type {root_cls}() =")
    lines.append(f"    member _.{fields[0]} = {prev_cls}()")
    lines.append(f"let {root} = {root_cls}()")
    return tuple(lines)


@beartype
def _fsharp_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return F# positional (tuple-form) stub declarations."""
    return _build_fsharp_call_stub_lines(
        parts=parts, params=params, curried=False
    )


@beartype
def _fsharp_curried_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return F# curried stub declarations."""
    return _build_fsharp_call_stub_lines(
        parts=parts, params=params, curried=True
    )


@beartype
def _fsharp_format_call_arg(_original: Value, formatted: str, /) -> str:
    """Wrap a formatted F# value in parentheses for curried
    application.
    """
    return f"({formatted})"


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class FSharp(metaclass=LanguageCls):
    """F# language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.FSHARP`` — ``System.DateOnly(...)`` call,
              e.g. ``System.DateOnly(2024, 1, 15)``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.FSHARP`` — ``System.DateTime(...)`` call,
              e.g. ``System.DateTime(2024, 1, 15, 12, 30, 0)``.

        type_name: Name of the generated custom type.  Defaults to
            ``"Val"``.

        constructor_prefix: Prefix for generated constructor names.
            Defaults to ``"F"``, producing constructors like ``FNull``,
            ``FBool``, ``FInt``, etc.

        json_type: When set to
            ``json_types.SYSTEM_TEXT_JSON_NODE``, render values through
            ``System.Text.Json.Nodes.JsonNode`` (``JsonObject`` /
            ``JsonArray`` / ``JsonValue.Create``) instead of the generated
            tagged ``Val`` discriminated union.  Dates / datetimes /
            times switch to ISO 8601 strings (unless ``datetime_format``
            is ``EPOCH``), heterogeneous collections are accepted, and
            non-string dict keys are rejected because JSON object keys
            must be strings.

    Notes:
        The default tagged ``Val`` discriminated union does not
        round-trip through ``System.Text.Json.JsonSerializer.Serialize``
        (with or without ``FSharp.SystemTextJson``) without a custom
        ``JsonConverter<Val>``.  Two pitfalls:

        * The map case is emitted as ``FMap of (string * Val) list``, a
          tuple list rather than a ``Map<,>``, so that insertion order
          survives (F#'s built-in ``Map<,>`` is sorted by key).  A
          generic JSON encoder emits it as ``[[k, v], ...]`` instead of
          ``{"k": v}``.
        * ``FSharp.SystemTextJson``'s ``Untagged`` encoding ignores
          ``UnwrapSingleFieldCases``, so ``FInt 42L`` round-trips as
          ``{"Item": 42}`` rather than ``42`` (upstream behavior
          reproduced on 1.3.13 and 1.4.36).

        Users serializing ``Val`` to JSON must walk the constructors
        explicitly; selecting ``json_type=SYSTEM_TEXT_JSON_NODE`` avoids
        the ``Val`` union entirely so a single ``.ToJsonString()`` call
        round-trips the rendered value.
    """

    format_integer_widened = no_format_integer_widened
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    module_name: str = "Module"

    leading_preamble = no_leading_preamble
    extension = ".fs"
    pygments_name = "fsharp"
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
    non_default_kwargs: ClassVar[dict[str, str]] = {
        "type_name": "JsonVal",
        "constructor_prefix": "J",
    }
    json_type_variant_name_suffix = "json_node"
    supports_record_struct_name_prefix = False
    supports_record_shape_names = False
    supports_non_string_dict_keys = False

    class DateFormats(enum.Enum):
        """Date format options for FSharp."""

        FSHARP = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="System.DateOnly({year}, {month}, {day})",
            ),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for FSharp."""

        FSHARP = DatetimeFormatConfig(
            formatter=datetime_ymdhms_formatter(
                template="System.DateTime({year}, {month}, {day}, "
                "{hour}, {minute}, {second})",
            ),
        )
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            type_produced=str,
        )

        EPOCH = DatetimeFormatConfig(
            formatter=_format_fsharp_datetime_epoch,
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
        """Sequence type options for F#."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="FList ["),
            close="]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type="Val",
            narrowed_empty_form=None,
        )
        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="[|"),
            close="|]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type="Val array",
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for F#."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="FSet ["),
            close="]",
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
        BLOCK = CommentConfig(
            prefix="(*",
            suffix=" *)",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        LET = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="let {name} = {value}",
            ),
            supports_redefinition=False,
        )
        LET_MUTABLE = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="let mutable {name} = {value}",
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
        positive_infinity="infinity",
        negative_infinity="-infinity",
        nan="nan",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=str)
        HEX = enum.member(value=format_integer_hex)
        OCTAL = enum.member(value=format_integer_octal)
        BINARY = enum.member(value=format_integer_binary)

        def __call__(self, value: int, /) -> str:
            """Format an integer."""
            formatter: Callable[[int], str] = self.value
            return formatter(value)

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = enum.auto()

    class NumericStyles(enum.Enum):
        """Numeric literal style options."""

        OVERLOADED = enum.auto()

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.auto()

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

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
        """FSharp call style options."""

        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )
        CURRIED = CommandCallStyle(
            arg_separator=" ",
        )

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

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for F#."""

        V8 = enum.auto()

    version_formats = VersionFormats

    class JsonTypes(enum.Enum):
        """JSON value type options for F#."""

        SYSTEM_TEXT_JSON_NODE = "JsonNode"
        """``System.Text.Json.Nodes.JsonNode``, the built-in .NET JSON
        document object model.
        """

    json_types = JsonTypes

    module_name_case: ClassVar[IdentifierCase] = IdentifierCase.PASCAL
    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.CAMEL,
        IdentifierCase.PASCAL,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    def validate_spec_for_data(self, data: Value) -> None:
        """Validate F#-specific data / format combinations.

        Under ``json_type`` only dict keys that are strings can be
        represented as JSON object keys, so a non-string dict key is
        rejected up-front.
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
                            "F# json_type can only represent dict keys "
                            f"as JSON object strings, not {type(key).__name__}"
                        )
                        raise UnrepresentableInputError(msg)
                    self._validate_json_value_keys(value)
            case list() | set():
                for item in data:
                    self._validate_json_value_keys(item)
            case _:
                return

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
        """Wrap an F# let declaration in a module."""
        del variable_name
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        return f"module {self.module_name}\n\n" + content

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap F# declaration + assignment in separate private
        functions.
        """
        del variable_name
        decl_indented = textwrap.indent(text=declaration, prefix=self.indent)
        assign_indented = textwrap.indent(text=assignment, prefix=self.indent)
        preamble = "\n".join(body_preamble) + "\n" if body_preamble else ""
        camel_name = IdentifierCase.CAMEL.convert(name=self.module_name)
        body = f"module {self.module_name}\n\n" + preamble
        body += (
            f"let private _{camel_name}Declaration () =\n"
            + decl_indented
            + f"\n{self.indent}ignore my_data\n\n"
            + f"let private _{camel_name}Assignment () =\n"
            + assign_indented
            + f"\n{self.indent}ignore my_data"
        )
        return body

    date_format: DateFormats = DateFormats.FSHARP
    datetime_format: DatetimeFormats = DatetimeFormats.FSHARP
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
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
    trailing_comma: TrailingCommas = TrailingCommas.NO
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.SEMICOLON
    )
    call_style: CallStyles = CallStyles.POSITIONAL
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    json_type: JsonTypes | None = None
    # Keep in sync with the `--langversion:` flag passed to the FSharp
    # linter in `.github/workflows/lint.yml`.
    language_version: VersionFormats = VersionFormats.V8
    indent: str = "    "
    type_name: str = "Val"
    constructor_prefix: str = "F"

    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = "; "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ""
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines."""
        return no_data_preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config.

        ``json_type`` relaxes scalar-type checks unconditionally because
        ``JsonObject`` / ``JsonArray`` accept heterogeneous ``JsonNode``
        children by construction.
        """
        if self._json_type_active:
            return dataclasses.replace(
                NO_HETEROGENEOUS_BEHAVIOR,
                skip_scalar_checks=True,
            )
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
        if isinstance(self.call_style.value, CommandCallStyle):
            return _fsharp_curried_call_stub
        return _fsharp_call_stub

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Callable that rewrites a formatted direct call argument.

        Curried calls parenthesize each argument so that constructor
        applications are not parsed as additional arguments to the outer
        call.  Under ``json_type`` every argument is wrapped as a
        ``JsonNode`` (via ``JsonValue.Create`` and an explicit ``:>
        JsonNode`` widening cast) so the underlying stub receives a
        JSON value.
        """
        if self._json_type_active:
            return _format_fsharp_json_call_arg
        if isinstance(self.call_style.value, CommandCallStyle):
            return _fsharp_format_call_arg
        return identity_call_arg

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
    def _entry_formatter(self) -> Callable[[Value, str], str]:
        """Shared entry formatter with the configured constructor
        prefix.
        """
        return _build_fsharp_entry_formatter(prefix=self.constructor_prefix)

    @cached_property
    def _json_type_active(self) -> bool:
        """Whether F# should render through ``JsonNode``."""
        return self.json_type is not None

    @cached_property
    def null_literal(self) -> str:
        """Literal representing ``None``."""
        if self._json_type_active:
            return "null"
        return f"{self.constructor_prefix}Null"

    @cached_property
    def true_literal(self) -> str:
        """Literal representing ``True``."""
        if self._json_type_active:
            return "true"
        return f"{self.constructor_prefix}Bool true"

    @cached_property
    def false_literal(self) -> str:
        """Literal representing ``False``."""
        if self._json_type_active:
            return "false"
        return f"{self.constructor_prefix}Bool false"

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        if self._json_type_active:
            return SequenceFormatConfig(
                sequence_open=fixed_open(open_str=_FSHARP_JSON_ARRAY_OPEN),
                close=_FSHARP_JSON_ARRAY_CLOSE,
                supports_heterogeneity=True,
                single_element_trailing_comma=False,
                supports_trailing_comma=False,
                empty_sequence=_FSHARP_JSON_EMPTY_ARRAY,
                preamble_lines=(),
                format_entry=_format_fsharp_json_entry,
                typed_opener_fallback=None,
                uses_typed_literal_for_scalars=False,
                requires_uniform_record_shapes=False,
                declared_type="JsonNode",
                narrowed_empty_form=None,
            )
        fmt = self.sequence_format.value
        if self.sequence_format.name == "ARRAY":
            return fmt
        return dataclasses.replace(
            fmt,
            sequence_open=fixed_open(
                open_str=f"{self.constructor_prefix}List [",
            ),
        )

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format_config.sequence_open

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        if self._json_type_active:
            return SetFormatConfig(
                set_open=fixed_open(open_str=_FSHARP_JSON_ARRAY_OPEN),
                close=_FSHARP_JSON_ARRAY_CLOSE,
                empty_set=_FSHARP_JSON_EMPTY_ARRAY,
                preamble_lines=(),
                set_opener_template="",
                supports_heterogeneity=True,
                supports_trailing_comma=False,
            )
        return dataclasses.replace(
            self.set_format.value,
            set_open=fixed_open(
                open_str=f"{self.constructor_prefix}Set [",
            ),
        )

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        if self._json_type_active:
            return DictFormatConfig(
                dict_open=fixed_open(open_str=_FSHARP_JSON_OBJECT_OPEN),
                close=_FSHARP_JSON_OBJECT_CLOSE,
                format_entry=tuple_dict_entry(
                    format_value=_format_fsharp_json_entry,
                ),
                empty_dict=_FSHARP_JSON_EMPTY_OBJECT,
                preamble_lines=(),
                narrowed_open=None,
                supports_trailing_comma=False,
            )
        return DictFormatConfig(
            dict_open=fixed_open(
                open_str=f"{self.constructor_prefix}Map [",
            ),
            close="]",
            format_entry=tuple_dict_entry(
                format_value=self._entry_formatter,
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
        if self._json_type_active:
            return format_date_iso
        return self.date_format

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal.

        Under ``json_type`` the EPOCH branch emits a bare ``int64``
        literal (e.g. ``1705320600L``) rather than the tagged ``FInt
        ...`` constructor used outside json mode: the ``Val``
        discriminated union does not exist under ``json_type``, and the
        entry / top-level formatter is responsible for wrapping the
        literal with ``JsonValue.Create`` so it becomes a ``JsonNode``.
        """
        if self._json_type_active:
            if self.datetime_format.value.type_produced is int:
                format_integer = self.format_integer

                def _format_json_epoch(value: datetime.datetime) -> str:
                    """Return an epoch-seconds ``int64`` literal."""
                    formatted = format_datetime_epoch(value=value)
                    return format_integer(int(formatted))

                return _format_json_epoch
            return format_datetime_iso
        if self.datetime_format.name == "EPOCH":
            return _build_fsharp_datetime_epoch(
                prefix=self.constructor_prefix,
            )
        return self.datetime_format

    @cached_property
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        if self._json_type_active:
            return format_time_iso
        return format_time_fsharp

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal.

        Under ``json_type`` integers carry an explicit F# suffix
        (``L`` for signed-64-bit, ``UL`` for values one beyond
        ``Int64.MaxValue`` up through ``UInt64.MaxValue``) so the
        ``JsonValue.Create`` overload set can resolve unambiguously to
        ``long`` / ``ulong``.  Negative values below ``Int64.MinValue``
        and positive values above ``UInt64.MaxValue`` have no
        ``JsonValue.Create`` overload and are rejected up-front rather
        than emitted as a literal F# would refuse to compile.
        """
        if self._json_type_active:
            base = self.integer_format

            def _format(value: int) -> str:
                """Return a json-mode integer literal."""
                rendered = base(value)
                if I64_MIN <= value <= I64_MAX:
                    return f"{rendered}L"
                if 0 <= value <= U64_MAX:
                    return f"{rendered}UL"
                msg = (
                    f"F# json_type cannot represent integer {value}: "
                    "JsonValue.Create has no overload for values outside "
                    "the Int64 / UInt64 ranges."
                )
                raise UnrepresentableIntegerError(msg)

            return _format
        return make_overflow_suffix_formatter(
            base=self.integer_format,
            min_value=I64_MIN,
            max_value=I64_MAX,
            suffix="I",
        )

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Callable that formats one sequence entry."""
        if self._json_type_active:
            return _format_fsharp_json_entry
        return self._entry_formatter

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Callable that formats one set entry."""
        if self._json_type_active:
            return _format_fsharp_json_entry
        return self._entry_formatter

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        if self._json_type_active:
            return OrderedMapFormatConfig(
                ordered_map_open=fixed_open(
                    open_str=_FSHARP_JSON_OBJECT_OPEN,
                ),
                close=_FSHARP_JSON_OBJECT_CLOSE,
                preamble_lines=(),
            )
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(
                open_str=f"{self.constructor_prefix}Map [",
            ),
            close="]",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        if self._json_type_active:
            return tuple_dict_entry(format_value=_format_fsharp_json_entry)
        return tuple_dict_entry(format_value=self._entry_formatter)

    @cached_property
    def _sequence_declared_type(self) -> str:
        """Resolved declared type for sequence values."""
        raw_declared = self.sequence_format.value.declared_type
        return (
            raw_declared.replace("Val", self.type_name)
            if raw_declared is not None
            else self.type_name
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        keyword = (
            "let mutable"
            if self.declaration_style.value.supports_redefinition
            else "let"
        )
        if self._json_type_active:
            return declaration_formatter_ignoring_modifiers(
                formatter=_build_fsharp_json_declaration_inner(
                    keyword=keyword,
                ),
            )
        return declaration_formatter_ignoring_modifiers(
            formatter=_build_fsharp_declaration(
                template=(
                    f"{keyword} {{name}}: {{declared_type}} = {{wrapped}}"
                ),
                sequence_declared_type=self._sequence_declared_type,
                scalar_declared_type=self.type_name,
                entry_formatter=self._entry_formatter,
            ),
        )

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        if self._json_type_active:
            return _format_fsharp_json_assignment
        return _build_fsharp_declaration(
            template="let {name}: {declared_type} = {wrapped}",
            sequence_declared_type=self._sequence_declared_type,
            scalar_declared_type=self.type_name,
            entry_formatter=self._entry_formatter,
        )

    @cached_property
    def format_call_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a declaration binding a call expression.

        The literal-binding declaration adds a leading ``name: Val``
        type annotation and wraps the value in a tagged-enum
        constructor (``FInt``, ``FStr``, …) derived from the bound
        value's runtime type; a call expression has no such tag, so
        both the annotation and the constructor wrapper are omitted and
        F# infers the call's return type instead.
        """
        return self.declaration_style.value.formatter

    @cached_property
    def format_call_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment binding a call expression.

        The literal-binding assignment injects a ``: Val`` annotation
        and a tagged-enum constructor derived from the bound value's
        runtime type; a call expression has no such tag, so both are
        omitted and F# infers the return type.  Mirrors
        :attr:`format_variable_assignment`, which always emits a plain
        ``let`` (never ``let mutable``) regardless of
        ``declaration_style``: an F# rebinding shadows with ``let``, so
        the ``mutable`` keyword would be spurious here.
        """
        return variable_formatter(template="let {name} = {value}")

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble with type declarations."""
        p = self.constructor_prefix
        header = f"type {self.type_name} ="
        f_str = f"    | {p}Str of string"
        return {
            type(None): (header, f"    | {p}Null"),
            bool: (header, f"    | {p}Bool of bool"),
            int: (header, f"    | {p}Int of int64"),
            float: (header, f"    | {p}Float of float"),
            str: (header, f_str),
            bytes: (header, f_str),
            list: (header, f"    | {p}List of {self.type_name} list"),
            dict: (
                header,
                f"    | {p}Map of (string * {self.type_name}) list",
            ),
            OrderedMap: (
                header,
                f"    | {p}Map of (string * {self.type_name}) list",
            ),
            set: (header, f"    | {p}Set of {self.type_name} list"),
            datetime.date: (
                header,
                f_str,
                f"    | {p}Date of System.DateTime",
            ),
            datetime.time: (header, f_str),
            datetime.datetime: (
                (header, f"    | {p}Int of int64")
                if self.datetime_format.value.type_produced is int
                else (
                    header,
                    f_str,
                    f"    | {p}Datetime of System.DateTime",
                )
            ),
        }

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines from the scalar map.

        Under ``json_type`` the file always ``open``s the
        ``System.Text.Json.Nodes`` types inside the module body so
        the ``JsonObject`` / ``JsonArray`` / ``JsonValue`` constructors
        resolve; the F# ``module`` declaration must be the first
        non-blank line, which rules out the file-level preamble that
        other languages use for an equivalent import.

        Swaps ``int64`` to ``bigint`` in the ``FInt`` variant when the
        data contains an integer outside signed 64-bit range.
        """
        if self._json_type_active:

            @beartype
            def _json_body_preamble(
                _types: frozenset[type], _data: Value, /
            ) -> tuple[str, ...]:
                """Return the JsonNode ``open`` directive."""
                return (_FSHARP_JSON_USING,)

            return _json_body_preamble
        static_compute = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )
        p = self.constructor_prefix
        header = f"type {self.type_name} ="
        bigint_override = {
            **self.scalar_body_preamble,
            int: (header, f"    | {p}Int of bigint"),
        }
        bigint_compute = body_preamble_from_scalars(
            scalar_body_preamble=bigint_override,
            format_lines=tuple,
        )

        @beartype
        def _compute(
            types: frozenset[type], data: Value, /
        ) -> tuple[str, ...]:
            """Return body preamble, preferring ``bigint`` when needed."""
            if data_has_out_of_range_int(data=data):
                return bigint_compute(types, data)
            return static_compute(types, data)

        return _compute

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        config: CallStyle = self.call_style.value
        return config
