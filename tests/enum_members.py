"""Look up named option members across languages' distinct enums.

Axis builders, rejection manifests and language metadata use the same
lookup when a formatter choice has a shared spelling across languages.
"""

import enum

from beartype import beartype


@beartype
def find_enum_member(
    *,
    enum_cls: type[enum.Enum],
    name: str,
) -> enum.Enum | None:
    """Return the member of *enum_cls* named *name*, or ``None``."""
    for member in enum_cls:
        if member.name == name:
            return member
    return None


@beartype
def enum_member_by_name(
    *,
    enum_cls: type[enum.Enum],
    name: str,
) -> enum.Enum:
    """Return the enum member in *enum_cls* whose ``.name`` matches."""
    member = find_enum_member(enum_cls=enum_cls, name=name)
    if member is None:
        msg = f"{enum_cls.__name__} has no member named {name!r}"
        raise ValueError(msg)
    return member
