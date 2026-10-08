"""Run one fixture command with a deadline and process-group cleanup."""

import argparse
import contextlib
import os
import shlex
import signal
import subprocess
import sys
import time
from collections.abc import Sequence


def run(*, fixture: str, command: Sequence[str], timeout: float) -> int:
    """Run a compiler command, reporting the fixture and elapsed
    failure.
    """
    started = time.monotonic()
    with subprocess.Popen(args=command, start_new_session=True) as process:
        try:
            returncode = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            # Compilers may spawn children. Terminate the entire group and
            # kill any descendants that ignore TERM, even if the parent exits.
            with contextlib.suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGTERM)
            try:
                _ = process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pass
            finally:
                with contextlib.suppress(ProcessLookupError):
                    os.killpg(process.pid, signal.SIGKILL)
                _ = process.wait()
            elapsed = time.monotonic() - started
            _ = sys.stderr.write(
                f"{fixture}: compiler deadline ({timeout:g}s) exceeded "
                f"after {elapsed:.2f}s: {shlex.join(split_command=command)}\n"
            )
            return 124
    if returncode != 0:
        elapsed = time.monotonic() - started
        _ = sys.stderr.write(
            f"{fixture}: command failed ({returncode}) after {elapsed:.2f}s: "
            f"{shlex.join(split_command=command)}\n"
        )
    if returncode < 0:
        return 128 - returncode
    return returncode


class _CompilerArguments(argparse.Namespace):
    """Typed arguments populated by the command-line parser."""

    fixture: str
    timeout: float
    command: list[str]


def main() -> None:
    """Parse a fixture label, time budget, and command to execute."""
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--fixture", required=True)
    _ = parser.add_argument("--timeout", type=float, default=60)
    _ = parser.add_argument("command", nargs=argparse.REMAINDER)
    args = _CompilerArguments()
    _ = parser.parse_args(namespace=args)
    command = args.command
    if command[:1] == ["--"]:
        command = command[1:]
    if len(command) == 0 or args.timeout <= 0:
        parser.error(message="provide a command and a positive timeout")
    sys.exit(run(fixture=args.fixture, command=command, timeout=args.timeout))


if __name__ == "__main__":
    main()
