"""Language-owned printing expressions and their import requirements."""

from dataclasses import dataclass
from typing import ClassVar, Protocol, runtime_checkable

from beartype import beartype

from literalizer._formatters.preamble_roles import import_preamble
from literalizer._language import Language
from literalizer._literalize import CallContext
from literalizer.exceptions import UnsupportedCallShapeError


@dataclass(frozen=True, kw_only=True)
class PrintResultFormat:
    """Native printing syntax, without a statement terminator."""

    prefix: str
    suffix: str
    imports: tuple[str, ...]


@runtime_checkable
class _PrintResultLanguage(Protocol):
    """Optional printing capability declared by a language."""

    @property
    def print_result_format(self) -> PrintResultFormat:
        """The language's native printing operation."""
        ...


@dataclass(frozen=True, kw_only=True)
class _PrintResultTransform:
    """Keep a print expression and its dependencies together."""

    format: PrintResultFormat
    uses_zipped: ClassVar[bool] = False

    @property
    def call_preamble(self) -> tuple[str, ...]:
        """Retain producer-owned import roles for composition."""
        return tuple(
            import_preamble(code=code) for code in self.format.imports
        )

    def __call__(self, context: CallContext) -> str:
        """Consume the call exactly once through native printing."""
        return self.format.prefix + context.call + self.format.suffix


@beartype
def print_result_transform(*, language: Language) -> _PrintResultTransform:
    """Select an explicit language capability without inspecting code."""
    if not isinstance(language, _PrintResultLanguage):
        raise UnsupportedCallShapeError(
            language_name=type(language).__name__,
            reason="print_result is not supported by this language",
        )
    return _PrintResultTransform(format=language.print_result_format)
