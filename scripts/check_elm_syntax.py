"""Check syntax of Elm golden files using ``elm make``."""

import functools
import os
import shutil
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


def _check_fixture(
    filename: str,
    *,
    elm_path: str,
) -> bool:
    """Check one fixture. Return True on failure."""
    with tempfile.TemporaryDirectory(suffix=NOINDEX_SUFFIX) as tmpdir:
        src_dir = Path(tmpdir) / "src"
        src_dir.mkdir()
        elm_json_path = Path(tmpdir) / "elm.json"
        elm_json_path.write_text(data=ELM_JSON, encoding="utf-8")
        env = {**os.environ, "ELM_HOME": str(object=worker_elm_home())}
        target = src_dir / "Check.elm"
        src = Path(filename)
        target.write_text(
            data=src.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        result = run_elm_make(
            args=[
                elm_path,
                "make",
                "src/Check.elm",
                "--output=/dev/null",
            ],
            cwd=tmpdir,
            env=env,
        )
    if result.returncode == 0:
        return False
    msg = f"{filename}: elm make failed\n"
    msg += result.stderr + result.stdout
    sys.stderr.write(msg)
    return True


def main() -> None:
    """Check syntax of the given Elm golden files."""
    filenames = sys.argv[1:]
    elm_path = shutil.which(cmd="elm") or "elm"
    with (
        tempfile.TemporaryDirectory(suffix=NOINDEX_SUFFIX) as primed_str,
        tempfile.TemporaryDirectory(suffix=NOINDEX_SUFFIX) as worker_homes_str,
    ):
        primed = Path(primed_str)
        prime_elm_home(elm_path=elm_path, elm_home=primed)
        worker = functools.partial(_check_fixture, elm_path=elm_path)
        with ProcessPoolExecutor(
            initializer=init_worker_elm_home,
            initargs=(str(object=primed), worker_homes_str),
        ) as pool:
            results = list(pool.map(worker, filenames))
    if any(results):
        sys.exit(1)


if __name__ == "__main__":
    main()
