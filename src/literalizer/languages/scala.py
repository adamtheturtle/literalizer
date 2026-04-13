"""Scala language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Sequence
from types import MappingProxyType

from beartype import beartype

from literalizer._formatters.collection_openers import (
    TypedOpenerConfig,
    TypeOpeners,
    fixed_sequence_open,
    fixed_set_open,
    make_type_to_opener,
    typed_collection_open,
    typed_dict_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_separator,
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
    format_integer_hex,
    format_integer_underscore,
)
from literalizer._formatters.format_strings import format_string_backslash
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
    body_preamble_from_scalars,
    date_scalar_preamble,
    no_call_stub,
    no_type_hint_preamble,
    prepend_body_preamble,
)
from literalizer._types import Value


@beartype
def _format_datetime_scala(value: datetime.datetime) -> str:
    """Format a datetime as a Scala ``ZonedDateTime.of(...)`` call."""
    timezone_name = value.tzname() or "UTC"
    nanoseconds = value.microsecond * 1000
    return (
        f"ZonedDateTime.of({value.year}, {value.month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second}, "
        f'{nanoseconds}, ZoneId.of("{timezone_name}"))'
    )


@beartype
def _list_sequence_open(
    *,
    cfg: TypedOpenerConfig,
    date_type: str | None,
    datetime_type: str | None,
) -> Callable[[list[Value]], str]:
    """Build a typed sequence opener for the List format."""
    return typed_collection_open(
        type_to_opener=make_type_to_opener(
            element_to_type=cfg.element_to_type(
                list_template="List[{inner}]",
                date_type=date_type,
                datetime_type=datetime_type,
                enable_dict_type=True,
            ),
            opener_template="List[{type_name}](",
        ),
        fallback="List(",
    )


@beartype
def _resolve_sequence_open(
    *,
    cfg: TypedOpenerConfig,
    sequence_format: enum.Enum,
    list_member: enum.Enum,
    fmt: SequenceFormatConfig,
    openers: TypeOpeners,
    date_type: str | None,
    datetime_type: str | None,
) -> Callable[[list[Value]], str]:
    """Resolve the sequence opener for a Scala sequence format."""
    if sequence_format is list_member:
        return _list_sequence_open(
            cfg=cfg,
            date_type=date_type,
            datetime_type=datetime_type,
        )
    if fmt.typed_opener_fallback is not None:
        return typed_collection_open(
            type_to_opener=openers.seq,
            fallback=fmt.typed_opener_fallback,
        )
    return fmt.sequence_open


@dataclasses.dataclass(frozen=True)
class _ScalaDictSpec:
    """Per-format dict config pieces resolved at init time."""

    opener_template: str
    fallback: str
    preamble_lines: tuple[str, ...]


def _scala_call_stub(name: str, params: Sequence[str], /) -> tuple[str, ...]:
    """Return Scala stub declarations for a call name."""
    param_list = ", ".join(f"{p}: Any = null" for p in params)
    parts = name.split(sep=".")
    if len(parts) == 1:
        return (f"def {parts[0]}({param_list}): Any = null",)
    root, method = parts[0], parts[1]
    cls = f"_{root.capitalize()}Type"
    return (
        f"class {cls} {{ def {method}({param_list}): Any = null }}",
        f"val {root} = new {cls}",
    )


@beartype
class Scala(metaclass=LanguageCls):
    """Scala language specification."""

    extension = ".scala"
    pygments_name = "scala"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True
    supports_variable_names = True

    _opener_config = TypedOpenerConfig(
        str_type="String",
        bool_type="Boolean",
        int_type="Int",
        float_type="Double",
        mixed_numeric_type="Double",
        bytes_type="String",
        date_type="LocalDate",
        datetime_type="ZonedDateTime",
        list_template="Array[{inner}]",
        sequence_opener_template="Array[{type_name}](",
        dict_opener_template="Map[String, {type_name}](",
        set_opener_template="Set[{type_name}](",
        dict_type_template="Map[String, {inner}]",
        fallback_value_type="Any",
    )

    class DateFormats(enum.Enum):
        """Date format options for Scala."""

        SCALA = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="LocalDate.of({year}, {month}, {day})",
            ),
            preamble_lines=("import java.time.LocalDate",),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Scala."""

        SCALA = DatetimeFormatConfig(
            formatter=_format_datetime_scala,
            preamble_lines=(
                "import java.time.ZoneId",
                "import java.time.ZonedDateTime",
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
        """Sequence type options for Scala."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="List("),
            close=")",
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
        SEQ = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="Seq("),
            close=")",
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
        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="Array("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback="Array(",
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
        """Set type options for Scala."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="Set("),
            close=")",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            coerce_mixed_to_str=False,
        )
        TREE_SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="TreeSet("),
            close=")",
            empty_set=None,
            preamble_lines=("import scala.collection.immutable.TreeSet",),
            set_opener_template="TreeSet[{type_name}](",
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

        VAL = DeclarationStyleConfig(
            formatter=variable_formatter(template="val {name} = {value}"),
            supports_redefinition=False,
        )
        VAR = DeclarationStyleConfig(
            formatter=variable_formatter(template="var {name} = {value}"),
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        MAP = _ScalaDictSpec(
            opener_template="Map[String, {type_name}](",
            fallback="Map(",
            preamble_lines=(),
        )
        LIST_MAP = _ScalaDictSpec(
            opener_template="ListMap[String, {type_name}](",
            fallback="ListMap(",
            preamble_lines=("import scala.collection.immutable.ListMap",),
        )

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="Double.PositiveInfinity",
        negative_infinity="Double.NegativeInfinity",
        nan="Double.NaN",
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
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class LineEndings(enum.Enum):
        """Line ending options."""

        SEMICOLON = "semicolon"

    line_endings = LineEndings

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a Scala declaration in an object."""
        del variable_name
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        return f"object Check {{\n{content}\n}}"

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Scala declaration + assignment in an object."""
        return Scala.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    def __init__(  # noqa: PLR0915
        self,
        *,
        date_format: DateFormats = DateFormats.SCALA,
        datetime_format: DatetimeFormats = DatetimeFormats.SCALA,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        declaration_style: DeclarationStyles = DeclarationStyles.VAL,
        dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT,
        dict_format: DictFormats = DictFormats.MAP,
        float_format: FloatFormats = FloatFormats.REPR,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_literal_suffix: NumericLiteralSuffixes = (
            NumericLiteralSuffixes.NONE
        ),
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.YES,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
    ) -> None:
        """Initialize Scala language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        date_tp = date_format.value.type_produced
        dt_tp = datetime_format.value.type_produced
        date_type_name = self._opener_config.type_name(py_type=date_tp)
        datetime_type_name = self._opener_config.type_name(py_type=dt_tp)
        openers = self._opener_config.build(
            date_type=date_type_name,
            datetime_type=datetime_type_name,
            set_opener_template=set_format.value.set_opener_template or None,
            narrow_dict_values=False,
        )
        self.set_format_config: SetFormatConfig = (
            set_format.value.with_typed_opener(
                type_to_opener=openers.set,
                fallback=set_format.value.set_open([]),
            )
        )
        self.sequence_open: Callable[[list[Value]], str] = (
            _resolve_sequence_open(
                cfg=self._opener_config,
                sequence_format=sequence_format,
                list_member=self.sequence_formats.LIST,
                fmt=fmt,
                openers=openers,
                date_type=date_type_name,
                datetime_type=datetime_type_name,
            )
        )
        dict_spec: _ScalaDictSpec = dict_format.value
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            dict_open=typed_dict_open(
                type_to_opener=make_type_to_opener(
                    element_to_type=self._opener_config.element_to_type(
                        list_template=None,
                        date_type=date_type_name,
                        datetime_type=datetime_type_name,
                        enable_dict_type=False,
                    ),
                    opener_template=dict_spec.opener_template,
                ),
                fallback=dict_spec.fallback,
            ),
            narrowed_open=None,
            close=")",
            format_entry=dict_entry_with_separator(
                separator=" -> ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=dict_spec.preamble_lines,
        )
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = format_string_backslash
        self.format_float: Callable[[float], str] = float_format
        self.format_integer: Callable[[int], str] = (
            integer_format.get_formatter(
                numeric_separator=numeric_separator,
            )
        )
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
                open_str="scala.collection.immutable.ListMap(",
                close=")",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            dict_entry_with_separator(
                separator=" -> ",
                format_value=passthrough_sequence_entry,
            )
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.supports_scalar_before_comments = True
        self.supports_scalar_inline_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            declaration_style.value.formatter
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name} = {value}")
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = (
            date_scalar_preamble(
                date_format=date_format,
                datetime_format=datetime_format,
            )
        )
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
        )

        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.special_float_preamble: tuple[str, ...] = ()
        self.call_style_config: CallStyleConfig = CallStyleConfig(
            kind=CallStyleKind.KEYWORD,
            keyword_separator=" = ",
        )
        self.format_call_stub = _scala_call_stub
        self.format_call_preamble_stub = no_call_stub
