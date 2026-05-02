"""Shared helpers for the Elm lint scripts."""

import json
import subprocess
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
