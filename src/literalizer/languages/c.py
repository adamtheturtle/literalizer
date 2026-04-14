"""C language specification."""

import collections.abc
import datetime
import enum
from typing import TYPE_CHECKING

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
    braced_dict_entry,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    format_integer_hex,
    make_long_suffix_formatter,
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
    no_type_hint_preamble,
    prepend_body_preamble,
)
from literalizer._types import Value

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


@beartype
def _make_format_c_entry(
    *,
    int_field: str,
    float_field: str,
    string_field: str,
) -> collections.abc.Callable[[Value, str], str]:
    """Return a formatter that wraps values in the appropriate
    ``CVal`` union literal using the given field names.
    """

    @beartype
    def _format_c_entry(original: Value, formatted: str) -> str:
        """Wrap a formatted entry in the appropriate union literal."""
        match original:
            case str() | bytes() | datetime.date():
                return f"((CVal){{.{string_field} = {formatted}}})"
            case bool():
                return formatted
            case int():
                return f"((CVal){{.{int_field} = {formatted}}})"
            case float():
                return f"((CVal){{.{float_field} = {formatted}}})"
            case _:
                return formatted

    return _format_c_entry


@beartype
class C(metaclass=LanguageCls):
    """C language specification."""

    extension = ".c"
    pygments_name = "c"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True
    supports_variable_names = True
    supports_dotted_calls = True

    class DateFormats(enum.Enum):
        """Date format options for C."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for C."""

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
        """Sequence type options for C."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(
                open_str="((CVal){.a = (CVal[]){",
            ),
            close="}})",
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

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for C."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="((CVal){.a = (CVal[]){"),
            close="}})",
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
        BLOCK = CommentConfig(
            prefix="/*",
            suffix=" */",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        TYPED = DeclarationStyleConfig(
            formatter=lambda name, value, _data: f"CVal {name} = {value};",
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
        positive_infinity="INFINITY",
        negative_infinity="-INFINITY",
        nan="NAN",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=str)
        HEX = enum.member(value=format_integer_hex)

        def __call__(self, value: int, /) -> str:
            """Format an integer."""
            formatter: Callable[[int], str] = self.value
            return formatter(value)

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()
        AUTO = enum.auto()

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

        SEMICOLON = "semicolon"

    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """C call style options."""

    call_styles = CallStyles

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a C declaration in a function."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        use_line = f"\n    (void){variable_name};" if variable_name else ""
        return f"void check_(void) {{\n{content}{use_line}\n}}"

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap C declaration + assignment in a function."""
        return C.wrap_in_file(
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
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        declaration_style: DeclarationStyles = DeclarationStyles.TYPED,
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
        trailing_comma: TrailingCommas = TrailingCommas.YES,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
        bool_field: str = "b",
        int_field: str = "i",
        float_field: str = "f",
        string_field: str = "s",
        array_field: str = "a",
        map_field: str = "m",
        key_field: str = "k",
        value_field: str = "v",
    ) -> None:
        """Initialize C language specification."""
        format_entry = _make_format_c_entry(
            int_field=int_field,
            float_field=float_field,
            string_field=string_field,
        )
        seq_open = f"((CVal){{.{array_field} = (CVal[]){{"
        map_open = f"((CVal){{.{map_field} = (CKV[]){{"
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal: str = f"((CVal){{.{string_field} = NULL}})"
        self.true_literal: str = f"((CVal){{.{bool_field} = true}})"
        self.false_literal: str = f"((CVal){{.{bool_field} = false}})"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = (
            SequenceFormatConfig(
                sequence_open=fixed_sequence_open(open_str=seq_open),
                close="}})",
                supports_heterogeneity=fmt.supports_heterogeneity,
                single_element_trailing_comma=(
                    fmt.single_element_trailing_comma
                ),
                supports_trailing_comma=fmt.supports_trailing_comma,
                empty_sequence=fmt.empty_sequence,
                preamble_lines=fmt.preamble_lines,
                format_entry=fmt.format_entry,
                typed_opener_fallback=fmt.typed_opener_fallback,
                uses_typed_literal_for_scalars=(
                    fmt.uses_typed_literal_for_scalars
                ),
                requires_uniform_record_shapes=(
                    fmt.requires_uniform_record_shapes
                ),
                declared_type=fmt.declared_type,
            )
        )
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = SetFormatConfig(
            set_open=fixed_set_open(open_str=seq_open),
            close="}})",
            empty_set=set_format.value.empty_set,
            preamble_lines=set_format.value.preamble_lines,
            set_opener_template=set_format.value.set_opener_template,
            coerce_mixed_to_str=set_format.value.coerce_mixed_to_str,
        )
        self.sequence_open: Callable[[list[Value]], str] = (
            self.sequence_format_config.sequence_open
        )
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            dict_open=fixed_dict_open(open_str=map_open),
            close="}})",
            format_entry=braced_dict_entry(
                format_value=format_entry,
            ),
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
        self.format_string: Callable[[str], str] = format_string_backslash
        self.format_float: Callable[[float], str] = float_format
        suffix_is_auto = numeric_literal_suffix.name == "AUTO"
        self.format_integer: Callable[[int], str] = (
            make_long_suffix_formatter(base=integer_format)
            if suffix_is_auto
            else integer_format
        )
        self.format_sequence_entry: Callable[[Value, str], str] = format_entry
        self.format_set_entry: Callable[[Value, str], str] = format_entry
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
                open_str=map_open,
                close="}})",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            braced_dict_entry(format_value=format_entry)
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.supports_scalar_before_comments = True
        self.supports_scalar_inline_comments = False

        @beartype
        def _format_decl(name: str, value: str, data: Value) -> str:
            """Format a C variable declaration."""
            wrapped = format_entry(data, value)
            return f"CVal {name} = {wrapped};"

        @beartype
        def _format_assign(name: str, value: str, data: Value) -> str:
            """Format a C variable assignment."""
            wrapped = format_entry(data, value)
            return f"{name} = {wrapped};"

        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _format_decl
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_assign
        )
        self.static_preamble: Sequence[str] = (
            "#include <stdbool.h>",
            "#include <stddef.h>",
            "typedef struct CVal CVal;",
            "typedef struct CKV CKV;",
            "struct CVal {",
            "    union {",
            f"        _Bool {bool_field};",
            f"        long long {int_field};",
            f"        double {float_field};",
            f"        const char *{string_field};",
            f"        const CVal *{array_field};",
            f"        const CKV *{map_field};",
            "    };",
            "};",
            f"struct CKV {{ const char *{key_field}; CVal {value_field}; }};",
        )
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )

        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.special_float_preamble: tuple[str, ...] = ("#include <math.h>",)
        self.call_style_config: CallStyleConfig | None = None
        self.statement_terminator = ";"
        self.format_call_stub = no_call_stub
        self.format_call_preamble_stub = no_call_stub
        self.format_call_target = identity_call_target
