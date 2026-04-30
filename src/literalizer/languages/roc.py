"""Roc language specification."""

import dataclasses
import datetime
import enum
import math
from collections.abc import Callable, Sequence
from functools import cached_property
from typing import ClassVar

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
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
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
)
from literalizer._formatters.format_strings import (
    escape_control_chars,
)
from literalizer._language import (
    NO_HETEROGENEOUS_BEHAVIOR,
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
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    identity_call_ref_identifier,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    no_validate_spec_for_data,
)
from literalizer._types import Value
from literalizer.exceptions import WrapCombinedInFileNotSupportedError


@beartype
def _escape_roc_string_body(value: str) -> str:
    r"""Apply Roc string escapes to *value* (no surrounding quotes).

    Escapes ``\\``, ``"``, ``\r``, ``\n``, ``\t``, the interpolation
    sequences ``$(`` and ``${``, and other C0 control characters via
    ``\u(XXXX)``.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("$(", "\\$(")
        .replace("${", "\\${")
    )
    return escape_control_chars(value=escaped, fmt="\\u({:04x})")


@beartype
def _format_roc_string_literal(value: str) -> str:
    """Wrap *value* in double quotes after applying Roc string escapes."""
    return f'"{_escape_roc_string_body(value=value)}"'


@beartype
def _apply_roc_str_wrapped_date(value: datetime.date, prefix: str) -> str:
    """Format a date as a Roc string via ISO 8601."""
    return f"{prefix}Str {format_date_iso(value=value)}"


def _build_roc_date_iso(
    prefix: str,
) -> Callable[[datetime.date], str]:
    """Build a date formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: datetime.date) -> str:
        """Delegate to module-level implementation."""
        return _apply_roc_str_wrapped_date(value=value, prefix=prefix)

    return _format


@beartype
def _apply_roc_str_wrapped_datetime(
    value: datetime.datetime, prefix: str
) -> str:
    """Format a datetime as a Roc string via ISO 8601."""
    return f"{prefix}Str {format_datetime_iso(value=value)}"


def _build_roc_datetime_iso(
    prefix: str,
) -> Callable[[datetime.datetime], str]:
    """Build a datetime formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: datetime.datetime) -> str:
        """Delegate to module-level implementation."""
        return _apply_roc_str_wrapped_datetime(value=value, prefix=prefix)

    return _format


@beartype
def _apply_roc_bytes_hex(value: bytes, prefix: str) -> str:
    """Format bytes as a Roc hex string."""
    return f"{prefix}Str {format_bytes_hex(value=value)}"


def _build_roc_bytes_hex(
    prefix: str,
) -> Callable[[bytes], str]:
    """Build a bytes formatter that produces ``{prefix}Str`` hex
    constructors.
    """

    def _format(value: bytes) -> str:
        """Delegate to module-level implementation."""
        return _apply_roc_bytes_hex(value=value, prefix=prefix)

    return _format


@beartype
def _apply_roc_bytes_base64(value: bytes, prefix: str) -> str:
    """Format bytes as a Roc base64 string."""
    return f"{prefix}Str {format_bytes_base64(value=value)}"


def _build_roc_bytes_base64(
    prefix: str,
) -> Callable[[bytes], str]:
    """Build a bytes formatter that produces ``{prefix}Str`` base64
    constructors.
    """

    def _format(value: bytes) -> str:
        """Delegate to module-level implementation."""
        return _apply_roc_bytes_base64(value=value, prefix=prefix)

    return _format


@beartype
def _apply_roc_string(value: str, prefix: str) -> str:
    """Format a string with a constructor prefix."""
    return f"{prefix}Str {_format_roc_string_literal(value=value)}"


def _build_roc_str_formatter(
    prefix: str,
) -> Callable[[str], str]:
    """Build a string formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_roc_string(value=value, prefix=prefix)

    return _format


@beartype
def _apply_roc_integer(
    value: int, prefix: str, base: Callable[[int], str]
) -> str:
    """Format an integer with a ``{prefix}Int`` constructor.

    The ``i128`` literal suffix pins the integer type, which the Roc
    inference engine otherwise narrows to the smallest signed/unsigned
    width that fits each individual literal — producing spurious
    list-element-type-mismatch errors when, say, ``255`` (fits ``U8``)
    sits beside ``-10`` (needs a signed type) inside the same
    ``List Val``.
    """
    return f"{prefix}Int {base(value)}i128"


