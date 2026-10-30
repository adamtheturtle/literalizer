"""Record worker collection and shutdown arrivals without per-test logging.

Load with ``pytest -p scripts.pytest_worker_timing``. The controller emits
one JSON summary. Shutdown includes teardown and communication; its tail
is an observation of released workers, not a promised scheduling speedup.

An upstream replacement is tracked at
https://github.com/messense/pytest-timing/issues/12 (workers-only capture) and
https://github.com/messense/pytest-timing/issues/11 (monotonic timings).
"""

import json
from collections.abc import Mapping
from dataclasses import dataclass
from time import perf_counter
from typing import Protocol

import pytest
from _pytest.terminal import TerminalReporter

__all__ = (
    "completion_tail",
    "pytest_sessionstart",
    "pytest_terminal_summary",
    "pytest_testnodedown",
    "pytest_xdist_node_collection_finished",
)


class _Gateway(Protocol):
    """Gateway identity supplied by pytest-xdist."""

    id: str


class _Worker(Protocol):
    """The controller fields this optional plugin reads."""

    gateway: _Gateway


@dataclass
class _Clock:
    """Mutable session timing state, reset for each pytest invocation."""

    started: float


_CLOCK = _Clock(started=0.0)
_COLLECTED: dict[str, float] = {}
_FINISHED: dict[str, float] = {}
_ERRORS: list[str] = []


def completion_tail(*, arrivals: Mapping[str, float]) -> float:
    """Sum the interval each released worker waits for the final
    release.
    """
    if len(arrivals) == 0:
        return 0.0
    last = max(arrivals.values())
    return sum(last - value for value in arrivals.values())


def pytest_sessionstart() -> None:
    """Reset state even when pytest is invoked repeatedly in one
    process.
    """
    _CLOCK.started = perf_counter()
    _COLLECTED.clear()
    _FINISHED.clear()
    _ERRORS.clear()


@pytest.hookimpl(optionalhook=True)
def pytest_xdist_node_collection_finished(node: _Worker) -> None:
    """Record collection completion as observed by the controller."""
    _COLLECTED[node.gateway.id] = perf_counter() - _CLOCK.started


@pytest.hookimpl(optionalhook=True)
def pytest_testnodedown(node: _Worker, error: object | None) -> None:
    """Record worker release, retaining failures instead of hiding
    them.
    """
    worker = node.gateway.id
    _FINISHED[worker] = perf_counter() - _CLOCK.started
    if error is not None:
        _ERRORS.append(worker)


def pytest_terminal_summary(terminalreporter: TerminalReporter) -> None:
    """Emit small machine-readable evidence without changing pytest
    results.
    """
    if len(_FINISHED) == 0:
        return
    report = {
        "collection_finished_seconds": _COLLECTED,
        "worker_released_seconds": _FINISHED,
        "released_worker_tail_seconds": completion_tail(arrivals=_FINISHED),
        "worker_errors": _ERRORS,
        "observation": "Arrivals include teardown and communication. "
        "the tail is not a measured recoverable speedup.",
    }
    terminalreporter.write_sep(sep="=", title="xdist worker timing")
    terminalreporter.write_line(line=json.dumps(obj=report, sort_keys=True))
