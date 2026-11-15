"""The timing plugin reports actual parallel worker callbacks."""

import os
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import BaseModel


class _Report(BaseModel, extra="forbid", frozen=True):
    """The controller's machine-readable timing summary."""

    collection_finished_seconds: dict[str, float]
    worker_released_seconds: dict[str, float]
    released_worker_tail_seconds: float
    worker_errors: list[str]
    observation: str


@pytest.mark.parametrize(
    argnames=("arrivals", "expected_tail"),
    argvalues=[
        pytest.param((), None, id="no_workers"),
        pytest.param((10.0,), 0.0, id="single_worker"),
        pytest.param((10.0, 10.0), 0.0, id="simultaneous_release"),
        pytest.param((10.0, 25.0, 30.0), 25.0, id="staggered_release"),
    ],
)
def test_worker_timing_summary(
    tmp_path: Path,
    arrivals: tuple[float, ...],
    expected_tail: float | None,
) -> None:
    """Run real workers while controlling only the measurement clock.

    Release timestamps follow callback arrival order, independent of
    worker IDs and host scheduling. No elapsed-time thresholds or sleeps
    are needed.
    """
    root = Path(__file__).resolve().parents[3]
    _ = (tmp_path / "test_sample.py").write_text(
        data="def test_sample():\n    assert 2 + 2 == 4\n",
        encoding="utf-8",
    )
    _ = (tmp_path / "conftest.py").write_text(
        data=(
            "from types import SimpleNamespace\n"
            "import pytest\n"
            "from scripts import pytest_worker_timing as timing\n"
            "\n"
            "clock = SimpleNamespace(now=0.0)\n"
            f"releases = iter({arrivals!r})\n"
            "timing.perf_counter = lambda: clock.now\n"
            "\n"
            "@pytest.hookimpl(tryfirst=True)\n"
            "def pytest_xdist_node_collection_finished():\n"
            "    clock.now = 1.0\n"
            "\n"
            "@pytest.hookimpl(tryfirst=True)\n"
            "def pytest_testnodedown():\n"
            "    clock.now = next(releases)\n"
        ),
        encoding="utf-8",
    )
    result = subprocess.run(  # noqa: S603 - run isolated pytest workers
        args=[
            sys.executable,
            "-m",
            "pytest",
            "-p",
            "xdist.plugin",
            "-p",
            "scripts.pytest_worker_timing",
            "-n",
            str(object=len(arrivals)),
            "-o",
            "addopts=",
            "-q",
            "test_sample.py",
        ],
        cwd=tmp_path,
        env={
            **os.environ,
            "PYTHONPATH": os.pathsep.join(
                (str(object=root), str(object=root / "src"))
            ),
            "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
            "PYTEST_ADDOPTS": "",
        },
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 passed" in result.stdout
    reports = [
        _Report.model_validate_json(json_data=line)
        for line in result.stdout.splitlines()
        if line.startswith('{"collection_finished_seconds":')
    ]
    if expected_tail is None:
        assert reports == []
        assert "xdist worker timing" not in result.stdout
        return
    (report,) = reports
    workers = {f"gw{index}" for index in range(len(arrivals))}
    assert report.collection_finished_seconds == dict.fromkeys(workers, 1.0)
    assert set(report.worker_released_seconds) == workers
    assert sorted(report.worker_released_seconds.values()) == list(arrivals)
    assert report.released_worker_tail_seconds == expected_tail
    assert report.worker_errors == []
    assert report.observation != ""
