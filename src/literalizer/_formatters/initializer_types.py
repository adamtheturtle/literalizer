"""Retain a collection producer's type through literal text assembly."""

from typing import Self

from beartype import beartype


class TypedCollectionOpen(str):
    """An opening delimiter with its selected declaration type."""

    __slots__ = ("_declared_type",)

    _declared_type: str

    @classmethod
    def create(cls, code: str, /, *, declared_type: str) -> Self:
        """Retain the selected type alongside the string value."""
        result = cls(object=code)
        result._declared_type = declared_type
        return result

    @property
    def declared_type(self) -> str:
        """The type selected alongside this opener."""
        return self._declared_type


class TypedInitializer(str):
    """A literal whose declaration type is already known."""

    __slots__ = ("_declared_type",)

    _declared_type: str

    @classmethod
    def create(cls, code: str, /, *, declared_type: str) -> Self:
        """Retain the selected type alongside the string value."""
        result = cls(object=code)
        result._declared_type = declared_type
        return result

    @property
    def declared_type(self) -> str:
        """The literal's selected declaration type."""
        return self._declared_type


@beartype
def finish_collection_initializer(*, opener: str, code: str) -> str:
    """Carry an opener's type through the completed collection."""
    if isinstance(opener, TypedCollectionOpen):
        return TypedInitializer.create(
            code, declared_type=opener.declared_type
        )
    return code


@beartype
def prefix_initializer(*, code: str, prefix: str) -> str:
    """Add layout indentation without losing the initializer type."""
    result = f"{prefix}{code}"
    if isinstance(code, TypedInitializer):
        return TypedInitializer.create(
            result, declared_type=code.declared_type
        )
    return result


@beartype
def initializer_type(code: str, /) -> str | None:
    """Read the type retained by an initializer producer."""
    return code.declared_type if isinstance(code, TypedInitializer) else None
