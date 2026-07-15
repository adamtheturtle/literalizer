"""SystemVerilog JSON round-trip check (issue #2679).

Literalize the shared ``roundtrip_input.json`` document to a
SystemVerilog ``static _VKV my_data[] = '{...};`` binding, wrap it in a
tiny ``module main`` whose ``initial`` block walks ``my_data`` and
``$write``s the re-emitted JSON, build that with ``verilator --binary``,
run the simulation, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by the ``SystemVerilog roundtrip`` step of the
``lint-systemverilog`` job in ``.github/workflows/lint.yml``, because
that job is where Verilator is installed; ``uv run`` (project mode) is
required so ``import literalizer`` resolves.  It is deliberately not a
pytest test under ``tests/``.

SystemVerilog ships no standard JSON encoder, so this helper hand-rolls
one (the "language has no standard option" carve-out from the issue's
prefer-a-library rule).  The literalizer's ``_VVal`` is a *flat* tagged
record -- ``_VVAL_INT`` / ``_VVAL_REAL`` / ``_VVAL_STR`` over a
``longint``, a ``real`` and a ``string`` -- with no recursive component:
nested arrays and objects are serialized to an *opaque string* holding
their SystemVerilog literal text (see ``_format_sv_entry`` /
``_escape_nested`` in ``src/literalizer/languages/systemverilog.py``),
and there is no boolean tag (``true`` / ``false`` share the ``_VVAL_INT``
slot with ``1`` / ``0``).  So the runtime value carries no way to walk
back into a container or to tell a boolean from an integer.

The serializer therefore reads the *shape* of the document from the
parsed JSON in Python (same pattern as the C / Forth / Tcl helpers) and
emits, per top-level key, one expression that reads the ``_VVal`` slot
matching the original JSON type -- ``.i`` for integers, a ``? "true" :
"false"`` test on ``.i`` for booleans, ``.r`` for reals, and a
``json_escape(.s)`` call for strings.  Knowing each key's JSON type up
front is what lets booleans round-trip despite sharing the integer slot.
Leaf string escaping is done by the ``json_escape`` helper below; reals
are printed with ``%.17g``, which emits 17 significant decimal digits and
so reparses to the same IEEE 754 ``binary64`` value (the comparison in
``roundtrip_common.verify`` is on parsed Python values).

The shared input's nested containers and ``biginteger`` are excluded:

* every array / object field (``empty_array`` ... ``nested_object``) --
  the backend stores a nested container as the opaque string described
  above, so its elements are unreachable as ``_VVal`` fields at run time;
  re-emitting them would require parsing SystemVerilog literal syntax
  inside the simulation.  Excluded rather than parsed.
* ``biginteger`` -- its 26-digit value overflows the ``longint`` (signed
  64-bit) ``i`` slot, so the literalizer raises
  :class:`literalizer.exceptions.UnrepresentableIntegerError` before any
  source is produced.  Same shape as the Go / TypeScript / Zig / C
  exclusions.

Every top-level scalar in the shared input -- signed and wide integers,
booleans, reals (including ``DBL_MAX`` and negative zero), and unicode /
escaped / empty strings -- round-trips losslessly.
"""

import json
import shutil

import roundtrip_common

from literalizer.languages import SystemVerilog

# ``json.loads`` returns this recursive shape; typing the value helper
# against it lets ``isinstance`` narrow cleanly under the type checkers.
type JsonValue = (
    None
    | bool
    | int
    | float
    | str
    | list["JsonValue"]
    | dict[str, "JsonValue"]
)

_VAR_NAME = "my_data"
_LABEL = "SystemVerilog"
_EXCLUDED_KEYS = (
    "biginteger",
    "empty_array",
    "int_array",
    "double_array",
    "bool_array",
    "mixed_array",
    "nested_array",
    "empty_object",
    "flat_object",
    "nested_object",
)

