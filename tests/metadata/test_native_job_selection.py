"""Regression checks for conservative native CI job selection."""

import re
from pathlib import Path

import pytest

from scripts.select_native_jobs import JOB_EXTENSIONS, select_jobs


def test_selection_covers_workflow_commands() -> None:
    """Fixture commands, conditions and dependency gates stay in sync."""
    path = Path(__file__).resolve().parents[2] / ".github/workflows/lint.yml"
    # Inspect top-level job blocks, retaining shell fixture commands too.
    jobs = dict(
        re.findall(
            pattern=r"^  ([\w-]+):\n(.*?)(?=^  [\w-]+:|\Z)",
            string=path.read_text(encoding="utf-8"),
            flags=re.MULTILINE | re.DOTALL,
        )
    )
    native_jobs = {
        job
        for job in jobs
        if job.startswith("lint-") or job == "build-cpp-toolchain"
    }
    assert native_jobs == JOB_EXTENSIONS.keys()
    for job_id, extensions in JOB_EXTENSIONS.items():
        job = jobs[job_id]
        assert (
            re.search(
                pattern=r"^    needs: \[.*\bnative-changes\b.*\]$",
                string=job,
                flags=re.MULTILINE,
            )
            is not None
        )
        assert (
            "    if: contains(fromJSON(needs.native-changes.outputs.jobs), "
            f"'{job_id}')\n"
        ) in job
        referenced = set(
            re.findall(pattern=r"-name '[^']*?(\.[\w]+)'", string=job)
        )
        referenced.update(
            re.findall(pattern=r"list_fixtures (\.[\w]+)", string=job)
        )
        assert referenced <= extensions, job_id
    assert "      - native-changes\n" in jobs["completion-lint"]


@pytest.mark.parametrize(
    argnames=("paths", "expected"),
    argvalues=[
        (list[str](), set[str]()),
        (
            ["docs/source/index.rst", "newsfragments/6912.change.md"],
            set[str](),
        ),
        (
            ["tests/integration/cases/scalar/Crystal@v1.cr"],
            {"lint-crystal"},
        ),
        (
            ["tests/integration/cases/scalar/Cpp@v20.cpp"],
            {"build-cpp-toolchain", "lint-cpp", "lint-cpp-tidy"},
        ),
        (
            ["tests/integration/cases/scalar/C@v99.c"],
            {"build-cpp-toolchain", "lint-c-tidy", "lint-fast"},
        ),
        (
            ["tests/integration/cases/scalar/TypeScript@v5.ts"],
            {"lint-npm-installed", "lint-typescript-run"},
        ),
        (
            ["tests/integration/cases/scalar/ObjectiveC@v2.m"],
            {"lint-matlab", "lint-objectivec", "lint-objectivec-tidy"},
        ),
        (
            [
                "tests/integration/cases/old/Python@py38.py",
                "tests/integration/cases/new/Crystal@v1.cr",
                "README.rst",
            ],
            {"lint-python", "lint-crystal"},
        ),
    ],
)
def test_select_affected_jobs(paths: list[str], expected: set[str]) -> None:
    """Select grouped jobs and toolchain producers as well as
    consumers.
    """
    assert set(select_jobs(paths=paths)) == expected


@pytest.mark.parametrize(
    argnames="path",
    argvalues=[
        "src/literalizer/languages/crystal.py",
        "src/literalizer/__init__.py",
        "scripts/run_crystal_roundtrip.py",
        "scripts/roundtrip_input.json",
        "tests/integration/list_fixtures.py",
        "tests/integration/cases/scalar/case.toml",
        "tests/integration/cases/scalar/input.json",
        "tests/integration/cases/scalar/input.yaml",
        "tests/integration/cases/scalar/Unknown@v1.unknown",
        ".github/workflows/lint.yml",
        ".github/npm-linters/package-lock.json",
        ".clang-tidy",
        "ci/clang/performance.patch",
        "pyproject.toml",
        "uv.lock",
    ],
)
def test_other_inputs_run_every_job(path: str) -> None:
    """A golden change must not hide a shared or unrecognized change."""
    assert select_jobs(
        paths=["tests/integration/cases/scalar/Crystal@v1.cr", path],
    ) == list(JOB_EXTENSIONS)
