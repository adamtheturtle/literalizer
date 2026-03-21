"""Language protocol and internal spec dataclass."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    import datetime
    import enum
    from collections.abc import Callable

    from literalizer._types import Value


class HasFormatEnums(type):
    """Meta-class that declares the nested format Enum class attributes.

    Language classes use ``metaclass=HasFormatEnums`` so that downstream
    code can write ``dict[str, HasFormatEnums]`` and access
    ``cls.DateFormats``, ``cls.SequenceFormats``, etc. without ``cast``
    or ``type: ignore``.
    """

    DateFormats: type[enum.Enum]
    DatetimeFormats: type[enum.Enum]
    BytesFormats: type[enum.Enum]
    SequenceFormats: type[enum.Enum]
    SetFormats: type[enum.Enum]


@runtime_checkable
class Language(Protocol):
    """Protocol describing how a language formats scalar literals and
    sequences.

    Predefined instances for common languages are available as module-level
    constants in :mod:`literalizer.languages` (e.g.
    :data:`~literalizer.languages.PYTHON`,
    :data:`~literalizer.languages.JAVASCRIPT`). To support additional
    languages or override defaults, write a class that provides all the
    required attributes.
    """

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

    sequence_close: str
    """The closing delimiter for sequences."""

    @property
    def dict_open(self) -> Callable[[dict[str, Value]], str]:
        """Callable that returns the opening delimiter for a dict literal.

        Receives the dict about to be formatted, so the delimiter can depend
        on the value types when needed.  For a fixed delimiter use
        :func:`~literalizer.fixed_dict_open`.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    dict_close: str
    """The closing delimiter for dict literals."""

    @property
    def format_dict_entry(self) -> Callable[[str, str], str]:
        """Callable that formats a dict entry from a pre-formatted key and
        value string.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    multiline_trailing_comma: bool
    """Whether to append a trailing comma after the last entry."""

    single_element_trailing_comma: bool
    """Whether a single-element sequence requires a trailing comma."""

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

    empty_sequence: str | None
    """Override for empty sequence literals, or ``None``."""

    empty_dict: str | None
    """Override for empty dict literals, or ``None``."""

    set_open: str
    """The opening delimiter for set literals."""

    set_close: str
    """The closing delimiter for set literals."""

    empty_set: str | None
    """Override for empty set literals, or ``None``."""

    @property
    def format_sequence_entry(self) -> Callable[[str], str]:
        """Callable that formats a sequence entry."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_set_entry(self) -> Callable[[str], str]:
        """Callable that formats a set entry."""
        ...  # pylint: disable=unnecessary-ellipsis

    comment_prefix: str
    """The comment prefix for the language."""

    comment_suffix: str
    """The comment suffix for the language."""

    omap_open: str
    """The opening delimiter for ordered-map literals."""

    omap_close: str
    """The closing delimiter for ordered-map literals."""

    @property
    def format_omap_entry(self) -> Callable[[str, str], str]:
        """Callable that formats one ordered-map entry."""
        ...  # pylint: disable=unnecessary-ellipsis

    multiline_close_indent: str
    """The prefix to prepend to the closing delimiter of multi-line
    structures.
    """

    element_separator: str
    """The separator placed between elements in inline sequences."""

    skip_null_dict_values: bool
    """Whether to omit dict entries whose value is ``None``."""

    coerce_heterogeneous_scalars_to_strings: bool
    """Whether to coerce all scalar values in heterogeneous collections
    to strings so that every element shares a single type.
    """

    coerce_heterogeneous_collection_values_to_strings: bool
    """Whether to coerce dict values and list elements that span
    multiple type families to strings so every value shares a single
    type.

    For example, ``{"name": "Bob", "tags": ["admin"]}`` becomes
    ``{"name": "Bob", "tags": "[\"admin\"]"}``, and
    ``[true, "hi", [1, 2]]`` becomes ``["True", "hi", "[1, 2]"]``.
    """

    supports_collection_comments: bool
    """Whether the language supports comments inside collection
    initializers.

    When ``False``, YAML comments on collection elements are emitted as
    standalone comment lines immediately before the collection (or before
    the variable declaration when a variable name is supplied) rather than
    being placed inside the ``{...}`` block.
    """

    @property
    def format_variable_declaration(self) -> Callable[[str, str], str]:
        """Callable that formats a new variable declaration.

        Called as ``format_variable_declaration(name, value)`` where *name* is
        the variable name and *value* is the already-formatted literal value.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_variable_assignment(self) -> Callable[[str, str], str]:
        """Callable that formats an assignment to an existing variable.

        Called as ``format_variable_assignment(name, value)`` where *name* is
        the variable name and *value* is the already-formatted literal value.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def sequence_format(self) -> enum.Enum:
        """The sequence format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis
