"""Empty worker histories have no release tail."""

from scripts.pytest_worker_timing import completion_tail


def test_no_workers_have_zero_release_tail() -> None:
    """Keep the empty-input contract that serial capture does not call."""
    assert completion_tail(arrivals={}) == 0.0
