"""Look up a language option's enum member by the name a file spells.

Every declared test file -- an axis in ``axes.toml``, a rejection
manifest, a language's own metadata -- names an option member as a
string.  Both are resolved here, so the suites that read one share a
spelling and an error message.
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
