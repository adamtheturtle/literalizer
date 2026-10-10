"""Exercise the shared deadline wrapper with real command processes."""

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

from scripts import roundtrip_common
from scripts.bounded_command import bounded_command

_WRAPPER = Path(__file__).resolve().parents[1] / "run-bounded.sh"
_KILLED_STATUS = 137
_MISSING_COMMAND_STATUS = 127
_requires_timeout = pytest.mark.skipif(
    os.name != "posix"
    or (
        shutil.which(cmd="timeout") is None
        and shutil.which(cmd="gtimeout") is None
    ),
    reason="the lint scripts require Bash and GNU timeout",
)


@_requires_timeout
@pytest.mark.parametrize(argnames="status", argvalues=[0, 7])
def test_command_streams_and_status(status: int) -> None:
    """Keep input, output, argv boundaries, and ordinary exit statuses."""
    payload = b"bytes\x00with\xffnewlines\n"
    result = subprocess.run(
        args=bounded_command(
            args=[
                sys.executable,
                "-c",
                (
                    "import sys; "
                    "sys.stdout.buffer.write(sys.stdin.buffer.read()); "
                    "print(sys.argv[1], file=sys.stderr); "
                    f"raise SystemExit({status})"
                ),
                "one argument with spaces",
            ],
            fixture="fixture with spaces.cpp",
            timeout_seconds=10,
        ),
        input=payload,
        capture_output=True,
        check=False,
        timeout=15,
    )
    assert result.returncode == status
    assert result.stdout == payload
    assert result.stderr.startswith(b"fixture with spaces.cpp: running")
    assert b"one argument with spaces\n" in result.stderr
    if status != 0:
        assert b"status 7; deadline 10s; elapsed" in result.stderr


@_requires_timeout
@pytest.mark.parametrize(
    argnames=("termination", "ignore_term", "status"),
    argvalues=[
        ("KILL", False, 137),
        ("0.1s", False, 124),
        ("0.1s", True, 137),
    ],
)
def test_deadline_policies(
    termination: str, status: int, *, ignore_term: bool
) -> None:
    """Support immediate KILL and a TERM grace period without hiding
    status.
    """
    program = "import time; time.sleep(10)"
    if ignore_term:
        program = (
            "import signal; signal.signal(signal.SIGTERM, signal.SIG_IGN); "
            + program
        )
    result = subprocess.run(
        args=[
            str(object=_WRAPPER),
            "deep file.elm",
            "0.5s",
            termination,
            sys.executable,
            "-c",
            program,
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=5,
    )
    assert result.returncode == status
    assert "deep file.elm: running" in result.stderr
    assert f"status {status}; deadline 0.5s" in result.stderr


@_requires_timeout
def test_timeout_stops_descendants(tmp_path: Path) -> None:
    """Kill a descendant that ignores TERM along with its timed-out parent."""
    heartbeat = tmp_path / "heartbeat"
    child = (
        "import signal,time; from pathlib import Path; "
        "signal.signal(signal.SIGTERM, signal.SIG_IGN); "
        f"path=Path({str(object=heartbeat)!r}); "
        "stop=time.monotonic()+10\n"
        "while time.monotonic()<stop:\n"
        " path.write_text(str(time.monotonic())); time.sleep(0.02)\n"
    )
    parent = (
        "import subprocess,time,sys; "
        f"subprocess.Popen([sys.executable,'-c',{child!r}]); time.sleep(10)"
    )
    result = subprocess.run(
        args=bounded_command(
            args=[sys.executable, "-c", parent],
            fixture="descendant.cpp",
            timeout_seconds=1,
        ),
        capture_output=True,
        check=False,
        timeout=5,
    )
    assert result.returncode == _KILLED_STATUS
    stopped = heartbeat.read_bytes()
    time.sleep(0.1)
    assert heartbeat.read_bytes() == stopped


@_requires_timeout
@pytest.mark.parametrize(argnames="available", argvalues=[True, False])
def test_gtimeout_discovery(tmp_path: Path, *, available: bool) -> None:
    """Find macOS gtimeout or explain a missing installation."""
    bash = shutil.which(cmd="bash")
    timeout = shutil.which(cmd="timeout")
    if timeout is None:
        timeout = shutil.which(cmd="gtimeout")
    assert bash is not None
    assert timeout is not None
    (tmp_path / "bash").symlink_to(target=bash)
    if available:
        (tmp_path / "gtimeout").symlink_to(target=timeout)
    result = subprocess.run(
        args=bounded_command(
            args=[sys.executable, "-c", "print('ok')"],
            fixture="discovery",
            timeout_seconds=10,
        ),
        env={**os.environ, "PATH": str(object=tmp_path)},
        capture_output=True,
        text=True,
        check=False,
        timeout=15,
    )
    if available:
        assert result.returncode == 0
        assert result.stdout == "ok\n"
    else:
        assert result.returncode == _MISSING_COMMAND_STATUS
        assert "install coreutils (gtimeout on macOS)" in result.stderr


@_requires_timeout
def test_wrapper_in_temporary_working_directory(tmp_path: Path) -> None:
    """Locate the wrapper from a different cwd and give each step a budget."""
    for _ in range(2):
        result = subprocess.run(
            args=bounded_command(
                args=[sys.executable, "-c", "import time; time.sleep(0.2)"],
                fixture="separate step",
                timeout_seconds=0.5,
            ),
            cwd=tmp_path,
            capture_output=True,
            check=False,
            timeout=5,
        )
        assert result.returncode == 0


@_requires_timeout
def test_roundtrip_runner_keeps_json_output(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Wrapper diagnostics must not contaminate the final JSON
    document.
    """
    roundtrip_common.execute(
        label="Python probe",
        source_filename="main.py",
        program="print('{\"ok\": true}')\n",
        steps=[
            roundtrip_common.Step(
                args=[sys.executable, "main.py"], failure_label="probe error"
            )
        ],
        excluded_keys=(),
        expected_json='{"ok": true}',
        extra_files=None,
    )
    assert capsys.readouterr().out == "Python probe round-trip OK\n"


@_requires_timeout
def test_roundtrip_failure_removes_temporary_source(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Report the command's status and source, then clean up the
    program.
    """
    with pytest.raises(expected_exception=SystemExit) as failure:
        roundtrip_common.execute(
            label="Python probe",
            source_filename="main.py",
            program="raise SystemExit(7)\n",
            steps=[
                roundtrip_common.Step(
                    args=[sys.executable, "main.py"],
                    failure_label="probe error",
                )
            ],
            excluded_keys=(),
            expected_json='{"ok": true}',
            extra_files=None,
        )
    assert failure.value.code == 1
    error = capsys.readouterr().err
    assert "status 7; deadline 60s; elapsed" in error
    assert "Program:\nraise SystemExit(7)" in error
    source = Path(error.splitlines()[1].split(sep=": running", maxsplit=1)[0])
    assert source.name == "main.py"
    assert not source.parent.exists()
