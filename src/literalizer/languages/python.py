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

from literalizer._formatters.collection_openers import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    format_date_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_separator,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    tuple_dict_entry,
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
from literalizer._formatters.format_strings import (
    format_string_backslash,
    format_string_backslash_single,
    format_string_raw_python,
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
    body_preamble_from_scalars,
    date_scalar_preamble,
    no_call_stub,
    wrap_combined_in_file_noop,
    wrap_in_file_noop,
)
from literalizer._types import Value


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
def _needs_type_annotation(data: Value) -> bool:
    """Whether *data* needs a type annotation for type-checkers.

    This is true when *data* is or contains an empty collection,
    because type-checkers cannot infer the element types.
    """
    match data:
        case dict():
            return len(data) == 0 or any(
                _needs_type_annotation(data=v) for v in data.values()
            )
        case set():
            return len(data) == 0
        case list():
            return len(data) == 0 or any(
                _needs_type_annotation(data=e) for e in data
            )
        case _:
            return False


@beartype
def _format_variable_declaration(
    name: str,
    value: str,
    data: Value,
    *,
    bytes_hint: str,
    date_hint: str,
    datetime_hint: str,
    sequence_hint: str,
    set_hint: str,
    default_set_element_type: str,
    default_sequence_element_type: str,
    default_dict_value_type: str,
    default_dict_key_type: str,
) -> str:
    """Format a Python variable declaration.

    For empty collections a type annotation is added so that
    type-checkers can infer the type.
    """
    if _needs_type_annotation(data=data):
        return _format_inline_type_hint_declaration(
            name=name,
            value=value,
            data=data,
            bytes_hint=bytes_hint,
            date_hint=date_hint,
            datetime_hint=datetime_hint,
            sequence_hint=sequence_hint,
            set_hint=set_hint,
            default_set_element_type=default_set_element_type,
            default_sequence_element_type=default_sequence_element_type,
            default_dict_value_type=default_dict_value_type,
            default_dict_key_type=default_dict_key_type,
        )
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
    default_set_element_type: str,
    default_sequence_element_type: str,
    default_dict_value_type: str,
    default_dict_key_type: str,
) -> str:
    """Format a Python variable declaration with an inline type hint."""
    hint = _python_type_hint(
        data=data,
        bytes_hint=bytes_hint,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        sequence_hint=sequence_hint,
        set_hint=set_hint,
        default_set_element_type=default_set_element_type,
        default_sequence_element_type=default_sequence_element_type,
        default_dict_value_type=default_dict_value_type,
        default_dict_key_type=default_dict_key_type,
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
    sort: bool,
    merge_dicts: bool,
    default_type: str,
) -> str:
    """Return the element union for a collection, or *default_type* if
    empty.

    When *merge_dicts* is ``True``, all dict elements are merged so
    that their values produce a single ``dict[str, …]`` hint.  This
    avoids ``dict[str, X] | dict[str, Y]`` unions that mypy rejects
    because ``dict`` is invariant in its type parameters.
    """
    if not elements:
        return default_type
    if merge_dicts:
        elements = _merge_dict_elements(elements=elements)
    types = [recurse(data=e) for e in elements]
    if sort:
        types.sort()
    return _element_union(types=types)


@beartype
def _merge_dict_elements(*, elements: list[Value]) -> list[Value]:
    """Pool values from like-typed dicts into single representatives."""
    plain_vals: list[Value] = []
    ordered_vals: list[Value] = []
    non_dict: list[Value] = []
    has_plain = False
    has_ordered = False
    for elem in elements:
        match elem:
            case ordereddict() | OrderedDict():
                has_ordered = True
                ordered_vals.extend(elem.values())  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
            case dict():
                has_plain = True
                plain_vals.extend(elem.values())
            case _:
                non_dict.append(elem)
    merged: list[Value] = list(non_dict)
    if has_plain:
        merged.append(
            {str(object=i): v for i, v in enumerate(iterable=plain_vals)}
        )
    if has_ordered:
        merged.append(
            OrderedDict(
                {str(object=i): v for i, v in enumerate(iterable=ordered_vals)}
            )
        )
    return merged


