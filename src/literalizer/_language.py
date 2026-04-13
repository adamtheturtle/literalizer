"""Language protocol and internal spec dataclass."""

import dataclasses
import datetime
import enum
import math
from collections.abc import Callable, Sequence
from typing import Protocol, cast, runtime_checkable

from beartype import beartype

from literalizer._formatters.collection_openers import typed_collection_open
from literalizer._formatters.type_inference import DictType, ListType
from literalizer._types import Value


@dataclasses.dataclass(frozen=True)
class SequenceFormatConfig:
    """Configuration for a single sequence format."""

    sequence_open: Callable[[list[Value]], str]
    close: str
    supports_heterogeneity: bool
    single_element_trailing_comma: bool
    supports_trailing_comma: bool
    empty_sequence: str | None
    preamble_lines: tuple[str, ...]
    format_entry: Callable[[Value, str], str]
    typed_opener_fallback: str | None
    uses_typed_literal_for_scalars: bool
    requires_uniform_record_shapes: bool
    declared_type: str | None


@dataclasses.dataclass(frozen=True)
class DateFormatConfig:
    """Configuration for a single date format."""

    formatter: Callable[[datetime.date], str]
    preamble_lines: tuple[str, ...] = ()
    type_produced: type = datetime.date


@dataclasses.dataclass(frozen=True)
class DatetimeFormatConfig:
    """Configuration for a single datetime format."""

    formatter: Callable[[datetime.datetime], str]
    preamble_lines: tuple[str, ...] = ()
    type_produced: type = datetime.datetime


@beartype
def date_scalar_preamble(
    *,
    date_format: enum.Enum,
    datetime_format: enum.Enum,
    extra: dict[type, tuple[str, ...]] | None = None,
) -> dict[type, tuple[str, ...]]:
    """Build the ``scalar_preamble`` dict for date/datetime formats.

    Args:
        date_format: The date format enum member whose ``.value`` has
            a ``preamble_lines`` attribute.
        datetime_format: The datetime format enum member whose ``.value``
            has a ``preamble_lines`` attribute.
        extra: Optional additional type→preamble mappings to include
            unconditionally (e.g. for C++ ``#include <string>``).

    Returns:
        A dict mapping Python types to their required preamble lines,
        omitting entries whose preamble is empty.
    """
    return {
        **(extra or {}),
        **{
            t: p
            for t, p in (
                (datetime.date, date_format.value.preamble_lines),
                (datetime.datetime, datetime_format.value.preamble_lines),
            )
            if p
        },
    }


@dataclasses.dataclass(frozen=True)
class SetFormatConfig:
    """Configuration for a single set format."""

    set_open: Callable[[list[Value]], str]
    close: str
    empty_set: str | None
    preamble_lines: tuple[str, ...]
    set_opener_template: str
    coerce_mixed_to_str: bool

    def with_typed_opener(
        self,
        *,
        type_to_opener: Callable[[type | ListType | DictType], str | None],
        fallback: str,
    ) -> "SetFormatConfig":
        """Return a copy with ``set_open`` replaced by a typed opener.

        The *type_to_opener* callable is used to infer the opener from the
        element type.  When inference fails, *fallback* is used instead.
        """
        return dataclasses.replace(
            self,
            set_open=typed_collection_open(
                type_to_opener=type_to_opener,
                fallback=fallback,
            ),
        )


@dataclasses.dataclass(frozen=True)
class CommentConfig:
    """Configuration for language comment syntax."""

    prefix: str
    suffix: str


@dataclasses.dataclass(frozen=True)
class DictFormatConfig:
    """Configuration for dict formatting."""

    dict_open: Callable[[dict[str, Value]], str]
    close: str
    format_entry: Callable[[str, Value, str], str]
    empty_dict: str | None
    preamble_lines: tuple[str, ...]
    narrowed_open: str | None


@dataclasses.dataclass(frozen=True)
class OrderedMapFormatConfig:
    """Configuration for ordered-map formatting."""

    open_str: str
    close: str
    preamble_lines: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class TrailingCommaConfig:
    """Configuration for trailing-comma behavior.

    When ``multiline_trailing_comma`` is ``True``, trailing commas are added
    to multiline collections where the chosen format supports them.
    Some sequence formats (e.g. Java's ``List.of()``) do not support trailing
    commas; in those cases the trailing comma is omitted regardless of this
    setting.
    """

    multiline_trailing_comma: bool


@dataclasses.dataclass(frozen=True)
class DeclarationStyleConfig:
    """Configuration for a single declaration style."""

    formatter: Callable[[str, str, Value], str]
    supports_redefinition: bool


