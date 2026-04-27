"""Elm language specification."""

import dataclasses
import datetime
import enum
import math
import string
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
from literalizer._formatters.format_integers import format_integer_hex
from literalizer._formatters.format_strings import (
    format_string_backslash_control,
)
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
    identity_call_ref_identifier,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    no_validate_spec_for_data,
)
from literalizer._types import Value


@beartype
def _apply_elm_date_iso(value: datetime.date, prefix: str) -> str:
    """Format a date as an Elm string via ISO 8601."""
    return f"{prefix}Str {format_date_iso(value=value)}"


def _build_elm_date_iso(
    prefix: str,
) -> Callable[[datetime.date], str]:
    """Build a date formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: datetime.date) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_date_iso(value=value, prefix=prefix)

    return _format


@beartype
def _apply_elm_datetime_iso(value: datetime.datetime, prefix: str) -> str:
    """Format a datetime as an Elm string via ISO 8601."""
    return f"{prefix}Str {format_datetime_iso(value=value)}"


def _build_elm_datetime_iso(
    prefix: str,
) -> Callable[[datetime.datetime], str]:
    """Build a datetime formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: datetime.datetime) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_datetime_iso(value=value, prefix=prefix)

    return _format


@beartype
def _apply_elm_bytes_hex(value: bytes, prefix: str) -> str:
    """Format bytes as an Elm hex string."""
    return f"{prefix}Str {format_bytes_hex(value=value)}"


def _build_elm_bytes_hex(
    prefix: str,
) -> Callable[[bytes], str]:
    """Build a bytes formatter that produces ``{prefix}Str`` hex
    constructors.
    """

    def _format(value: bytes) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_bytes_hex(value=value, prefix=prefix)

    return _format


@beartype
def _apply_elm_bytes_base64(value: bytes, prefix: str) -> str:
    """Format bytes as an Elm base64 string."""
    return f"{prefix}Str {format_bytes_base64(value=value)}"


def _build_elm_bytes_base64(
    prefix: str,
) -> Callable[[bytes], str]:
    """Build a bytes formatter that produces ``{prefix}Str`` base64
    constructors.
    """

    def _format(value: bytes) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_bytes_base64(value=value, prefix=prefix)

    return _format


@beartype
def _apply_elm_integer_formatter(
    value: int, prefix: str, base: Callable[[int], str]
) -> str:
    """Format an integer with a constructor prefix."""
    formatted = base(value)
    if value < 0:
        return f"{prefix}Int ({formatted})"
    return f"{prefix}Int {formatted}"


