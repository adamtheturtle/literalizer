"""Elm language specification."""

import dataclasses
import datetime
import enum
import math
from collections.abc import Callable
from typing import TYPE_CHECKING

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._formatters.collection_openers import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
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
    CallStyleConfig,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
    TrailingCommaConfig,
    identity_call_target,
    no_call_stub,
    no_type_hint_preamble,
)
from literalizer._types import Value

if TYPE_CHECKING:
    from collections.abc import Sequence


def _build_elm_date_iso(
    prefix: str,
) -> Callable[[datetime.date], str]:
    """Build a date formatter that produces ``{prefix}Str``
    constructors.
    """

    @beartype
    def _format(value: datetime.date) -> str:
        """Format a date as an Elm string via ISO 8601."""
        return f"{prefix}Str {format_date_iso(value=value)}"

    return _format


def _build_elm_datetime_iso(
    prefix: str,
) -> Callable[[datetime.datetime], str]:
    """Build a datetime formatter that produces ``{prefix}Str``
    constructors.
    """

    @beartype
    def _format(value: datetime.datetime) -> str:
        """Format a datetime as an Elm string via ISO 8601."""
        return f"{prefix}Str {format_datetime_iso(value=value)}"

    return _format


def _build_elm_bytes_hex(
    prefix: str,
) -> Callable[[bytes], str]:
    """Build a bytes formatter that produces ``{prefix}Str`` hex
    constructors.
    """

    @beartype
    def _format(value: bytes) -> str:
        """Format bytes as an Elm hex string."""
        return f"{prefix}Str {format_bytes_hex(value=value)}"

    return _format


def _build_elm_bytes_base64(
    prefix: str,
) -> Callable[[bytes], str]:
    """Build a bytes formatter that produces ``{prefix}Str`` base64
    constructors.
    """

    @beartype
    def _format(value: bytes) -> str:
        """Format bytes as an Elm base64 string."""
        return f"{prefix}Str {format_bytes_base64(value=value)}"

    return _format


