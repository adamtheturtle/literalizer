"""Scheme JSON round-trip check (issue #2677).

Literalize the shared ``roundtrip_input.json`` document to a Scheme
``(define my-data ...)`` binding, wrap it in a Guile script that
normalizes the literalized value into the alist / vector tree
``scm->json`` expects, run it under ``guile-3.0``, and hand the emitted
JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Scheme roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job is
where ``guile-3.0`` and the ``guile-3.0-json`` apt package are
installed.  It shares the same input and comparison logic as the other
per-language round-trip helpers.

The serializer is the ``(json)`` module from guile-json rather than a
hand-rolled encoder (matching the preference expressed in the issue
notes); Guile itself ships no JSON library.  The literalized Scheme
output is shape-ambiguous: a dict becomes ``(list "k" v ...)`` and an
array becomes ``(list v ...)``; both an empty dict and an empty array
literalize to ``(list)``.  A purely runtime encoder therefore cannot
tell ``{}`` from ``[]``.

To avoid emitting one ``list-ref`` per leaf (as the Tcl / Common Lisp
helpers do), Python instead emits a compact *shape tree* describing
which subtrees of ``my-data`` are objects and which are arrays, plus a
generic Scheme ``normalize`` walker that rebuilds the typed structure
``scm->json`` accepts: an *alist* of ``(key . value)`` pairs for each
object (``scm->json``'s ``json-valid?`` rejects hash tables, see
``builder.scm:188``), and a vector for each array.  Shape nodes are
``(obj (key . sub-shape) ...)``, ``(arr sub-shape ...)``, or the leaf
symbol ``scalar``.  All JSON encoding -- string escaping, number
formatting, separator placement -- is then done by a single
``scm->json`` call, so no encoder details are hand-rolled.  No
top-level keys are excluded: Guile has arbitrary-precision integers
(so the 26-digit ``biginteger`` survives) and ``scm->json`` emits
inexact reals via ``number->string``, which round-trips
``1.7976931348623157e+308``; ``-0.0`` compares equal to ``0.0`` under
the parsed-value diff in :func:`roundtrip_common.verify`.
"""

import json
import shutil

import roundtrip_common

from literalizer.languages import Scheme

# `json.loads` returns this recursive shape; typing the walker against
# it lets `isinstance` narrow cleanly under pyright, pyrefly, and ty
# without `cast`.
type JsonValue = (
    None
    | bool
    | int
    | float
    | str
    | list["JsonValue"]
    | dict[str, "JsonValue"]
)

_VAR_NAME = "my-data"
_LABEL = "Scheme"

# `set-port-encoding!` pins stdout to UTF-8 so unicode string leaves
# (e.g. ``"unicode é 中"``) survive the byte-level handoff to the
# Python verifier regardless of the runner's locale.  The `normalize`
# walker pairs each shape node with the matching sub-value inside the
# literalized `my-data`: an `obj` shape consumes the flat alternating
# key/value list (taking the value at every odd index) and returns an
# alist of `(key . value)` pairs (the only object form `scm->json`'s
# `json-valid?` accepts; see `json/builder.scm:188`), an `arr` shape
# walks its children in lockstep with the literalized list and returns
# a vector, and the `scalar` leaf passes the value straight through to
# `scm->json`.  Indexing is done with hand-rolled accumulators so the
# walker has no implicit dependency on SRFI-1 (`iota`).
_HEADER = """\
(use-modules (json))
(set-port-encoding! (current-output-port) "UTF-8")

(define (normalize shape data)
  (cond
    ((eq? shape (quote scalar)) data)
    ((eq? (car shape) (quote obj))
     (let loop ((entries (cdr shape)) (index 0) (acc (quote ())))
       (if (pair? entries)
           (loop (cdr entries)
                 (+ index 1)
                 (cons (cons (car (car entries))
                             (normalize (cdr (car entries))
                                        (list-ref data
                                                  (+ (* index 2) 1))))
                       acc))
           (reverse acc))))
    ((eq? (car shape) (quote arr))
     (let loop ((children (cdr shape)) (index 0) (acc (quote ())))
       (if (pair? children)
           (loop (cdr children)
                 (+ index 1)
                 (cons (normalize (car children) (list-ref data index))
                       acc))
           (list->vector (reverse acc)))))))
"""


def _scheme_string(text: str) -> str:
    """Return a Scheme string literal whose value is *text*."""
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _shape(value: JsonValue) -> str:
    """Return a Scheme datum describing the JSON shape of *value*.

    Leaves render as the symbol ``scalar``; objects as
    ``(obj ("k" . sub-shape) ...)``; arrays as ``(arr sub-shape ...)``.
    The walker in ``_HEADER`` consumes this tree in lockstep with the
    literalized ``my-data``.
    """
    if isinstance(value, dict):
        entries = " ".join(
            f"({_scheme_string(text=key)} . {_shape(value=sub)})"
            for key, sub in value.items()
        )
        return f"(obj {entries})"
    if isinstance(value, list):
        children = " ".join(_shape(value=item) for item in value)
        return f"(arr {children})"
    return "scalar"


def _build_program(json_text: str) -> str:
    """Return a runnable Scheme program literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Scheme(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    shape_datum = _shape(value=json.loads(s=json_text))
    emit = f"(scm->json (normalize (quote {shape_datum}) {_VAR_NAME}))"
    return f"{_HEADER}\n{preamble}\n{result.code}\n{emit}\n"


def main() -> None:
    """Round-trip the shared document through the Scheme backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    # Invoke `guile-3.0` directly rather than `guile` because the
    # `Install apt packages` step does not replay the package's
    # `update-alternatives` postinst on cache hit, so `/usr/bin/guile`
    # is missing (mirrors the `Lint Scheme` step).
    guile = shutil.which(cmd="guile-3.0") or "guile-3.0"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.scm",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[guile, "--no-auto-compile", "-s", "main.scm"],
                failure_label="guile runtime error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
