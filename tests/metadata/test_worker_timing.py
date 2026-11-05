"""Worker-release measurements distinguish simultaneous and idle
releases.
"""

import pytest
from pydantic import BaseModel, TypeAdapter

from scripts.pytest_worker_timing import completion_tail
from tests.toml_cases import load_toml_cases


class _ReleaseCase(BaseModel, extra="forbid", frozen=True):
    """One worker arrival history and its expected release tail."""

    name: str
    arrivals: dict[str, float]
    expected: float


class _Cases(BaseModel, extra="forbid", frozen=True):
    """The declarative worker measurement controls."""

    cases: tuple[_ReleaseCase, ...]


_CASES = TypeAdapter(type=_Cases).validate_python(
    load_toml_cases(name="worker_release_measurements")
)


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.cases, ids=lambda case: case.name
)
def test_worker_release_tail(case: _ReleaseCase) -> None:
    """Sum released-worker intervals, rather than longest job duration."""
    assert completion_tail(arrivals=case.arrivals) == case.expected
