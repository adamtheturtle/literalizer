"""Execute MATLAB golden files using declared consumer entry points.

Octave runs ordinary scripts directly. Function consumers declare their
entry point in the same metadata that generates them; their versioned
golden is copied to the corresponding function filename before execution.
"""

import concurrent.futures
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from literalizer.languages import Matlab
from scripts.bounded_command import bounded_command
from tests.integration.shared_checked_cases import shared_checked_cases

_LOGGER = logging.getLogger(name=__name__)
_CASES_DIR = Path(__file__).resolve().parents[1] / "tests/integration/cases"


def fixture_entrypoints() -> dict[Path, str]:
    """Read function entry points from the fixture owner's metadata."""
    entrypoints: dict[Path, str] = {}
    for case in shared_checked_cases(cases_dir=_CASES_DIR):
        if case.lang_cls is Matlab:
            entrypoint = case.consumer.entrypoint
            if entrypoint is None:
                msg = (
                    f"MATLAB function consumer has no entry point: {case.name}"
                )
                raise ValueError(msg)
            entrypoints[case.golden_path.resolve()] = entrypoint
    return entrypoints


def _skip_reason(*, source: str) -> str | None:
    """Retain the existing MATLAB features unsupported by Octave."""
    if '""' in source:
        return "MATLAB-escaped double quotes"
    if re.search(pattern=r"\bdatetime\b", string=source) is not None:
        return "datetime() is not implemented in Octave"
    if "containers.Map({''" in source:
        return "Octave rejects MATLAB's empty containers.Map key"
    return None


def _execute(*, fixture: Path, octave: str, arguments: list[str]) -> None:
    """Keep native failures and per-fixture timeout diagnostics
    visible.
    """
    _ = subprocess.run(
        args=bounded_command(
            args=[octave, "--norc", "--no-gui", *arguments],
            fixture=str(object=fixture),
            timeout_seconds=60,
        ),
        check=True,
    )


def run_fixture(*, fixture: Path, entrypoint: str | None, octave: str) -> None:
    """Run a script or a declared function without inspecting its
    syntax.
    """
    reason = _skip_reason(source=fixture.read_text(encoding="utf-8"))
    if reason is not None:
        _LOGGER.info("Skipping %s: %s", fixture, reason)
        return
    if entrypoint is None:
        _execute(
            fixture=fixture, octave=octave, arguments=[str(object=fixture)]
        )
        return
    with tempfile.TemporaryDirectory(
        suffix="-literalizer-matlab"
    ) as temporary:
        directory = Path(temporary)
        _ = shutil.copyfile(src=fixture, dst=directory / f"{entrypoint}.m")
        _execute(
            fixture=fixture,
            octave=octave,
            arguments=["--path", temporary, "--eval", f"{entrypoint}()"],
        )


def find_octave() -> str:
    """Require the native runtime supplied by the MATLAB CI job."""
    octave = shutil.which(cmd="octave")
    if octave is None:
        msg = "Octave executable was not found."
        raise RuntimeError(msg)
    return octave


def main() -> None:
    """Read null-separated fixture paths and execute them in parallel."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    fixtures = [
        Path(os.fsdecode(filename=name)).resolve()
        for name in sys.stdin.buffer.read().split(sep=b"\0")
        if len(name) > 0
    ]
    if len(fixtures) == 0:
        msg = "No MATLAB fixture paths were provided."
        raise ValueError(msg)
    entrypoints = fixture_entrypoints()
    octave = find_octave()
    workers = os.cpu_count()
    if workers is None:
        workers = 1
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=workers
    ) as executor:
        for future in [
            executor.submit(
                run_fixture,
                fixture=fixture,
                entrypoint=entrypoints.get(fixture),
                octave=octave,
            )
            for fixture in fixtures
        ]:
            future.result()


if __name__ == "__main__":
    main()
