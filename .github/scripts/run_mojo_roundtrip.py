"""Mojo JSON round-trip check (issue #2664).

Literalize the shared ``roundtrip_input.json`` document to a Mojo
``var my_data = {...}`` binding, wrap it in a ``def main() raises:`` that
copies each value into a CPython ``dict`` and ``print``s
``json.dumps(...)`` of it, run that with ``mojo run``, and hand the
emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Mojo roundtrip`` step of the
``lint-mojo`` job in ``.github/workflows/lint.yml``, because that job is
where the Mojo toolchain is installed.  It is deliberately not a pytest
test under ``tests/``.

``uv run`` (project mode, not ``--no-project``) is load-bearing twice
over: it makes ``import literalizer`` resolve here, *and* it puts uv's
managed CPython on ``PATH`` so Mojo's ``std.python`` interop bridges to a
``libpython`` that is guaranteed present on the runner (the same uv that
runs this script supplies the Python it talks to).

Mojo ships no JSON encoder in its own standard library, but it is built
around Python interop, so the idiomatic "standard option" is to borrow
CPython's :mod:`json` via ``Python.import_module("json")`` -- preferred
over a hand-rolled serializer per the issue.  String escaping, unicode
and number formatting are therefore CPython's; this helper only has to
move each value out of Mojo into a ``Python.dict()``.

The shared input's top-level object holds scalar values of several types,
so it is literalized with the ``VARIANT`` heterogeneous strategy: the
binding is a ``Dict[String, JsonValue]`` where
``comptime JsonValue = Variant[Int, Float64, Bool, String]``.  Mojo
cannot reflect over a ``Variant`` generically, so each value is read from
the slot matching its original JSON type -- ``[Int]`` for integers,
``[Bool]`` for booleans, ``[Float64]`` for floats and ``[String]`` for
strings.  Knowing each key's JSON type up front (read from the parsed
JSON in Python, same pattern as the C / Forth / Tcl / SystemVerilog
helpers) is what lets booleans round-trip despite Python treating
``True`` / ``False`` as ``int`` instances: assigning the ``[Bool]`` slot
into the CPython dict yields a Python ``bool`` that ``json.dumps`` emits
as ``true`` / ``false``.

The shared input's nested containers and ``biginteger`` are excluded:

* every array / object field (``empty_array`` ... ``nested_object``) --
  the ``VARIANT`` strategy cannot place a container alongside scalars in
  one dict (it raises
  :class:`literalizer.exceptions.MixedDictValuesError`), so the mixed
  top-level object is reduced to its scalar fields.  This is a limit of
  the Mojo backend, not of the serializer.
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


def _mojo_string_literal(text: str) -> str:
    """Return *text* as a double-quoted Mojo string literal."""
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _variant_slot(*, value: JsonValue) -> str:
    """Return the ``Variant`` slot type for *value*'s JSON type.

    ``bool`` is checked before ``int`` because Python treats ``True`` /
    ``False`` as ``int`` instances; reading the ``[Bool]`` slot keeps the
    value a Mojo ``Bool`` so it crosses into CPython as a ``bool``.
    Containers and ``None`` never reach here -- the former are trimmed via
    ``_EXCLUDED_KEYS`` and the latter is absent from the shared input --
    so an unexpected type raises rather than emitting wrong code.
    """
    if isinstance(value, bool):
        return "Bool"
    if isinstance(value, int):
        return "Int"
    if isinstance(value, float):
        return "Float64"
    if isinstance(value, str):
        return "String"
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
    walk = [
        '    var json = Python.import_module("json")',
        "    var out = Python.dict()",
    ]
    for key, value in parsed.items():
        key_literal = _mojo_string_literal(text=key)
        slot = _variant_slot(value=value)
        walk.append(
            f"    out[{key_literal}] = {_VAR_NAME}[{key_literal}][{slot}]",
        )
    walk.append('    print(json.dumps(out), end="")')
    walk_body = "\n".join(walk)
    preamble = "\n".join(result.preamble)
    return (
        "from std.python import Python\n"
        f"{preamble}\n"
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
