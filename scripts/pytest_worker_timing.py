"""Adapt pytest-timing's public worker JSON to the existing CI summary.

Load with ``-p timing -p scripts.pytest_worker_timing`` and
``--timing-capture=workers --timing-json-file=PATH``. pytest-timing owns
worker observation; this adapter retains the release-tail calculation.
Offsets use the upstream run's origin. Shutdown includes fixture cleanup and
communication, so the tail is not a promised scheduling speedup.
"""

import json
from collections.abc import Mapping

import pytest
from _pytest.terminal import TerminalReporter
from pydantic import BaseModel

__all__ = ("completion_tail", "pytest_terminal_summary")


class _Worker(BaseModel, extra="ignore", frozen=True, strict=True):
    """The public timing fields needed for one worker."""

    id: str
    collected: float | None
    down: float | None
    error: str | None


class _Report(BaseModel, extra="ignore", frozen=True, strict=True):
    """Read the public report while allowing unrelated upstream fields."""

    run: Mapping[str, object]
    workers: tuple[_Worker, ...]


def completion_tail(*, arrivals: Mapping[str, float]) -> float:
    """Sum the interval each released worker waits for the final
    release.
    """
    if len(arrivals) == 0:
        return 0.0
    last = max(arrivals.values())
    return sum(last - value for value in arrivals.values())


def pytest_terminal_summary(
    terminalreporter: TerminalReporter, config: pytest.Config
) -> None:
    """Summarize the report without changing pytest's outcome on read
    errors.
    """
    report_name = config.getoption(name="timing_json_file", default=None)
    if not isinstance(report_name, str):
        return
    try:
        data = _Report.model_validate_json(
            json_data=(config.rootpath / report_name).read_text(
                encoding="utf-8"
            )
        )
    except (OSError, ValueError) as error:
        terminalreporter.write_line(
            line=f"worker timing summary unavailable: {error}", yellow=True
        )
        return
    if data.run.get("workers_only") is not True or not isinstance(
        data.run.get("dist"), str
    ):
        return
    collected = {
        worker.id: worker.collected
        for worker in data.workers
        if worker.collected is not None
    }
    finished = {
        worker.id: worker.down
        for worker in data.workers
        if worker.down is not None
    }
    if len(finished) == 0:
        return
    report = {
        "collection_finished_seconds": collected,
        "worker_released_seconds": finished,
        "released_worker_tail_seconds": completion_tail(arrivals=finished),
        "worker_errors": [
            worker.id for worker in data.workers if worker.error is not None
        ],
        "observation": "Arrivals include teardown and communication. "
        "the tail is not a measured recoverable speedup.",
    }
    terminalreporter.write_sep(sep="=", title="xdist worker timing")
    terminalreporter.write_line(line=json.dumps(obj=report, sort_keys=True))
