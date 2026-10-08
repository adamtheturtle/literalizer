"""Exercise round-trip deadlines and error boundaries with real
processes.
"""

import re
import shlex
import sys
import time
from pathlib import Path

import pytest

from scripts.roundtrip_common import Step, TimedStep, execute


def _execute_python(
    *,
    program: str,
    timeout_seconds: float | None,
) -> None:
    """Run a tiny Python program through the production execution
    helper.
    """
    args = [sys.executable, "main.py"]
    step: Step
    if timeout_seconds is None:
        step = Step(args=args, failure_label="compiler error")
    else:
        step = TimedStep(
            args=args,
            failure_label="compiler error",
            timeout_seconds=timeout_seconds,
        )
    execute(
        label="Test",
        source_filename="main.py",
        program=program,
        steps=[step],
        excluded_keys=(),
        expected_json='{"value": 1}',
        extra_files={"nested/extra.txt": "extra"},
    )


def _attempt_start(attempt: int) -> str:
    """Return the complete expected attempt-start diagnostic."""
    command = shlex.join(split_command=[sys.executable, "main.py"])
    return f"Test: attempt {attempt}/2 starting (timeout 1s): {command}\n"


def _timeout_diagnostic(*, attempt: int, program: str) -> str:
    """Return a timeout diagnostic with the elapsed time normalized."""
    command = shlex.join(split_command=[sys.executable, "main.py"])
    return (
        _attempt_start(attempt=attempt)
        + f"Test: compiler error: attempt {attempt}/2 "
        "timed out after <elapsed>s\n"
        + f"Command: {command}\n"
        + "Stdout:\npartial stdout\n\nStderr:\npartial stderr\n\n"
        + f"Program:\n{program}\n"
    )


@pytest.mark.parametrize(argnames="timeout_seconds", argvalues=[None, 1.0])
def test_roundtrip_success(
    timeout_seconds: float | None,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Normal and bounded steps verify JSON and create extra files."""
    program = (
        "from pathlib import Path\n"
        "assert Path('nested/extra.txt').read_text() == 'extra'\n"
        "print('{\"value\": 1}')\n"
    )
    _execute_python(program=program, timeout_seconds=timeout_seconds)
    captured = capsys.readouterr()
    assert captured.out == "Test round-trip OK\n"
    assert captured.err == (
        "" if timeout_seconds is None else _attempt_start(attempt=1)
    )


def test_timeout_cleans_up_and_retries_once(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Two stalls kill parents and descendants and emit full
    diagnostics.
    """
    attempts = tmp_path / "attempts.txt"
    survived = tmp_path / "survived.txt"
    attempts_path = f"{attempts}"
    survived_path = f"{survived}"
    child = (
        "import time\n"
        "from pathlib import Path\n"
        "time.sleep(2)\n"
        f"Path({survived_path!r}).write_text('survived')\n"
    )
    program = (
        "import subprocess, sys, time\n"
        "from pathlib import Path\n"
        f"with Path({attempts_path!r}).open('a') as file:\n"
        "    file.write('attempt\\n')\n"
        f"subprocess.Popen([sys.executable, '-c', {child!r}])\n"
        "print('partial stdout', flush=True)\n"
        "print('partial stderr', file=sys.stderr, flush=True)\n"
        "time.sleep(30)\n"
    )
    with pytest.raises(expected_exception=SystemExit) as exc_info:
        _execute_python(program=program, timeout_seconds=1)
    assert exc_info.value.code == 1
    # Each child would leave a marker two seconds after being spawned if
    # group cleanup missed it. Wait for the second child's deadline too.
    time.sleep(2.2)
    assert attempts.read_text(encoding="utf-8") == "attempt\nattempt\n"
    assert survived.exists() is False
    captured = capsys.readouterr()
    assert captured.out == ""
    assert re.sub(
        pattern=r"after \d+\.\d{2}s",
        repl="after <elapsed>s",
        string=captured.err,
    ) == "".join(
        _timeout_diagnostic(attempt=attempt, program=program)
        for attempt in (1, 2)
    )


def test_success_after_timeout(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A timeout is cleaned up before a successful second invocation."""
    attempts = tmp_path / "attempts.txt"
    attempts_path = f"{attempts}"
    program = (
        "import sys, time\n"
        "from pathlib import Path\n"
        f"attempts = Path({attempts_path!r})\n"
        "first = not attempts.exists()\n"
        "with attempts.open('a') as file:\n"
        "    file.write('attempt\\n')\n"
        "if first:\n"
        "    print('partial stdout', flush=True)\n"
        "    print('partial stderr', file=sys.stderr, flush=True)\n"
        "    time.sleep(30)\n"
        "print('{\"value\": 1}')\n"
    )
    _execute_python(program=program, timeout_seconds=1)
    assert attempts.read_text(encoding="utf-8") == "attempt\nattempt\n"
    captured = capsys.readouterr()
    assert captured.out == "Test round-trip OK\n"
    assert re.sub(
        pattern=r"after \d+\.\d{2}s",
        repl="after <elapsed>s",
        string=captured.err,
    ) == (
        _timeout_diagnostic(attempt=1, program=program)
        + _attempt_start(attempt=2)
    )


@pytest.mark.parametrize(
    argnames=("output", "exit_code", "diagnostic"),
    argvalues=[
        ("compiler failed", 2, "compiler error"),
        ('{"value": 2}', 0, "round-trip mismatch"),
        ("invalid JSON", 0, "produced invalid JSON"),
    ],
)
def test_completed_errors_fail_without_retry(
    output: str,
    exit_code: int,
    diagnostic: str,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Compilation, mismatched data, and malformed JSON fail
    immediately.
    """
    attempts = tmp_path / "attempts.txt"
    attempts_path = f"{attempts}"
    program = (
        "import sys\n"
        "from pathlib import Path\n"
        f"with Path({attempts_path!r}).open('a') as file:\n"
        "    file.write('attempt\\n')\n"
        f"print({output!r})\n"
        f"sys.exit({exit_code})\n"
    )
    with pytest.raises(expected_exception=SystemExit) as exc_info:
        _execute_python(program=program, timeout_seconds=1)
    assert exc_info.value.code == 1
    assert attempts.read_text(encoding="utf-8") == "attempt\n"
    captured = capsys.readouterr()
    assert captured.out == ""
    lines = captured.err.splitlines()
    assert lines[0] == _attempt_start(attempt=1).rstrip()
    assert lines[1].startswith(f"Test: {diagnostic}")
