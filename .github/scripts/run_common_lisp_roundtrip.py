"""Common Lisp JSON round-trip check (issue #2644).

Literalize the shared ``roundtrip_input.json`` document to a Common Lisp
``(defparameter *my-data* ...)`` binding, wrap it in a script that
normalizes the literalized value into a hash-table / vector tree and
prints ``com.inuoe.jzon:stringify`` of that tree, run it under ``sbcl``
(through ``ros run``), and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by the ``Common Lisp roundtrip`` step of the
``lint-commonlisp`` job in ``.github/workflows/lint.yml``, because that
job is where SBCL is installed (pinned by the ``Install SBCL`` step).
It shares the same input and comparison logic as the other per-language
round-trip helpers.

The literalized Common Lisp output is shape-ambiguous: a dict becomes
``(list (cons "k" v) ...)`` (an alist) and an array becomes
``(list v ...)``; both an empty dict and an empty array literalize to
``nil``, and the boolean ``false`` is also ``nil``.  A purely runtime
encoder therefore cannot tell ``{}`` from ``[]`` or ``false`` from a
missing key.  This script sidesteps the ambiguity the same way the Tcl
helper does: Python walks the parsed input and emits a single Common
Lisp expression that rebuilds the literalized data along the *known*
JSON shape into the typed structure ``com.inuoe.jzon`` expects -- hash
tables for objects, vectors for arrays, ``t`` / ``nil`` for booleans
(with ``*nil-as*`` bound to ``:false`` so ``nil`` encodes as ``false``).
Each leaf is read from the literalized ``*my-data*`` via
``cdr``/``assoc`` (object members) or ``nth`` (array elements).  All
JSON encoding -- string escaping, number formatting, separator
placement -- is then done by a single ``com.inuoe.jzon:stringify`` call,
so no encoder details are hand-rolled.  ``com.inuoe.jzon`` is a modern,
actively maintained Quicklisp library and is the de-facto choice for
new Common Lisp code that needs JSON.
"""

import json
import shutil

import roundtrip_common

from literalizer.languages import CommonLisp

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
_LABEL = "Common Lisp"

# `*read-default-float-format*` defaults to `single-float`, which would
# overflow on the `float_large_exponent` (`1.7976931348623157e308`)
# field; pinning the reader to `double-float` lets the literalized
# `defparameter` form parse without loss.  `com.inuoe.jzon` is
# pre-installed by the `Install com.inuoe.jzon` CI step (`ros install
# com.inuoe.jzon`); the `ql:quickload` call here then just loads the
# cached system.  Roswell ships Quicklisp pre-registered in `ros run`,
# so no extra bootstrap is needed.
_HEADER = """\
(setf *read-default-float-format* 'double-float)
(ql:quickload :com.inuoe.jzon :silent t)
"""


def _cl_string(text: str) -> str:
    """Return a Common Lisp string literal whose value is *text*."""
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _build(*, value: JsonValue, path_expr: str) -> str:
    """Return a Common Lisp expression that produces the jzon-encodable
    rebuild of *value* at *path_expr*.

    *path_expr* is a Common Lisp expression that evaluates to the
    sub-value at this position inside the literalized ``*my-data*``.
    Scalars pass straight through (jzon encodes ``t`` / ``nil`` /
    numbers / strings natively); arrays are rebuilt as vectors and
    objects as hash tables so jzon can tell them apart from
    each other and from booleans.
    """
    if isinstance(value, bool):
        # `bool` must precede `int` (it is a subclass).  Both `t` and
        # `nil` pass through: jzon's default mapping already encodes
        # `t` as `true` and `nil` as `false` (the symbol `cl:null` is
        # what it reserves for JSON `null`), so no encoder configuration
        # is needed for the boolean side.
        return path_expr
    if isinstance(value, (int, float, str)):
        return path_expr
    if isinstance(value, list):
        parts = [
            _build(value=item, path_expr=f"(nth {index} {path_expr})")
            for index, item in enumerate(iterable=value)
        ]
        return f"(vector {' '.join(parts)})"
    if isinstance(value, dict):
        sets: list[str] = []
        for key, sub_value in value.items():
            key_literal = _cl_string(text=key)
            sub_path = f"(cdr (assoc {key_literal} {path_expr} :test #'equal))"
            sub_build = _build(value=sub_value, path_expr=sub_path)
            sets.append(f"(setf (gethash {key_literal} ht) {sub_build})")
        body = " ".join(sets)
        return f"(let ((ht (make-hash-table :test 'equal))) {body} ht)"
    # `roundtrip_input.json` is deliberately `null`-free; the residual
    # `None` branch keeps the walker total without expanding the shared
    # input's coverage promise.  jzon reserves the symbol `cl:null` as
    # its JSON `null` sentinel.
    return "'cl:null"


def _build_program(json_text: str) -> str:
    """Return a runnable Common Lisp program literalized from
    *json_text*.
    """
    result = roundtrip_common.literalize_new_variable(
        language=CommonLisp(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    parsed: JsonValue = json.loads(s=json_text)
    rebuild = _build(value=parsed, path_expr=f"*{_VAR_NAME}*")
    emit = f"(write-string (com.inuoe.jzon:stringify {rebuild}))"
    return f"{_HEADER}\n{preamble}\n{result.code}\n{emit}\n"


def main() -> None:
    """Round-trip the shared document through the Common Lisp backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    ros = shutil.which(cmd="ros") or "ros"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.lisp",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[
                    ros,
                    "run",
                    "--eval",
                    "(sb-ext:disable-debugger)",
                    "--load",
                    "main.lisp",
                    "--quit",
                ],
                failure_label="sbcl runtime error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