def _build_roc_integer_formatter(
    prefix: str,
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Build an integer formatter that produces ``{prefix}Int``
    constructors.
    """

    def _format(value: int) -> str:
        """Delegate to module-level implementation."""
        return _apply_roc_integer(value=value, prefix=prefix, base=base)

    return _format


@beartype
def _apply_roc_float(
    value: float, prefix: str, inner: Callable[[float], str]
) -> str:
    """Format a float with a ``{prefix}Float`` constructor."""
    return f"{prefix}Float {inner(value)}"


def _build_roc_float_formatter(
    prefix: str,
    inner: Callable[[float], str],
) -> Callable[[float], str]:
    """Build a float formatter that produces ``{prefix}Float``
    constructors.
    """

    def _format(value: float) -> str:
        """Delegate to module-level implementation."""
        return _apply_roc_float(value=value, prefix=prefix, inner=inner)

    return _format


@beartype
def _apply_roc_dict_entry(
    key: str,
    _raw_value: Value,
    formatted_value: str,
    str_prefix: str,
) -> str:
    """Format a dict entry as a tuple with a plain-string key.

    Dict keys are ``Str``, not ``Val``, so the ``{prefix}Str`` constructor
    must be stripped from the formatted key.
    """
    key = key.removeprefix(str_prefix)
    return f"({key}, {formatted_value})"


def _build_roc_dict_entry(
    prefix: str,
) -> Callable[[str, Value, str], str]:
    """Build a dict-entry formatter that strips the ``{prefix}Str`` prefix
    from keys.
    """
    _str_prefix = f"{prefix}Str "

    def _format(key: str, _raw_value: Value, formatted_value: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_roc_dict_entry(
            key=key,
            _raw_value=_raw_value,
            formatted_value=formatted_value,
            str_prefix=_str_prefix,
        )

    return _format


# Backward-compatible module-level aliases used by the Enum members.
_format_roc_date_iso = _build_roc_date_iso(prefix="R")
_format_roc_datetime_iso = _build_roc_datetime_iso(prefix="R")
_format_roc_bytes_hex = _build_roc_bytes_hex(prefix="R")
_format_roc_bytes_base64 = _build_roc_bytes_base64(prefix="R")
_format_roc_string = _build_roc_str_formatter(prefix="R")
_format_roc_integer_decimal = _build_roc_integer_formatter(
    prefix="R",
    base=str,
)
_format_roc_integer_hex = _build_roc_integer_formatter(
    prefix="R",
    base=format_integer_hex,
)
_format_roc_integer_octal = _build_roc_integer_formatter(
    prefix="R",
    base=format_integer_octal,
)
_format_roc_integer_binary = _build_roc_integer_formatter(
    prefix="R",
    base=format_integer_binary,
)
_format_roc_float_repr = _build_roc_float_formatter(
    prefix="R",
    inner=format_float_repr,
)
_format_roc_float_scientific = _build_roc_float_formatter(
    prefix="R",
    inner=format_float_scientific,
)
_format_roc_float_fixed = _build_roc_float_formatter(
    prefix="R",
    inner=format_float_fixed,
)
_roc_dict_entry = _build_roc_dict_entry(prefix="R")


_ROC_INT_BASE: dict[str, Callable[[int], str]] = {
    "DECIMAL": str,
    "HEX": format_integer_hex,
    "OCTAL": format_integer_octal,
    "BINARY": format_integer_binary,
}

_ROC_FLOAT_BASE: dict[str, Callable[[float], str]] = {
    "REPR": format_float_repr,
    "SCIENTIFIC": format_float_scientific,
    "FIXED": format_float_fixed,
}

_ROC_BYTES_FORMATTERS: dict[
    str,
    Callable[[str], Callable[[bytes], str]],
] = {
    "HEX": _build_roc_bytes_hex,
    "BASE64": _build_roc_bytes_base64,
}


@beartype
def _build_roc_body_preamble(
    *,
    type_name: str,
    constructor_prefix: str,
) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
    """Build a callable that computes body-preamble lines for Roc.

    The callable receives the set of types present in the data and
    returns the tag-union type alias with only the constructors that
    are actually needed.
    """

    def _compute(types: frozenset[type], data: Value, /) -> tuple[str, ...]:
        """Return the tag-union type alias for *types*."""
        del data  # unused
        p = constructor_prefix
        constructors = [
            constructor
            for type_set, constructor in (
                (frozenset({type(None)}), f"{p}Null"),
                (frozenset({bool}), f"{p}Bool Bool"),
                (frozenset({int}), f"{p}Int I128"),
                (frozenset({float}), f"{p}Float F64"),
                (
                    frozenset(
                        {str, bytes, datetime.date, datetime.datetime},
                    ),
                    f"{p}Str Str",
                ),
                (frozenset({list}), f"{p}List (List {type_name})"),
                (
                    frozenset({dict, ordereddict}),
                    f"{p}Dict (List (Str, {type_name}))",
                ),
                (frozenset({set}), f"{p}Set (List {type_name})"),
            )
            if types & type_set
        ]
        body = ",\n".join(f"    {c}" for c in constructors)
        return (f"{type_name} : [\n{body},\n]",)

    return _compute


def _roc_format_call_target(parts: Sequence[str]) -> str:
    """Flatten a sequence of call target parts to an underscored Roc
    identifier.

    Roc identifiers cannot contain ``.``, so ``["app", "client",
    "fetch"]`` becomes ``app_client_fetch``.
    """
    return "_".join(parts)


def _roc_type_var(index: int) -> str:
    """Return a unique lowercase identifier for a Roc type variable."""
    letter = chr(ord("a") + index % 26)
    group = index // 26
    if group == 0:
        return letter
    return f"{letter}{group}"  # pragma: no cover


def _roc_call_body_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    /,
) -> tuple[str, ...]:
    """Return Roc top-level function stubs for a call target.

    Dotted names are flattened to underscored identifiers.  Each
    parameter gets a fresh type variable so the stub is polymorphic
    across call sites that pass different argument types.  The stub
    returns the empty record ``{}``.
    """
    flat_name = _roc_format_call_target(parts=parts)
    n = len(params)
    if n == 0:  # pragma: no cover
        sig = f"{flat_name} : {{}}"
        impl = f"{flat_name} = {{}}"
    else:
        type_vars = ", ".join(_roc_type_var(index=i) for i in range(n))
        wildcards = ", ".join("_" for _ in range(n))
        sig = f"{flat_name} : {type_vars} -> {{}}"
        impl = f"{flat_name} = \\{wildcards} -> {{}}"
    return (sig, impl)


@beartype
def _roc_format_call_arg(_value: Value, formatted: str) -> str:
    """Wrap *formatted* in parentheses so multi-token tags like
    ``RInt 1`` are parsed as a single argument by the Roc
    space-separated call syntax.
    """
    return f"({formatted})"


def _indent_call_lines(*, content: str, indent: str) -> str:
    """Indent each line of *content* into a Roc ``main`` body.

    Top-level lines (no leading whitespace) are wrapped in
    ``dbg (...)`` so Roc does not flag the discarded pure-function
    result as an ``UNNECESSARY DEFINITION``.  Continuation lines that
    already start with whitespace are kept as-is so multi-line
    expressions remain syntactically intact.
    """
    out: list[str] = []
    for line in content.split(sep="\n"):
        if not line:  # pragma: no cover
            out.append("")
        elif line[0].isspace():  # pragma: no cover
            out.append(f"{indent}{line}")
        else:
            out.append(f"{indent}dbg ({line})")
    return "\n".join(out)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Roc(metaclass=LanguageCls):
    """Roc language specification.

    The generated output uses custom tag constructors (``RNull``,
    ``RBool``, ``RList``, ``RDict``, ``RSet``) that are wrapped in a
    ``Val`` tag-union type alias emitted in the body preamble.  For
    example, data consisting solely of an integer yields:

    .. code-block:: text

       Val : [
           RInt I128,
       ]

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.ISO`` — ISO 8601 string,
              e.g. ``RStr "2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.ISO`` — ISO 8601 string,
              e.g. ``RStr "2024-01-15T12:30:00"``.

        type_name: Name of the generated tag-union alias.  Defaults to
            ``"Val"``.

        constructor_prefix: Prefix for generated constructor names.
            Defaults to ``"R"``, producing constructors like ``RNull``,
            ``RBool``, ``RInt``, etc.
    """

    extension = ".roc"
    pygments_name = "text"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_variable_names = True
    supports_dotted_calls = True
    supports_special_floats = True

    class DateFormats(enum.Enum):
        """Date format options for Roc."""

        ISO = DateFormatConfig(
            formatter=_format_roc_date_iso,
            type_produced=str,
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Roc."""

        ISO = DatetimeFormatConfig(
            formatter=_format_roc_datetime_iso,
            type_produced=str,
        )

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=_format_roc_bytes_hex)
        BASE64 = enum.member(value=_format_roc_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Roc."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="RList ["),
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

    class SetFormats(enum.Enum):
        """Set type options for Roc."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="RSet ["),
            close="]",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        HASH = CommentConfig(
            prefix="#",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        ASSIGN = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="{name} = {value}"
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
        positive_infinity="RFloat Num.infinity_f64",
        negative_infinity="RFloat -Num.infinity_f64",
        nan="RFloat Num.nan_f64",
    ):
        """Float format options."""

        REPR = enum.member(value=_format_roc_float_repr)
        SCIENTIFIC = enum.member(value=_format_roc_float_scientific)
        FIXED = enum.member(value=_format_roc_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=_format_roc_integer_decimal)
        HEX = enum.member(value=_format_roc_integer_hex)
        OCTAL = enum.member(value=_format_roc_integer_octal)
        BINARY = enum.member(value=_format_roc_integer_binary)

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

        NONE = enum.auto()

    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """Roc call style options."""

        COMMAND = CommandCallStyle(
            arg_separator=" ",
            wrapped_call_template="{wrapper} ({inner})",
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

    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.PASCAL,
    )

    validate_spec_for_data = no_validate_spec_for_data

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a Roc value declaration in a module.

        The module exposes *variable_name* (or ``main`` when empty, in
        call mode) so the file is a syntactically valid Roc module.
        Body-preamble lines (the ``Val`` type alias and any call
        stubs) sit at module scope after the header.  In call mode
        each top-level call expression is wrapped in ``dbg (...)``
        inside ``main``: a plain ``_ = pure_call`` would trip the
        Roc ``UNNECESSARY DEFINITION`` warning, which ``roc check``
        exits non-zero on, whereas ``dbg`` is treated as side
        effecting.

        In call mode the ``Val`` type alias is dropped because nothing
        in the wrapped output annotates a binding with ``: Val`` —
        keeping it would trip the Roc ``UNUSED DEFINITION`` warning
        when the alias has no recursive (``List``/``Dict``/``Set``)
        self-reference for the compiler to consider load-bearing.
        """
        exposed = variable_name or "main"
        if variable_name:
            effective_preamble = body_preamble
        else:
            effective_preamble = self._strip_type_alias(
                body_preamble=body_preamble,
            )
        preamble_str = (
            "\n".join(effective_preamble) + "\n\n"
            if effective_preamble
            else ""
        )
        if not variable_name:
            body = _indent_call_lines(content=content, indent=self.indent)
            content = f"main =\n{body}\n{self.indent}{{}}"
        return f"module [{exposed}]\n\n{preamble_str}{content}"

    def _strip_type_alias(
        self,
        *,
        body_preamble: tuple[str, ...],
    ) -> tuple[str, ...]:
        """Drop the ``Val`` tag-union alias from *body_preamble*.

        Used in call modes where nothing in the wrapped output
        references ``: Val``, so emitting the alias would generate an
        ``UNUSED DEFINITION`` warning in Roc.
        """
        prefix = f"{self.type_name} : ["
        return tuple(
            line for line in body_preamble if not line.startswith(prefix)
        )

    def wrap_calls_with_declarations(
        self,
        declarations: tuple[str, ...],
        calls: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Roc declarations and call expressions in a module.

        Declarations (variable bindings spanning multiple lines) are
        kept verbatim at module scope alongside the ``Val`` type
        alias and call stubs; only the top-level call lines inside
        ``main`` are wrapped in ``dbg (...)``.
        """
        decl_block = "\n".join(declarations) + "\n" if declarations else ""
        body = _indent_call_lines(content=calls, indent=self.indent)
        main_block = f"main =\n{body}\n{self.indent}{{}}"
        effective_preamble = (
            body_preamble
            if declarations
            else self._strip_type_alias(body_preamble=body_preamble)
        )
        preamble_str = (
            "\n".join(effective_preamble) + "\n\n"
            if effective_preamble
            else ""
        )
        return f"module [main]\n\n{preamble_str}{decl_block}{main_block}"

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
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.HASH
    declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN
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
    trailing_comma: TrailingCommas = TrailingCommas.YES
    line_ending: LineEndings = LineEndings.NONE
    call_style: CallStyles = CallStyles.COMMAND
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    indent: str = "    "
    type_name: str = "Val"
    constructor_prefix: str = "R"

    indent_closing_delimiter: ClassVar[bool] = True
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
    def call_style_config(self) -> CallStyle:
        """Configuration for the Roc call style."""
        return self.call_style.value

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
        """Return data-dependent preamble lines (none for Roc — the type
        alias is emitted via :meth:`compute_body_preamble` so it sits
        after the module header inside :meth:`wrap_in_file`).
        """
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
    def format_call_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return stub declarations for a call expression — emitted via
        ``body_preamble`` so they sit after the module header.
        """
        return _roc_call_body_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return file-scope stubs for a call expression."""
        return no_call_stub

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Wrap each call argument in parentheses for the Roc
        space-separated call syntax.
        """
        return _roc_format_call_arg

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into a Roc identifier."""
        return _roc_format_call_target

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
    def null_literal(self) -> str:
        """Literal representing ``None``."""
        return f"{self.constructor_prefix}Null"

    @cached_property
    def true_literal(self) -> str:
        """Literal representing ``True``."""
        return f"{self.constructor_prefix}Bool Bool.true"

    @cached_property
    def false_literal(self) -> str:
        """Literal representing ``False``."""
        return f"{self.constructor_prefix}Bool Bool.false"

    @cached_property
    def _seq_open(self) -> Callable[[list[Value]], str]:
        """Shared sequence opener with configured constructor prefix."""
        return fixed_open(
            open_str=f"{self.constructor_prefix}List [",
        )

    @cached_property
    def _dict_entry(self) -> Callable[[str, Value, str], str]:
        """Shared dict-entry formatter used by dict and ordered-map."""
        return _build_roc_dict_entry(prefix=self.constructor_prefix)

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return dataclasses.replace(
            self.sequence_format.value,
            sequence_open=self._seq_open,
        )

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self._seq_open

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
                open_str=f"{self.constructor_prefix}Dict [",
            ),
            close="]",
            format_entry=self._dict_entry,
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
        if self.constructor_prefix == "R":
            return self.bytes_format
        return _ROC_BYTES_FORMATTERS[self.bytes_format.name](
            self.constructor_prefix,
        )

    @cached_property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a date as a string literal."""
        if self.constructor_prefix == "R":
            return self.date_format
        return _build_roc_date_iso(prefix=self.constructor_prefix)

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        if self.constructor_prefix == "R":
            return self.datetime_format
        return _build_roc_datetime_iso(prefix=self.constructor_prefix)

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        if self.constructor_prefix == "R":
            return _format_roc_string
        return _build_roc_str_formatter(prefix=self.constructor_prefix)

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        if self.constructor_prefix == "R":
            return self.integer_format
        return _build_roc_integer_formatter(
            prefix=self.constructor_prefix,
            base=_ROC_INT_BASE[self.integer_format.name],
        )

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        if self.constructor_prefix == "R":
            return self.float_format
        _pos_inf = f"{self.constructor_prefix}Float Num.infinity_f64"
        _neg_inf = f"{self.constructor_prefix}Float -Num.infinity_f64"
        _nan_val = f"{self.constructor_prefix}Float Num.nan_f64"
        _float_finite = _build_roc_float_formatter(
            prefix=self.constructor_prefix,
            inner=_ROC_FLOAT_BASE[self.float_format.name],
        )

        @beartype
        def _format_float_with_specials(value: float) -> str:
            """Format a float, handling inf and nan."""
            if math.isinf(value):
                return _neg_inf if value < 0 else _pos_inf
            if math.isnan(value):
                return _nan_val
            return _float_finite(value)

        return _format_float_with_specials

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(
                open_str=f"{self.constructor_prefix}Dict [",
            ),
            close="]",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return self._dict_entry

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        _base_declaration = self.declaration_style.value.formatter
        _type_name = self.type_name

        @beartype
        def _roc_declaration(
            name: str,
            value: str,
            data: Value,
            _modifiers: frozenset[enum.Enum],
        ) -> str:
            """Format a Roc variable declaration with type annotation."""
            base = _base_declaration(name, value, data, _modifiers)
            return f"{name} : {_type_name}\n{base}"

        return _roc_declaration

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        return variable_formatter(template="{name} = {value}")

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Roc needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Roc needs none)."""
        return {}

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Emit the tag-union type alias for the types present in the
        data — placed inside :meth:`wrap_in_file` so it sits after the
        module header.
        """
        return _build_roc_body_preamble(
            type_name=self.type_name,
            constructor_prefix=self.constructor_prefix,
        )
