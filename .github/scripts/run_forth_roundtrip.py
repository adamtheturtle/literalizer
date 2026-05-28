"""Forth JSON round-trip check (issue #2651).

Literalize the shared ``roundtrip_input.json`` document to a Forth
``: myData ... ;`` colon definition, wrap it in a ``gforth`` script that
re-emits JSON on standard output through the Forth Foundation Library
(FFL) ``jos`` JSON-output-stream module, run it under ``gforth``, and
hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Forth roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job is
where the ``gforth`` apt package (pinned by the ``Install apt packages``
step) and the FFL checkout (pinned by the ``Install FFL`` step that
sets ``LITERALIZER_FFL_PATH``) are provisioned.  It shares the same
input and comparison logic as the other per-language round-trip
helpers.

Forth ships no JSON serializer in its standard library, but FFL's
``jos`` module provides a typed JSON-output-stream API (``jos-write-
number`` / ``-float`` / ``-string`` / ``-boolean``, plus
``jos-write-start-object`` / ``-end-object`` / ``-start-array`` /
``-end-array``) and is the canonical general-purpose gforth library.
It handles JSON string escapes and float formatting, so this script
delegates all leaf formatting to ``jos``.

The Forth backend's sequence/dict openers and closers are empty, so
the literalized ``: myData ... ;`` simply pushes every scalar onto the
data and FP stacks with no run-time structure left.  To round-trip the
values, the Python side walks the *known* JSON shape (like the Tcl
helper, which must also drive its typed JSON constructors along the
parsed shape) and emits:

* one ``2variable`` / ``variable`` / ``fvariable`` per scalar, in
  document order;
* a ``pop-all`` colon definition that pops values back off the stacks
  in *reverse* order into those variables (LIFO ordering); and
* an ``emit-all`` colon definition that walks the shape forward,
  reading the stored values and driving the ``jos`` output stream.

Two top-level keys are excluded from the comparison:

* ``biginteger`` -- its 26-digit value overflows the 64-bit cell that
  ``gforth`` uses on the Ubuntu runner; same shape as the Go, TypeScript,
  Lua, Zig, Swift, Rust, D, C++, and Wren exclusions.
* ``float_large_exponent`` -- ``Forth.float_format`` is
  ``format_float_scientific``, which uses Python's ``f"{value:e}"``
  (six fractional digits) and emits ``1.797693e308``, losing the
  trailing significant digits of ``1.7976931348623157e+308``; the
  truncation happens at literalize time before the Forth toolchain
  ever sees the value, so the field is excluded from the round-trip.
"""

import json
import os
import shutil
from dataclasses import dataclass

import roundtrip_common

from literalizer.languages import Forth

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
_LABEL = "Forth"
_EXCLUDED_KEYS = ("biginteger", "float_large_exponent")

# Header template for the generated gforth program.  ``fpath+`` adds
# the FFL checkout to gforth's source-search path so the bare
# ``include ffl/jos.fs`` resolves; the path is filled in from the
# ``LITERALIZER_FFL_PATH`` environment variable that the
# ``Install FFL`` step in ``.github/workflows/lint.yml`` exports.
# ``17 set-precision`` is the maximum precision that FFL's
# ``tos-write-float`` honors (``precision 80 min`` in ``tos.fs``) and
# is enough to round-trip every IEEE-754 double through the emitted
# ``[-]0.dddddddddddddddddE[-]N`` form.
_HEADER_TEMPLATE = """\
fpath+ {ffl_path}
include ffl/jos.fs
17 set-precision
jos-create json-out
"""

_FOOTER = f"""\
{_VAR_NAME} pop-all emit-all
json-out str-get type bye
"""


@dataclass(frozen=True)
class _Slot:
    r"""One literalized scalar pulled back off the Forth stacks.

    *name* is the Forth variable name (``v0``, ``v1``, ...).  *kind*
    selects the Forth storage word: ``"cell"`` for ints/bools (``!``),
    ``"string"`` for ``s\" ..."`` literals stored as addr+len
    (``2!``), or ``"float"`` for FP-stack values (``f!``).
    """

    name: str
    kind: str


def _store_op(slot: _Slot) -> str:
    """Return the Forth pop-and-store operation for *slot*."""
    match slot.kind:
        case "string":
            return f"{slot.name} 2!"
        case "float":
            return f"{slot.name} f!"
        case "cell":
            return f"{slot.name} !"
        case _:
            raise ValueError(slot.kind)


def _declaration(slot: _Slot) -> str:
    """Return the Forth top-level declaration for *slot*."""
    match slot.kind:
        case "string":
            return f"2variable {slot.name}"
        case "float":
            return f"fvariable {slot.name}"
        case "cell":
            return f"variable {slot.name}"
        case _:
            raise ValueError(slot.kind)


