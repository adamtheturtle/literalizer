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

from literalizer import LiteralizeResult


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


@runtime_checkable
class _ReasonedError(Protocol):
    """An error that carries its own account of what it rejected."""

    reason: str


@beartype
def cleanup_stale_golden(*, golden_path: Path, config: pytest.Config) -> None:
    """Remove a skipped fixture only during explicit regeneration."""
    if config.getoption(name="regen_all") is True:
        golden_path.unlink(missing_ok=True)
    elif golden_path.exists():
        pytest.fail(
            reason=(
                f"Stale golden file: {golden_path}. "
                "Run its golden test with --regen-all to remove it."
            ),
        )


@beartype
def skip_golden(
    *,
    reason: str,
    golden_path: Path,
    unlink: bool,
    config: pytest.Config,
) -> NoReturn:
    """Skip the current golden case with *reason*.

    A stale fixture fails ordinary verification without modifying the
    file. Explicit regeneration removes it before skipping the case.
    """
    if unlink:
        cleanup_stale_golden(golden_path=golden_path, config=config)
    pytest.skip(reason=reason)


@dataclasses.dataclass(frozen=True, kw_only=True)
class GoldenSkips:
    """A block whose declared errors skip the golden rather than fail it.

    The first matching policy entry supplies both the skip message and
    the stale-fixture policy. Errors without a matching entry propagate.
    """

    policy: SkipPolicy
    golden_path: Path
    prefix: str
    config: pytest.Config

    def __enter__(self) -> None:
        """Enter the guarded rendering."""

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        exc: BaseException | None,
        _traceback: TracebackType | None,
    ) -> None:
        """Skip the case when the rendering raised a declared error."""
        for entry in self.policy.reasons:
            if isinstance(exc, entry.error):
                detail = (
                    f": {exc.reason}"
                    if isinstance(exc, _ReasonedError)
                    else ""
                )
                skip_golden(
                    reason=(
                        f"{self.prefix} {entry.reason}"
                        f"{detail}{self.policy.suffix}"
                    ),
                    golden_path=self.golden_path,
                    unlink=entry.unlink,
                    config=self.config,
                )


@beartype
def check_golden(
    *,
    contents: str,
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
        extension=golden_path.suffix,
        newline="",
        fullpath=golden_path,
    )


@beartype
def format_consumer(
    *, template: str, result: LiteralizeResult, golden_path: Path
) -> str:
    """Format a native consumer from the result and fixture path."""
    return template.format(
        preamble="\n".join(result.preamble),
        body_preamble="\n".join(result.body_preamble),
        code=result.code,
        bare_code=result.bare_code,
        module_name=(
            f"Fixture_{golden_path.parent.name}_"
            f"{golden_path.stem.rsplit(sep='@', maxsplit=1)[0]}"
        ),
    )
