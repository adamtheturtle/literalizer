"""Type aliases used across the literalizer package."""

import datetime
import enum

from beartype import beartype

type Scalar = (
    str | int | float | bool | None | datetime.date | datetime.datetime | bytes
)
type Value = Scalar | list[Value] | dict[str, Value] | set[Scalar]


@beartype
def set_sort_key(value: Scalar) -> tuple[str, str]:
    """Return a stable sort key for set elements.

    Sets are unordered, so we sort by type name and then ``repr`` to get
    a deterministic output that also copes with heterogeneous element
    types that may not be mutually comparable.

    Shared so that any code that needs to match the order emitted by the
    core set formatters (e.g. comment extraction) uses the same key.
    """
    return (type(value).__name__, repr(value))


class ValueKind(enum.Enum):
    """Classifies a formatted value for variable declaration purposes.

    Passed to declaration/assignment formatters so they can choose the
    correct type keyword without inspecting the formatted string.
    """

    STRING_LITERAL = "string_literal"
    """C-style string literal (``"..."``).  Relevant for C++ where
    ``readability-qualified-auto`` requires ``const auto*``.
    """

    TYPED_EXPRESSION = "typed_expression"
    """Expression with an explicit type (``std::vector<int>{...}``,
    ``42``, ``true``, etc.).
    """
