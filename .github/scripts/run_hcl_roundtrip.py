"""HCL JSON round-trip check (issue #2657).

Literalize the shared ``roundtrip_input.json`` document to an HCL
``myData = { ... }`` attribute, parse the resulting HCL document with
``hcl2json``, then re-serialize the inner value as JSON and hand it to
:func:`roundtrip_common.verify`.

Unlike the executable-language round-trips, there is no language
runtime to invoke: the analogous "back to JSON" step is the
``hcl2json`` parser re-emitting the parsed value.  ``hcl2json`` is the
same binary the ``Lint Hcl`` syntax check uses, so the pinned
toolchain in the ``lint-go-installed`` job already provides it; no
extra install step is needed.

This lives here, driven by the ``Hcl roundtrip`` step of the
``lint-go-installed`` job in ``.github/workflows/lint.yml``, alongside
the existing ``Lint Hcl`` syntax check that uses the same ``hcl2json``
dependency.  It shares the same input and comparison logic as the
other per-language round-trip helpers.

``float_large_exponent`` is excluded from the comparison because
``hcl2json`` emits ``1.7976931348623157e+308`` as a fully-expanded
309-digit integer literal in its JSON output, and parsing that integer
back through Python's ``json`` yields a value that does not compare
equal to the original ``float`` (large ints are not equal to floats of
the same magnitude when the rounded conversion would lose bits).
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import roundtrip_common

from literalizer.languages import Hcl

_VAR_NAME = "myData"
_LABEL = "HCL"
_EXCLUDED_KEYS = ("float_large_exponent",)


def _build_document(json_text: str) -> str:
    """Return an HCL document literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Hcl(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    return f"{result.code}\n"


def main() -> None:
    """Round-trip the shared document through the HCL backend."""
    document = _build_document(json_text=roundtrip_common.read_input())
    hcl2json = shutil.which(cmd="hcl2json") or "hcl2json"
    with tempfile.TemporaryDirectory() as tmpdir_name:
        source_path = Path(tmpdir_name) / "main.hcl"
        source_path.write_text(data=document, encoding="utf-8")
        completed = subprocess.run(
            args=[hcl2json, str(object=source_path)],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )
    if completed.returncode != 0:
        sys.stderr.write(
            f"{_LABEL}: hcl2json error\n"
            f"{completed.stdout}{completed.stderr}"
            f"\nProgram:\n{document}\n",
        )
        sys.exit(1)
    parsed: dict[str, object] = json.loads(s=completed.stdout)
    inner = parsed[_VAR_NAME]
    produced_json = json.dumps(obj=inner)
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=produced_json,
        exclude_keys=_EXCLUDED_KEYS,
    )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
