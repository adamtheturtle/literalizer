"""Report actual runner allocation separately from workflow waiting time.

Run ``python -m scripts.measure_ci_workload OWNER/REPO RUN_ID ...``.
Only a completed successful attempt is accepted as baseline evidence.
This reads GitHub metadata; it neither reruns jobs nor changes check status.
"""

import argparse
import json
import subprocess
import sys
from collections.abc import Sequence
from datetime import datetime

from pydantic import BaseModel, TypeAdapter


class Run(BaseModel):
    """The attempt whose timestamps and successful result are measured."""

    id: int
    name: str
    head_sha: str
    run_attempt: int
    status: str
    conclusion: str | None
    created_at: datetime


class Job(BaseModel):
    """One runner allocation, including skipped jobs without a runner."""

    id: int
    name: str
    status: str
    conclusion: str | None
    started_at: datetime | None
    completed_at: datetime | None


class JobPage(BaseModel):
    """One paginated GitHub jobs response."""

    jobs: list[Job]


def summarize(*, run: Run, jobs: Sequence[Job]) -> dict[str, object]:
    """Keep allocation, execution span and run-creation intervals
    distinct.
    """
    if run.status != "completed" or run.conclusion != "success":
        msg = "baseline evidence requires a completed successful run"
        raise ValueError(msg)
    if len(jobs) == 0 or len({job.id for job in jobs}) != len(jobs):
        msg = "jobs must be nonempty and unique within one attempt"
        raise ValueError(msg)
    rows: list[dict[str, object]] = []
    starts: list[datetime] = []
    ends: list[datetime] = []
    runner_seconds = 0.0
    for job in jobs:
        if job.status != "completed" or job.conclusion not in {
            "success",
            "skipped",
            "neutral",
        }:
            msg = f"job {job.id} is incomplete or unsuccessful"
            raise ValueError(msg)
        if job.conclusion == "skipped":
            rows.append({"id": job.id, "name": job.name, "result": "skipped"})
            continue
        start, end = job.started_at, job.completed_at
        if (
            start is None
            or end is None
            or end < start
            or start < run.created_at
        ):
            msg = f"job {job.id} has missing or inconsistent timestamps"
            raise ValueError(msg)
        seconds = (end - start).total_seconds()
        runner_seconds += seconds
        starts.append(start)
        ends.append(end)
        rows.append(
            {
                "id": job.id,
                "name": job.name,
                "runner_seconds": seconds,
                "result": job.conclusion,
            }
        )
    if len(starts) == 0:
        msg = "no successful runner allocations were found"
        raise ValueError(msg)
    return {
        "run_id": run.id,
        "workflow": run.name,
        "head_sha": run.head_sha,
        "attempt": run.run_attempt,
        "runner_minutes": runner_seconds / 60,
        "run_creation_to_first_job_seconds": (
            min(starts) - run.created_at
        ).total_seconds(),
        "workload_span_seconds": (max(ends) - min(starts)).total_seconds(),
        "run_creation_to_last_job_seconds": (
            max(ends) - run.created_at
        ).total_seconds(),
        "jobs": rows,
        "limits": "Runner allocation includes setup and cleanup. The workload "
        "span includes dependency and runner waits; it is not CPU time "
        "or a sum of per-job queue durations. Creation-based intervals use "
        "the original run creation, so they include earlier attempts and "
        "rerun delays when this is a repeated attempt.",
    }


def _api(*, route: str, paginate: bool) -> str:
    """Read one response or every jobs page with a finite network deadline."""
    args = ["gh", "api", route]
    if paginate:
        args.extend(["--paginate", "--slurp"])
    return subprocess.run(
        args=args, check=True, capture_output=True, text=True, timeout=60
    ).stdout


def main() -> None:
    """Write independently auditable reports for the requested green
    runs.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("repository")
    _ = parser.add_argument("runs", nargs="+", type=int)
    args = parser.parse_args()
    repository = str(object=args.repository)
    reports: list[dict[str, object]] = []
    for run_id in TypeAdapter(type=list[int]).validate_python(args.runs):
        run = Run.model_validate_json(
            json_data=_api(
                route=f"repos/{repository}/actions/runs/{run_id}",
                paginate=False,
            )
        )
        pages = TypeAdapter(type=list[JobPage]).validate_json(
            _api(
                route=f"repos/{repository}/actions/runs/{run_id}/attempts/"
                f"{run.run_attempt}/jobs?per_page=100",
                paginate=True,
            )
        )
        reports.append(
            summarize(run=run, jobs=[j for page in pages for j in page.jobs])
        )
    _ = sys.stdout.write(json.dumps(obj=reports, indent=2) + "\n")


if __name__ == "__main__":
    main()
