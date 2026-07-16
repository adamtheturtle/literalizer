"""Tcl JSON round-trip check (issue #2680).

Literalize the shared ``roundtrip_input.json`` document to a Tcl
``set myData [dict create ...]`` binding, wrap it in a ``tclsh`` script
that re-emits JSON on standard output via tcllib's ``json::write``, run
it under ``tclsh``, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by the ``Tcl roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job is
where the ``tcl`` and ``tcllib`` apt packages are installed.  It shares
the same input and comparison logic as the other per-language round-trip
helpers.

Tcl is type-less (every value is a string), so a generic encoder cannot
tell a dict from a same-shape list, or a literalized boolean (``1``/
``0``) from an integer.  ``tcllib``'s ``json::write`` is a *constructor*
library: ``json::write string``, ``json::write array``, ``json::write
object`` build typed fragments, but the caller still has to know each
value's JSON type.  This script therefore drives ``json::write`` along
the *known* JSON shape: Python walks the parsed input and emits a single
nested ``json::write`` expression whose leaves read scalars out of the
literalized ``$myData`` via ``dict get`` / ``lindex``.  Tcl preserves
the textual rep of un-shimmered numeric scalars stored in a ``dict``, so
wide integers and large exponents round-trip without needing the
precision-loss exclusions seen in the typed-language scripts.
"""

import json
import shutil

from literalizer.languages import Tcl
from scripts import roundtrip_common

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

_VAR_NAME = "myData"
_LABEL = "Tcl"

_HEADER = """\
package require json::write
json::write indented 0
json::write aligned 0
fconfigure stdout -encoding utf-8 -translation lf
"""


def _emit_array(*, items: list[JsonValue], path_expr: str) -> str:
    """Return a Tcl expression that yields a JSON array for *items*."""
    parts = [
        _emit(value=item, path_expr=f"[lindex {path_expr} {index}]")
        for index, item in enumerate(iterable=items)
    ]
    return f"[json::write array {' '.join(parts)}]"


def _emit_object(*, entries: dict[str, JsonValue], path_expr: str) -> str:
    """Return a Tcl expression that yields a JSON object for *entries*."""
    # Shared `roundtrip_input.json` only has ASCII-identifier keys, so
    # each key embeds cleanly as a `{...}` Tcl word; `json::write
    # object` escapes the key on its own.
    parts: list[str] = []
    for key, sub_value in entries.items():
        sub_path = f"[dict get {path_expr} {{{key}}}]"
        parts.append(f"{{{key}}}")
        parts.append(_emit(value=sub_value, path_expr=sub_path))
    return f"[json::write object {' '.join(parts)}]"


def _emit(*, value: JsonValue, path_expr: str) -> str:
    """Return a Tcl expression yielding the JSON encoding of *value*.

    *path_expr* is a Tcl expression that, when evaluated, yields the
    sub-value at this position inside the literalized ``$myData``.
    """
    if isinstance(value, bool):
        return f'[expr {{{path_expr} ? "true" : "false"}}]'
    if isinstance(value, (int, float)):
        # Raw Tcl token serves as a JSON number literal; `json::write`
        # passes numeric values through unmodified.
        return path_expr
    if isinstance(value, str):
        return f"[json::write string {path_expr}]"
    if isinstance(value, list):
        return _emit_array(items=value, path_expr=path_expr)
    if isinstance(value, dict):
        return _emit_object(entries=value, path_expr=path_expr)
    return '"null"'


def _build_program(json_text: str) -> str:
    """Return a runnable Tcl script literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Tcl(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    parsed: JsonValue = json.loads(s=json_text)
    emit_expr = _emit(value=parsed, path_expr=f"${_VAR_NAME}")
    return (
        f"{_HEADER}\n{preamble}\n{result.code}\nputs -nonewline {emit_expr}\n"
    )


def main() -> None:
    """Round-trip the shared document through the Tcl backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    tclsh = shutil.which(cmd="tclsh") or "tclsh"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.tcl",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[tclsh, "main.tcl"],
                failure_label="tclsh runtime error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
