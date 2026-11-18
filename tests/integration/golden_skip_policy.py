"""Declarative skip policies carried by golden rendering records."""

import dataclasses


@dataclasses.dataclass(frozen=True, kw_only=True)
class SkipReason:
    """Why one error skips a golden rather than failing it.

    ``unlink`` marks an earlier golden as stale. Explicit regeneration
    removes it; ordinary verification reports it without modifying it.
    """

    error: type[Exception]
    reason: str
    unlink: bool


type SkipReasons = tuple[SkipReason, ...]


@dataclasses.dataclass(frozen=True, kw_only=True)
class SkipPolicy:
    """Which errors skip a rendering, and what the skip message says.

    ``suffix`` is appended to the reason, so a skip that turns on more
    than the error type -- the strategy the golden was rendered under,
    say -- says so without restating the reason.
    """

    reasons: SkipReasons
    suffix: str


NO_SKIPS: SkipPolicy = SkipPolicy(reasons=(), suffix="")
"""Every error is a real failure."""
