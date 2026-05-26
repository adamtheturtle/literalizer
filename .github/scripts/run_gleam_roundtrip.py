"""Gleam JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Gleam
``let my_data: json.Json = json.object([...])`` binding using
``Gleam(json_type=Gleam.json_types.GLEAM_JSON_JSON)``, wrap it in a
``main`` module that prints ``json.to_string(my_data)`` on standard
output, copy the primed Gleam project from ``LINT_GLEAM_PRIMED_DIR``
into a tmpdir, run ``gleam run -m main``, and hand the emitted JSON
to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Gleam roundtrip`` step of the
``lint-gleam`` job in ``.github/workflows/lint.yml``, because that job
is where the Gleam toolchain is installed and the
``LINT_GLEAM_PRIMED_DIR`` primed project (with ``gleam_stdlib`` and
``gleam_json`` already downloaded by ``Prime Gleam project``) is
available.  It shares the same input and comparison logic as the
other per-language round-trip helpers.

The serializer is ``gleam_json``'s built-in encoder.  The literalizer
emits ``json.Json`` builder calls directly, so the previous hand-rolled
``GVal`` -> ``Json`` walker has gone away.

The shared input's ``float_large_exponent`` field is excluded from
the comparison: Gleam's float literal grammar rejects the explicit
``+`` sign Python's ``repr`` emits for large exponents (``1.0e+308``
fails with ``This float is missing an exponent``).  Trimming the
field before literalization keeps the generated program inside what
the Gleam compiler accepts; this is a literalizer-side concern that
will be tracked separately rather than worked around here.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer.languages import Gleam

_VAR_NAME = "my_data"
_LABEL = "Gleam"
_EXCLUDED_KEYS = ("float_large_exponent",)


def _build_program(json_text: str) -> str:
    """Return a runnable Gleam module literalized from *json_text*."""
    trimmed = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Gleam(json_type=Gleam.json_types.GLEAM_JSON_JSON),
        json_text=trimmed,
        var_name=_VAR_NAME,
        pre_indent_level=1,
    )
    return (
        "import gleam/io\n"
        "import gleam/json\n"
        "\n"
        "pub fn main() {\n"
        f"{result.declaration_code}\n"
        f"  io.println(json.to_string({_VAR_NAME}))\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the Gleam backend."""
    primed_dir = Path(os.environ["LINT_GLEAM_PRIMED_DIR"])
    gleam_path = shutil.which(cmd="gleam") or "gleam"
    program = _build_program(json_text=roundtrip_common.read_input())
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = Path(tmpdir_name)
        # The primed dir already has `gleam.toml`, `manifest.toml`, and
        # `build/packages/<dep>` populated, so the in-tmpdir `gleam
        # run` does not need to download deps.
        shutil.copytree(src=primed_dir, dst=tmpdir, dirs_exist_ok=True)
        source_path = tmpdir / "src" / "main.gleam"
        source_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.write_text(data=program, encoding="utf-8")
        result = subprocess.run(
            args=[gleam_path, "run", "-m", "main"],
            capture_output=True,
            text=True,
            check=False,
            cwd=tmpdir,
            encoding="utf-8",
        )
        if result.returncode != 0:
            sys.stderr.write(
                f"{_LABEL}: gleam run error\n"
                f"{result.stdout}{result.stderr}\n"
                f"Program:\n{program}\n",
            )
            sys.exit(1)
        # `gleam run` prints `Compiled in ...` / `Running main.main`
        # progress on stderr, so stdout is exactly the program's
        # `io.println` output (a single JSON document plus newline).
        roundtrip_common.verify(
            label=_LABEL,
            produced_json=result.stdout,
            exclude_keys=_EXCLUDED_KEYS,
        )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
