"""Shared helpers for the Elm lint scripts."""

import dataclasses
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

# Suffix appended to every temporary directory that ``elm make`` writes
# into (per-fixture build dirs, the primed ELM_HOME, per-worker ELM_HOME
# copies).
#
# Under heavy parallel load on macOS, ``elm make`` intermittently fails
# on its own per-fixture ``elm-stuff/0.19.1/{d,o,i}.dat`` cache files
# with ``withBinaryFile: resource busy (file is locked)`` or with
# ``CORRUPT CACHE`` reports at random byte offsets.  The directories
# are isolated per fixture, so the contention comes from outside our
# code: either macOS file scanners (Spotlight ``mds_stores``,
# quarantine, FSEvents consumers) briefly holding handles on the new
# files, or the Haskell runtime under elm 0.19.1 racing on its own
# locks.
#
# A directory whose name ends in ``.noindex`` is skipped by Spotlight,
# which reduces (but in our testing does not eliminate) the failure
# rate.  The retry loop in ``run_elm_make`` covers what remains.
# The suffix is a no-op on Linux (where CI runs) and on Windows.
NOINDEX_SUFFIX = ".noindex"


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
    with tempfile.TemporaryDirectory(suffix=NOINDEX_SUFFIX) as tmpdir:
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


@dataclasses.dataclass
class _ElmHomeState:
    """Mutable container for per-worker ELM_HOME state."""

    primed: Path | None
    workers_root: Path | None
    worker_dir: Path | None


_state = _ElmHomeState(primed=None, workers_root=None, worker_dir=None)


def init_worker_elm_home(primed_elm_home: str, worker_homes_root: str) -> None:
    """``ProcessPoolExecutor`` initializer that records the primed
    ELM_HOME and the parent directory under which each worker's
    private ELM_HOME copy is created by ``worker_elm_home``.

    Workers create their copies under ``worker_homes_root`` so the
    parent process can clean every copy up by removing that single
    directory after the pool shuts down.  ``atexit`` is unreliable
    here: ``ProcessPoolExecutor`` workers terminate via
    ``os._exit`` (CPython's ``multiprocessing._bootstrap``), which
    skips registered ``atexit`` callbacks on Python <= 3.14.
    """
    _state.primed = Path(primed_elm_home)
    _state.workers_root = Path(worker_homes_root)


def worker_elm_home() -> Path:
    """Return this worker's private ELM_HOME, copied from the primed
    one on first call.

    ``elm make`` does not support concurrent access to a shared
    ELM_HOME (it locks the cache and fails with "resource busy"),
    so each worker keeps its own copy for its lifetime.
    """
    if _state.worker_dir is not None:
        return _state.worker_dir
    if _state.primed is None or _state.workers_root is None:
        msg = "init_worker_elm_home was not called"
        raise RuntimeError(msg)
    worker_dir = Path(
        tempfile.mkdtemp(
            prefix="elm-home-worker-",
            suffix=NOINDEX_SUFFIX,
            dir=_state.workers_root,
        ),
    )
    shutil.copytree(src=_state.primed, dst=worker_dir, dirs_exist_ok=True)
    _state.worker_dir = worker_dir
    return _state.worker_dir


_ELM_TRANSIENT_BINARY_FILE_MARKERS = ("openBinaryFile", "withBinaryFile")
_ELM_TRANSIENT_BUSY_MARKER = "resource busy (file is locked)"
_ELM_TRANSIENT_CORRUPT_MARKER = "CORRUPT CACHE"


def _is_elm_transient_error(result: subprocess.CompletedProcess[str]) -> bool:
    """Return True if ``elm make`` failed with one of the transient
    cache-related errors documented above ``NOINDEX_SUFFIX``.
    """
    output = result.stderr + result.stdout
    if _ELM_TRANSIENT_CORRUPT_MARKER in output:
        return True
    if _ELM_TRANSIENT_BUSY_MARKER not in output:
        return False
    return any(m in output for m in _ELM_TRANSIENT_BINARY_FILE_MARKERS)


def run_elm_make(
    *,
    args: Sequence[str],
    cwd: str | Path,
    env: Mapping[str, str],
) -> subprocess.CompletedProcess[str]:
    """Run ``elm make``, retrying transient cache failures."""
    retries = 4
    for attempt in range(retries):
        result = subprocess.run(
            args=list(args),
            capture_output=True,
            text=True,
            check=False,
            cwd=cwd,
            env=dict(env),
        )
        if result.returncode == 0 or not _is_elm_transient_error(result):
            return result
        # Transient failures (especially CORRUPT CACHE) leave a
        # bad ``elm-stuff`` cache on disk; subsequent attempts
        # would just re-read the corruption.  Wipe it so the
        # retry starts from a clean cache.
        shutil.rmtree(Path(cwd) / "elm-stuff", ignore_errors=True)
        time.sleep(0.5 * (attempt + 1))
    return subprocess.run(
        args=list(args),
        capture_output=True,
        text=True,
        check=False,
        cwd=cwd,
        env=dict(env),
    )
