"""TypeScript language specification."""

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
    fixed_open,
)
from literalizer._formatters.format_dates import (
    date_iso_formatter,
    datetime_iso_formatter,
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
    format_time_iso,
)
from literalizer._formatters.format_entries import (
    assignment_formatter_from_declaration,
    dict_entry_with_separator,
    dict_entry_with_template,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    variable_declaration_formatter,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    format_integer_underscore,
)
from literalizer._formatters.format_strings import (
    format_string_backslash,
    format_string_backslash_single,
)
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
    ObjectCallStyle,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
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
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import Scalar, Value


def _ts_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return TypeScript stub declarations for a call name.

    Mirrors :func:`_js_call_stub`: dotted roots become a ``Proxy`` that
    returns a callable ``Proxy`` for any attribute access, so nested
    member calls succeed; bare roots become a no-op function. The ``:
    any`` annotation keeps the stub accepted by the type checker
    regardless of how the fixture uses it.
    """
    root = parts[0]
    if len(parts) > 1:
        proxy = "new Proxy(function(){}, {get: g})"
        handler = f"get: function g() {{ return {proxy}; }}"
        return (f"const {root}: any = new Proxy({{}}, {{{handler}}});",)
    return (f"const {root}: any = () => {{}};",)


@beartype
def _ts_element_union(*, types: list[str]) -> str:
    """Remove duplicate types and join into a TypeScript union."""
    unique: list[str] = list(dict.fromkeys(types))
    match unique:
        case [only]:
            return only
        case _:
            return " | ".join(unique)


@beartype
def _ts_scalar_hint(
    *,
    data: Scalar,
    date_hint: str,
    datetime_hint: str,
) -> str:
    """Derive a TypeScript annotation for a scalar value."""
    match data:
        case bool():
            hint = "boolean"
        case int() | float():
            hint = "number"
        case str() | bytes():
            hint = "string"
        case datetime.datetime():
            hint = datetime_hint
        case datetime.date():
            hint = date_hint
        case datetime.time():
            hint = "string"
        case None:
            hint = "null"
        case _ as unreachable:
            assert_never(unreachable)
    return hint


@beartype
def _ts_dict_hint(
    *,
    is_ordered: bool,
    is_empty: bool,
    val_types: list[str],
    dict_hint_template: str,
) -> str:
    """Derive a TypeScript type annotation for a dict value."""
    template = "Record<string, {val}>" if is_ordered else dict_hint_template
    # The MAP opener always uses ``unknown`` as the value type, so
    # the annotation must match.
    if is_empty or "Map<" in template:
        return template.format(val="unknown")
    return template.format(val=_ts_element_union(types=val_types))


@beartype
def _ts_set_hint(
    *,
    data: set[Scalar],
    recurse: Callable[..., str],
) -> str:
    """Derive a TypeScript type annotation for a set value."""
    if not data:
        return "Set<unknown>"
    elem_types = sorted(recurse(data=e) for e in data)
    return f"Set<{_ts_element_union(types=elem_types)}>"


@beartype
def _ts_list_hint(
    *,
    data: list[Value],
    recurse: Callable[..., str],
    sequence_is_tuple: bool,
) -> str:
    """Derive a TypeScript type annotation for a list value."""
    if not data:
        return "readonly []" if sequence_is_tuple else "unknown[]"
    elem_types = [recurse(data=e) for e in data]
    if sequence_is_tuple:
        return f"readonly [{', '.join(elem_types)}]"
    elem_union = _ts_element_union(types=elem_types)
    return f"({elem_union})[]" if " | " in elem_union else f"{elem_union}[]"


@beartype
def _ts_type_hint(
    *,
    data: Value,
    date_hint: str,
    datetime_hint: str,
    dict_hint_template: str,
    sequence_is_tuple: bool,
) -> str:
    """Derive a TypeScript type annotation from *data*."""
    recurse = functools.partial(
        _ts_type_hint,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        dict_hint_template=dict_hint_template,
        sequence_is_tuple=sequence_is_tuple,
    )
    match data:
        case dict():
            hint = _ts_dict_hint(
                is_ordered=isinstance(data, (ordereddict, OrderedDict)),
                is_empty=not data,
                val_types=[recurse(data=v) for v in data.values()],
                dict_hint_template=dict_hint_template,
            )
        case set():
            hint = _ts_set_hint(data=data, recurse=recurse)
        case list():
            hint = _ts_list_hint(
                data=data,
                recurse=recurse,
                sequence_is_tuple=sequence_is_tuple,
            )
        case _:
            hint = _ts_scalar_hint(
                data=data,
                date_hint=date_hint,
                datetime_hint=datetime_hint,
            )
    return hint


@beartype
def _ts_inference_widens_unsafely(*, data: Value) -> bool:
    """Return True if TypeScript inference for *data* would widen to a
    permissive type (e.g. ``unknown[]`` for ``[]``) where downstream
    consumption can no longer rely on a concrete element type.

    Empty collection literals are the canonical trigger: the inferred
    element type cannot be pinned down, so :func:`_ts_type_hint`
    falls back to ``unknown``.
    """
    match data:
        case list() | set() | dict():
            return not data
        case _:
            return False


@beartype
def _format_ts_typed_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
    keyword: str,
    date_hint: str,
    datetime_hint: str,
    dict_hint_template: str,
    sequence_is_tuple: bool,
) -> str:
    """Format a TypeScript variable declaration with an explicit type."""
    hint = _ts_type_hint(
        data=data,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        dict_hint_template=dict_hint_template,
        sequence_is_tuple=sequence_is_tuple,
    )
    return f"{keyword} {name}: {hint} = {value};"


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class TypeScript(metaclass=LanguageCls):
    """TypeScript language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.JS`` — ``new Date(...)`` call,
              e.g. ``new Date("2024-01-15")``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.JS`` — ``new Date(...)`` call,
              e.g. ``new Date("2024-01-15T12:30:00")``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.

        sequence_format: Which TypeScript sequence type to use.

            * ``sequence_formats.ARRAY`` — array literal,
              e.g. ``[1, 2, 3]``.
            * ``sequence_formats.TUPLE`` — ``as const`` tuple literal,
              e.g. ``[1, 2, 3] as const``.  TypeScript infers
              per-element types instead of a union array type.
    """

    extension = ".ts"
    pygments_name = "typescript"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = True
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
    supports_module_name = False
    supports_empty_dict_key = False
    supports_call_style = True
    supports_default_dict_key_type = False
    supports_default_dict_value_type = False
    supports_default_sequence_element_type = False
    supports_default_set_element_type = False
    supports_default_ordered_map_value_type = False
    supports_non_string_dict_keys = False

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

    class DateFormats(enum.Enum):
        """Date formatting options for TypeScript."""

        JS = DateFormatConfig(
            formatter=date_iso_formatter(template='new Date("{iso}")'),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime formatting options for TypeScript."""

        JS = DatetimeFormatConfig(
            formatter=datetime_iso_formatter(
                template='new Date("{iso}")',
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
        """Sequence type options for TypeScript."""

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
        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="["),
            close="] as const",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence="[] as const",
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for TypeScript."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="new Set(["),
            close="])",
            empty_set="new Set()",
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
            prefix="/*",
            suffix=" */",
        )

    class StatementTerminatorStyles(enum.Enum):
        """Statement terminator options."""

        SEMICOLON = enum.auto()
        NONE = "none"

        def wrap_formatter(
            self,
            formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
        ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
            """Wrap a formatter to match this statement terminator
            style.
            """
            if self.value != "none":
                return formatter

            def without_semicolon(
                name: str,
                value: str,
                data: Value,
                _modifiers: frozenset[enum.Enum],
            ) -> str:
                """Format without a trailing semicolon."""
                return formatter(name, value, data, _modifiers).removesuffix(
                    ";"
                )

            return without_semicolon

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        CONST = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="const {name} = {value};"
            ),
            supports_redefinition=False,
        )
        LET = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="let {name} = {value};"
            ),
            supports_redefinition=True,
        )
        VAR = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="var {name} = {value};"
            ),
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        OBJECT = DictFormatConfig(
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
        MAP = DictFormatConfig(
            dict_open=fixed_open(open_str="new Map<string, unknown>(["),
            close="])",
            format_entry=dict_entry_with_template(
                template="[{key}, {value}]",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict="new Map()",
            preamble_lines=(),
            narrowed_open=None,
            supports_trailing_comma=True,
        )

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="Infinity",
        negative_infinity="-Infinity",
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

        DOUBLE = enum.member(value=format_string_backslash)
        SINGLE = enum.member(value=format_string_backslash_single)

        def __call__(self, value: str, /) -> str:
            """Format a string."""
            return self.value(value=value)

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
            dict_hint_template: str,
            sequence_is_tuple: bool,
        ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
            """Return the variable declaration formatter."""

            def _typed_formatter(
                name: str,
                value: str,
                data: Value,
                modifiers: frozenset[enum.Enum],
            ) -> str:
                """Adapt :func:`_format_ts_typed_declaration` to the
                positional formatter interface.
                """
                return _format_ts_typed_declaration(
                    name=name,
                    value=value,
                    data=data,
                    _modifiers=modifiers,
                    keyword=keyword,
                    date_hint=date_hint,
                    datetime_hint=datetime_hint,
                    dict_hint_template=dict_hint_template,
                    sequence_is_tuple=sequence_is_tuple,
                )

            if self is type(self).ALWAYS:
                return _typed_formatter

            def _safe_formatter(
                name: str,
                value: str,
                data: Value,
                modifiers: frozenset[enum.Enum],
            ) -> str:
                """Annotate only when inference would widen unsafely.

                Applies to both NEVER and SAFE: empty collection
                literals are inferred as evolving ``any[]`` / ``{}`` /
                ``Set<unknown>`` and break under ``--noImplicitAny``
                once the variable is consumed elsewhere, so the
                annotation is unavoidable even when callers asked to
                suppress hints.
                """
                if _ts_inference_widens_unsafely(data=data):
                    return _typed_formatter(
                        name=name,
                        value=value,
                        data=data,
                        modifiers=modifiers,
                    )
                return auto_formatter(name, value, data, modifiers)

            return _safe_formatter

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
    statement_terminator_styles = StatementTerminatorStyles

    class CallStyles(enum.Enum):
        """TypeScript call style options."""

        OBJECT = ObjectCallStyle(separator=": ")
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
        """Version options for TypeScript."""

        V5 = enum.auto()

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
        """Wrap a TypeScript declaration as a module."""
        del variable_name
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        return f"{content}\nexport {{}};"

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap TypeScript declaration + assignment as a module."""
        return TypeScript.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.JS
    datetime_format: DatetimeFormats = DatetimeFormats.JS
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.CONST
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.OBJECT
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
    call_style: CallStyles = CallStyles.OBJECT
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    # Keep in sync with the `tsc` syntax-check call in
    # `.github/workflows/lint.yml`, which parses `.ts` fixtures, and with
    # `JavaScript.language_version` in
    # `src/literalizer/languages/javascript.py` (the shared ECMAScript
    # target).
    language_version: VersionFormats = VersionFormats.V5
    indent: str = "  "

    null_literal: ClassVar[str] = "null"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = True
    statement_terminator: ClassVar[str] = ";"
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines."""
        return no_data_preamble

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
        return _ts_call_stub

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
        """Callable that formats a datetime as a string literal."""
        return self.datetime_format

    @cached_property
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        return format_time_iso

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
        base_decl = self.variable_type_hints.formatter(
            auto_formatter=self.declaration_style.value.formatter,
            keyword=self.declaration_style.name.lower(),
            date_hint=(
                "string"
                if self.date_format.value.type_produced is str
                else "Date"
            ),
            datetime_hint=(
                "number"
                if self.datetime_format.value.type_produced is int
                else (
                    "string"
                    if self.datetime_format.value.type_produced is str
                    else "Date"
                )
            ),
            dict_hint_template=(
                "Map<string, {val}>"
                if self.dict_format.name == "MAP"
                else "Record<string, {val}>"
            ),
            sequence_is_tuple=(self.sequence_format.name == "TUPLE"),
        )
        return self.statement_terminator_style.wrap_formatter(
            formatter=base_decl
        )

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        return assignment_formatter_from_declaration(
            formatter=self.statement_terminator_style.wrap_formatter(
                formatter=variable_declaration_formatter(
                    template="{name} = {value};"
                ),
            ),
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (TypeScript needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (TypeScript needs none)."""
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
