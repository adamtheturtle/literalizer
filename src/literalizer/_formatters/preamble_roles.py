"""Retain import roles through generated preamble assembly."""

from collections.abc import Sequence
from typing import Self

from beartype import beartype


class _PreambleImport(str):
    """An import or include selected by a preamble producer."""

    __slots__ = ()


@beartype
class _PreambleBlock(str):
    """A joined block whose constituent roles remain available."""

    __slots__ = ("_entries",)

    _entries: tuple[str, ...]

    def __new__(cls, code: str, /, *, entries: tuple[str, ...]) -> Self:
        """Allocate text; the initializer retains producer metadata."""
        del entries
        return super().__new__(cls, object=code)

    def __init__(self, _code: str, /, *, entries: tuple[str, ...]) -> None:
        """Retain components when a producer joins a supporting block."""
        self._entries = entries

    @property
    def entries(self) -> tuple[str, ...]:
        """The entries supplied by the producer before flattening."""
        return self._entries


@beartype
def import_preamble(*, code: str) -> str:
    """Mark an owned import or include at its producer."""
    return _PreambleImport(object=code)


@beartype
def join_preamble(*, entries: Sequence[str]) -> str:
    """Join supporting source without losing constituent import roles."""
    return _PreambleBlock("\n".join(entries), entries=tuple(entries))


@beartype
def _preamble_lines(entries: Sequence[str], /) -> tuple[str, ...]:
    """Expand producer-owned blocks into lines with their retained
    roles.
    """
    lines: list[str] = []
    for entry in entries:
        if isinstance(entry, _PreambleBlock):
            lines.extend(_preamble_lines(entry.entries))
        elif isinstance(entry, _PreambleImport):
            lines.append(entry)
        else:
            lines.extend(entry.split(sep="\n"))
    return tuple(lines)


@beartype
def preamble_imports(entries: Sequence[str], /) -> tuple[str, ...]:
    """Select imports from the producer's roles rather than source
    prefixes.
    """
    return tuple(
        entry
        for entry in _preamble_lines(entries)
        if isinstance(entry, _PreambleImport)
    )


@beartype
def imports_first(
    *, entries: Sequence[str], deduplicate_imports: bool
) -> tuple[str, ...]:
    """Hoist retained imports while preserving all other line order."""
    lines = _preamble_lines(entries)
    imports = tuple(
        entry for entry in lines if isinstance(entry, _PreambleImport)
    )
    if deduplicate_imports:
        imports = tuple(dict.fromkeys(imports))
    other = tuple(
        entry for entry in lines if not isinstance(entry, _PreambleImport)
    )
    return (*imports, *other)
