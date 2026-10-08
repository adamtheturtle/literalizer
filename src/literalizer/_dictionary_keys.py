"""String-key rendering shared by the recursive and document renderers."""

from collections.abc import Callable
from typing import Protocol, runtime_checkable

from beartype import beartype

from literalizer._language import Language


@runtime_checkable
class _DictionaryKeyLanguage(Protocol):
    """A language whose string keys have different syntax from values."""

    @property
    def format_dict_key(self) -> Callable[[str], str]:
        """Render a string key with its scalar escaping rules."""
        ...


@beartype
def dictionary_key_formatter(
    *, language: Language
) -> Callable[[str], str] | None:
    """Return the scalar formatter for the semantic dictionary-key
    role.
    """
    if isinstance(language, _DictionaryKeyLanguage):
        return language.format_dict_key
    return None
