"""Python language specification."""

import datetime
import enum
import functools
from collections import OrderedDict
from collections.abc import Callable, Sequence
from types import MappingProxyType
from typing import assert_never

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._formatters import (
    dict_entry_with_separator,
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
    format_bytes_hex,
    format_date_iso,
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    format_integer_underscore,
    format_string_backslash,
    format_string_backslash_single,
    passthrough_sequence_entry,
    passthrough_set_entry,
    tuple_dict_entry,
    variable_formatter,
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
    date_scalar_preamble,
)
from literalizer._types import Value


@beartype
def _format_date_python(value: datetime.date) -> str:
    """Format a date as a Python ``datetime.date(...)`` constructor
    call.
    """
    return (
        f"datetime.date("
        f"year={value.year}, month={value.month}, day={value.day})"
    )


@beartype
def _format_datetime_python(value: datetime.datetime) -> str:
    """Format a datetime as a Python ``datetime.datetime(...)`` constructor
    call.
    """
    parts = [
        f"year={value.year}",
        f"month={value.month}",
        f"day={value.day}",
        f"hour={value.hour}",
        f"minute={value.minute}",
        f"second={value.second}",
    ]
    if value.microsecond:
        parts.append(f"microsecond={value.microsecond}")
    args = ", ".join(parts)
    return f"datetime.datetime({args})"


@beartype
def _format_datetime_epoch(value: datetime.datetime) -> str:
    """Format a datetime as seconds since the Unix epoch."""
    return repr(value.timestamp())


@beartype
def _format_bytes_python(value: bytes) -> str:
    """Format bytes as a Python ``bytes`` literal."""
    return repr(value)


@beartype
def _format_variable_declaration(name: str, value: str, _data: Value) -> str:
    """Format a Python variable declaration."""
    return f"{name} = {value}"


@beartype
def _format_inline_type_hint_declaration(
    name: str,
    value: str,
    data: Value,
    *,
    bytes_hint: str,
    date_hint: str,
    datetime_hint: str,
    sequence_hint: str,
    set_hint: str,
) -> str:
    """Format a Python variable declaration with an inline type hint."""
    hint = _python_type_hint(
        data=data,
        bytes_hint=bytes_hint,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        sequence_hint=sequence_hint,
        set_hint=set_hint,
    )
    return f"{name}: {hint} = {value}"


@beartype
def _element_union(*, types: list[str]) -> str:
    """Remove duplicate *types* and join them into a union."""
    unique: list[str] = list(dict.fromkeys(types))
    if len(unique) == 1:
        return unique[0]
    return " | ".join(unique)


@beartype
def _collection_element_union(
    *,
    elements: list[Value],
    recurse: Callable[..., str],
    sort: bool = False,
) -> str:
    """Return the element union for a collection, or ``"Any"`` if
    empty.
    """
    if not elements:
        return "Any"
    types = [recurse(data=e) for e in elements]
    if sort:
        types.sort()
    return _element_union(types=types)


@beartype
def _python_type_hint(  # pylint: disable=too-complex,too-many-branches  # noqa: C901, PLR0911, PLR0912
    data: Value,
    *,
    bytes_hint: str,
    date_hint: str,
    datetime_hint: str,
    sequence_hint: str,
    set_hint: str,
) -> str:
    """Derive a Python type hint from the original data and format
    config.
    """
    recurse = functools.partial(
        _python_type_hint,
        bytes_hint=bytes_hint,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        sequence_hint=sequence_hint,
        set_hint=set_hint,
    )

    # Order matters: datetime before date (datetime is a date subclass),
    # bool before int (bool is an int subclass).
    match data:
        case bool():
            return "bool"
        case int():
            return "int"
        case float():
            return "float"
        case str():
            return "str"
        case bytes():
            return bytes_hint
        case datetime.datetime():
            return datetime_hint
        case datetime.date():
            return date_hint
        case None:
            return "None"
        case dict():
            outer = (
                "OrderedDict"
                if isinstance(data, (ordereddict, OrderedDict))
                else "dict"
            )
            val_union = _collection_element_union(
                elements=list(data.values()),  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
                recurse=recurse,
            )
            return f"{outer}[str, {val_union}]"
        case set():
            elem_union = _collection_element_union(
                elements=list(data),
                recurse=recurse,
                sort=True,
            )
            return f"{set_hint}[{elem_union}]"
        case list():
            elem_union = _collection_element_union(
                elements=data,
                recurse=recurse,
            )
            if sequence_hint == "tuple":
                return f"{sequence_hint}[{elem_union}, ...]"
            return f"{sequence_hint}[{elem_union}]"
        case _:  # pragma: no cover
            assert_never(data)


