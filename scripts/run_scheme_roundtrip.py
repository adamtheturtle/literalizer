"""Scheme JSON round-trip check (issue #2677).

Literalize the shared ``roundtrip_input.json`` document to a Scheme
``(define my-data ...)`` binding under
``Scheme(json_type=Scheme.json_types.GUILE_JSON)``, wrap it in a Guile
script, run it under ``guile-3.0``, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by the ``Scheme roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job
is where ``guile-3.0`` is installed and where the ``Install guile-json``
step clones the guile-json checkout that ``LITERALIZER_GUILE_JSON_PATH``
points at.  It shares the same input and comparison logic as the other
per-language round-trip helpers.

Under ``json_type=GUILE_JSON`` the literalized value is already the tree
of association lists and vectors (with ``'null`` for JSON null) that
guile-json's ``scm->json`` accepts directly, so the program emits a
single ``(scm->json my-data)`` call.  All JSON encoding -- string
escaping, number formatting, separator placement -- is done by that one
call, so no encoder details are hand-rolled.  No top-level keys are
excluded: Guile has arbitrary-precision integers (so the 26-digit
``biginteger`` survives) and ``scm->json`` emits inexact reals via
``number->string``, which round-trips ``1.7976931348623157e+308``;
``-0.0`` compares equal to ``0.0`` under the parsed-value diff in
:func:`roundtrip_common.verify`.
"""

import os
import shutil

from literalizer.languages import Scheme
from scripts import roundtrip_common

_VAR_NAME = "my-data"
_LABEL = "Scheme"

# `set-port-encoding!` pins stdout to UTF-8 so unicode string leaves
# (e.g. ``"unicode é 中"``) survive the byte-level handoff to the
# Python verifier regardless of the runner's locale.  `(use-modules
# (json))` is also emitted by the language's `static_preamble` under
# `json_type=GUILE_JSON`, but repeating it here is harmless and keeps
# the wrapper runnable in the default mode too.
_HEADER = """\
(use-modules (json))
(set-port-encoding! (current-output-port) "UTF-8")
"""


def _build_program(json_text: str) -> str:
    """Return a runnable Scheme program literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Scheme(json_type=Scheme.json_types.GUILE_JSON),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    emit = f"(scm->json {_VAR_NAME})"
    return f"{_HEADER}\n{preamble}\n{result.code}\n{emit}\n"


def main() -> None:
    """Round-trip the shared document through the Scheme backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    # Invoke `guile-3.0` directly rather than `guile` because the
    # `Install apt packages` step does not replay the package's
    # `update-alternatives` postinst on cache hit, so `/usr/bin/guile`
    # is missing (mirrors the `Lint Scheme` step).
    guile = shutil.which(cmd="guile-3.0") or "guile-3.0"
    # `LITERALIZER_GUILE_JSON_PATH` points at the guile-json checkout
    # (the `Install guile-json` step in `.github/workflows/lint.yml`
    # exports it).  Adding it via `-L` puts `json.scm` on Guile's
    # source-load path so the bare `(use-modules (json))` resolves
    # there; `--no-auto-compile` keeps the run from trying to write
    # a `.go` cache for it.
    guile_json_path = os.environ["LITERALIZER_GUILE_JSON_PATH"]
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.scm",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[
                    guile,
                    "--no-auto-compile",
                    "-L",
                    guile_json_path,
                    "-s",
                    "main.scm",
                ],
                failure_label="guile runtime error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
