"""Shared helpers for the Elm lint scripts."""

import atexit
import json
import os
import shutil
import subprocess
import tempfile
import time
from collections.abc import Mapping, Sequence
from pathlib import Path

ELM_JSON = json.dumps(
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

_ELM_FILE_LOCK_MARKERS = (
    "openBinaryFile",
    "resource busy (file is locked)",
)


def _is_elm_file_lock_error(result: subprocess.CompletedProcess[str]) -> bool:
    """Return True if Elm failed with its transient cache lock error."""
    output = result.stderr + result.stdout
    return all(marker in output for marker in _ELM_FILE_LOCK_MARKERS)


_PRIME_CHECK_ELM = """\
module Check exposing (value)


value : Int
value =
    0
"""


def prime_elm_home(*, elm_path: str, elm_home: Path) -> None:
    """Populate ``elm_home`` so concurrent workers can share its package
    cache without each downloading ``elm/core`` separately.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        src_dir = Path(tmpdir) / "src"
        src_dir.mkdir()
        (Path(tmpdir) / "elm.json").write_text(data=ELM_JSON, encoding="utf-8")
        (src_dir / "Check.elm").write_text(
            data=_PRIME_CHECK_ELM,
            encoding="utf-8",
        )
        env = {**os.environ, "ELM_HOME": str(object=elm_home)}
        result = run_elm_make(
            args=[elm_path, "make", "src/Check.elm", "--output=/dev/null"],
            cwd=tmpdir,
            env=env,
        )
        if result.returncode != 0:
            msg = "Failed to prime ELM_HOME:\n" + result.stderr + result.stdout
            raise RuntimeError(msg)


_primed_elm_home: Path | None = None
_worker_elm_home_dir: Path | None = None


def init_worker_elm_home(primed_elm_home: str) -> None:
    """``ProcessPoolExecutor`` initializer that records the primed
    ELM_HOME path for later lazy copying by ``worker_elm_home``.
    """
    global _primed_elm_home  # noqa: PLW0603
    _primed_elm_home = Path(primed_elm_home)


def worker_elm_home() -> Path:
    """Return this worker's private ELM_HOME, copied from the primed
    one on first call.

    ``elm make`` does not support concurrent access to a shared
    ELM_HOME (it locks the cache and fails with "resource busy"),
    so each worker keeps its own copy for its lifetime.
    """
    global _worker_elm_home_dir  # noqa: PLW0603
    if _worker_elm_home_dir is not None:
        return _worker_elm_home_dir
    if _primed_elm_home is None:
        msg = "init_worker_elm_home was not called"
        raise RuntimeError(msg)
    worker_dir = Path(tempfile.mkdtemp(prefix="elm-home-worker-"))
    shutil.copytree(src=_primed_elm_home, dst=worker_dir, dirs_exist_ok=True)
    atexit.register(shutil.rmtree, str(object=worker_dir), ignore_errors=True)
    _worker_elm_home_dir = worker_dir
    return _worker_elm_home_dir


def run_elm_make(
    *,
    args: Sequence[str],
    cwd: str | Path,
    env: Mapping[str, str],
) -> subprocess.CompletedProcess[str]:
    """Run ``elm make``, retrying Elm's transient file-lock failure."""
    attempts = 3
    result: subprocess.CompletedProcess[str] | None = None
    for attempt in range(attempts):
        result = subprocess.run(
            args=list(args),
            capture_output=True,
            text=True,
            check=False,
            cwd=cwd,
            env=dict(env),
        )
        if result.returncode == 0 or not _is_elm_file_lock_error(result):
            return result
        if attempt + 1 < attempts:
            time.sleep(0.2 * (attempt + 1))
    if result is None:  # pragma: no cover
        msg = "elm make was not attempted"
        raise RuntimeError(msg)
    return result