def _scalar_kind_and_emit(
    *,
    value: bool | float | str,
) -> tuple[str, str]:
    """Return the ``(kind, emit)`` pair for a JSON scalar.

    ``bool`` must be checked before ``int``: Python treats ``True`` /
    ``False`` as ``int`` instances.  Booleans share the ``cell`` kind
    (storage word ``!``) with ints but call ``jos-write-boolean``
    rather than ``jos-write-number``.
    """
    if isinstance(value, bool):
        return ("cell", "@ json-out jos-write-boolean")
    if isinstance(value, int):
        return ("cell", "@ json-out jos-write-number")
    if isinstance(value, float):
        return ("float", "f@ json-out jos-write-float")
    return ("string", "2@ json-out jos-write-string")


def _add_scalar(
    *,
    value: bool | float | str,
    slots: list[_Slot],
    emit_lines: list[str],
) -> None:
    """Append a fresh scalar slot and its emit line for *value*."""
    name = f"v{len(slots)}"
    kind, emit = _scalar_kind_and_emit(value=value)
    slots.append(_Slot(name=name, kind=kind))
    emit_lines.append(f"    {name} {emit}")


def _walk(
    *,
    value: JsonValue,
    slots: list[_Slot],
    emit_lines: list[str],
) -> None:
    """Append slots and emit lines for *value* in document order.

    Each scalar leaf gets one fresh ``v{N}`` slot whose value is read
    via ``@`` / ``2@`` / ``f@`` and handed to the matching
    ``jos-write-*`` word.  Container nodes recurse and add the
    surrounding ``jos-write-start-array`` / ``-end-array`` (and
    object equivalents).  Keys are stored as string slots so the
    literalized order matches the document order.
    """
    if isinstance(value, list):
        emit_lines.append("    json-out jos-write-start-array")
        for item in value:
            _walk(value=item, slots=slots, emit_lines=emit_lines)
        emit_lines.append("    json-out jos-write-end-array")
        return
    if isinstance(value, dict):
        emit_lines.append("    json-out jos-write-start-object")
        for sub in value.values():
            key_name = f"v{len(slots)}"
            slots.append(_Slot(name=key_name, kind="string"))
            emit_lines.append(f"    {key_name} 2@ json-out jos-write-name")
            _walk(value=sub, slots=slots, emit_lines=emit_lines)
        emit_lines.append("    json-out jos-write-end-object")
        return
    # `roundtrip_input.json` is deliberately null-free (the shared
    # input documents this), so a scalar leaf must be one of the four
    # types handled by `_add_scalar`.
    if value is None:
        message = "unsupported JSON null in round-trip input"
        raise TypeError(message)
    _add_scalar(value=value, slots=slots, emit_lines=emit_lines)


def _shape_program(*, parsed: JsonValue, slots: list[_Slot]) -> str:
    """Return the Forth program fragment that walks *parsed*.

    Produces the variable declarations, the ``pop-all`` colon
    definition (pops in reverse-document order, matching the LIFO
    stacks), and the ``emit-all`` colon definition (walks the shape
    forward, driving the FFL ``jos`` stream).
    """
    emit_lines: list[str] = []
    _walk(value=parsed, slots=slots, emit_lines=emit_lines)
    declarations = "\n".join(_declaration(slot=slot) for slot in slots)
    pops = "\n".join(f"    {_store_op(slot=slot)}" for slot in reversed(slots))
    emit_body = "\n".join(emit_lines)
    return (
        f"{declarations}\n\n"
        f": pop-all\n{pops}\n;\n\n"
        f": emit-all\n{emit_body}\n;\n"
    )


def _build_program(*, json_text: str, ffl_path: str) -> str:
    """Return a runnable gforth script literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Forth(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    parsed: JsonValue = json.loads(s=trimmed_json)
    slots: list[_Slot] = []
    shape = _shape_program(parsed=parsed, slots=slots)
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    header = _HEADER_TEMPLATE.format(ffl_path=ffl_path)
    return f"{header}\n{preamble}\n{result.code}\n\n{shape}\n{_FOOTER}"


def main() -> None:
    """Round-trip the shared document through the Forth backend."""
    # ``LITERALIZER_FFL_PATH`` points at the FFL checkout (the
    # ``Install FFL`` step in ``.github/workflows/lint.yml`` exports
    # it); the generated program prepends that to gforth's source
    # search path via ``fpath+`` so the bare ``include ffl/jos.fs``
    # resolves there.
    ffl_path = os.environ["LITERALIZER_FFL_PATH"]
    program = _build_program(
        json_text=roundtrip_common.read_input(),
        ffl_path=ffl_path,
    )
    gforth = shutil.which(cmd="gforth") or "gforth"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.fth",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[gforth, "main.fth"],
                failure_label="gforth runtime error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
