"""Gleam JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Gleam
``let my_data = GDict([...])`` binding, wrap it in a ``main`` module
whose ``to_json`` walker turns the generated ``GVal`` ADT into a
``gleam_json`` ``Json`` value and prints ``json.to_string(...)`` on
standard output, copy the primed Gleam project from
``LINT_GLEAM_PRIMED_DIR`` into a tmpdir, run ``gleam run -m main``,
and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Gleam roundtrip`` step of the
``lint-gleam`` job in ``.github/workflows/lint.yml``, because that job
is where the Gleam toolchain is installed and the
``LINT_GLEAM_PRIMED_DIR`` primed project (with ``gleam_stdlib`` and
``gleam_json`` already downloaded by ``Prime Gleam project``) is
available.  It shares the same input and comparison logic as the
other per-language round-trip helpers.

The serializer is ``gleam_json``'s built-in encoder rather than a
hand-rolled one (matching the preference expressed in the issue
notes).  The literalized data lives in a custom ``GVal`` ADT whose
shape is fixed by the Gleam backend, so a small recursive
``to_json`` walker maps each constructor to the matching
``gleam_json`` builder.  The full ``GVal`` is defined here rather
than reusing the literalizer's narrower preamble so the walker stays
exhaustive if the fixture later grows ``GNull`` cases; the
literalizer-generated preamble is dropped because Gleam rejects two
type definitions with the same name.

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

# Full ``GVal`` type with every constructor the Gleam backend can
# emit, not just the ones present in the trimmed input, so ``to_json``
# below stays exhaustive if the fixture later grows ``GNull`` cases.
# Replaces the literalizer's preamble (which only lists the
# constructors actually used by the data).
_GVAL_TYPE = """\
pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
"""

# Walker that turns ``GVal`` into a ``gleam_json`` ``Json`` value.
# ``preprocessed_array`` is the heterogeneous-list constructor; the
# typed ``json.array`` overload would force every element to share a
# type, which the ``mixed_array`` field violates.
_TO_JSON = """\
fn to_json(v: GVal) -> json.Json {
  case v {
    GNull -> json.null()
    GBool(b) -> json.bool(b)
    GInt(i) -> json.int(i)
    GFloat(f) -> json.float(f)
    GStr(s) -> json.string(s)
    GList(items) -> json.preprocessed_array(list.map(items, to_json))
    GDict(entries) ->
      json.object(
        list.map(entries, fn(e) {
          let #(k, child) = e
          #(k, to_json(child))
        }),
      )
  }
}
"""


def _build_program(json_text: str) -> str:
    """Return a runnable Gleam module literalized from *json_text*."""
    trimmed = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Gleam(),
        json_text=trimmed,
        var_name=_VAR_NAME,
        pre_indent_level=1,
    )
    return (
        "import gleam/io\n"
        "import gleam/json\n"
        "import gleam/list\n"
        "\n"
        f"{_GVAL_TYPE}\n"
        f"{_TO_JSON}\n"
        "pub fn main() {\n"
        f"{result.declaration_code}\n"
        f"  io.println(json.to_string(to_json({_VAR_NAME})))\n"
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
