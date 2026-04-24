"""Run PureScript golden files end-to-end via ``purs compile`` + Node
to catch runtime errors that survive the compile-only check.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from purescript_common import PRELUDE_JS, PRELUDE_PURS

# Dynamically import the compiled ``Check`` module so Node runs its
# top-level bindings. PureScript compiles each top-level value into a
# strict expression that is evaluated at module load, so importing
# ``Check`` forces ``my_data`` to be constructed, surfacing foreign
# implementation errors or other load-time crashes that a compile-only
# check would miss.
_NODE_DRIVER = (
    "import('./output/Check/index.js')"
    ".then(m => {"
    " if (typeof m.my_data === 'undefined')"
    " { throw new Error('Check.my_data is undefined'); }"
    " })"
    ".catch(e => {"
    " console.error(e && e.stack ? e.stack : e);"
    " process.exit(1);"
    " })"
)


def _run_fixture(
    *,
    filename: str,
    tmpdir: Path,
    check_path: Path,
    prelude_purs: Path,
    output_dir: Path,
    purs_path: str,
    node_path: str,
) -> bool:
    """Compile and run one fixture.  Return True on failure."""
    src = Path(filename)
    check_path.write_text(
        data=src.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    compile_result = subprocess.run(
        args=[
            purs_path,
            "compile",
            check_path.as_posix(),
            prelude_purs.as_posix(),
            "-o",
            output_dir.as_posix(),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if compile_result.returncode != 0:
        msg = f"{filename}: purs compile failed\n"
        msg += compile_result.stderr + compile_result.stdout
        sys.stderr.write(msg)
        return True
    run_result = subprocess.run(
        args=[node_path, "--input-type=module", "-e", _NODE_DRIVER],
        capture_output=True,
        text=True,
        check=False,
        cwd=tmpdir,
    )
    if run_result.returncode != 0:
        msg = f"{filename}: node run failed\n"
        msg += run_result.stderr + run_result.stdout
        sys.stderr.write(msg)
        return True
    return False


def main() -> None:
    """Run each PureScript golden file end-to-end."""
    filenames = sys.argv[1:]
    purs_path = shutil.which(cmd="purs") or "purs"
    node_path = shutil.which(cmd="node") or "node"
    failed = False
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        prelude_purs = tmpdir / "Prelude.purs"
        prelude_js = tmpdir / "Prelude.js"
        prelude_purs.write_text(data=PRELUDE_PURS, encoding="utf-8")
        prelude_js.write_text(data=PRELUDE_JS, encoding="utf-8")
        check_path = tmpdir / "Check.purs"
        output_dir = tmpdir / "output"
        for filename in filenames:
            if _run_fixture(
                filename=filename,
                tmpdir=tmpdir,
                check_path=check_path,
                prelude_purs=prelude_purs,
                output_dir=output_dir,
                purs_path=purs_path,
                node_path=node_path,
            ):
                failed = True
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
