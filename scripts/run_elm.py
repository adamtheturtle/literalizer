"""Run Elm golden files end-to-end via ``elm make`` + Node to catch
runtime errors that survive the compile-only check.
"""

import functools
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from scripts.elm_common import (
    ELM_JSON,
    NOINDEX_SUFFIX,
    init_worker_elm_home,
    prime_elm_home,
    run_elm_make,
    worker_elm_home,
)

# Wrap ``Check.my_data`` in a ``Platform.worker`` so loading the compiled
# JavaScript evaluates the fixture's top-level value, surfacing runtime
# crashes such as ``Debug.todo`` or references that pass type-checking
# but fail at evaluation.
_MAIN_ELM = """\
module Main exposing (main)

import Check
import Platform


main : Program () () Never
main =
    Platform.worker
        { init = \\_ -> forceData Check.my_data
        , update = \\_ m -> ( m, Cmd.none )
        , subscriptions = \\_ -> Sub.none
        }


forceData : a -> ( (), Cmd Never )
forceData _ =
    ( (), Cmd.none )
"""

# Call-mode golden files expose ``main : Program () () Never`` directly
# instead of ``my_data``, so just re-export it.
_CALL_MAIN_ELM = """\
module Main exposing (main)

import Check
import Platform


main : Program () () Never
main =
    Check.main
"""

# The Elm 0.19.1 code generator emits ``--<digits>`` (two unary minuses
# glued together) when it negates an integer literal whose magnitude
# reaches the int64 boundary.  JavaScript parses ``--<digits>`` as a
# prefix-decrement of a numeric literal and rejects the file with a
# ``SyntaxError``.  ``check_elm_syntax.py`` still validates the Elm
# source for these fixtures; only the compile-and-execute step is
# skipped.
_SKIP_SUFFIXES = (
    "tests/integration/cases/scalar_int_very_negative_large/Elm@v0_19.elm",
)


def _run_fixture(
    filename: str,
    *,
    elm_path: str,
    node_path: str,
) -> bool:
    """Compile and run one fixture.  Return True on failure."""
    with tempfile.TemporaryDirectory(suffix=NOINDEX_SUFFIX) as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        src_dir = tmpdir / "src"
        src_dir.mkdir()
        (tmpdir / "elm.json").write_text(data=ELM_JSON, encoding="utf-8")
        main_path = src_dir / "Main.elm"
        env = {**os.environ, "ELM_HOME": str(object=worker_elm_home())}
        check_path = src_dir / "Check.elm"
        output_js = tmpdir / "main.js"
        src = Path(filename)
        # Strip the ``@<version>`` tag every fixture filename carries before
        # checking for the ``_call`` suffix that selects the call-mode driver.
        logical_stem = src.stem.split(sep="@", maxsplit=1)[0]
        is_call = logical_stem.endswith("_call")
        main_path.write_text(
            data=_CALL_MAIN_ELM if is_call else _MAIN_ELM,
            encoding="utf-8",
        )
        check_path.write_text(
            data=src.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        compile_result = run_elm_make(
            args=[
                elm_path,
                "make",
                "src/Main.elm",
                f"--output={output_js}",
            ],
            cwd=tmpdir,
            env=env,
        )
        if compile_result.returncode != 0:
            msg = f"{filename}: elm make failed\n"
            msg += compile_result.stderr + compile_result.stdout
            sys.stderr.write(msg)
            return True
        run_result = subprocess.run(
            args=[node_path, str(object=output_js)],
            capture_output=True,
            text=True,
            check=False,
        )
    if run_result.returncode == 0:
        return False
    msg = f"{filename}: node run failed\n"
    msg += run_result.stderr + run_result.stdout
    sys.stderr.write(msg)
    return True


def main() -> None:
    """Run each Elm golden file end-to-end."""
    filenames = [
        f
        for f in sys.argv[1:]
        if not any(f.endswith(suffix) for suffix in _SKIP_SUFFIXES)
    ]
    elm_path = shutil.which(cmd="elm") or "elm"
    node_path = shutil.which(cmd="node") or "node"
    with (
        tempfile.TemporaryDirectory(suffix=NOINDEX_SUFFIX) as primed_str,
        tempfile.TemporaryDirectory(suffix=NOINDEX_SUFFIX) as worker_homes_str,
    ):
        primed = Path(primed_str)
        prime_elm_home(elm_path=elm_path, elm_home=primed)
        worker = functools.partial(
            _run_fixture,
            elm_path=elm_path,
            node_path=node_path,
        )
        with ProcessPoolExecutor(
            initializer=init_worker_elm_home,
            initargs=(str(object=primed), worker_homes_str),
        ) as pool:
            results = list(pool.map(worker, filenames))
    if any(results):
        sys.exit(1)


if __name__ == "__main__":
    main()
