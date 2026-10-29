"""CI timing evidence must not confuse concurrency, skips or failed
runs.
"""

from datetime import UTC, datetime, timedelta

import pytest

from scripts.measure_ci_workload import Job, Run, summarize

_CREATED = datetime(year=2026, month=10, day=29, tzinfo=UTC)


def _run(*, status: str, conclusion: str | None) -> Run:
    """Create one explicitly identified attempt."""
    return Run(
        id=12,
        name="CI",
        head_sha="abc",
        run_attempt=2,
        status=status,
        conclusion=conclusion,
        created_at=_CREATED,
    )


def _job(*, job_id: int, start: int, end: int) -> Job:
    """Create a successful allocation with independently chosen timestamps."""
    return Job(
        id=job_id,
        name=f"job-{job_id}",
        status="completed",
        conclusion="success",
        started_at=_CREATED + timedelta(seconds=start),
        completed_at=_CREATED + timedelta(seconds=end),
    )


def test_allocations_preserve_concurrency_and_skips() -> None:
    """Only actual allocations contribute runner time; skipped jobs do not."""
    report = summarize(
        run=_run(status="completed", conclusion="success"),
        jobs=[
            _job(job_id=1, start=10, end=70),
            _job(job_id=2, start=40, end=100),
            Job(
                id=3,
                name="skip",
                status="completed",
                conclusion="skipped",
                started_at=None,
                completed_at=None,
            ),
        ],
    )
    keys = (
        "runner_minutes",
        "run_creation_to_first_job_seconds",
        "workload_span_seconds",
        "run_creation_to_last_job_seconds",
        "attempt",
    )
    assert {key: report[key] for key in keys} == {
        "runner_minutes": 2,
        "run_creation_to_first_job_seconds": 10,
        "workload_span_seconds": 90,
        "run_creation_to_last_job_seconds": 100,
        "attempt": 2,
    }


@pytest.mark.parametrize(
    argnames=("status", "conclusion"),
    argvalues=[
        ("in_progress", None),
        ("completed", "failure"),
        ("completed", "cancelled"),
    ],
)
def test_only_completed_successes_are_baseline_evidence(
    status: str,
    conclusion: str | None,
) -> None:
    """A failed, pending or canceled workflow cannot become a green
    baseline.
    """
    with pytest.raises(
        expected_exception=ValueError, match="completed successful"
    ):
        _ = summarize(
            run=_run(status=status, conclusion=conclusion),
            jobs=[_job(job_id=1, start=10, end=20)],
        )


@pytest.mark.parametrize(
    argnames="jobs",
    argvalues=[[], [_job(job_id=1, start=10, end=20)] * 2],
)
def test_missing_or_duplicated_pages_are_rejected(jobs: list[Job]) -> None:
    """An incomplete page inventory must not silently reduce
    allocation totals.
    """
    with pytest.raises(
        expected_exception=ValueError, match="nonempty and unique"
    ):
        _ = summarize(
            run=_run(status="completed", conclusion="success"), jobs=jobs
        )


@pytest.mark.parametrize(
    argnames="job",
    argvalues=[
        _job(job_id=1, start=20, end=10),
        _job(job_id=1, start=-1, end=10),
        Job(
            id=1,
            name="pending",
            status="queued",
            conclusion=None,
            started_at=None,
            completed_at=None,
        ),
        Job(
            id=1,
            name="failed",
            status="completed",
            conclusion="failure",
            started_at=_CREATED,
            completed_at=_CREATED,
        ),
        Job(
            id=1,
            name="missing",
            status="completed",
            conclusion="success",
            started_at=None,
            completed_at=None,
        ),
        Job(
            id=1,
            name="skip",
            status="completed",
            conclusion="skipped",
            started_at=None,
            completed_at=None,
        ),
    ],
)
def test_invalid_allocations_cannot_produce_timing_evidence(job: Job) -> None:
    """Reject contradictory timestamps, unfinished jobs and empty
    allocations.
    """
    with pytest.raises(
        expected_exception=ValueError, match=r"job 1|no successful runner"
    ):
        _ = summarize(
            run=_run(status="completed", conclusion="success"), jobs=[job]
        )
