"""The one way an integration test compares output to a golden file.

Every golden-file harness -- ``literalize``, ``literalize_call``, the
``$ref`` cases and the constructor targets -- finishes the same two
ways: the render succeeded and its text is compared against a
checked-in fixture, or it raised something the language was never
expected to represent and the case is skipped.

Both endings live here so neither can be spelled two ways.  The skip
vocabulary (:class:`SkipReason`, :class:`SkipPolicy`) is declared here
as well; the tables built from it belong to the scenarios that use
them.
"""

import dataclasses
from pathlib import Path
from types import TracebackType
from typing import NoReturn, Protocol, runtime_checkable

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture


@dataclasses.dataclass(frozen=True, kw_only=True)
class SkipReason:
    """Why one error skips a golden rather than failing it.

    ``unlink`` drops any golden file left by an earlier run, so a stale
    fixture cannot pose as a real result on the next one.
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

    @property
    def errors(self) -> tuple[type[Exception], ...]:
        """Return the errors that skip rather than fail.

        The tuple is derived from the policy's reasons so an error can
        never be caught without a message to skip with, nor listed with
        a message that no ``except`` clause reaches.
        """
        return tuple(entry.error for entry in self.reasons)


NO_SKIPS: SkipPolicy = SkipPolicy(reasons=(), suffix="")
"""Every error is a real failure."""


@runtime_checkable
class _ReasonedError(Protocol):
    """An error that carries its own account of what it rejected."""

    reason: str


@beartype
def skip_golden(
    *,
    reason: str,
    golden_path: Path,
    unlink: bool,
) -> NoReturn:
    """Skip the current golden case with *reason*.

    Dropping the golden file is part of skipping it: a fixture left by
    an earlier run would otherwise pose as a real result on the next
    one, and the orphan-files check would count it as covered.  The two
    steps are spelled together here so a skip cannot be written without
    deciding which it is.
    """
    if unlink:
        golden_path.unlink(missing_ok=True)
    pytest.skip(reason=reason)


@beartype
def _skip_for_error(
    *,
    exc: Exception,
    reasons: SkipReasons,
    golden_path: Path,
    prefix: str,
    suffix: str,
) -> NoReturn:
    """Skip the current test with a message keyed off the caught error.

    The message reads ``"{prefix} {reason}{suffix}"``, so a rendering
    whose skip turns on more than the error type -- the strategy it was
    rendered under, say -- says so in *suffix* rather than restating the
    reason.  An error that carries its own ``reason`` -- which argument
    or identifier the language rejected -- has it appended after the
    declared one, since only the error knows it.  The ``except`` clause
    is built from the same table, so the lookup below is total by
    construction; ``StopIteration`` propagating out of this helper would
    indicate a divergence between the two.
    """
    entry = next(entry for entry in reasons if isinstance(exc, entry.error))
    detail = f": {exc.reason}" if isinstance(exc, _ReasonedError) else ""
    skip_golden(
        reason=f"{prefix} {entry.reason}{detail}{suffix}",
        golden_path=golden_path,
        unlink=entry.unlink,
    )


@dataclasses.dataclass(frozen=True, kw_only=True)
class GoldenSkips:
    """A block whose declared errors skip the golden rather than fail it.

    Wrapping the rendering in this rather than catching *policy*'s
    errors at each site keeps the table and its ``except`` clause in one
    place, so a harness cannot catch an error it has no message for.  An
    error the policy does not name propagates: ``__exit__`` never
    swallows one, it either skips or returns.
    """

    policy: SkipPolicy
    golden_path: Path
    prefix: str

    def __enter__(self) -> None:
        """Enter the guarded rendering."""

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        exc: BaseException | None,
        _traceback: TracebackType | None,
    ) -> None:
        """Skip the case when the rendering raised a declared error."""
        if isinstance(exc, self.policy.errors):
            _skip_for_error(
                exc=exc,
                reasons=self.policy.reasons,
                golden_path=self.golden_path,
                prefix=self.prefix,
                suffix=self.policy.suffix,
            )


@beartype
def check_golden(
    *,
    contents: str,
    extension: str,
    golden_path: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Compare *contents* against the fixture at *golden_path*."""
    # newline="" prevents Python text-mode from converting \r\n to \n on
    # Windows, which would corrupt golden files containing literal CR
    # bytes (e.g. CommonLisp string_control_chars).
    file_regression.check(
        contents=contents,
        encoding="utf-8",
        extension=extension,
        newline="",
        fullpath=golden_path,
    )