@beartype
class Python(metaclass=LanguageCls):
    """Python language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.PYTHON`` — ``datetime.date`` constructor call,
              e.g. ``datetime.date(year=2024, month=1, day=15)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.PYTHON`` — ``datetime.datetime`` constructor
              call, e.g. ``datetime.datetime(year=2024, month=1,
              day=15, hour=12, minute=30, second=0)``.
            * ``datetime_formats.EPOCH`` — Unix epoch float,
              e.g. ``1705312200.0``.

        bytes_format: How to format :class:`bytes` values.

            * ``bytes_formats.HEX`` — lowercase hex string,
              e.g. ``"48656c6c6f"``.
            * ``bytes_formats.PYTHON`` — Python bytes literal,
              e.g. ``b'Hello'``.

        sequence_format: Which Python sequence type to use.

            * ``sequence_formats.TUPLE`` — tuple literal,
              e.g. ``(1, 2, 3)``.
            * ``sequence_formats.LIST`` — list literal,
              e.g. ``[1, 2, 3]``.

        set_format: Which Python set type to use.

            * ``set_formats.SET`` — mutable set literal,
              e.g. ``{1, 2, 3}``.
            * ``set_formats.FROZENSET`` — immutable frozenset,
              e.g. ``frozenset({1, 2, 3})``.

        variable_type_hints: Whether to add inline type hints to
            variable declarations.

            * ``VariableTypeHints.NONE`` — bare assignment,
              e.g. ``my_var = {...}``.
            * ``VariableTypeHints.INLINE`` — with type annotation,
              e.g. ``my_var: dict[str, Any] = {...}``.
    """

    extension = ".py"
    pygments_name = "python"

    class DateFormats(enum.Enum):
        """Date formatting options for Python."""

        PYTHON = DateFormatConfig(
            formatter=_format_date_python,
            preamble_lines=("import datetime",),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

        @property
        def type_hint(self) -> str:
            """The Python type hint for this date format."""
            if self is type(self).PYTHON:
                return "datetime.date"
            return "str"

    class DatetimeFormats(enum.Enum):
        """Datetime formatting options for Python."""

        PYTHON = DatetimeFormatConfig(
            formatter=_format_datetime_python,
            preamble_lines=("import datetime",),
        )
        EPOCH = DatetimeFormatConfig(formatter=_format_datetime_epoch)

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

        @property
        def type_hint(self) -> str:
            """The Python type hint for this datetime format."""
            if self is type(self).PYTHON:
                return "datetime.datetime"
            return "float"

    class BytesFormats(enum.Enum):
        """Bytes formatting options for Python."""

        HEX = enum.member(value=format_bytes_hex)
        PYTHON = enum.member(value=_format_bytes_python)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

        @property
        def type_hint(self) -> str:
            """The Python type hint for this bytes format."""
            if self is type(self).PYTHON:
                return "bytes"
            return "str"

    class SequenceFormats(enum.Enum):
        """Sequence type options for Python."""

        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
        )
        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="["),
            close="]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
        )

        @property
        def type_hint(self) -> str:
            """Python type hint name for this sequence format."""
            return "tuple" if self is type(self).TUPLE else "list"

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Python."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="{"),
            close="}",
            empty_set="set()",
            preamble_lines=(),
            set_opener_template="",
        )
        FROZENSET = SetFormatConfig(
            set_open=fixed_set_open(open_str="frozenset({"),
            close="})",
            empty_set="frozenset()",
            preamble_lines=(),
            set_opener_template="",
        )

        @property
        def type_hint(self) -> str:
            """Python type hint name for this set format."""
            return "frozenset" if self is type(self).FROZENSET else "set"

    class VariableTypeHints(enum.Enum):
        """Variable type hint options for Python."""

        NONE = "none"
        INLINE = "inline"

        def formatter(
            self,
            *,
            bytes_hint: str,
            date_hint: str,
            datetime_hint: str,
            sequence_hint: str,
            set_hint: str,
        ) -> Callable[[str, str, Value], str]:
            """Return the variable declaration formatter for this hint
            style.
            """
            if self is type(self).INLINE:
                return functools.partial(
                    _format_inline_type_hint_declaration,
                    bytes_hint=bytes_hint,
                    date_hint=date_hint,
                    datetime_hint=datetime_hint,
                    sequence_hint=sequence_hint,
                    set_hint=set_hint,
                )
            return _format_variable_declaration

    class CommentFormats(enum.Enum):
        """Comment style options."""

        HASH = CommentConfig(
            prefix="#",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        ASSIGN = "assign"

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = "default"

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

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = "none"
        UNDERSCORE = "underscore"

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.member(value=format_string_backslash)
        SINGLE = enum.member(value=format_string_backslash_single)

        def __call__(self, value: str, /) -> str:
            """Format a string."""
            return self.value(value=value)

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        YES = "yes"
        NO = "no"

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats
    variable_type_hints_formats = VariableTypeHints
    declaration_styles = DeclarationStyles
    dict_formats = DictFormats
    integer_formats = IntegerFormats
    numeric_separators = NumericSeparators
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class LineEndings(enum.Enum):
        """Line ending options."""

        SEMICOLON = "semicolon"

    line_endings = LineEndings

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.PYTHON,
        datetime_format: DatetimeFormats = DatetimeFormats.PYTHON,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.TUPLE,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.HASH,
        declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN,
        dict_format: DictFormats = DictFormats.DEFAULT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.YES,
        line_ending: LineEndings = LineEndings.SEMICOLON,
    ) -> None:
        """Initialize Python language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "None"
        self.true_literal = "True"
        self.false_literal = "False"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="{"),
            close="}",
            format_entry=dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
        )
        self.multiline_trailing_comma: bool = trailing_comma.name == "YES"

        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )

        self.format_string: Callable[[str], str] = string_format
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
        self.dict_format = dict_format
        self.integer_format = integer_format
        self.numeric_separator = numeric_separator
        self.string_format = string_format
        self.trailing_comma = trailing_comma
        self.line_ending = line_ending
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="OrderedDict([",
                close="])",
                preamble_lines=("from collections import OrderedDict",),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            tuple_dict_entry(format_value=passthrough_sequence_entry)
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        bytes_hint = bytes_format.type_hint
        date_hint = date_format.type_hint
        datetime_hint = datetime_format.type_hint
        sequence_hint = sequence_format.type_hint
        set_hint = set_format.type_hint
        decl_fmt: Callable[[str, str, Value], str] = (
            variable_type_hints.formatter(
                bytes_hint=bytes_hint,
                date_hint=date_hint,
                datetime_hint=datetime_hint,
                sequence_hint=sequence_hint,
                set_hint=set_hint,
            )
        )
        self.format_variable_declaration = decl_fmt
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name} = {value}")
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.static_code_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = (
            date_scalar_preamble(
                date_format=date_format,
                datetime_format=datetime_format,
            )
        )
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = (
            ("from typing import Any",)
            if variable_type_hints.name == "INLINE"
            else ()
        )