class SequenceFormat(Protocol):
    """Protocol for sequence format Enum members."""

    @property
    def supports_heterogeneity(self) -> bool:
        """Whether this sequence format supports mixed-type elements."""
        ...  # pylint: disable=unnecessary-ellipsis


class FloatSpecialsMixin:
    """Mixin for ``FloatFormats`` enums that provides ``__call__``.

    Subclasses pass ``positive_infinity``, ``negative_infinity``, and
    ``nan`` as keyword arguments to the class definition.  The mixin
    stores them and provides a ``__call__`` that handles the
    ``isinf``/``isnan`` dispatch, delegating finite values to the enum
    member's formatter.
    """

    _positive_infinity: str
    _negative_infinity: str
    _nan: str

    def __init_subclass__(
        cls,
        *,
        positive_infinity: str,
        negative_infinity: str,
        nan: str,
    ) -> None:
        """Store float-special strings as class attributes."""
        super().__init_subclass__()
        cls._positive_infinity = positive_infinity
        cls._negative_infinity = negative_infinity
        cls._nan = nan

    def __call__(self, value: float, /) -> str:
        """Format a float, handling inf and nan."""
        if math.isinf(value):
            if value < 0:
                return self._negative_infinity
            return self._positive_infinity
        if math.isnan(value):
            return self._nan
        formatter: Callable[[float], str] = cast("enum.Enum", self).value
        return formatter(value)


class LanguageCls(type):
    """Meta-class that declares the nested format Enum class attributes.

    Language classes use ``metaclass=LanguageCls`` so that downstream
    code can write ``dict[str, LanguageCls]`` and access
    ``cls.DateFormats``, ``cls.SequenceFormats``, etc. without ``cast``
    or ``type: ignore``.
    """

    DateFormats: type[enum.Enum]
    DatetimeFormats: type[enum.Enum]
    BytesFormats: type[enum.Enum]
    SequenceFormats: type[enum.Enum]
    SetFormats: type[enum.Enum]
    CommentFormats: type[enum.Enum]
    VariableTypeHints: type[enum.Enum]
    DeclarationStyles: type[enum.Enum]
    DictEntryStyles: type[enum.Enum]
    DictFormats: type[enum.Enum]
    EmptyDictKey: type[enum.Enum]
    FloatFormats: type[enum.Enum]
    IntegerFormats: type[enum.Enum]
    NumericLiteralSuffixes: type[enum.Enum]
    NumericSeparators: type[enum.Enum]
    StringFormats: type[enum.Enum]
    TrailingCommas: type[enum.Enum]
    LineEndings: type[enum.Enum]
    extension: str
    pygments_name: str | None
    supports_default_set_element_type: bool
    supports_default_sequence_element_type: bool
    supports_default_dict_value_type: bool
    supports_default_dict_key_type: bool
    supports_default_ordered_map_value_type: bool
    supports_non_printable_ascii_dict_keys: bool
    supports_variable_names: bool

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a code snippet in a complete, valid file."""
        raise NotImplementedError  # pragma: no cover

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a declaration and assignment in a complete, valid file."""
        raise NotImplementedError  # pragma: no cover


