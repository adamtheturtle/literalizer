"""Explicit fallback selection for absent and empty formatter values."""

from collections.abc import Sized

from beartype import beartype


@beartype
def nonempty_or_default[T: Sized](*, value: T | None, default: T) -> T:
    """Use the default when the supplied value is absent or empty."""
    if value is None or len(value) == 0:
        return default
    return value
