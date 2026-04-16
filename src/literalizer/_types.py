"""Type aliases used across the literalizer package."""

import datetime
import enum

type Scalar = (
    str | int | float | bool | None | datetime.date | datetime.datetime | bytes
)
type Value = Scalar | list[Value] | dict[str, Value] | set[Scalar]


class ValueKind(enum.Enum):
    """Classifies a formatted value for variable declaration purposes.

    Passed to declaration/assignment formatters so they can choose the
    correct type keyword without inspecting the formatted string.
    """

    BARE_BRACE_INIT = "bare_brace_init"
    """Bare brace-init list (``{...}``) with no type prefix."""

    STRING_LITERAL = "string_literal"
    """C-style string literal (``"..."``).  Relevant for C++ where
    ``readability-qualified-auto`` requires ``const auto*``.
    """

    TYPED_EXPRESSION = "typed_expression"
    """Expression with an explicit type (``std::vector<int>{...}``,
    ``42``, ``true``, etc.).
    """