@runtime_checkable
class Language(Protocol):  # pylint: disable=too-many-public-methods
    """Protocol describing how a language formats scalar literals and
    sequences.

    Predefined instances for common languages are available as module-level
    constants in :mod:`literalizer.languages` (e.g.
    :data:`~literalizer.languages.PYTHON`,
    :data:`~literalizer.languages.JAVASCRIPT`). To support additional
    languages or override defaults, write a class that provides all the
    required attributes.
    """

    # Each language class defines PascalCase nested Enum classes
    # (``DateFormats``, ``SequenceFormats``, …) and snake_case class
    # attributes that alias them (``date_formats = DateFormats``, …).
    # The aliases look redundant but are required: nested classes are
    # class-level (ClassVar) attributes, while Protocol properties are
    # instance-level.  No single declaration style (``@property``,
    # ``ClassVar``, or plain annotation) satisfies mypy, pyright, *and*
    # pyrefly simultaneously for PascalCase names that shadow nested
    # classes.  The snake_case aliases sidestep the issue entirely.

    @property
    def bytes_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the bytes formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def sequence_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the sequence formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def set_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the set formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def date_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the date formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def datetime_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the datetime formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def comment_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the comment formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def variable_type_hints_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the variable type hint options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def declaration_styles(self) -> type[enum.Enum]:
        """Enum class whose members list the declaration style options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dict_entry_styles(self) -> type[enum.Enum]:
        """Enum class whose members list the dict entry style options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dict_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the dict/map format options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def float_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the float format options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def integer_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the integer format options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def numeric_literal_suffixes(self) -> type[enum.Enum]:
        """Enum class whose members list the numeric literal suffix
        options this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def numeric_separators(self) -> type[enum.Enum]:
        """Enum class whose members list the numeric separator options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def string_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the string format options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def trailing_commas(self) -> type[enum.Enum]:
        """Enum class whose members list the trailing comma options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def line_endings(self) -> type[enum.Enum]:
        """Enum class whose members list the line ending options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    extension: str
    """The file extension for this language, including the leading dot."""

    @property
    def pygments_name(self) -> str | None:
        """The Pygments lexer short name for syntax highlighting.

        ``None`` if Pygments does not support this language.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    null_literal: str
    """The literal representing null/None."""

    true_literal: str
    """The literal representing true/True."""

    false_literal: str
    """The literal representing false/False."""

    @property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence.

        Receives the list of items about to be formatted, so the delimiter
        can depend on the element types when needed.  For a fixed delimiter
        use :func:`~literalizer.fixed_sequence_open`.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    sequence_format_config: SequenceFormatConfig
    """Configuration for the chosen sequence format."""

    dict_format_config: DictFormatConfig
    """Configuration for dict formatting."""

    trailing_comma_config: TrailingCommaConfig
    """Configuration for trailing-comma behavior.

    Trailing commas are only added to collection formats that support them.
    See :class:`TrailingCommaConfig` for details.
    """

    @property
    def format_bytes(self) -> Callable[[bytes], str]:
        """Callable that formats a :class:`bytes` value as a string
        literal.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a :class:`datetime.date` as a string
        literal.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a :class:`datetime.datetime` as a string
        literal.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    set_format_config: SetFormatConfig
    """Configuration for the chosen set format."""

    @property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Callable that formats a sequence entry."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Callable that formats a set entry."""
        ...  # pylint: disable=unnecessary-ellipsis

    comment_config: CommentConfig
    """Configuration for the language's comment syntax."""

    ordered_map_format_config: OrderedMapFormatConfig
    """Configuration for ordered-map formatting."""

    @property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        ...  # pylint: disable=unnecessary-ellipsis

    indent: str
    """The indentation step for elements inside delimiters in multi-line
    structures (e.g. ``"    "`` for 4-space indent).
    """

    indent_closing_delimiter: bool
    """Whether to indent the closing delimiter of multi-line structures
    by one ``indent`` step.
    """

    element_separator: str
    """The separator placed between elements in inline sequences."""

    skip_null_dict_values: bool
    """Whether to omit dict entries whose value is ``None``."""

    supports_collection_comments: bool
    """Whether the language supports comments inside collection
    initializers.

    When ``False``, YAML comments on collection elements are emitted as
    standalone comment lines immediately before the collection (or before
    the variable declaration when a variable name is supplied) rather than
    being placed inside the ``{...}`` block.
    """

    supports_scalar_before_comments: bool
    """Whether the language supports a line comment between the
    assignment operator and the value on the next line.

    For example, in JavaScript ``const x = // note\\n42;`` is valid
    because the parser continues the incomplete expression past the
    line comment.  In Python ``x = # note\\n42`` is a syntax error
    because the ``#`` comment terminates the statement.

    When ``False``, YAML comments that appear before a scalar value
    are emitted as standalone comment lines immediately before the
    variable declaration rather than between the ``=`` and the value.
    """

    supports_scalar_inline_comments: bool
    """Whether the language supports a trailing line comment on a
    scalar value without breaking surrounding syntax.

    For example, in JavaScript ``const x = 42  // note`` is valid
    because no closing token follows on the same line.  In C
    ``((_CVal){.i = 42  // note});`` is a syntax error because the
    ``//`` comment consumes the closing ``});``.

    When ``False``, YAML inline comments on scalar values are emitted
    as standalone comment lines immediately before the variable
    declaration rather than being appended after the value.
    """

    @property
    def format_variable_declaration(self) -> Callable[[str, str, Value], str]:
        """Callable that formats a new variable declaration.

        Called as ``format_variable_declaration(name, value, data)`` where
        *name* is the variable name, *value* is the already-formatted literal
        value, and *data* is the original parsed data structure.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable.

        Called as ``format_variable_assignment(name, value, data)`` where
        *name* is the variable name, *value* is the already-formatted literal
        value, and *data* is the original parsed data structure.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def variable_type_hints(self) -> enum.Enum:
        """The variable type hint option chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def sequence_format(self) -> SequenceFormat:
        """The sequence format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def set_format(self) -> enum.Enum:
        """The set format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def comment_format(self) -> enum.Enum:
        """The comment format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def declaration_style(self) -> enum.Enum:
        """The declaration style chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dict_entry_style(self) -> enum.Enum:
        """The dict entry style chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dict_format(self) -> enum.Enum:
        """The dict/map format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def float_format(self) -> enum.Enum:
        """The float format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def integer_format(self) -> enum.Enum:
        """The integer format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def numeric_literal_suffix(self) -> enum.Enum:
        """The numeric literal suffix chosen for this language
        instance.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def numeric_separator(self) -> enum.Enum:
        """The numeric separator option chosen for this language
        instance.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def string_format(self) -> enum.Enum:
        """The string format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def trailing_comma(self) -> enum.Enum:
        """The trailing comma option chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def line_ending(self) -> enum.Enum:
        """The line ending option chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    static_preamble: Sequence[str]
    """Lines (imports, package declarations, etc.) that are always
    emitted before the generated code, regardless of what types appear
    in the data.  Use an empty sequence when none are needed.
    """

    scalar_preamble: dict[type, tuple[str, ...]]
    """Maps Python scalar types to the preamble lines required when
    that type appears in the data.  For example, a language that needs
    ``import datetime`` when dates are present would include
    ``{datetime.date: ("import datetime",)}``.
    """

    static_body_preamble: Sequence[str]
    """Lines that are always prepended to the generated code,
    regardless of what types appear in the data.  Appears after the
    header preamble but before the code body.  Use an empty sequence
    when none are needed.
    """

    scalar_body_preamble: dict[type, tuple[str, ...]]
    """Maps Python scalar types to body-preamble lines that are
    prepended to the generated code.

    Most languages leave this empty.  Haskell uses it for typeclass
    instance definitions.
    """

    compute_body_preamble: Callable[[frozenset[type], Value], tuple[str, ...]]
    """Computes body-preamble lines based on which types are present in
    the data.  Most languages build this from
    :attr:`scalar_body_preamble`; Haskell overrides it to compose the
    ``data Val`` declaration and imports dynamically.

    The second argument is the original data value, allowing
    implementations to inspect actual values when needed (e.g. to
    determine whether datetime microsecond-precision imports are
    required).
    """

    type_hint_collection_preamble_lines: Callable[
        [frozenset[type]], tuple[str, ...]
    ]
    """Callable that receives the set of collection types that have
    empty instances in the data and returns preamble lines needed for
    type-hint annotations.

    Most languages return ``()`` unconditionally; Python uses this to
    emit ``from typing import Any`` only when the specific empty
    collection types present actually require it.
    """

    special_float_preamble: tuple[str, ...]
    """Preamble lines added only when special float values (inf, -inf,
    nan) appear in the data.  Most languages set this to ``()``.
    Languages whose special-float literals require imports (e.g. Go
    needs ``import "math"``) populate this field so the import is only
    emitted when actually needed.
    """


def _no_type_hint_preamble(
    _empty_collection_types: frozenset[type],
    /,
) -> tuple[str, ...]:
    """Return no preamble lines — used by languages that do not emit
    type hints for empty collections.
    """
    return ()


no_type_hint_preamble: Callable[[frozenset[type]], tuple[str, ...]] = (
    _no_type_hint_preamble
)
"""Shared callable for languages that need no type-hint preamble."""


@beartype
def prepend_body_preamble(
    content: str,
    body_preamble: tuple[str, ...],
) -> str:
    """Prepend *body_preamble* lines to *content*."""
    if not body_preamble:
        return content
    return "\n".join(body_preamble) + "\n" + content


@beartype
def wrap_in_file_noop(
    content: str,
    variable_name: str,
    body_preamble: tuple[str, ...],
) -> str:
    """Default ``wrap_in_file`` that only adds body preamble."""
    del variable_name  # unused
    return prepend_body_preamble(content=content, body_preamble=body_preamble)


@beartype
def wrap_combined_in_file_noop(
    declaration: str,
    assignment: str,
    variable_name: str,
    body_preamble: tuple[str, ...],
) -> str:
    """Default ``wrap_combined_in_file``: join with newline, prepend
    preamble.
    """
    return wrap_in_file_noop(
        content=declaration + "\n" + assignment,
        variable_name=variable_name,
        body_preamble=body_preamble,
    )


def body_preamble_from_scalars(
    *,
    scalar_body_preamble: dict[type, tuple[str, ...]],
) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
    """Build a ``compute_body_preamble`` from a scalar-body-preamble
    dict.
    """

    def _compute(types: frozenset[type], data: Value, /) -> tuple[str, ...]:
        """Return unique body-preamble lines for *types*."""
        del data  # unused by the generic implementation
        seen: set[str] = set()
        result: list[str] = []
        for scalar_type, lines in scalar_body_preamble.items():
            if scalar_type in types:
                for line in lines:
                    if line not in seen:
                        seen.add(line)
                        result.append(line)
        return tuple(result)

    return _compute
