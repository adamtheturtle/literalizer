"""Wren JSON round-trip check (issue #2683).

Literalize the shared ``roundtrip_input.json`` document to a Wren
``var myData = ...`` declaration, wrap it in a script that re-emits JSON
on standard output through a small in-program encoder, run it under
``wren_cli``, and hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Wren roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job is
where the ``wren_cli`` binary (pinned by the ``Install Wren CLI`` step)
is installed.  It shares the same input and comparison logic as the
other per-language round-trip helpers.

Wren ships no standard-library JSON encoder, so this script hand-rolls
one in Wren itself.  Wren is dynamically typed (``value is Num`` /
``is String`` / ``is List`` / ``is Map``), so a generic walker over the
literalized ``myData`` can produce JSON directly without needing the
Python side to know the document's shape, unlike the Tcl helper which
must drive ``tcllib``'s typed constructors along the parsed shape.

Two top-level keys are excluded from the comparison:

* ``biginteger`` -- Wren has a single ``Num`` numeric type backed by a
  64-bit double, so the 26-digit literal is parsed as the nearest double
  and ``Num.toString`` re-emits it as ``1e+26``; same shape as the Go,
  TypeScript, Lua, Zig, Swift, Rust, D, and C++ exclusions.
* ``float_large_exponent`` -- ``Num.toString`` uses ``%.14g``, which
  rounds ``1.7976931348623157e+308`` to ``1.7976931348623e+308`` and
  loses the trailing significant digits; same shape as the Lua
  exclusion.
"""

import json
import shutil
from collections.abc import Iterable

from literalizer.languages import Wren
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "Wren"

# ``Num.toString`` renders through ``%.14g``, so a number needing more
# than fourteen significant digits comes back rounded.  The keys that
# carry one are computed from the document rather than listed, so a
# corpus that grows a wide number excludes it instead of failing
# (issue #4545).
_WREN_SIGNIFICANT_DIGITS = 14

type _JsonValue = (
    str | int | float | bool | list[_JsonValue] | dict[str, _JsonValue] | None
)


def _survives_wren_num(*, value: _JsonValue) -> bool:
    """Return whether ``Num`` holds and re-prints *value* exactly."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return True
    as_double = float(value)
    if as_double != value:
        return False
    rendered = f"{as_double:.{_WREN_SIGNIFICANT_DIGITS}g}"
    return float(rendered) == as_double


def _all_numbers(*, value: _JsonValue) -> Iterable[_JsonValue]:
    """Yield every number reachable from *value*."""
    match value:
        case dict():
            for item in value.values():
                yield from _all_numbers(value=item)
        case list():
            for item in value:
                yield from _all_numbers(value=item)
        case _:
            yield value


def _excluded_keys(*, json_text: str) -> tuple[str, ...]:
    """Return the top-level keys holding a number ``Num`` cannot keep."""
    document: dict[str, _JsonValue] = json.loads(s=json_text)
    return tuple(
        key
        for key, value in document.items()
        if not all(
            _survives_wren_num(value=number)
            for number in _all_numbers(value=value)
        )
    )


# Walks ``myData`` and emits JSON to standard output.  Lives at module
# scope (rather than inside ``main``) because Wren's ``import`` cannot
# resolve sibling files inside the per-run tmpdir, so the encoder must
# be prepended to the same source file as the literalized data.
_ENCODER = """\
class JsonEnc {
    static encode(value) {
        if (value == null) return "null"
        if (value is Bool) return value ? "true" : "false"
        if (value is Num) return value.toString
        if (value is String) return JsonEnc.encodeString(value)
        if (value is List) {
            var parts = []
            for (item in value) parts.add(JsonEnc.encode(item))
            return "[" + parts.join(",") + "]"
        }
        if (value is Map) {
            var parts = []
            for (key in value.keys) {
                var entry = JsonEnc.encodeString(key) + ":"
                parts.add(entry + JsonEnc.encode(value[key]))
            }
            return "{" + parts.join(",") + "}"
        }
        Fiber.abort("unsupported type")
    }

    static encodeString(s) {
        var out = "\\""
        for (c in s) {
            if (c == "\\"") {
                out = out + "\\\\\\""
            } else if (c == "\\\\") {
                out = out + "\\\\\\\\"
            } else if (c == "\\n") {
                out = out + "\\\\n"
            } else if (c == "\\r") {
                out = out + "\\\\r"
            } else if (c == "\\t") {
                out = out + "\\\\t"
            } else {
                out = out + c
            }
        }
        return out + "\\""
    }
}
"""


def _build_program(json_text: str) -> str:
    """Return a runnable Wren program literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Wren(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        f"{_ENCODER}\n"
        f"{preamble}\n"
        f"{result.code}\n"
        f"System.write(JsonEnc.encode({_VAR_NAME}))\n"
    )


def main() -> None:
    """Round-trip the shared document through the Wren backend."""
    json_text = roundtrip_common.input_for_capabilities(
        capabilities=Wren.variant_metadata.round_trip_capabilities,
    )
    excluded_keys = _excluded_keys(json_text=json_text)
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=excluded_keys,
    )
    program = _build_program(json_text=trimmed_json)
    wren = shutil.which(cmd="wren_cli") or "wren_cli"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.wren",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[wren, "main.wren"],
                failure_label="wren_cli runtime error",
            ),
        ],
        excluded_keys=excluded_keys,
        expected_json=json_text,
        extra_files=None,
    )


if __name__ == "__main__":
    main()
