"""OCaml language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    datetime_ymdhms_formatter,
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    declaration_formatter_ignoring_modifiers,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    tuple_dict_entry,
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
    make_overflow_fallback_formatter,
    raise_for_unrepresentable_int,
)
from literalizer._formatters.format_strings import format_string_backslash
from literalizer._language import (
    NO_HETEROGENEOUS_BEHAVIOR,
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
    OrderedMapFormatConfig,
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    default_wrap_calls_with_declarations,
    identity_call_ref_identifier,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import Value
from literalizer.exceptions import WrapCombinedInFileNotSupportedError


@beartype
def _apply_ocaml_entry(original: Value, formatted: str, prefix: str) -> str:
    """Wrap a formatted entry in the appropriate OCaml ``val_t``
    constructor.
    """
    match original:
        case bool():
            return formatted
        case int():
            needs_parens = formatted.startswith("-")
            return (
                f"{prefix}Int ({formatted})"
                if needs_parens
                else f"{prefix}Int {formatted}"
            )
        case float():
            negative = formatted.startswith("-")
            return (
                f"{prefix}Float ({formatted})"
                if negative
                else f"{prefix}Float {formatted}"
            )
        case str() | bytes():
            return f"{prefix}Str {formatted}"
        case datetime.date() if formatted.startswith('"'):
            return f"{prefix}Str {formatted}"
        case _:
            return formatted


def _build_ocaml_entry_formatter(
    prefix: str,
) -> Callable[[Value, str], str]:
    """Build an entry formatter that wraps values in OCaml ``val_t``
    constructors using the given *prefix*.
    """

    def _format(original: Value, formatted: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_ocaml_entry(
            original=original, formatted=formatted, prefix=prefix
        )

    return _format


_format_ocaml_entry = _build_ocaml_entry_formatter(prefix="O")


@beartype
def _ocaml_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    /,
) -> tuple[str, ...]:
    """Return OCaml stub declarations for a call name.

    For dotted names like ``app.client.fetch``, nested OCaml modules
    are emitted so that ``App.Client.fetch arg`` is valid at the call
    site.  The innermost name becomes a ``let`` declaration that accepts
    any argument and returns unit.  Each module-path component has its
    first character in uppercase, as OCaml requires module names to begin
    with an uppercase letter.
    """
    method = parts[-1]
    lines: list[str] = [f"let {method} _ = ()"]
    for part in reversed(parts[:-1]):
        cap = part[0].upper() + part[1:]
        lines = [f"module {cap} = struct", *lines, "end"]
    return tuple(lines)


@beartype
def _ocaml_call_target(parts: Sequence[str], /) -> str:
    """Return the dotted OCaml call target for a sequence of name parts.

    Module components (all but the last) have their first character
    converted to uppercase because OCaml requires module names to begin
    with an uppercase letter.
    """
    if len(parts) == 1:
        return parts[0]
    modules = [p[0].upper() + p[1:] for p in parts[:-1]]
    return ".".join([*modules, parts[-1]])


@beartype
def _apply_ocaml_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    sequence_declared_type: str,
    scalar_declared_type: str,
    entry_formatter: Callable[[Value, str], str],
) -> str:
    """Format a variable declaration."""
    decl_type = (
        sequence_declared_type
        if isinstance(data, list)
        else scalar_declared_type
    )
    wrapped = entry_formatter(data, value)
    return f"let {name} : {decl_type} = {wrapped}"


@beartype
def _build_ocaml_declaration(
    *,
    sequence_declared_type: str,
    scalar_declared_type: str,
    entry_formatter: Callable[[Value, str], str],
) -> Callable[[str, str, Value], str]:
    """Build an OCaml variable declaration formatter."""

    def _format(name: str, value: str, data: Value) -> str:
        """Delegate to module-level implementation."""
        return _apply_ocaml_declaration(
            name=name,
            value=value,
            data=data,
            sequence_declared_type=sequence_declared_type,
            scalar_declared_type=scalar_declared_type,
            entry_formatter=entry_formatter,
        )

    return _format


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class OCaml(metaclass=LanguageCls):
    """OCaml language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.OCAML`` — tuple literal,
              e.g. ``(2024, 1, 15)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.OCAML`` — pair of tuples,
              e.g. ``((2024, 1, 15), (12, 30, 0))``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.

        type_name: Name of the generated custom type.  Defaults to
            ``"val_t"``.

        constructor_prefix: Prefix for generated constructor names.
            Defaults to ``"O"``, producing constructors like ``ONull``,
            ``OBool``, ``OInt``, etc.
    """

    extension = ".ml"
    pygments_name = "ocaml"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_special_floats = True
    supports_variable_names = True
    supports_dotted_calls = True

    class DateFormats(enum.Enum):
        """Date format options for OCaml."""

        OCAML = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="ODate ({year}, {month}, {day})",
            ),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for OCaml."""

        OCAML = DatetimeFormatConfig(
            formatter=datetime_ymdhms_formatter(
                template="ODatetime (({year}, {month}, {day}), "
                "({hour}, {minute}, {second}))",
            ),
        )
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            type_produced=str,
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
        """Sequence type options for OCaml."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="OList ["),
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
            declared_type="val_t",
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
            declared_type="val_t array",
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for OCaml."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="OSet ["),
            close="]",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        PAREN_STAR = CommentConfig(
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
        negative_infinity="neg_infinity",
        nan="nan",
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

        DOUBLE = "double"

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

        AUTO = enum.auto()

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

    class LineEndings(enum.Enum):
        """Line ending options."""

        SEMICOLON = "semicolon"

    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """OCaml call style options."""

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

    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.PASCAL,
    )

    validate_spec_for_data = no_validate_spec_for_data
    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap an OCaml let declaration in a module."""
        del variable_name
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        return "module Check = struct\n\n" + content + "\n\nend"

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

    date_format: DateFormats = DateFormats.OCAML
    datetime_format: DatetimeFormats = DatetimeFormats.OCAML
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.PAREN_STAR
    declaration_style: DeclarationStyles = DeclarationStyles.LET
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.DEFAULT
    float_format: FloatFormats = FloatFormats.REPR
    integer_format: IntegerFormats = IntegerFormats.DECIMAL
    numeric_literal_suffix: NumericLiteralSuffixes = (
        NumericLiteralSuffixes.NONE
    )
    numeric_separator: NumericSeparators = NumericSeparators.NONE
    numeric_style: NumericStyles = NumericStyles.OVERLOADED
    string_format: StringFormats = StringFormats.DOUBLE
    trailing_comma: TrailingCommas = TrailingCommas.NO
    line_ending: LineEndings = LineEndings.SEMICOLON
    call_style: CallStyles = CallStyles.POSITIONAL
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    indent: str = "    "
    type_name: str = "val_t"
    constructor_prefix: str = "O"

    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = "; "
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
        return format_string_backslash

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines."""
        return no_data_preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config."""
        return self.heterogeneous_strategy.value

    @cached_property
    def type_hint_collection_preamble_lines(
        self,
    ) -> Callable[[frozenset[type]], tuple[str, ...]]:
        """Return preamble lines for empty-collection type hints."""
        return no_type_hint_preamble

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return stub declarations for a call expression."""
        return _ocaml_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return file-scope stubs for a call expression."""
        return no_call_stub

    @cached_property
    def format_call_statement(self) -> Callable[[str], str]:
        """Wrap a call expression as a let binding."""
        return lambda statement: f"let _ = {statement}"

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into the language's call
        syntax.
        """
        return _ocaml_call_target

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
    def null_literal(self) -> str:
        """Null literal using the configured constructor prefix."""
        return f"{self.constructor_prefix}Null"

    @cached_property
    def true_literal(self) -> str:
        """True literal using the configured constructor prefix."""
        return f"{self.constructor_prefix}Bool true"

    @cached_property
    def false_literal(self) -> str:
        """False literal using the configured constructor prefix."""
        return f"{self.constructor_prefix}Bool false"

    @cached_property
    def _entry_formatter(self) -> Callable[[Value, str], str]:
        """Entry formatter built from the configured prefix."""
        return _build_ocaml_entry_formatter(prefix=self.constructor_prefix)

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        fmt = self.sequence_format.value
        if self.sequence_format.name == "LIST":
            _seq_open = fixed_open(
                open_str=f"{self.constructor_prefix}List [",
            )
            return dataclasses.replace(fmt, sequence_open=_seq_open)
        return fmt

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        fmt = self.sequence_format.value
        if self.sequence_format.name == "LIST":
            return fixed_open(
                open_str=f"{self.constructor_prefix}List [",
            )
        return fmt.sequence_open

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return dataclasses.replace(
            self.set_format.value,
            set_open=fixed_open(
                open_str=f"{self.constructor_prefix}Set [",
            ),
        )

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
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
        if self.date_format.name == "OCAML":
            return date_ymd_formatter(
                template=(
                    f"{self.constructor_prefix}Date "
                    "({year}, {month}, {day})"
                ),
            )
        return self.date_format

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        if self.datetime_format.name == "OCAML":
            return datetime_ymdhms_formatter(
                template=(
                    f"{self.constructor_prefix}Datetime "
                    f"(({{year}}, {{month}}, {{day}}), "
                    f"({{hour}}, {{minute}}, {{second}}))"
                ),
            )
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
            fallback=raise_for_unrepresentable_int(language_name="OCaml"),
        )

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Callable that formats a set entry."""
        return self._entry_formatter

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Callable that formats a sequence entry."""
        return self._entry_formatter

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
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
        return tuple_dict_entry(format_value=self._entry_formatter)

    @cached_property
    def _ocaml_declaration(self) -> Callable[[str, str, Value], str]:
        """Declaration formatter built from the configured type name."""
        _raw_declared = self.sequence_format.value.declared_type
        _sequence_declared_type = (
            _raw_declared.replace("val_t", self.type_name)
            if _raw_declared is not None
            else self.type_name
        )
        return _build_ocaml_declaration(
            sequence_declared_type=_sequence_declared_type,
            scalar_declared_type=self.type_name,
            entry_formatter=self._entry_formatter,
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return declaration_formatter_ignoring_modifiers(
            formatter=self._ocaml_declaration
        )

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        return self._ocaml_declaration

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (OCaml needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble for OCaml."""
        p = self.constructor_prefix
        _h = f"type {self.type_name} ="
        _date_constructor = (
            f"  | {p}Str of string"
            if self.date_format.value.type_produced is str
            else f"  | {p}Date of (int * int * int)"
        )
        _datetime_constructor = (
            f"  | {p}Str of string"
            if self.datetime_format.value.type_produced is str
            else f"  | {p}Datetime of ((int * int * int) * (int * int * int))"
        )
        return {
            type(None): (_h, f"  | {p}Null"),
            bool: (_h, f"  | {p}Bool of bool"),
            int: (_h, f"  | {p}Int of int"),
            float: (_h, f"  | {p}Float of float"),
            str: (_h, f"  | {p}Str of string"),
            bytes: (_h, f"  | {p}Str of string"),
            datetime.date: (_h, _date_constructor),
            datetime.datetime: (_h, _datetime_constructor),
            list: (_h, f"  | {p}List of {self.type_name} list"),
            dict: (_h, f"  | {p}Map of (string * {self.type_name}) list"),
            ordereddict: (
                _h,
                f"  | {p}Map of (string * {self.type_name}) list",
            ),
            set: (_h, f"  | {p}Set of {self.type_name} list"),
        }

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines from the scalar map."""
        return body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )
