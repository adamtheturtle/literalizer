"""Native equality assertions for call transforms."""

import dataclasses
from collections.abc import Callable
from typing import Protocol, runtime_checkable

from beartype import beartype

from literalizer._language import Language
from literalizer._literalize import CallContext


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class EqualityAssertion:
    """A two-operand call transform and its file-level dependencies."""

    format_assertion: Callable[[str, str], str]
    preamble: tuple[str, ...]

    def __call__(self, context: CallContext, /) -> str:
        """Compare the two rendered operands using native assertion syntax."""
        actual, expected = context.arguments
        return self.format_assertion(actual, expected)


@runtime_checkable
class _EqualityAssertionLanguage(Protocol):
    """A language that supplies a native equality assertion."""

    @property
    def equality_assertion(self) -> EqualityAssertion:
        """Return the configured assertion and its preamble."""
        ...


@beartype
def equality_assertion_for(*, language: Language) -> EqualityAssertion | None:
    """Return the language's equality assertion when available."""
    if isinstance(language, _EqualityAssertionLanguage):
        return language.equality_assertion
    return None
