"""Exercise fixture deadlines using real child processes."""

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from scripts.run_bounded_compiler import run

_TIMEOUT_EXIT_STATUS = 124

_requires_posix = pytest.mark.skipif(
    os.name != "posix", reason="compiler deadlines run in POSIX lint jobs"
)


@_requires_posix
@pytest.mark.parametrize(argnames="exit_status", argvalues=[0, 7])
def test_compiler_exit_status(exit_status: int) -> None:
    """Preserve successful and failed compiler exit codes."""
    assert (
        run(
            fixture="exit-status",
            command=[sys.executable, "-c", f"raise SystemExit({exit_status})"],
            timeout=10,
        )
        == exit_status
    )


@_requires_posix
def test_timeout_stops_descendants(tmp_path: Path) -> None:
    """Stop a descendant that ignores TERM when its parent times out."""
    heartbeat = tmp_path / "heartbeat"
    child = f"""import signal
import time
from pathlib import Path
signal.signal(signal.SIGTERM, signal.SIG_IGN)
path = Path({str(object=heartbeat)!r})
stop = time.monotonic() + 10
while time.monotonic() < stop:
    path.write_text(str(time.monotonic()))
    time.sleep(0.02)
"""
    parent = (
        "import subprocess,time,sys; "
        f"subprocess.Popen([sys.executable,'-c',{child!r}]); "
        "time.sleep(10)"
    )
    assert (
        run(
            fixture="descendant-cleanup",
            command=[sys.executable, "-c", parent],
            timeout=1,
        )
        == _TIMEOUT_EXIT_STATUS
    )
    stopped = heartbeat.read_text(encoding="utf-8")
    time.sleep(0.1)
    assert heartbeat.read_text(encoding="utf-8") == stopped


@_requires_posix
def test_timeout_diagnostic_names_fixture() -> None:
    """Name the original fixture and timed-out command in CLI output."""
    result = subprocess.run(
        args=[
            sys.executable,
            "scripts/run_bounded_compiler.py",
            "--fixture",
            "deep.cpp",
            "--timeout",
            "0.1",
            "--",
            sys.executable,
            "-c",
            "import time; time.sleep(10)",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == _TIMEOUT_EXIT_STATUS
    assert result.stderr.startswith(
        "deep.cpp: compiler deadline (0.1s) exceeded after "
    )
    assert "import time; time.sleep(10)" in result.stderr
