"""Expectations resolved before exercising a golden rendering."""

import dataclasses


@dataclasses.dataclass(frozen=True, kw_only=True)
class Success:
    """Run the renderer and compare the resulting text."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class Rejection:
    """Exercise a documented error at the public API boundary."""

    error: type[Exception]
    match: str | None
    exact_type: bool = False  # noqa: NOD001 - existing subclass contracts


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exclusion:
    """The scenario intentionally omits this combination."""

    reason: str


type GoldenOutcome = Success | Rejection | Exclusion

SUCCESS: Success = Success()
