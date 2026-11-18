"""Golden comparison and the remaining legacy skip policies.

Expected outcomes are resolved by the individual runners. The legacy
skip policies cover constraints still evaluated during rendering.
"""

import dataclasses
import enum
from pathlib import Path
from types import TracebackType
from typing import Protocol, runtime_checkable

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import Language, LiteralizeResult

from .fixture_names import fixture_module_name
from .language_metadata import language_metadata


@dataclasses.dataclass(frozen=True, kw_only=True)
class SkipReason:
    """Why one error skips a golden rather than failing it."""

    error: type[Exception]
    reason: str


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
def assert_no_golden(*, golden_path: Path) -> None:
    """Fail when an unsuccessful rendering still has a success fixture."""
    if golden_path.exists():
        pytest.fail(
            reason=f"Unexpected success fixture: {golden_path}",
        )


@dataclasses.dataclass(frozen=True, kw_only=True)
class GoldenSkips:
    """A block whose declared errors skip the golden rather than fail it.

    Errors outside the policy propagate. Every skip checks ownership.
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
        for entry in self.policy.reasons:
            if isinstance(exc, entry.error):
                detail = (
                    f": {exc.reason}"
                    if isinstance(exc, _ReasonedError)
                    else ""
                )
                assert_no_golden(golden_path=self.golden_path)
                pytest.skip(
                    reason=(
                        f"{self.prefix} {entry.reason}"
                        f"{detail}{self.policy.suffix}"
                    )
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
    *,
    template: str,
    result: LiteralizeResult,
    golden_path: Path,
    spec: Language,
) -> str:
    """Format a native consumer from the result and fixture path."""
    return template.format(
        **{
            name: value.name
            for name, value in vars(spec).items()
            if isinstance(value, enum.Enum)
        },
        preamble="\n".join(result.preamble),
        body_preamble="\n".join(result.body_preamble),
        code=result.code,
        bare_code=result.bare_code,
        module_name=fixture_module_name(golden_path=golden_path),
    )


@beartype
def fixture_contents(
    *, code: str, language_id: str, intentional_identifier: bool
) -> str:
    """Finish a fixture with its declared identifier preamble and
    newline.
    """
    preamble = (
        language_metadata(
            language_id=language_id
        ).golden.intentional_identifier_preamble
        if intentional_identifier
        else ()
    )
    return "\n".join((*preamble, code, ""))
