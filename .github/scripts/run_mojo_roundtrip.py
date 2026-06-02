r"""Mojo JSON round-trip check (issue #2664).

Literalize the shared ``roundtrip_input.json`` document to a Mojo
``var my_data = {...}`` binding, wrap it in a ``def main() raises:`` whose
body walks ``my_data`` and ``print``s the re-emitted JSON, run that with
``mojo run``, and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Mojo roundtrip`` step of the
``lint-mojo`` job in ``.github/workflows/lint.yml``, because that job is
where the Mojo toolchain is installed; ``uv run`` (project mode) is
required so ``import literalizer`` resolves.  It is deliberately not a
pytest test under ``tests/``.

Mojo ships no standard JSON encoder, so this helper hand-rolls one (the
"language has no standard option" carve-out from the issue's
prefer-a-library rule).  The shared input's top-level object holds scalar
values of several types, so it is literalized with the ``VARIANT``
heterogeneous strategy: the binding is a ``Dict[String, JsonValue]`` where
``comptime JsonValue = Variant[Int, Float64, Bool, String]``.  Each value
is read back from the slot matching its original JSON type --
``[Int]`` for integers, ``[Bool]`` for booleans, ``[Float64]`` for floats
and ``[String]`` for strings.  Knowing each key's JSON type up front (read
from the parsed JSON in Python, same pattern as the C / Forth / Tcl /
SystemVerilog helpers) is what lets booleans round-trip despite Python
treating ``True`` / ``False`` as ``int`` instances.

Integers and booleans print via ``String(...)`` / a ``"true"``/``"false"``
ternary.  Floats print via ``String(Float64)``, whose Mojo shortest
round-trip representation reparses to the same IEEE 754 ``binary64`` value
(the comparison in :func:`roundtrip_common.verify` is on parsed Python
values, and negative zero compares equal to zero there anyway).  Leaf
string escaping is done by the ``json_escape`` helper below, which works
on raw UTF-8 bytes so multi-byte codepoints survive byte-for-byte and only
``"``, ``\`` and control characters are escaped.

The shared input's nested containers and ``biginteger`` are excluded:

* every array / object field (``empty_array`` ... ``nested_object``) --
  the ``VARIANT`` strategy cannot place a container alongside scalars in
  one dict (it raises
  :class:`literalizer.exceptions.MixedDictValuesError`), so the mixed
  top-level object is reduced to its scalar fields.
* ``biginteger`` -- its 26-digit value overflows Mojo's signed 64-bit
  ``Int``, so it cannot be represented losslessly.  Same shape as the
  Go / TypeScript / Zig / C / SystemVerilog exclusions.

Every top-level scalar in the shared input -- signed and wide integers,
booleans, floats (including ``DBL_MAX`` and negative zero), and unicode /
escaped / empty strings -- round-trips losslessly.
"""

import json
import shutil

import roundtrip_common

from literalizer.languages import Mojo

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
_LABEL = "Mojo"
_VARIANT_NAME = "JsonValue"
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

# Static Mojo helpers backing the shape-driven walk: a single hex-digit
# encoder and a JSON string escaper that operates on raw UTF-8 bytes so
# the multi-byte codepoints of ``string_unicode`` pass through unchanged
# (only ``"``, ``\`` and control characters are escaped).
_HELPERS = """def hex_digit(v: Int) -> UInt8:
    if v < 10:
        return UInt8(48 + v)
    return UInt8(87 + v)

def json_escape(t: String) -> String:
    var buf = List[UInt8]()
    buf.append(34)
    for b in t.as_bytes():
        var c = Int(b)
        if c == 34:
            buf.append(92)
            buf.append(34)
        elif c == 92:
            buf.append(92)
            buf.append(92)
        elif c == 8:
            buf.append(92)
            buf.append(98)
        elif c == 9:
            buf.append(92)
            buf.append(116)
        elif c == 10:
            buf.append(92)
            buf.append(110)
        elif c == 12:
            buf.append(92)
            buf.append(102)
        elif c == 13:
            buf.append(92)
            buf.append(114)
        elif c < 32:
            buf.append(92)
            buf.append(117)
            buf.append(48)
            buf.append(48)
            buf.append(hex_digit((c >> 4) & 15))
            buf.append(hex_digit(c & 15))
        else:
            buf.append(b)
    buf.append(34)
    return String(StringSlice(unsafe_from_utf8=Span(buf)))"""


def _mojo_string_literal(text: str) -> str:
    """Return *text* as a double-quoted Mojo string literal."""
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _value_expr(*, value: JsonValue, key: str) -> str:
    """Return a Mojo string expression re-emitting *value* for *key*.

    ``bool`` is checked before ``int`` because Python treats ``True`` /
    ``False`` as ``int`` instances; the boolean reads the ``[Bool]`` slot
    as a ``"true"``/``"false"`` ternary.  Containers and ``None`` never
    reach here -- the former are trimmed via ``_EXCLUDED_KEYS`` and the
    latter is absent from the shared input -- so an unexpected type raises
    rather than emitting wrong code.
    """
    access = f"{_VAR_NAME}[{_mojo_string_literal(text=key)}]"
    if isinstance(value, bool):
        return f'(String("true") if {access}[Bool] else String("false"))'
    if isinstance(value, int):
        return f"String({access}[Int])"
    if isinstance(value, float):
        return f"String({access}[Float64])"
    if isinstance(value, str):
        return f"json_escape({access}[String])"
    message = f"unsupported round-trip value {value!r}"
    raise TypeError(message)


def _build_program(*, json_text: str) -> str:
    """Return a runnable Mojo program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Mojo(
            heterogeneous_strategy=Mojo.heterogeneous_strategies.VARIANT,
            heterogeneous_value_variant_name=_VARIANT_NAME,
        ),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=1,
    )
    parsed: dict[str, JsonValue] = json.loads(s=trimmed_json)
    walk = ['    var out = String("{")']
    for index, (key, value) in enumerate(parsed.items()):
        fragment = ("," if index else "") + json.dumps(obj=key) + ":"
        expr = _value_expr(value=value, key=key)
        walk.append(
            f"    out += {_mojo_string_literal(text=fragment)} + {expr}",
        )
    walk.append('    out += "}"')
    walk.append('    print(out, end="")')
    walk_body = "\n".join(walk)
    preamble = "\n".join(result.preamble)
    return (
        f"{preamble}\n"
        f"{_HELPERS}\n"
        "def main() raises:\n"
        f"{result.code}\n"
        f"{walk_body}\n"
    )


def main() -> None:
    """Round-trip the shared document through the Mojo backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    mojo = shutil.which(cmd="mojo") or "mojo"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.mojo",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[mojo, "run", "--Werror", "main.mojo"],
                failure_label="mojo run error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
