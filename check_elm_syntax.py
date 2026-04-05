"""Check syntax of an Elm golden file using ``elm make``."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

_ELM_JSON = json.dumps(
    obj={
        "type": "application",
        "source-directories": ["src"],
        "elm-version": "0.19.1",
        "dependencies": {
            "direct": {"elm/core": "1.0.5"},
            "indirect": {"elm/json": "1.1.3"},
        },
        "test-dependencies": {"direct": {}, "indirect": {}},
    },
)

_MAX_RETRIES = 3
_RETRY_DELAY_SECONDS = 1


def _run_elm_make(
    *,
    elm_path: str,
    filename: str,
) -> subprocess.CompletedProcess[str]:
    """Run elm make in a fresh temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        src_dir = Path(tmpdir) / "src"
        src_dir.mkdir()
        elm_json_path = Path(tmpdir) / "elm.json"
        elm_json_path.write_text(data=_ELM_JSON, encoding="utf-8")
        src = Path(filename)
        target = src_dir / "Check.elm"
        target.write_text(
            data=src.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        elm_home = Path(tmpdir) / ".elm"
        elm_home.mkdir()
        env = {**os.environ, "ELM_HOME": str(object=elm_home)}
        return subprocess.run(
            args=[elm_path, "make", "src/Check.elm", "--output=/dev/null"],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
            env=env,
        )


def main() -> None:
    """Check syntax of the given Elm golden file."""
    filename = sys.argv[1]
    elm_path = shutil.which(cmd="elm") or "elm"
    for attempt in range(_MAX_RETRIES):
        result = _run_elm_make(elm_path=elm_path, filename=filename)
        if result.returncode == 0:
            return
        output = result.stderr + result.stdout
        is_file_lock_error = "file is locked" in output
        if is_file_lock_error and attempt < _MAX_RETRIES - 1:
            time.sleep(_RETRY_DELAY_SECONDS)
            continue
        msg = f"{filename}: elm make failed\n{output}"
        sys.stderr.write(msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
