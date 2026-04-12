"""PureScript language specification."""

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
    CallStyleKind,
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
    no_type_hint_preamble,
)
from literalizer._types import Value

if TYPE_CHECKING:
    from collections.abc import Sequence


@beartype
def _format_purescript_date_iso(value: datetime.date) -> str:
    """Format a date as a PureScript string via ISO 8601."""
    return f"PStr {format_date_iso(value=value)}"


@beartype
def _format_purescript_datetime_iso(value: datetime.datetime) -> str:
    """Format a datetime as a PureScript string via ISO 8601."""
    return f"PStr {format_datetime_iso(value=value)}"


@beartype
def _format_purescript_bytes_hex(value: bytes) -> str:
    """Format bytes as a PureScript hex string."""
    return f"PStr {format_bytes_hex(value=value)}"


@beartype
def _format_purescript_bytes_base64(value: bytes) -> str:
    """Format bytes as a PureScript base64 string."""
    return f"PStr {format_bytes_base64(value=value)}"


@beartype
def _format_purescript_integer_decimal(value: int) -> str:
    """Format an integer as a PureScript ``PInt`` constructor."""
    if value < 0:
        return f"PInt ({value})"
    return f"PInt {value}"


@beartype
def _format_purescript_integer_hex(value: int) -> str:
    """Format an integer as a PureScript ``PInt`` hex constructor."""
    hex_repr = format_integer_hex(value=value)
    if value < 0:
        return f"PInt ({hex_repr})"
    return f"PInt {hex_repr}"


@beartype
def _purescript_float_wrapper(
    inner: Callable[[float], str],
) -> Callable[[float], str]:
    """Wrap a float formatter to produce ``PFloat`` constructors."""

    @beartype
    def _format(value: float) -> str:
        """Format a float with a ``PFloat`` constructor."""
        formatted = inner(value)
        if formatted.startswith("-"):
            return f"PFloat ({formatted})"
        return f"PFloat {formatted}"

    return _format


_format_purescript_float_repr = _purescript_float_wrapper(
    inner=format_float_repr,
)
_format_purescript_float_scientific = _purescript_float_wrapper(
    inner=format_float_scientific,
)
_format_purescript_float_fixed = _purescript_float_wrapper(
    inner=format_float_fixed,
)


@beartype
def _format_purescript_string(value: str) -> str:
    """Format a string as a PureScript ``PStr`` constructor."""
    escaped = format_string_backslash_control(
        value=value,
        control_char_fmt="\\x{:02x}",
    )
    return f"PStr {escaped}"


@beartype
def _purescript_dict_entry(key: str, _val: Value, value: str) -> str:
    """Format a dict entry as a ``Tuple`` with a plain-string key.

    Dict keys are ``String``, not ``Val``, so the ``PStr`` constructor
    must be stripped from the formatted key.
    """
    key = key.removeprefix("PStr ")
    return f"(Tuple {key} ({value}))"


@beartype
def _build_purescript_body_preamble() -> Callable[
    [frozenset[type], Value], tuple[str, ...]
]:
    """Build a callable that computes body-preamble lines for PureScript.

    The callable receives the set of types present in the data and returns
    the ``data Val`` declaration with only the constructors that are
    actually needed, plus any necessary imports.
    """

    def _needs_prelude(val: Value) -> bool:
        """Return True if *val* needs ``import Prelude``.

        Prelude is required for ``negate`` (any negative int or float)
        and for ``/`` (infinity / NaN expressed as ``1.0 / 0.0``).
        """
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            if isinstance(val, float):
                return (
                    math.copysign(1, val) < 0
                    or math.isinf(val)
                    or math.isnan(val)
                )
            return val < 0
        if isinstance(val, list):
            return any(_needs_prelude(val=v) for v in val)
        if isinstance(val, dict):
            return any(_needs_prelude(val=v) for v in val.values())
        if isinstance(val, set):
            return any(
                _needs_prelude(val=v)
                for v in val
                if isinstance(v, (int, float)) and not isinstance(v, bool)
            )
        return False

    def _compute(types: frozenset[type], data: Value, /) -> tuple[str, ...]:
        """Return body-preamble lines for the given *types*."""
        needs_tuple = bool(types & {dict, ordereddict})
        constructors = [
            constructor
            for type_set, constructor in (
                (frozenset({type(None)}), "PNull"),
                (frozenset({bool}), "PBool Boolean"),
                (frozenset({int}), "PInt Int"),
                (frozenset({float}), "PFloat Number"),
                (
                    frozenset(
                        {str, bytes, datetime.date, datetime.datetime},
                    ),
                    "PStr String",
                ),
                (frozenset({list}), "PList (Array Val)"),
                (
                    frozenset({dict, ordereddict}),
                    "PDict (Array (Tuple String Val))",
                ),
                (frozenset({set}), "PSet (Array Val)"),
            )
            if types & type_set
        ]
        needs_prelude = bool(types & {int, float}) and _needs_prelude(val=data)
        lines: list[str] = ["import Prelude"] if needs_prelude else []
        if needs_tuple:
            lines.append("data Tuple a b = Tuple a b")
        first_line = f"data Val\n    = {constructors[0]}"
        rest_lines = [f"    | {c}" for c in constructors[1:]]
        lines.append("\n".join([first_line, *rest_lines]))
        return tuple(lines)

    return _compute


