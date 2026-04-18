"""Gleam language specification."""

import dataclasses
import datetime
import enum
import math
import textwrap
from collections.abc import Callable, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar

from beartype import beartype

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
from literalizer._formatters.format_integers import (
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    format_integer_underscore,
)
from literalizer._formatters.format_strings import format_string_backslash
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
    body_preamble_from_scalars,
    identity_call_target,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    prepend_body_preamble,
)
from literalizer._types import Value


@beartype
def _gleam_nonneg_only(
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Wrap *base* so negative values fall back to decimal.

    Gleam does not support negative hex/octal/binary literals.
    """

    @beartype
    def _format(value: int) -> str:
        """Format an integer, falling back to decimal for negatives."""
        if value < 0:
            return str(object=value)
        return base(value)

    return _format


def _build_gleam_date_iso(
    prefix: str,
) -> Callable[[datetime.date], str]:
    """Build a date formatter that produces ``{prefix}Str``
    constructors.
    """

    @beartype
    def _format(value: datetime.date) -> str:
        """Format a date as a Gleam string via ISO 8601."""
        return f"{prefix}Str({format_date_iso(value=value)})"

    return _format


def _build_gleam_datetime_iso(
    prefix: str,
) -> Callable[[datetime.datetime], str]:
    """Build a datetime formatter that produces ``{prefix}Str``
    constructors.
    """

    @beartype
    def _format(value: datetime.datetime) -> str:
        """Format a datetime as a Gleam string via ISO 8601."""
        return f"{prefix}Str({format_datetime_iso(value=value)})"

    return _format


def _build_gleam_bytes_hex(
    prefix: str,
) -> Callable[[bytes], str]:
    """Build a bytes formatter that produces ``{prefix}Str`` hex
    constructors.
    """

    @beartype
    def _format(value: bytes) -> str:
        """Format bytes as a Gleam hex string."""
        return f"{prefix}Str({format_bytes_hex(value=value)})"

    return _format


def _build_gleam_bytes_base64(
    prefix: str,
) -> Callable[[bytes], str]:
    """Build a bytes formatter that produces ``{prefix}Str`` base64
    constructors.
    """

    @beartype
    def _format(value: bytes) -> str:
        """Format bytes as a Gleam base64 string."""
        return f"{prefix}Str({format_bytes_base64(value=value)})"

    return _format


def _build_gleam_str_formatter(
    prefix: str,
) -> Callable[[str], str]:
    """Build a string formatter that produces ``{prefix}Str``
    constructors.
    """

    @beartype
    def _format(value: str) -> str:
        """Format a string with a constructor prefix."""
        escaped = format_string_backslash(value)
        return f"{prefix}Str({escaped})"

    return _format


def _build_gleam_integer_wrapper(
    prefix: str,
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Build an integer formatter that produces ``{prefix}Int``
    constructors.
    """

    @beartype
    def _format(value: int) -> str:
        """Format an integer with a ``{prefix}Int`` constructor."""
        return f"{prefix}Int({base(value)})"

    return _format


def _build_gleam_float_wrapper(
    prefix: str,
    inner: Callable[[float], str],
) -> Callable[[float], str]:
    """Build a float formatter that produces ``{prefix}Float``
    constructors.
    """

    @beartype
    def _format(value: float) -> str:
        """Format a float with a ``{prefix}Float`` constructor."""
        return f"{prefix}Float({inner(value)})"

    return _format


def _build_gleam_dict_entry(
    prefix: str,
) -> Callable[[str, Value, str], str]:
    """Build a dict-entry formatter that strips the ``{prefix}Str`` prefix
    from keys.
    """
    _str_prefix = f"{prefix}Str("

    @beartype
    def _format(key: str, _raw_value: Value, formatted_value: str) -> str:
        """Format a dict entry as a hash tuple with a plain-string key.

        Dict keys are ``String``, not ``GVal``, so the ``{prefix}Str(...)``
        constructor must be stripped from the formatted key.
        """
        key = key.removeprefix(_str_prefix).removesuffix(")")
        return f"#({key}, {formatted_value})"

    return _format


# Backward-compatible module-level aliases used by the Enum members.
_format_gleam_date_iso = _build_gleam_date_iso(prefix="G")
_format_gleam_datetime_iso = _build_gleam_datetime_iso(prefix="G")
_format_gleam_bytes_hex = _build_gleam_bytes_hex(prefix="G")
_format_gleam_bytes_base64 = _build_gleam_bytes_base64(prefix="G")
_format_gleam_string = _build_gleam_str_formatter(prefix="G")
_format_gleam_integer_decimal = _build_gleam_integer_wrapper(
    prefix="G",
    base=str,
)
_gleam_integer_wrapper = _build_gleam_integer_wrapper
_gleam_float_wrapper = _build_gleam_float_wrapper
_gleam_dict_entry = _build_gleam_dict_entry(prefix="G")


_GLEAM_INT_BASE: dict[tuple[str, str], Callable[[int], str]] = {
    ("DECIMAL", "NONE"): str,
    ("DECIMAL", "UNDERSCORE"): format_integer_underscore,
    ("HEX", "NONE"): _gleam_nonneg_only(base=format_integer_hex),
    ("HEX", "UNDERSCORE"): _gleam_nonneg_only(base=format_integer_hex),
    ("OCTAL", "NONE"): _gleam_nonneg_only(base=format_integer_octal),
    ("OCTAL", "UNDERSCORE"): _gleam_nonneg_only(base=format_integer_octal),
    ("BINARY", "NONE"): _gleam_nonneg_only(base=format_integer_binary),
    ("BINARY", "UNDERSCORE"): _gleam_nonneg_only(base=format_integer_binary),
}

_GLEAM_FLOAT_BASE: dict[str, Callable[[float], str]] = {
    "REPR": format_float_repr,
    "SCIENTIFIC": format_float_scientific,
    "FIXED": format_float_fixed,
}

_GLEAM_BYTES_FORMATTERS: dict[
    str,
    Callable[[str], Callable[[bytes], str]],
] = {
    "HEX": _build_gleam_bytes_hex,
    "BASE64": _build_gleam_bytes_base64,
}


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Gleam(metaclass=LanguageCls):
    """Gleam language specification.

    The generated output uses custom constructors (``GNull``, ``GBool``,
    ``GList``, ``GDict``, ``GSet``) that are **not** built-in Gleam types.
    To compile the generated code, a ``GVal`` custom type is emitted in
    the body preamble:

    .. code-block:: gleam

       type GVal {
         GNull
         GBool(Bool)
         GInt(Int)
         GFloat(Float)
         GStr(String)
         GList(List(GVal))
         GDict(List(#(String, GVal)))
         GSet(List(GVal))
       }

    The body preamble automatically emits only the constructors that are
    actually used by the data.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.ISO`` — ISO 8601 string,
              e.g. ``GStr("2024-01-15")``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.ISO`` — ISO 8601 string,
              e.g. ``GStr("2024-01-15T12:30:00")``.

        sequence_format: Which Gleam sequence type to use.

            * ``sequence_formats.LIST`` — list literal,
              e.g. ``GList([GInt(1), GInt(2), GInt(3)])``.
            * ``sequence_formats.TUPLE`` — tuple literal,
              e.g. ``#(GInt(1), GInt(2), GInt(3))``.

        type_name: Name of the generated custom type.  Defaults to
            ``"GVal"``.

        constructor_prefix: Prefix for generated constructor names.
            Defaults to ``"G"``, producing constructors like ``GNull``,
            ``GBool``, ``GInt``, etc.
    """

    extension = ".gleam"
    pygments_name = "gleam"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True
    supports_variable_names = True
    supports_dotted_calls = True

    class DateFormats(enum.Enum):
        """Date format options for Gleam."""

        ISO = DateFormatConfig(
            formatter=_format_gleam_date_iso,
            type_produced=str,
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Gleam."""

        ISO = DatetimeFormatConfig(
            formatter=_format_gleam_datetime_iso,
            type_produced=str,
        )

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=_format_gleam_bytes_hex)
        BASE64 = enum.member(value=_format_gleam_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Gleam."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="GList(["),
            close="])",
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
        )
        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="#("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence="#()",
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Gleam."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="GSet(["),
            close="])",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            coerce_mixed_to_str=False,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_SLASH = CommentConfig(
            prefix="//",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        LET = DeclarationStyleConfig(
            formatter=variable_formatter(template="let {name} = {value}"),
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
        positive_infinity="GFloat(todo)",
        negative_infinity="GFloat(todo)",
        nan="GFloat(todo)",
    ):
        """Float format options."""

        REPR = enum.member(
            value=_build_gleam_float_wrapper(
                prefix="G",
                inner=format_float_repr,
            )
        )
        SCIENTIFIC = enum.member(
            value=_build_gleam_float_wrapper(
                prefix="G",
                inner=format_float_scientific,
            )
        )
        FIXED = enum.member(
            value=_build_gleam_float_wrapper(
                prefix="G",
                inner=format_float_fixed,
            )
        )

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = MappingProxyType(
            mapping={
                "NONE": _format_gleam_integer_decimal,
                "UNDERSCORE": _build_gleam_integer_wrapper(
                    prefix="G",
                    base=format_integer_underscore,
                ),
            }
        )
        HEX = MappingProxyType(
            mapping={
                "NONE": _build_gleam_integer_wrapper(
                    prefix="G",
                    base=_gleam_nonneg_only(base=format_integer_hex),
                ),
                "UNDERSCORE": _build_gleam_integer_wrapper(
                    prefix="G",
                    base=_gleam_nonneg_only(base=format_integer_hex),
                ),
            }
        )
        OCTAL = MappingProxyType(
            mapping={
                "NONE": _build_gleam_integer_wrapper(
                    prefix="G",
                    base=_gleam_nonneg_only(base=format_integer_octal),
                ),
                "UNDERSCORE": _build_gleam_integer_wrapper(
                    prefix="G",
                    base=_gleam_nonneg_only(base=format_integer_octal),
                ),
            }
        )
        BINARY = MappingProxyType(
            mapping={
                "NONE": _build_gleam_integer_wrapper(
                    prefix="G",
                    base=_gleam_nonneg_only(base=format_integer_binary),
                ),
                "UNDERSCORE": _build_gleam_integer_wrapper(
                    prefix="G",
                    base=_gleam_nonneg_only(base=format_integer_binary),
                ),
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

        NONE = "none"

    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """Gleam call style options."""

    call_styles = CallStyles

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a Gleam let binding in a main function."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        indented = textwrap.indent(text=content, prefix="  ")
        return f"\npub fn main() {{\n{indented}\n  let _ = {variable_name}\n}}"

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Gleam declaration + assignment in a main function."""
        return Gleam.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
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
    trailing_comma: TrailingCommas = TrailingCommas.YES
    line_ending: LineEndings = LineEndings.NONE
    indent: str = "  "
    type_name: str = "GVal"
    constructor_prefix: str = "G"

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
    call_style_config: ClassVar[CallStyleConfig | None] = None
    format_sequence_entry = staticmethod(passthrough_sequence_entry)
    format_set_entry = staticmethod(passthrough_set_entry)
    data_dependent_preamble = staticmethod(no_data_preamble)
    type_hint_collection_preamble_lines = staticmethod(no_type_hint_preamble)
    format_call_stub = staticmethod(no_call_stub)
    format_call_preamble_stub = staticmethod(no_call_stub)
    format_call_target = staticmethod(identity_call_target)

    @cached_property
    def null_literal(self) -> str:
        """Literal representing ``None``."""
        return f"{self.constructor_prefix}Null"

    @cached_property
    def true_literal(self) -> str:
        """Literal representing ``True``."""
        return f"{self.constructor_prefix}Bool(True)"

    @cached_property
    def false_literal(self) -> str:
        """Literal representing ``False``."""
        return f"{self.constructor_prefix}Bool(False)"

    @cached_property
    def _dict_entry(self) -> Callable[[str, Value, str], str]:
        """Shared dict-entry formatter used by dict and ordered-map."""
        return _build_gleam_dict_entry(prefix=self.constructor_prefix)

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        fmt = self.sequence_format.value
        if self.sequence_format.name == "LIST":
            return dataclasses.replace(
                fmt,
                sequence_open=fixed_sequence_open(
                    open_str=f"{self.constructor_prefix}List([",
                ),
            )
        return fmt

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format_config.sequence_open

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return dataclasses.replace(
            self.set_format.value,
            set_open=fixed_set_open(
                open_str=f"{self.constructor_prefix}Set([",
            ),
        )

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=fixed_dict_open(
                open_str=f"{self.constructor_prefix}Dict([",
            ),
            close="])",
            format_entry=self._dict_entry,
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
        )

    @cached_property
    def trailing_comma_config(self) -> TrailingCommaConfig:
        """Configuration for trailing-comma behavior."""
        return self.trailing_comma.value

    @cached_property
    def format_bytes(self) -> Callable[[bytes], str]:
        """Callable that formats a bytes value as a string literal."""
        if self.constructor_prefix == "G":
            return self.bytes_format
        return _GLEAM_BYTES_FORMATTERS[self.bytes_format.name](
            self.constructor_prefix,
        )

    @cached_property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a date as a string literal."""
        if self.constructor_prefix == "G":
            return self.date_format
        return _build_gleam_date_iso(prefix=self.constructor_prefix)

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        if self.constructor_prefix == "G":
            return self.datetime_format
        return _build_gleam_datetime_iso(prefix=self.constructor_prefix)

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        if self.constructor_prefix == "G":
            return _format_gleam_string
        return _build_gleam_str_formatter(prefix=self.constructor_prefix)

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        if self.constructor_prefix == "G":
            return self.integer_format.get_formatter(
                numeric_separator=self.numeric_separator,
            )
        base = _GLEAM_INT_BASE[
            (self.integer_format.name, self.numeric_separator.name)
        ]
        return _build_gleam_integer_wrapper(
            prefix=self.constructor_prefix,
            base=base,
        )

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        if self.constructor_prefix == "G":
            return self.float_format
        _pos_inf = f"{self.constructor_prefix}Float(todo)"
        _neg_inf = f"{self.constructor_prefix}Float(todo)"
        _nan_val = f"{self.constructor_prefix}Float(todo)"
        _float_finite = _build_gleam_float_wrapper(
            prefix=self.constructor_prefix,
            inner=_GLEAM_FLOAT_BASE[self.float_format.name],
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
            ordered_map_open=fixed_dict_open(
                open_str=f"{self.constructor_prefix}Dict([",
            ),
            close="])",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return self._dict_entry

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats a new variable declaration."""
        return self.declaration_style.value.formatter

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        return variable_formatter(template="let {name} = {value}")

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble with Gleam type declaration."""
        p = self.constructor_prefix
        return dict.fromkeys(
            (
                type(None),
                bool,
                int,
                float,
                str,
                bytes,
                datetime.date,
                datetime.datetime,
                list,
                dict,
                set,
            ),
            (
                f"pub type {self.type_name} {{\n"
                f"  {p}Null\n"
                f"  {p}Bool(Bool)\n"
                f"  {p}Int(Int)\n"
                f"  {p}Float(Float)\n"
                f"  {p}Str(String)\n"
                f"  {p}List(List({self.type_name}))\n"
                f"  {p}Dict(List(#(String, {self.type_name})))\n"
                f"  {p}Set(List({self.type_name}))\n"
                "}",
            ),
        )

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Gleam needs none)."""
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
