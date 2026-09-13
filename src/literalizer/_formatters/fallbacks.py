"""Explicit fallback selection for optional and empty formatter values."""

from collections.abc import Sized

from beartype import beartype

from literalizer._types import Scalar, Value


@beartype
def value_or_default[T](*, value: T | None, default: T) -> T:
    """Use the default only when no value was supplied."""
    if value is None:
        return default
    return value


@beartype
def nonempty_or_default[T: Sized](*, value: T | None, default: T) -> T:
    """Use the default when the supplied value is absent or empty."""
    if value is None or len(value) == 0:
        return default
    return value


@beartype
def collection_or_default(
    *,
    value: Value,
    default: list[Value] | dict[Scalar, Value] | set[Scalar],
) -> list[Value] | dict[Scalar, Value] | set[Scalar]:
    """Use a resolved collection for its opener, or retain the source."""
    if isinstance(value, (list, dict, set)):
        return value
    return default