@beartype
class PureScript(metaclass=LanguageCls):
    """PureScript language specification.

    The generated output uses custom constructors (``PNull``, ``PBool``,
    ``PList``, ``PDict``, ``PSet``) that are **not** built-in PureScript
    types. To compile the generated code, define a ``Val`` ADT in the
    consuming module:

    .. code-block:: haskell

       import Prelude

       data Tuple a b = Tuple a b

       data Val
           = PNull
           | PBool Boolean
           | PInt Int
           | PFloat Number
           | PStr String
           | PList (Array Val)
           | PDict (Array (Tuple String Val))
           | PSet (Array Val)

    The body preamble automatically emits only the constructors that are
    actually used by the data.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.ISO`` — ISO 8601 string,
              e.g. ``PStr "2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.ISO`` — ISO 8601 string,
              e.g. ``PStr "2024-01-15T12:30:00"``.
    """

    extension = ".purs"
    pygments_name = None
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True

    class DateFormats(enum.Enum):
        """Date format options for PureScript."""

        ISO = DateFormatConfig(
            formatter=_format_purescript_date_iso,
            type_produced=str,
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for PureScript."""

        ISO = DatetimeFormatConfig(
            formatter=_format_purescript_datetime_iso,
            type_produced=str,
        )

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=_format_purescript_bytes_hex)
        BASE64 = enum.member(value=_format_purescript_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for PureScript."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="PList ["),
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
        """Set type options for PureScript."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="PSet ["),
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
        positive_infinity="PFloat (1.0 / 0.0)",
        negative_infinity="PFloat (-(1.0 / 0.0))",
        nan="PFloat (0.0 / 0.0)",
    ):
        """Float format options."""

        REPR = enum.member(value=_format_purescript_float_repr)
        SCIENTIFIC = enum.member(value=_format_purescript_float_scientific)
        FIXED = enum.member(value=_format_purescript_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=_format_purescript_integer_decimal)
        HEX = enum.member(value=_format_purescript_integer_hex)

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
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class LineEndings(enum.Enum):
        """Line ending options."""

        SEMICOLON = "semicolon"

    line_endings = LineEndings

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
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
    ) -> None:
        """Initialize PureScript language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "PNull"
        self.true_literal = "PBool true"
        self.false_literal = "PBool false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="PDict ["),
            close="]",
            format_entry=_purescript_dict_entry,
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
        )
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _format_purescript_string
        self.format_float: Callable[[float], str] = float_format
        self.format_integer: Callable[[int], str] = integer_format
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
        self.string_format = string_format
        self.trailing_comma = trailing_comma
        self.line_ending = line_ending
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="PDict [",
                close="]",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            _purescript_dict_entry
        )
        self.indent = indent
        self.indent_closing_delimiter = True
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.supports_scalar_before_comments = False
        self.supports_scalar_inline_comments = True
        _base_declaration = declaration_style.value.formatter
        _sequence_declared_type = sequence_format.value.declared_type

        @beartype
        def _purescript_declaration(
            name: str,
            value: str,
            data: Value,
        ) -> str:
            """Format a variable declaration with type annotation."""
            base = _base_declaration(name, value, data)
            decl_type = (
                _sequence_declared_type if isinstance(data, list) else "Val"
            )
            return f"{name} :: {decl_type}\n{base}"

        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _purescript_declaration
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
        ] = _build_purescript_body_preamble()
        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.special_float_preamble: tuple[str, ...] = ()
        self.call_style_config: CallStyleConfig = CallStyleConfig(
            kind=CallStyleKind.POSITIONAL,
        )
