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
from typing import NoReturn

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


@beartype
def skip_for_error(
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
    reason.  The ``except`` clause is built from the same table, so the
    lookup below is total by construction; ``StopIteration`` propagating
    out of this helper would indicate a divergence between the two.
    """
    entry = next(entry for entry in reasons if isinstance(exc, entry.error))
    if entry.unlink:
        golden_path.unlink(missing_ok=True)
    pytest.skip(f"{prefix} {entry.reason}{suffix}")


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
