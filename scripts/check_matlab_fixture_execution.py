"""Prove that Octave executes both script and function assertions.

Run by the MATLAB CI job against its pinned Octave runtime. Python-only
CI needs no native toolchain and does not substitute a mocked compiler.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

from scripts.run_matlab_fixtures import (
    find_octave,
    fixture_entrypoints,
    run_fixture,
)


def main() -> None:
    """Require success and failure to propagate through both execution
    modes.
    """
    octave = find_octave()
    with tempfile.TemporaryDirectory() as temporary:
        fixture = Path(temporary) / "Matlab@r2022a.m"
        for entrypoint in (None, "fixture_main"):
            for succeeds in (True, False):
                assertion = f"assert({str(object=succeeds).lower()});\n"
                program = assertion
                if entrypoint is not None:
                    # A return value is valid MATLAB syntax that the old
                    # declaration regex did not recognize. Leading comments
                    # and blank lines must not change execution either.
                    program = (
                        "\n% Native entry-point regression\n"
                        f"function result = {entrypoint}()\n"
                        "result = true;\n"
                        f"{assertion}end\n"
                    )
                _ = fixture.write_text(data=program, encoding="utf-8")
                actual_success = True
                try:
                    run_fixture(
                        fixture=fixture, entrypoint=entrypoint, octave=octave
                    )
                except subprocess.CalledProcessError:
                    actual_success = False
                if actual_success != succeeds:
                    msg = f"Unexpected MATLAB assertion status: {entrypoint}"
                    raise AssertionError(msg)
                if entrypoint is None:
                    completed = subprocess.run(
                        args=[
                            sys.executable,
                            "-m",
                            "scripts.run_matlab_fixtures",
                        ],
                        input=os.fsencode(filename=fixture) + b"\0",
                        capture_output=True,
                        check=False,
                    )
                    if (completed.returncode == 0) != succeeds:
                        msg = (
                            "MATLAB batch runner lost the assertion status: "
                            f"{completed.stderr!r}"
                        )
                        raise AssertionError(msg)
    for fixture, entrypoint in fixture_entrypoints().items():
        run_fixture(fixture=fixture, entrypoint=entrypoint, octave=octave)


if __name__ == "__main__":
    main()