def _build_elm_integer_formatter(
    prefix: str,
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Build an integer formatter that produces ``{prefix}Int``
    constructors.
    """

    def _format(value: int) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_integer_formatter(
            value=value, prefix=prefix, base=base
        )

    return _format


@beartype
def _apply_elm_float_wrapper(
    value: float, prefix: str, inner: Callable[[float], str]
) -> str:
    """Format a float with a constructor prefix."""
    formatted = inner(value)
    if formatted.startswith("-"):
        return f"{prefix}Float ({formatted})"
    return f"{prefix}Float {formatted}"


def _build_elm_float_wrapper(
    prefix: str,
    inner: Callable[[float], str],
) -> Callable[[float], str]:
    """Build a float formatter that produces ``{prefix}Float``
    constructors.
    """

    def _format(value: float) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_float_wrapper(
            value=value, prefix=prefix, inner=inner
        )

    return _format


@beartype
def _apply_elm_string(value: str, prefix: str) -> str:
    """Format a string with a constructor prefix."""
    escaped = format_string_backslash_control(
        value=value,
        control_char_fmt="\\u{{{:04x}}}",
    )
    return f"{prefix}Str {escaped}"


def _build_elm_str_formatter(
    prefix: str,
) -> Callable[[str], str]:
    """Build a string formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_string(value=value, prefix=prefix)

    return _format


@beartype
def _apply_elm_dict_entry(
    key: str,
    _raw_value: Value,
    formatted_value: str,
    str_prefix: str,
) -> str:
    """Format a dict entry as a tuple with a plain-string key.

    Dict keys are ``String``, not ``Val``, so the ``{prefix}Str``
    constructor must be stripped from the formatted key.
    """
    key = key.removeprefix(str_prefix)
    return f"({key}, {formatted_value})"


def _build_elm_dict_entry(
    prefix: str,
) -> Callable[[str, Value, str], str]:
    """Build a dict-entry formatter that strips the ``{prefix}Str`` prefix
    from keys.
    """
    _str_prefix = f"{prefix}Str "

    def _format(key: str, _raw_value: Value, formatted_value: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_dict_entry(
            key=key,
            _raw_value=_raw_value,
            formatted_value=formatted_value,
            str_prefix=_str_prefix,
        )

    return _format


# Backward-compatible module-level aliases used by the Enum members.
_format_elm_date_iso = _build_elm_date_iso(prefix="E")
_format_elm_datetime_iso = _build_elm_datetime_iso(prefix="E")
_format_elm_bytes_hex = _build_elm_bytes_hex(prefix="E")
_format_elm_bytes_base64 = _build_elm_bytes_base64(prefix="E")
_format_elm_integer_decimal = _build_elm_integer_formatter(
    prefix="E",
    base=str,
)
_format_elm_integer_hex = _build_elm_integer_formatter(
    prefix="E",
    base=format_integer_hex,
)
_format_elm_float_repr = _build_elm_float_wrapper(
    prefix="E",
    inner=format_float_repr,
)
_format_elm_float_scientific = _build_elm_float_wrapper(
    prefix="E",
    inner=format_float_scientific,
)
_format_elm_float_fixed = _build_elm_float_wrapper(
    prefix="E",
    inner=format_float_fixed,
)
_format_elm_string = _build_elm_str_formatter(prefix="E")
_elm_dict_entry = _build_elm_dict_entry(prefix="E")


@beartype
def _build_elm_body_preamble(
    *,
    type_name: str,
    constructor_prefix: str,
) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
    """Build a callable that computes body-preamble lines for Elm.

    The callable receives the set of types present in the data and returns
    the type declaration with only the constructors that are actually
    needed.
    """

    def _compute(types: frozenset[type], data: Value, /) -> tuple[str, ...]:
        """Return body-preamble lines for the given *types*."""
        del data  # unused
        p = constructor_prefix
        constructors = [
            constructor
            for type_set, constructor in (
                (frozenset({type(None)}), f"{p}Null"),
                (frozenset({bool}), f"{p}Bool Bool"),
                (frozenset({int}), f"{p}Int Int"),
                (frozenset({float}), f"{p}Float Float"),
                (
                    frozenset(
                        {str, bytes, datetime.date, datetime.datetime},
                    ),
                    f"{p}Str String",
                ),
                (frozenset({list}), f"{p}List (List {type_name})"),
                (
                    frozenset({dict, ordereddict}),
                    f"{p}Dict (List ( String, {type_name} ))",
                ),
                (frozenset({set}), f"{p}Set (List {type_name})"),
            )
            if types & type_set
        ]
        first_line = f"type {type_name}\n    = {constructors[0]}"
        rest_lines = [f"    | {c}" for c in constructors[1:]]
        return ("\n".join([first_line, *rest_lines]),)

    return _compute


def _elm_flatten_dotted(name: str) -> str:
    """Flatten a dotted call target to an Elm identifier.

    Elm identifiers cannot contain ``.``, so ``app.client.fetch``
    becomes ``appClientFetch`` (each part after the first is
    capitalized and the dots are dropped).
    """
    parts = name.split(sep=".")
    if len(parts) == 1:
        return name
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def _elm_call_stub(
    name: str,
    params: Sequence[str],
    _stub_return: StubReturn,
    /,
) -> tuple[str, ...]:
    """Return Elm top-level stub declarations for a call target.

    Dotted names are flattened (each part after the first is
    capitalized).  For a single parameter the stub is polymorphic
    (``a -> ()``); for multiple parameters the stub takes a tuple
    (``( a, b ) -> ()``), matching the tuple that
    ``PositionalCallStyle`` emits at the call site.
    """
    flat_name = _elm_flatten_dotted(name=name)
    n = len(params)
    if n == 0:  # pragma: no cover
        type_sig = f"{flat_name} : ()"
        impl = f"{flat_name} = ()"
    elif n == 1:
        type_sig = f"{flat_name} : a -> ()"
        impl = f"{flat_name} _ = ()"
    else:
        _alphabet_size = len(string.ascii_lowercase)
        type_vars = ", ".join(
            chr(ord("a") + (i % _alphabet_size))
            + (str(object=i // _alphabet_size) if i >= _alphabet_size else "")
            for i in range(n)
        )
        type_sig = f"{flat_name} : ( {type_vars} ) -> ()"
        impl = f"{flat_name} _ = ()"
    return (type_sig, impl)


_INT_BASE: dict[str, Callable[[int], str]] = {
    "DECIMAL": str,
    "HEX": format_integer_hex,
}

_FLOAT_BASE: dict[str, Callable[[float], str]] = {
    "REPR": format_float_repr,
    "SCIENTIFIC": format_float_scientific,
    "FIXED": format_float_fixed,
}

_BYTES_FORMATTERS: dict[
    str,
    Callable[[str], Callable[[bytes], str]],
] = {
    "HEX": _build_elm_bytes_hex,
    "BASE64": _build_elm_bytes_base64,
}

_ELM_PLATFORM_WORKER_SUFFIX: str = (
    "\n    in\n"
    "    Platform.worker\n"
    "        { init = \\_ -> ( (), Cmd.none )\n"
    "        , update = \\_ m -> ( m, Cmd.none )\n"
    "        , subscriptions = \\_ -> Sub.none\n"
    "        }"
)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Elm(metaclass=LanguageCls):
    """Elm language specification.

    The generated output uses custom constructors (``ENull``, ``EBool``,
    ``EList``, ``EDict``, ``ESet``) that are **not** built-in Elm types.
    To compile the generated code, define a ``Val`` custom type in the
    consuming module:

    .. code-block:: elm

       type Val
           = ENull
           | EBool Bool
           | EInt Int
           | EFloat Float
           | EStr String
           | EList (List Val)
           | EDict (List ( String, Val ))
           | ESet (List Val)

    The body preamble automatically emits only the constructors that are
    actually used by the data.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.ISO`` — ISO 8601 string,
              e.g. ``EStr "2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.ISO`` — ISO 8601 string,
              e.g. ``EStr "2024-01-15T12:30:00"``.

        type_name: Name of the generated custom type.  Defaults to
            ``"Val"``.

        constructor_prefix: Prefix for generated constructor names.
            Defaults to ``"E"``, producing constructors like ``ENull``,
            ``EBool``, ``EInt``, etc.
    """

    extension = ".elm"
    pygments_name = "elm"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True
    supports_variable_names = True
    supports_dotted_calls = True

    class DateFormats(enum.Enum):
        """Date format options for Elm."""

        ISO = DateFormatConfig(
            formatter=_format_elm_date_iso,
            type_produced=str,
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Elm."""

        ISO = DatetimeFormatConfig(
            formatter=_format_elm_datetime_iso,
            type_produced=str,
        )

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=_format_elm_bytes_hex)
        BASE64 = enum.member(value=_format_elm_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Elm."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="EList ["),
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
            declared_type="Val",
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Elm."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="ESet ["),
            close="]",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_DASH = CommentConfig(
            prefix="--",
            suffix="",
        )
        BLOCK = CommentConfig(
            prefix="{-",
            suffix=" -}",
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
        positive_infinity="EFloat (1 / 0)",
        negative_infinity="EFloat (-(1 / 0))",
        nan="EFloat (0 / 0)",
    ):
        """Float format options."""

        REPR = enum.member(value=_format_elm_float_repr)
        SCIENTIFIC = enum.member(value=_format_elm_float_scientific)
        FIXED = enum.member(value=_format_elm_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=_format_elm_integer_decimal)
        HEX = enum.member(value=_format_elm_integer_hex)

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
        """Elm call style options."""

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
        IdentifierCase.CAMEL,
        IdentifierCase.PASCAL,
    )

    validate_spec_for_data = no_validate_spec_for_data

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap an Elm value declaration in a module.

        When *variable_name* is empty (call mode), each call expression
        in *content* is bound via ``_ = …`` inside a ``let`` block so
        the generated file is syntactically valid Elm.
        """
        preamble = "\n".join(body_preamble)
        if not variable_name:
            let_lines: list[str] = []
            for line in content.split(sep="\n"):
                if not line:  # pragma: no cover
                    let_lines.append("")
                elif not line[0].isspace():
                    let_lines.append(f"        _ = {line}")
                else:  # pragma: no cover
                    let_lines.append(f"        {line}")
            return (
                f"module Check exposing (..)\n\n\n"
                f"{preamble}\n\n\n"
                "main : Program () () Never\nmain =\n    let\n"
                + "\n".join(let_lines)
                + _ELM_PLATFORM_WORKER_SUFFIX
            )
        return f"module Check exposing (..)\n\n\n{preamble}\n\n\n{content}"

    @staticmethod
    def wrap_calls_with_declarations(
        declarations: tuple[str, ...],
        calls: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Elm declarations and call expressions in a module.

        Both variable declarations and call statements are placed inside
        a ``let`` block so the generated file is a valid Elm module.
        Declarations are indented without a ``_ =`` prefix; call
        statements are bound via ``_ = …`` to satisfy Elm's requirement
        that every ``let`` binding produces a value.
        """
        preamble = "\n".join(body_preamble)
        let_lines: list[str] = []
        for decl in declarations:
            for line in decl.split(sep="\n"):
                if not line:  # pragma: no cover
                    let_lines.append("")
                else:
                    let_lines.append(f"        {line}")
        for line in calls.split(sep="\n"):
            if not line:  # pragma: no cover
                let_lines.append("")
            elif not line[0].isspace():
                let_lines.append(f"        _ = {line}")
            else:  # pragma: no cover
                let_lines.append(f"        {line}")
        return (
            f"module Check exposing (..)\n\n\n"
            f"{preamble}\n\n\n"
            "main : Program () () Never\nmain =\n    let\n"
            + "\n".join(let_lines)
            + _ELM_PLATFORM_WORKER_SUFFIX
        )

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
        raise NotImplementedError

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.DOUBLE_DASH
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
    trailing_comma: TrailingCommas = TrailingCommas.NO
    line_ending: LineEndings = LineEndings.SEMICOLON
    call_style: CallStyles = CallStyles.POSITIONAL
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    indent: str = "    "
    type_name: str = "Val"
    constructor_prefix: str = "E"

    indent_closing_delimiter: ClassVar[bool] = True
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = True
    statement_terminator: ClassVar[str] = ""
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
    def type_hint_collection_preamble_lines(
        self,
    ) -> Callable[[frozenset[type]], tuple[str, ...]]:
        """Return preamble lines for empty-collection type hints."""
        return no_type_hint_preamble

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for Elm's call style."""
        return self.call_style.value

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[[str, Sequence[str], StubReturn], tuple[str, ...]]:
        """Return stub declarations for a call expression."""
        return _elm_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[[str, Sequence[str], StubReturn], tuple[str, ...]]:
        """Return file-scope stubs for a call expression."""
        return no_call_stub

    @cached_property
    def format_call_target(self) -> Callable[[str], str]:
        """Rewrite a dotted call target into an Elm identifier.

        Parts after the first are capitalized and the dots are
        dropped (e.g. ``app.client.fetch`` becomes
        ``appClientFetch``).
        """
        return _elm_flatten_dotted

    @cached_property
    def format_call_ref_identifier(self) -> Callable[[str], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier into the
        language's call expression syntax.
        """
        return identity_call_ref_identifier

    @cached_property
    def null_literal(self) -> str:
        """Literal representing ``None``."""
        return f"{self.constructor_prefix}Null"

    @cached_property
    def true_literal(self) -> str:
        """Literal representing ``True``."""
        return f"{self.constructor_prefix}Bool True"

    @cached_property
    def false_literal(self) -> str:
        """Literal representing ``False``."""
        return f"{self.constructor_prefix}Bool False"

    @cached_property
    def _seq_open(self) -> Callable[[list[Value]], str]:
        """Shared sequence opener with configured constructor prefix."""
        return fixed_open(
            open_str=f"{self.constructor_prefix}List [",
        )

    @cached_property
    def _dict_entry(self) -> Callable[[str, Value, str], str]:
        """Shared dict-entry formatter used by dict and ordered-map."""
        return _build_elm_dict_entry(prefix=self.constructor_prefix)

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return dataclasses.replace(
            self.sequence_format.value,
            sequence_open=self._seq_open,
        )

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
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self._seq_open

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
        if self.constructor_prefix == "E":
            return self.bytes_format
        return _BYTES_FORMATTERS[self.bytes_format.name](
            self.constructor_prefix,
        )

    @cached_property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a date as a string literal."""
        if self.constructor_prefix == "E":
            return self.date_format
        return _build_elm_date_iso(prefix=self.constructor_prefix)

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        if self.constructor_prefix == "E":
            return self.datetime_format
        return _build_elm_datetime_iso(prefix=self.constructor_prefix)

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        if self.constructor_prefix == "E":
            return _format_elm_string
        return _build_elm_str_formatter(prefix=self.constructor_prefix)

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        if self.constructor_prefix == "E":
            return self.integer_format
        return _build_elm_integer_formatter(
            prefix=self.constructor_prefix,
            base=_INT_BASE[self.integer_format.name],
        )

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        if self.constructor_prefix == "E":
            return self.float_format
        _pos_inf = f"{self.constructor_prefix}Float (1 / 0)"
        _neg_inf = f"{self.constructor_prefix}Float (-(1 / 0))"
        _nan_val = f"{self.constructor_prefix}Float (0 / 0)"
        _float_finite = _build_elm_float_wrapper(
            prefix=self.constructor_prefix,
            inner=_FLOAT_BASE[self.float_format.name],
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
        _raw_declared = self.sequence_format.value.declared_type
        _type_name = self.type_name
        _sequence_declared_type = (
            _raw_declared.replace("Val", _type_name)
            if _raw_declared is not None
            else None
        )

        @beartype
        def _elm_declaration(
            name: str,
            value: str,
            data: Value,
            _modifiers: frozenset[enum.Enum],
        ) -> str:
            """Format a variable declaration with type annotation."""
            base = _base_declaration(name, value, data, _modifiers)
            decl_type = (
                _sequence_declared_type
                if isinstance(data, list)
                else _type_name
            )
            return f"{name} : {decl_type}\n{base}"

        return _elm_declaration

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        return variable_formatter(template="{name} = {value}")

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Elm needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Elm needs none)."""
        return {}

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines using Elm type declaration."""
        return _build_elm_body_preamble(
            type_name=self.type_name,
            constructor_prefix=self.constructor_prefix,
        )
