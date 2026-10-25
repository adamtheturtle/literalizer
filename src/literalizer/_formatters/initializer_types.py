"""Retain a collection producer's type through literal text assembly."""

from typing import Self

from beartype import beartype

from literalizer._formatters.collection_openers import CollectionOverride


@beartype
class TypedCollectionOpen(str):
    """An opening delimiter with its selected declaration type."""

    __slots__ = ("_declared_type",)

    _declared_type: str

    def __new__(cls, code: str, /, *, declared_type: str) -> Self:
        """Allocate text; the initializer retains producer metadata."""
        del declared_type
        return super().__new__(cls, object=code)

    def __init__(self, _code: str, /, *, declared_type: str) -> None:
        """Retain the selected type alongside the string value."""
        self._declared_type = declared_type

    @property
    def declared_type(self) -> str:
        """The type selected alongside this opener."""
        return self._declared_type


@beartype
class SingleElementCollectionOpen(TypedCollectionOpen):
    """A native constructor with separate delimiters around its one
    child.
    """

    __slots__ = ("_delimiters",)

    _delimiters: tuple[str, str]

    def __new__(
        cls,
        code: str,
        /,
        *,
        declared_type: str,
        delimiters: tuple[str, str],
    ) -> Self:
        """Allocate the opener while retaining the original native
        type.
        """
        del delimiters
        return super().__new__(cls, code, declared_type=declared_type)

    def __init__(
        self,
        code: str,
        /,
        *,
        declared_type: str,
        delimiters: tuple[str, str],
    ) -> None:
        """Retain the constructor separately from its selected type."""
        super().__init__(code, declared_type=declared_type)
        self._delimiters = delimiters

    @property
    def delimiters(self) -> tuple[str, str]:
        """The constructor's opening and closing source text."""
        return self._delimiters


@beartype
class TypedInitializer(str):
    """A literal whose declaration type is already known."""

    __slots__ = ("_declared_type",)

    _declared_type: str

    def __new__(cls, code: str, /, *, declared_type: str) -> Self:
        """Allocate text; the initializer retains producer metadata."""
        del declared_type
        return super().__new__(cls, object=code)

    def __init__(self, _code: str, /, *, declared_type: str) -> None:
        """Retain the selected type alongside the string value."""
        self._declared_type = declared_type

    @property
    def declared_type(self) -> str:
        """The literal's selected declaration type."""
        return self._declared_type


@beartype
def single_element_initializer_delimiters(
    opener: str, /
) -> tuple[str, str] | None:
    """Read a native singleton constructor without losing its type."""
    if not isinstance(opener, SingleElementCollectionOpen):
        return None
    opening, closing = opener.delimiters
    return (
        TypedCollectionOpen(opening, declared_type=opener.declared_type),
        closing,
    )


@beartype
def finish_collection_initializer(*, opener: str, code: str) -> str:
    """Carry an opener's type through the completed collection."""
    if isinstance(opener, CollectionOverride):
        opener = opener.original
    if isinstance(opener, TypedCollectionOpen):
        return TypedInitializer(code, declared_type=opener.declared_type)
    return code


@beartype
def prefix_initializer(*, code: str, prefix: str) -> str:
    """Add layout indentation without losing the initializer type."""
    result = f"{prefix}{code}"
    if isinstance(code, TypedInitializer):
        return TypedInitializer(result, declared_type=code.declared_type)
    return result


@beartype
def initializer_type(code: str, /) -> str | None:
    """Read the type retained by an initializer producer."""
    return code.declared_type if isinstance(code, TypedInitializer) else None