def _build_elm_integer_formatter(
    prefix: str,
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Build an integer formatter that produces ``{prefix}Int``
    constructors.
    """

    @beartype
    def _format(value: int) -> str:
        """Format an integer with a constructor prefix."""
        formatted = base(value)
        if value < 0:
            return f"{prefix}Int ({formatted})"
        return f"{prefix}Int {formatted}"

    return _format


def _build_elm_float_wrapper(
    prefix: str,
    inner: Callable[[float], str],
) -> Callable[[float], str]:
    """Build a float formatter that produces ``{prefix}Float``
    constructors.
    """

    @beartype
    def _format(value: float) -> str:
        """Format a float with a constructor prefix."""
        formatted = inner(value)
        if formatted.startswith("-"):
            return f"{prefix}Float ({formatted})"
        return f"{prefix}Float {formatted}"

    return _format


def _build_elm_str_formatter(
    prefix: str,
) -> Callable[[str], str]:
    """Build a string formatter that produces ``{prefix}Str``
    constructors.
    """

    @beartype
    def _format(value: str) -> str:
        """Format a string with a constructor prefix."""
        escaped = format_string_backslash_control(
            value=value,
            control_char_fmt="\\u{{{:04x}}}",
        )
        return f"{prefix}Str {escaped}"

    return _format


def _build_elm_dict_entry(
    prefix: str,
) -> Callable[[str, Value, str], str]:
    """Build a dict-entry formatter that strips the ``{prefix}Str`` prefix
    from keys.
    """
    _str_prefix = f"{prefix}Str "

    @beartype
    def _format(key: str, _raw_value: Value, formatted_value: str) -> str:
        """Format a dict entry as a tuple with a plain-string key.

        Dict keys are ``String``, not ``Val``, so the ``{prefix}Str``
        constructor must be stripped from the formatted key.
        """
        key = key.removeprefix(_str_prefix)
        return f"({key}, {formatted_value})"

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


@beartype
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
            sequence_open=fixed_sequence_open(open_str="EList ["),
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
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Elm."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="ESet ["),
            close="]",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            coerce_mixed_to_str=False,
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
            formatter=variable_formatter(template="{name} = {value}"),
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

    call_styles = CallStyles

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap an Elm value declaration in a module."""
        del variable_name
        preamble = "\n".join(body_preamble)
        return f"module Check exposing (..)\n\n\n{preamble}\n\n\n{content}"

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Elm declaration + assignment in a module."""
        return Elm.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    def __init__(  # noqa: PLR0915
        self,
        *,
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.DOUBLE_DASH,
        declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN,
        dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT,
        dict_format: DictFormats = DictFormats.DEFAULT,
        float_format: FloatFormats = FloatFormats.REPR,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_literal_suffix: NumericLiteralSuffixes = (
            NumericLiteralSuffixes.NONE
        ),
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        numeric_style: NumericStyles = NumericStyles.OVERLOADED,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
        type_name: str = "Val",
        constructor_prefix: str = "E",
    ) -> None:
        """Initialize Elm language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal: str = f"{constructor_prefix}Null"
        self.true_literal: str = f"{constructor_prefix}Bool True"
        self.false_literal: str = f"{constructor_prefix}Bool False"
        fmt = sequence_format.value
        _seq_open = fixed_sequence_open(
            open_str=f"{constructor_prefix}List [",
        )
        self.sequence_format_config: SequenceFormatConfig = (
            dataclasses.replace(fmt, sequence_open=_seq_open)
        )
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = dataclasses.replace(
            set_format.value,
            set_open=fixed_set_open(
                open_str=f"{constructor_prefix}Set [",
            ),
        )
        self.sequence_open: Callable[[list[Value]], str] = _seq_open
        _dict_entry = _build_elm_dict_entry(prefix=constructor_prefix)
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            dict_open=fixed_dict_open(
                open_str=f"{constructor_prefix}Dict [",
            ),
            close="]",
            format_entry=_dict_entry,
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
        )
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        if constructor_prefix == "E":
            self.format_bytes: Callable[[bytes], str] = bytes_format
            self.format_date: Callable[[datetime.date], str] = date_format
            self.format_datetime: Callable[[datetime.datetime], str] = (
                datetime_format
            )
            self.format_string: Callable[[str], str] = _format_elm_string
            self.format_integer: Callable[[int], str] = integer_format
        else:
            self.format_bytes = _BYTES_FORMATTERS[bytes_format.name](
                constructor_prefix
            )
            self.format_date = _build_elm_date_iso(prefix=constructor_prefix)
            self.format_datetime = _build_elm_datetime_iso(
                prefix=constructor_prefix
            )
            self.format_string = _build_elm_str_formatter(
                prefix=constructor_prefix,
            )
            self.format_integer = _build_elm_integer_formatter(
                prefix=constructor_prefix,
                base=_INT_BASE[integer_format.name],
            )

        if constructor_prefix == "E":
            self.format_float: Callable[[float], str] = float_format
        else:
            _pos_inf = f"{constructor_prefix}Float (1 / 0)"
            _neg_inf = f"{constructor_prefix}Float (-(1 / 0))"
            _nan_val = f"{constructor_prefix}Float (0 / 0)"
            _float_finite = _build_elm_float_wrapper(
                prefix=constructor_prefix,
                inner=_FLOAT_BASE[float_format.name],
            )

            @beartype
            def _format_float_with_specials(value: float) -> str:
                """Format a float, handling inf and nan."""
                if math.isinf(value):
                    return _neg_inf if value < 0 else _pos_inf
                if math.isnan(value):
                    return _nan_val
                return _float_finite(value)

            self.format_float = _format_float_with_specials
        self.format_sequence_entry: Callable[[Value, str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[Value, str], str] = (
            passthrough_set_entry
        )
        self.comment_format = comment_format
        self.declaration_style = declaration_style
        self.dict_entry_style = dict_entry_style
        self.dict_format = dict_format
        self.float_format = float_format
        self.integer_format = integer_format
        self.numeric_literal_suffix = numeric_literal_suffix
        self.numeric_separator = numeric_separator
        self.numeric_style = numeric_style
        self.string_format = string_format
        self.trailing_comma = trailing_comma
        self.line_ending = line_ending
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str=f"{constructor_prefix}Dict [",
                close="]",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            _dict_entry
        )
        self.indent = indent
        self.indent_closing_delimiter = True
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.supports_scalar_before_comments = False
        self.supports_scalar_inline_comments = True
        _base_declaration = declaration_style.value.formatter
        _raw_declared = sequence_format.value.declared_type
        _sequence_declared_type = (
            _raw_declared.replace("Val", type_name)
            if _raw_declared is not None
            else None
        )

        @beartype
        def _elm_declaration(
            name: str,
            value: str,
            data: Value,
        ) -> str:
            """Format a variable declaration with type annotation."""
            base = _base_declaration(name, value, data)
            decl_type = (
                _sequence_declared_type
                if isinstance(data, list)
                else type_name
            )
            return f"{name} : {decl_type}\n{base}"

        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _elm_declaration
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name} = {value}")
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = _build_elm_body_preamble(
            type_name=type_name,
            constructor_prefix=constructor_prefix,
        )
        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.special_float_preamble: tuple[str, ...] = ()
        self.call_style_config: CallStyleConfig | None = None
        self.statement_terminator = ""
        self.format_call_stub = no_call_stub
        self.format_call_preamble_stub = no_call_stub
        self.format_call_target = identity_call_target
