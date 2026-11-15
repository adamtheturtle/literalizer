"""The CI adapter consumes public reports from real pytest workers."""

import os
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import BaseModel


class _Summary(BaseModel, extra="forbid", frozen=True):
    """The existing machine-readable CI summary."""

    collection_finished_seconds: dict[str, float]
    worker_released_seconds: dict[str, float]
    released_worker_tail_seconds: float
    worker_errors: list[str]
    observation: str


@pytest.fixture(name="project")
def fixture_project(tmp_path: Path) -> Path:
    """A standalone pytest project with an explicit root."""
    _ = (tmp_path / "pytest.ini").write_text(
        data="[pytest]\n", encoding="utf-8"
    )
    _ = (tmp_path / "test_sample.py").write_text(
        data="def test_sample():\n    assert 2 + 2 == 4\n", encoding="utf-8"
    )
    return tmp_path


def _run_pytest(
    *, project: Path, cwd: Path, workers: int, options: tuple[str, ...]
) -> subprocess.CompletedProcess[str]:
    """Load the upstream plugin and adapter exactly as CI does."""
    root = Path(__file__).resolve().parents[3]
    return subprocess.run(  # noqa: S603 - run an isolated pytest project
        args=[
            sys.executable,
            "-m",
            "pytest",
            "-p",
            "timing",
            "-p",
            "xdist.plugin",
            "-p",
            "scripts.pytest_worker_timing",
            "-n",
            str(object=workers),
            "-o",
            "addopts=",
            "-q",
            *options,
            str(object=project / "test_sample.py"),
        ],
        cwd=cwd,
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


def _summaries(output: str) -> list[_Summary]:
    """Read the adapter's JSON separately from the upstream terminal
    output.
    """
    return [
        _Summary.model_validate_json(json_data=line)
        for line in output.splitlines()
        if line.startswith('{"collection_finished_seconds":')
    ]


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
    project: Path, arrivals: tuple[float, ...], expected_tail: float | None
) -> None:
    """Use real workers and upstream capture with a deterministic
    clock.
    """
    _ = (project / "conftest.py").write_text(
        data=(
            "from types import SimpleNamespace\n"
            "import pytest\n"
            "import pytest_timing.plugin as timing\n"
            "\n"
            "clock = SimpleNamespace(now=0.0)\n"
            f"releases = iter({arrivals!r})\n"
            "timing.time = SimpleNamespace(\n"
            "    time=lambda: 0.0, perf_counter=lambda: clock.now\n"
            ")\n"
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
    result = _run_pytest(
        project=project,
        cwd=project,
        workers=len(arrivals),
        options=(
            "--timing-capture=workers",
            "--timing-json-file=worker-timing.json",
            "--dist=worksteal",
        ),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 passed" in result.stdout
    reports = _summaries(output=result.stdout)
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


@pytest.mark.parametrize(argnames="crash", argvalues=[False, True])
def test_worker_timing_keeps_failure_status(
    *, project: Path, crash: bool
) -> None:
    """A failing test or worker crash remains a failure with a CI
    summary.
    """
    source = (
        "def test_sample():\n    import os\n    os._exit(3)\n"
        if crash
        else "def test_sample():\n    assert False\n"
    )
    _ = (project / "test_sample.py").write_text(data=source, encoding="utf-8")
    result = _run_pytest(
        project=project,
        cwd=project,
        workers=2,
        options=(
            "--timing-capture=workers",
            "--timing-json-file=worker-timing.json",
            "--max-worker-restart=0",
        ),
    )
    assert result.returncode == pytest.ExitCode.TESTS_FAILED, (
        result.stdout + result.stderr
    )
    (report,) = _summaries(output=result.stdout)
    assert len(report.worker_errors) == int(crash)
    assert report.released_worker_tail_seconds >= 0


@pytest.mark.parametrize(argnames="damage", argvalues=["missing", "invalid"])
def test_worker_report_read_error_keeps_test_outcome(
    project: Path, damage: str
) -> None:
    """Unavailable telemetry must not turn a passing test into an
    error.
    """
    mutation = (
        "report.unlink()"
        if damage == "missing"
        else "report.write_text('not JSON', encoding='utf-8')"
    )
    _ = (project / "conftest.py").write_text(
        data=(
            "import pytest\n"
            "@pytest.hookimpl(hookwrapper=True, trylast=True)\n"
            "def pytest_sessionfinish(session):\n"
            "    yield\n"
            "    report = session.config.rootpath / 'worker-timing.json'\n"
            f"    {mutation}\n"
        ),
        encoding="utf-8",
    )
    result = _run_pytest(
        project=project,
        cwd=project,
        workers=0,
        options=(
            "--timing-capture=workers",
            "--timing-json-file=worker-timing.json",
        ),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "worker timing summary unavailable" in result.stdout
    assert _summaries(output=result.stdout) == []


def test_worker_report_path_is_relative_to_pytest_root(project: Path) -> None:
    """Resolve report paths against the pytest root for subdirectory
    runs.
    """
    cwd = project / "subdirectory"
    cwd.mkdir()
    result = _run_pytest(
        project=project,
        cwd=cwd,
        workers=1,
        options=(
            "--timing-capture=workers",
            "--timing-json-file=worker-timing.json",
        ),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert len(_summaries(output=result.stdout)) == 1
    assert (project / "worker-timing.json").is_file()
    assert not (cwd / "worker-timing.json").exists()


@pytest.mark.parametrize(argnames="capture", argvalues=["disabled", "full"])
def test_other_capture_modes_do_not_emit_adapter_summary(
    project: Path, capture: str
) -> None:
    """The adapter is inactive unless worker-only capture is requested."""
    options = (
        ("--timing-capture=full", "--timing-json-file=worker-timing.json")
        if capture == "full"
        else ()
    )
    result = _run_pytest(
        project=project, cwd=project, workers=1, options=options
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert _summaries(output=result.stdout) == []
