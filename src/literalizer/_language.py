"""Language protocol and concrete LanguageSpec data class."""

from __future__ import annotations

import dataclasses
import datetime  # noqa: TC003
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any


@runtime_checkable
class Language(Protocol):  # pylint: disable=too-many-public-methods
    """Protocol describing how a language formats scalar literals and
    collections.

    Implement this protocol to add support for additional languages
    beyond the built-in defaults.
    """

    @property
    def null_literal(self) -> str:
        """The literal representing null/None."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def true_literal(self) -> str:
        """The literal representing true/True."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def false_literal(self) -> str:
        """The literal representing false/False."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def collection_open(self) -> str:
        """The opening delimiter for collections."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def collection_close(self) -> str:
        """The closing delimiter for collections."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dict_separator(self) -> str:
        """The separator between dict keys and values."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dict_open(self) -> str:
        """The opening delimiter for dict literals."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dict_close(self) -> str:
        """The closing delimiter for dict literals."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_dict_entry(self) -> Callable[[str, str], str] | None:
        """Callable that formats a dict entry from a pre-formatted key
        and value string, or ``None`` to use ``dict_separator``.
        """
        ...  # pylint: disable=unnecessary-ellipsis

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
    def trailing_comma(self) -> bool:
        """Whether to append a trailing comma after the last entry."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def single_element_trailing_comma(self) -> bool:
        """Whether a single-element collection requires a trailing comma
        to be syntactically unambiguous (e.g. Python tuples).
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a :class:`datetime.datetime` as a
        string literal.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def empty_collection(self) -> str | None:
        """Override for empty list literals, or ``None`` to use
        ``collection_open + collection_close``.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def set_open(self) -> str:
        """The opening delimiter for set literals."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def set_close(self) -> str:
        """The closing delimiter for set literals."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def empty_dict(self) -> str | None:
        """Override for empty dict literals, or ``None`` to use
        ``dict_open + dict_close``.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def empty_set(self) -> str | None:
        """Override for empty set literals, or ``None`` to use
        ``set_open + set_close``.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_set_entry(self) -> Callable[[str], str] | None:
        """Callable that formats a set entry from a pre-formatted item
        string, or ``None`` to use the item directly.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def comment_prefix(self) -> str:
        """The comment prefix for the language (e.g. ``"#"`` or
        ``"//"``).
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def omap_open(self) -> str:
        """The opening delimiter for ordered-map literals."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def omap_close(self) -> str:
        """The closing delimiter for ordered-map literals."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_omap_entry(self) -> Callable[[str, str], str]:
        """Callable that formats one ordered-map entry from a
        pre-formatted key and value string.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def multiline_close_indent(self) -> str:
        """The prefix to prepend to the closing delimiter of multi-line
        collections, sets, and dicts.  Defaults to ``""`` (closing
        delimiter at column 0).  Set to ``"    "`` for languages like
        Haskell where the layout rule requires the closing bracket to
        be indented.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_variable_declaration(self) -> Callable[[str, str], str] | None:
        """Callable that formats a variable declaration from a name and
        value string, or ``None`` if not supported.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def skip_null_dict_values(self) -> bool:
        """Whether to omit dict entries whose value is ``None``."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_collection_open(self) -> Callable[[list[Any]], str] | None:
        """Callable that returns the collection opener string for a given
        list of values, or ``None`` to use ``collection_open``.

        When set, the callable receives the raw list values and returns
        the opening delimiter (e.g. ``"new String[]{"`` for an all-string
        Java array).  The closing delimiter is always taken from
        ``collection_close``.
        """
        ...  # pylint: disable=unnecessary-ellipsis


@dataclasses.dataclass(frozen=True)
class LanguageSpec:
    """A concrete implementation of :class:`Language`.

    Predefined specs for common languages are available as module-level
    constants (e.g. :data:`PYTHON`, :data:`JAVASCRIPT`).  Create custom
    instances to support additional languages or override defaults.
    """

    null_literal: str
    true_literal: str
    false_literal: str
    collection_open: str
    collection_close: str
    dict_separator: str
    dict_open: str
    dict_close: str
    format_dict_entry: Callable[[str, str], str] | None
    trailing_comma: bool
    single_element_trailing_comma: bool
    format_bytes: Callable[[bytes], str]
    format_date: Callable[[datetime.date], str]
    format_datetime: Callable[[datetime.datetime], str]
    empty_collection: str | None
    empty_dict: str | None
    set_open: str
    set_close: str
    empty_set: str | None
    format_set_entry: Callable[[str], str] | None
    comment_prefix: str
    omap_open: str
    omap_close: str
    format_omap_entry: Callable[[str, str], str]
    multiline_close_indent: str
    skip_null_dict_values: bool
    format_variable_declaration: Callable[[str, str], str] | None
    format_collection_open: Callable[[list[Any]], str] | None
