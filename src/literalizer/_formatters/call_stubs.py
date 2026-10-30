"""Names for the type declarations used by dotted call stubs."""

from collections import Counter
from collections.abc import Sequence
from typing import Literal

from beartype import beartype


@beartype
def dotted_helper_type_names(
    *,
    parts: Sequence[str],
    suffix: Literal["Type", "Type_"],
    ignore_underscores: bool,
    capitalize_parts: bool,
) -> tuple[str, ...]:
    """Preserve ordinary names and index only colliding helper types.

    Nim compares these capitalized names without case or underscores.
    The fixed type suffixes end in a letter or underscore, so an indexed
    name cannot collide with an unchanged name. Distinct positions have
    distinct indices even when their source components repeat.
    """
    names = tuple(
        f"{part.capitalize() if capitalize_parts else part.title()}{suffix}"
        for part in parts
    )
    keys = tuple(
        name.replace("_", "").casefold() if ignore_underscores else name
        for name in names
    )
    counts = Counter(keys)
    return tuple(
        f"{name}{index}" if counts[key] > 1 else name
        for index, (name, key) in enumerate(
            iterable=zip(names, keys, strict=True)
        )
    )
