"""Explicit source-layout policy and placement for generated fragments."""

import dataclasses
import enum

from beartype import beartype

from literalizer.exceptions import SourceLayoutError


class SourceFormat(enum.StrEnum):
    """Source layout selected by a supporting language specification."""

    PRESERVE = "preserve"
    CANONICAL = "canonical"


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class SourceContext:
    """Placement and available width of one generated source fragment.

    ``initial_column`` accounts for caller-owned text before the first
    character of the fragment. ``continuation_column`` sets the absolute
    indentation of continuation lines when the caller supplies an enclosing
    expression. Ordinary statements use their enclosing indentation.
    """

    indent_level: int = 0
    initial_column: int = 0
    continuation_column: int | None = None
    column_limit: int = 80

    def __post_init__(self) -> None:
        """Reject positions and widths which cannot describe source."""
        if self.indent_level < 0 or self.initial_column < 0:
            msg = "Source indentation and initial column must be nonnegative"
            raise SourceLayoutError(msg)
        if (
            self.continuation_column is not None
            and self.continuation_column < 0
        ):
            msg = "Source continuation column must be nonnegative"
            raise SourceLayoutError(msg)
        if self.column_limit < 1:
            msg = "Source column limit must be positive"
            raise SourceLayoutError(msg)
