"""Source-format-independent comment metadata."""

import dataclasses

from beartype import beartype


@beartype
@dataclasses.dataclass(frozen=True)
class ElementComments:
    """Comments associated with a single collection element."""

    before: tuple[str, ...]
    inline: str


@beartype
@dataclasses.dataclass(frozen=True)
class CollectionComments:
    """Comments extracted from a sequence or mapping."""

    elements: tuple[ElementComments, ...]
    trailing: tuple[str, ...]


@beartype
@dataclasses.dataclass(frozen=True)
class ScalarComments:
    """Comments extracted from a scalar document."""

    before: list[str]
    inline: str
    after: list[str]