@beartype
def _python_type_hint(  # pylint: disable=too-complex,too-many-branches  # noqa: C901, PLR0911, PLR0912
    data: Value,
    *,
    bytes_hint: str,
    date_hint: str,
    datetime_hint: str,
    sequence_hint: str,
    set_hint: str,
    default_set_element_type: str,
    default_sequence_element_type: str,
    default_dict_value_type: str,
    default_dict_key_type: str,
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
        default_set_element_type=default_set_element_type,
        default_sequence_element_type=default_sequence_element_type,
        default_dict_value_type=default_dict_value_type,
        default_dict_key_type=default_dict_key_type,
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
            key_hint = default_dict_key_type if not data else "str"
            val_union = _collection_element_union(
                elements=list(data.values()),  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
                recurse=recurse,
                sort=False,
                merge_dicts=False,
                default_type=default_dict_value_type,
            )
            return f"{outer}[{key_hint}, {val_union}]"
        case set():
            elem_union = _collection_element_union(
                elements=list(data),
                recurse=recurse,
                sort=True,
                merge_dicts=False,
                default_type=default_set_element_type,
            )
            return f"{set_hint}[{elem_union}]"
        case list():
            elem_union = _collection_element_union(
                elements=data,
                recurse=recurse,
                sort=False,
                merge_dicts=True,
                default_type=default_sequence_element_type,
            )
            if sequence_hint == "tuple":
                return f"{sequence_hint}[{elem_union}, ...]"
            return f"{sequence_hint}[{elem_union}]"
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _build_type_hint_preamble(
    *,
    default_set_element_type: str,
    default_sequence_element_type: str,
    default_dict_value_type: str,
    default_dict_key_type: str,
) -> Callable[[frozenset[type]], tuple[str, ...]]:
    """Build a callable that returns preamble lines for type hints.

    The returned callable checks which empty collection types are
    present in the data and only emits ``from typing import Any``
    when at least one of them would produce an ``Any`` type hint.
    """
    # Pre-compute which collection types need "Any".
    _any_types: frozenset[type] = frozenset(
        t
        for t, needs in (
            (
                dict,
                default_dict_value_type == "Any"
                or default_dict_key_type == "Any",
            ),
            (set, default_set_element_type == "Any"),
            (list, default_sequence_element_type == "Any"),
        )
        if needs
    )

    def _preamble(
        empty_collection_types: frozenset[type],
        /,
    ) -> tuple[str, ...]:
        """Return ``from typing import Any`` if needed."""
        if _any_types & empty_collection_types:
            return ("from typing import Any",)
        return ()

    return _preamble


_VARIADIC = "*_args: object, **_kwargs: object"


def _python_call_stub(name: str, _params: Sequence[str], /) -> tuple[str, ...]:
    """Return Python stub declarations for a call name."""
    parts = name.split(sep=".")
    if len(parts) == 1:
        return (f"def {name}({_VARIADIC}) -> object: ...",)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        cls = f"_{root.capitalize()}Type"
        return (
            f"class {cls}:",
            f"    def {method}(self, {_VARIADIC}) -> object: ...",
            f"{root} = {cls}()",
        )
    lines: list[str] = []
    inner_cls = f"_{fields[-1].capitalize()}Type"
    lines.append(f"class {inner_cls}:")
    lines.append(f"    def {method}(self, {_VARIADIC}) -> object: ...")
    prev_cls = inner_cls
    for i in range(len(fields) - 2, -1, -1):
        cls = f"_{fields[i].capitalize()}Type"
        lines.append(f"class {cls}:")
        lines.append(f"    {fields[i + 1]} = {prev_cls}()")
        prev_cls = cls
    root_cls = f"_{root.capitalize()}Type"
    lines.append(f"class {root_cls}:")
    lines.append(f"    {fields[0]} = {prev_cls}()")
    lines.append(f"{root} = {root_cls}()")
    return tuple(lines)


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

        default_set_element_type: Type name used for empty set type
            hints.  Defaults to ``"Any"``.

        default_sequence_element_type: Type name used for empty
            list/tuple type hints.  Defaults to ``"Any"``.

        default_dict_key_type: Type name used for empty dict key
            type hints.  Defaults to ``"str"``.

        default_dict_value_type: Type name used for empty dict value
            type hints.  Defaults to ``"Any"``.

        variable_type_hints: Whether to add inline type hints to
            variable declarations.

            * ``VariableTypeHints.AUTO`` — bare assignment,
              e.g. ``my_var = {...}``.  Empty collections still
              receive a type annotation so that type-checkers can
              infer the element types,
              e.g. ``my_var: dict[str, Any] = {}``.
            * ``VariableTypeHints.ALWAYS`` — every declaration has
              a type annotation,
              e.g. ``my_var: dict[str, Any] = {...}``.
    """

    extension = ".py"
    pygments_name = "python"
    supports_default_set_element_type = True
    supports_default_sequence_element_type = True
    supports_default_dict_value_type = True
    supports_default_dict_key_type = True
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True
    supports_variable_names = True
    supports_call = True

    class DateFormats(enum.Enum):
        """Date formatting options for Python."""

        PYTHON = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="datetime.date("
                "year={year}, month={month}, day={day})",
            ),
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
        BASE64 = enum.member(value=format_bytes_base64)
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
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
        )
        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="["),
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
            coerce_mixed_to_str=False,
        )
        FROZENSET = SetFormatConfig(
            set_open=fixed_set_open(open_str="frozenset({"),
            close="})",
            empty_set="frozenset()",
            preamble_lines=(),
            set_opener_template="",
            coerce_mixed_to_str=False,
        )

        @property
        def type_hint(self) -> str:
            """Python type hint name for this set format."""
            return "frozenset" if self is type(self).FROZENSET else "set"

    class VariableTypeHints(enum.Enum):
        """Variable type hint options for Python."""

        AUTO = enum.auto()
        ALWAYS = enum.auto()

        def formatter(
            self,
            *,
            bytes_hint: str,
            date_hint: str,
            datetime_hint: str,
            sequence_hint: str,
            set_hint: str,
            default_set_element_type: str,
            default_sequence_element_type: str,
            default_dict_value_type: str,
            default_dict_key_type: str,
        ) -> Callable[[str, str, Value], str]:
            """Return the variable declaration formatter for this hint
            style.
            """
            if self is type(self).ALWAYS:
                return functools.partial(
                    _format_inline_type_hint_declaration,
                    bytes_hint=bytes_hint,
                    date_hint=date_hint,
                    datetime_hint=datetime_hint,
                    sequence_hint=sequence_hint,
                    set_hint=set_hint,
                    default_set_element_type=default_set_element_type,
                    default_sequence_element_type=default_sequence_element_type,
                    default_dict_value_type=default_dict_value_type,
                    default_dict_key_type=default_dict_key_type,
                )
            return functools.partial(
                _format_variable_declaration,
                bytes_hint=bytes_hint,
                date_hint=date_hint,
                datetime_hint=datetime_hint,
                sequence_hint=sequence_hint,
                set_hint=set_hint,
                default_set_element_type=default_set_element_type,
                default_sequence_element_type=default_sequence_element_type,
                default_dict_value_type=default_dict_value_type,
                default_dict_key_type=default_dict_key_type,
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
            formatter=variable_formatter(template="{name} = {value}"),
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
        positive_infinity='float("inf")',
        negative_infinity='float("-inf")',
        nan='float("nan")',
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

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.member(value=format_string_backslash)
        SINGLE = enum.member(value=format_string_backslash_single)
        RAW = enum.member(value=format_string_raw_python)

        def __call__(self, value: str, /) -> str:
            """Format a string."""
            return self.value(value=value)

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
        """Wrap Python code in a valid file (no-op)."""
        return wrap_in_file_noop(
            content=content,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Python declaration + assignment in a valid file."""
        return wrap_combined_in_file_noop(
            declaration=declaration,
            assignment=assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    def __init__(  # noqa: PLR0915
        self,
        *,
        date_format: DateFormats = DateFormats.PYTHON,
        datetime_format: DatetimeFormats = DatetimeFormats.PYTHON,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.TUPLE,
        set_format: SetFormats = SetFormats.SET,
        default_set_element_type: str = "Any",
        default_sequence_element_type: str = "Any",
        default_dict_key_type: str = "str",
        default_dict_value_type: str = "Any",
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.HASH,
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
        trailing_comma: TrailingCommas = TrailingCommas.YES,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
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
            dict_open=fixed_dict_open(open_str="{"),
            close="}",
            format_entry=dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
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

        self.format_string: Callable[[str], str] = string_format
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
                open_str="OrderedDict([",
                close="])",
                preamble_lines=("from collections import OrderedDict",),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            tuple_dict_entry(format_value=passthrough_sequence_entry)
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.supports_scalar_before_comments = False
        self.supports_scalar_inline_comments = True
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
                default_set_element_type=default_set_element_type,
                default_sequence_element_type=default_sequence_element_type,
                default_dict_value_type=default_dict_value_type,
                default_dict_key_type=default_dict_key_type,
            )
        )
        self.format_variable_declaration = decl_fmt
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
            format_lines=tuple,
        )

        self.type_hint_collection_preamble_lines: Callable[
            [frozenset[type]], tuple[str, ...]
        ] = _build_type_hint_preamble(
            default_set_element_type=default_set_element_type,
            default_sequence_element_type=default_sequence_element_type,
            default_dict_value_type=default_dict_value_type,
            default_dict_key_type=default_dict_key_type,
        )
        self.special_float_preamble: tuple[str, ...] = ()
        self.call_style_config: CallStyleConfig = CallStyleConfig(
            kind=CallStyleKind.KEYWORD,
            keyword_separator="=",
        )
        self.statement_terminator = ""
        self.format_call_stub = _python_call_stub
        self.format_call_preamble_stub = no_call_stub
