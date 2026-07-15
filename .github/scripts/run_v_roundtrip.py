"""V JSON round-trip check (issue #2681).

Literalize the shared ``roundtrip_input.json`` document to a V
``my_data := { ... }`` ``map[string]IVal`` binding (under the
``INTERFACE`` heterogeneous strategy so the mixed-type fields compile),
wrap it in a tiny ``main`` that walks the literalized value into a
``map[string]x.json2.Any`` and prints it via ``json2.encode``, run it
with ``v -cc gcc run``, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-v`` job in
``.github/workflows/lint.yml``, because that job is where the V
toolchain is installed.  It shares the same input and comparison logic
as the other per-language round-trip helpers.

The shared input is trimmed to the subset the V backend can type safely.
Its 26-digit ``biginteger`` overflows ``u64`` (the widest unsigned
integer the backend emits).  The other excluded fields combine empty or
differently typed collections, or mix bool and int interface members;
V's default compiler backend cannot lower those shapes reliably.  The
remaining document still covers signed and wide integers, floats,
strings, and a homogeneous array.
"""

import shutil

import roundtrip_common

from literalizer.languages import V

_VAR_NAME = "my_data"
_LABEL = "V"
_EXCLUDED_KEYS = (
    "biginteger",
    "bool_true",
    "bool_false",
    "empty_array",
    "double_array",
    "bool_array",
    "mixed_array",
    "nested_array",
    "empty_object",
    "flat_object",
    "nested_object",
)

# Walk the literalized ``IVal``-wrapped value into a ``json2.Any`` tree
# so ``json2.encode`` can re-emit it.  ``IVal`` is the empty interface
# the ``INTERFACE`` strategy declares for V; the concrete payload is one
# of the listed scalar / collection types.  ``json2.Any`` is a sumtype
# with members for every scalar and a recursive ``[]Any`` /
# ``map[string]Any``, so the conversion is one type-test per concrete
# type the literalized literal can carry.  Homogeneous arrays of
# non-``IVal`` element types (``[]int`` / ``[]f64`` / ``[]bool``) and
# the all-``bool`` ``map[string]bool`` inner object reach this function
# unwrapped, so they need their own arms.
_TO_ANY = """
fn to_any(v IVal) json2.Any {
\tif v is int {
\t\treturn json2.Any(v)
\t}
\tif v is i64 {
\t\treturn json2.Any(v)
\t}
\tif v is f64 {
\t\treturn json2.Any(v)
\t}
\tif v is bool {
\t\treturn json2.Any(v)
\t}
\tif v is string {
\t\treturn json2.Any(v)
\t}
\tif v is []IVal {
\t\tmut arr := []json2.Any{}
\t\tfor item in v {
\t\t\tarr << to_any(item)
\t\t}
\t\treturn json2.Any(arr)
\t}
\tif v is []int {
\t\tmut arr := []json2.Any{}
\t\tfor item in v {
\t\t\tarr << json2.Any(item)
\t\t}
\t\treturn json2.Any(arr)
\t}
\tif v is []f64 {
\t\tmut arr := []json2.Any{}
\t\tfor item in v {
\t\t\tarr << json2.Any(item)
\t\t}
\t\treturn json2.Any(arr)
\t}
\tif v is []bool {
\t\tmut arr := []json2.Any{}
\t\tfor item in v {
\t\t\tarr << json2.Any(item)
\t\t}
\t\treturn json2.Any(arr)
\t}
\tif v is map[string]IVal {
\t\tmut m := map[string]json2.Any{}
\t\tfor k, item in v {
\t\t\tm[k] = to_any(item)
\t\t}
\t\treturn json2.Any(m)
\t}
\tif v is map[string]bool {
\t\tmut m := map[string]json2.Any{}
\t\tfor k, item in v {
\t\t\tm[k] = json2.Any(item)
\t\t}
\t\treturn json2.Any(m)
\t}
\treturn json2.Any(json2.null)
}
"""


def _build_program(json_text: str) -> str:
    """Return a runnable V program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    # pyright cannot resolve the nested ``HeterogeneousStrategies`` enum
    # through V's metaclass (it widens the attribute to ``type[Enum]``),
    # so the lookup needs an explicit suppression.
    language = V(
        heterogeneous_strategy=V.HeterogeneousStrategies.INTERFACE,  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType, reportAttributeAccessIssue]
    )
    result = roundtrip_common.literalize_new_variable(
        language=language,
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=1,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        "import x.json2\n"
        f"{preamble}\n"
        f"{_TO_ANY}"
        "\n"
        "fn main() {\n"
        f"{result.code}\n"
        f"\tprint(json2.encode(to_any({_VAR_NAME})))\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the V backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    v = shutil.which(cmd="v") or "v"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.v",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[v, "-gc", "none", "-cc", "gcc", "run", "main.v"],
                failure_label="v run error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
