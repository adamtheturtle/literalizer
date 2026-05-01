"""Run Elm golden files end-to-end via ``elm make`` + Node to catch
runtime errors that survive the compile-only check.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from elm_common import ELM_JSON, run_elm_make

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
    "tests/integration/cases/scalar_int_very_negative_large/Elm.elm",
)


def _run_fixture(
    *,
    filename: str,
    elm_path: str,
    node_path: str,
    elm_home: Path,
) -> bool:
    """Compile and run one fixture.  Return True on failure."""
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        src_dir = tmpdir / "src"
        src_dir.mkdir()
        (tmpdir / "elm.json").write_text(data=ELM_JSON, encoding="utf-8")
        main_path = src_dir / "Main.elm"
        env = {**os.environ, "ELM_HOME": str(object=elm_home)}
        check_path = src_dir / "Check.elm"
        output_js = tmpdir / "main.js"
        src = Path(filename)
        is_call = src.stem.endswith("_call")
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
    filenames = sys.argv[1:]
    elm_path = shutil.which(cmd="elm") or "elm"
    node_path = shutil.which(cmd="node") or "node"
    failed = False
    with tempfile.TemporaryDirectory() as elm_home_str:
        elm_home = Path(elm_home_str)
        for filename in filenames:
            if any(filename.endswith(suffix) for suffix in _SKIP_SUFFIXES):
                continue
            if _run_fixture(
                filename=filename,
                elm_path=elm_path,
                node_path=node_path,
                elm_home=elm_home,
            ):
                failed = True
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
