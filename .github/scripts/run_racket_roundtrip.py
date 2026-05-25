"""Racket JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Racket
``(define my-data ...)`` binding, wrap it in a tiny ``#lang racket``
module that normalizes the literalized value into a Racket JSON
``jsexpr?`` and prints ``write-json`` on standard output, run it under
``racket``, and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Racket roundtrip`` step of the
``lint-racket`` job in ``.github/workflows/lint.yml``, because that job
is where the Racket toolchain is installed.  It shares the same input
and comparison logic as the other per-language round-trip helpers.

The serializer is Racket's built-in ``json`` module rather than a
hand-rolled encoder (matching the preference expressed in the issue
notes).  The ``json`` module's ``write-json`` requires JSON objects to
be hash tables keyed by symbols, but the literalized output uses string
keys (Racket dicts support arbitrary keys), so the program first walks
the value: every ``hash?`` is rebuilt as a ``hasheq`` with
``string->symbol`` keys, and lists/atoms pass through.  No top-level
keys are excluded: Racket has arbitrary-precision integers (so the
26-digit ``biginteger`` survives) and ``write-json`` emits inexact reals
via ``number->string``, which round-trips ``1.7976931348623157e+308``
and ``-0.0`` exactly.
"""

import shutil

import roundtrip_common

from literalizer.languages import Racket

_VAR_NAME = "my-data"
_LABEL = "Racket"

_NORMALIZE_AND_WRITE = """\
(define (->jsexpr v)
  (cond
    [(hash? v)
     (for/hasheq ([(k val) (in-hash v)])
       (values (string->symbol k) (->jsexpr val)))]
    [(list? v) (map ->jsexpr v)]
    [else v]))

(write-json (->jsexpr my-data))
"""


def _build_program(json_text: str) -> str:
    """Return a runnable Racket program literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Racket(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return f"{preamble}\n(require json)\n{result.code}\n{_NORMALIZE_AND_WRITE}"


def main() -> None:
    """Round-trip the shared document through the Racket backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    racket = shutil.which(cmd="racket") or "racket"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.rkt",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[racket, "main.rkt"],
                failure_label="racket runtime error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
