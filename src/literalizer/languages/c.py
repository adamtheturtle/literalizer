"""C language specification."""

import datetime
import enum
from collections.abc import Callable, Sequence

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
)
from literalizer._language import (
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DictFormatConfig,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
    SupportsHeterogeneityMixin,
)
from literalizer._types import Value


@beartype
def _to_val(value: str) -> str:
    """Convert a value to a C union cast expression."""
    if value.startswith("((_CVal)"):
        return value
    if value.startswith('"') and value.endswith('"'):
        return f"((_CVal){{.s = {value}}})"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"((_CVal){{.i = {value}}})"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float(rest)
    return f"((_CVal){{.f = {value}}})"


@beartype
def _format_c_dict_entry(key: str, value: str) -> str:
    """Format a C dict entry as a ``_CKV`` compound literal."""
    return f"{{{key}, {_to_val(value=value)}}}"


@beartype
def _format_c_list_entry(item: str) -> str:
    """Format a C list entry as a ``_CVal`` compound literal."""
    return _to_val(value=item)


@beartype
def _format_c_set_entry(item: str) -> str:
    """Format a C set entry as a ``_CVal`` compound literal."""
    return _to_val(value=item)


@beartype
def _format_variable_declaration(name: str, value: str, _data: Value) -> str:
    """Format a C variable declaration."""
    return f"_CVal {name} = {_to_val(value=value)};"


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format a C variable assignment."""
    return f"{name} = {_to_val(value=value)};"


_string_format: Callable[[str], str] = format_string_backslash


_C_PREAMBLE: tuple[str, ...] = (
    "#include <stdbool.h>",
    "#include <stddef.h>",
    "typedef struct _CVal _CVal;",
    "typedef struct _CKV _CKV;",
    "struct _CVal {",
    "    union {",
    "        _Bool b;",
    "        long long i;",
    "        double f;",
    "        const char *s;",
    "        const _CVal *a;",
    "        const _CKV *m;",
    "    };",
    "};",
    "struct _CKV { const char *k; _CVal v; };",
)


@beartype
class C(metaclass=LanguageCls):
    """C language specification."""

    extension = ".c"
    pygments_name = "c"

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

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(SupportsHeterogeneityMixin, enum.Enum):
        """Sequence type options for C."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(
                open_str="((_CVal){.a = (_CVal[]){",
            ),
            close="}})",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
        )

    class SetFormats(enum.Enum):
        """Set type options for C."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="((_CVal){.a = (_CVal[]){"),
            close="}})",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
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

        TYPED = "typed"

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = "default"

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = "decimal"

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = "none"

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = "double"

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        YES = "yes"

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats

    class VariableTypeHints(enum.Enum):
        """Variable type hint options."""

        NONE = "none"

    variable_type_hints_formats = VariableTypeHints
    declaration_styles = DeclarationStyles
    dict_formats = DictFormats
    integer_formats = IntegerFormats
    numeric_separators = NumericSeparators
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.TYPED,
        dict_format: DictFormats = DictFormats.DEFAULT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.YES,
    ) -> None:
        """Initialize C language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "((_CVal){.s = NULL})"
        self.true_literal = "((_CVal){.b = true})"
        self.false_literal = "((_CVal){.b = false})"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="((_CVal){.m = (_CKV[]){"),
            close="}})",
            format_entry=_format_c_dict_entry,
            empty_dict=None,
            preamble_lines=(),
        )
        self.multiline_trailing_comma = True
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.format_integer: Callable[[int], str] = str
        self.format_sequence_entry: Callable[[str], str] = _format_c_list_entry
        self.format_set_entry: Callable[[str], str] = _format_c_set_entry
        self.comment_format = comment_format
        self.declaration_style = declaration_style
        self.dict_format = dict_format
        self.integer_format = integer_format
        self.numeric_separator = numeric_separator
        self.string_format = string_format
        self.trailing_comma = trailing_comma
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="((_CVal){.m = (_CKV[]){",
                close="}})",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_c_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_variable_assignment
        )
        self.static_preamble: Sequence[str] = _C_PREAMBLE
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