# Static SystemVerilog helpers backing the shape-driven walk: a real
# formatter (17 significant digits round-trip every binary64 value) and a
# JSON string escaper that passes bytes >= 0x20 through unchanged so the
# UTF-8 of ``string_unicode`` survives byte-for-byte.
_HELPERS = r"""  function automatic string format_real(input real x);
    return $sformatf("%.17g", x);
  endfunction
  function automatic string json_escape(input string t);
    string out;
    int unsigned c;
    out = "\"";
    for (int i = 0; i < t.len(); i++) begin
      c = int'(t.getc(i)) & 32'hFF;
      case (c)
        34: out = {out, "\\\""};
        92: out = {out, "\\\\"};
        8:  out = {out, "\\b"};
        9:  out = {out, "\\t"};
        10: out = {out, "\\n"};
        12: out = {out, "\\f"};
        13: out = {out, "\\r"};
        default: begin
          if (c < 32) out = {out, $sformatf("\\u%04x", c)};
          else out = {out, t.substr(i, i)};
        end
      endcase
    end
    out = {out, "\""};
    return out;
  endfunction"""


def _sv_string_literal(text: str) -> str:
    """Return *text* as a double-quoted SystemVerilog string literal."""
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _value_expr(*, value: JsonValue, access: str) -> str:
    """Return a SystemVerilog string expression re-emitting *value*.

    *access* is the ``_VVal`` slot expression (e.g. ``my_data[0].v``).
    ``bool`` is checked before ``int`` because Python treats ``True`` /
    ``False`` as ``int`` instances and both share the ``_VVAL_INT`` ``.i``
    slot; the boolean reads it as a truthiness test.  Containers and
    ``None`` never reach here -- the former are trimmed via
    ``_EXCLUDED_KEYS`` and the latter is absent from the shared input --
    so an unexpected type raises rather than emitting wrong code.
    """
    if isinstance(value, bool):
        return f'(({access}.i != 0) ? "true" : "false")'
    if isinstance(value, int):
        return f'$sformatf("%0d", {access}.i)'
    if isinstance(value, float):
        return f"format_real({access}.r)"
    if isinstance(value, str):
        return f"json_escape({access}.s)"
    message = f"unsupported round-trip value {value!r}"
    raise TypeError(message)


def _build_program(*, json_text: str) -> str:
    """Return a runnable SystemVerilog program literalized from
    *json_text*.
    """
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=SystemVerilog(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=2,
    )
    parsed: dict[str, JsonValue] = json.loads(s=trimmed_json)
    walk = ['        out = "{";']
    for index, (key, value) in enumerate(iterable=parsed.items()):
        fragment = ("," if index else "") + json.dumps(obj=key) + ":"
        expr = _value_expr(value=value, access=f"{_VAR_NAME}[{index}].v")
        walk.append(
            f"        out = {{out, {_sv_string_literal(text=fragment)}, "
            f"{expr}}};",
        )
    walk.append('        out = {out, "}"};')
    walk_body = "\n".join(walk)
    preamble = "\n".join(result.preamble)
    # No ``$finish``; with ``+verilator+quiet`` at run time the
    # simulation ends after the single ``initial`` block with nothing but
    # the JSON on stdout (``$finish`` would print a location line there).
    return (
        f"{preamble}\n"
        "module main;\n"
        f"{_HELPERS}\n"
        "  initial begin\n"
        f"{result.code}\n"
        "        string out;\n"
        f"{walk_body}\n"
        '    $write("%s", out);\n'
        "  end\n"
        "endmodule\n"
    )


def main() -> None:
    """Round-trip the shared document through the SystemVerilog
    backend.
    """
    program = _build_program(json_text=roundtrip_common.read_input())
    verilator = shutil.which(cmd="verilator") or "verilator"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.sv",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[
                    verilator,
                    "--binary",
                    "--quiet",
                    "-Wno-REALCVT",
                    "main.sv",
                    "-o",
                    "sim",
                ],
                failure_label="verilator error",
            ),
            roundtrip_common.Step(
                args=["obj_dir/sim", "+verilator+quiet"],
                failure_label="simulation error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
