"""Worker-release measurements distinguish simultaneous and idle
releases.
"""

import pytest

from scripts.pytest_worker_timing import completion_tail


@pytest.mark.parametrize(
    argnames=("arrivals", "expected"),
    argvalues=[
        ({}, 0.0),
        ({"gw0": 10.0}, 0.0),
        ({"gw0": 10.0, "gw1": 10.0}, 0.0),
        ({"gw0": 10.0, "gw1": 25.0, "gw2": 30.0}, 25.0),
    ],
)
def test_worker_release_tail(
    arrivals: dict[str, float], expected: float
) -> None:
    """Sum released-worker intervals, rather than longest job duration."""
    assert completion_tail(arrivals=arrivals) == expected
