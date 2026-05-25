"""Go JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Go
``myData := ...`` declaration, wrap it in a tiny ``main`` that prints
``json.Marshal(myData)``, run it with ``go run``, and hand the emitted
JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-go`` job in
``.github/workflows/lint.yml``, because that job is where the Go
toolchain is invoked.  It shares the same input and comparison logic as
the other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value overflows ``uint64`` (the widest Go integer literal
type the literalizer emits), so the program would not compile if the
field were kept.  Every other field round-trips through ``encoding/json``
losslessly under the parsed-value comparison in
:func:`roundtrip_common.verify`.
"""

import shutil

import roundtrip_common

from literalizer.languages import Go

_VAR_NAME = "myData"
_LABEL = "Go"
_EXCLUDED_KEYS = ("biginteger",)

# ``go 1.18`` matches ``Go.language_version`` in
# ``src/literalizer/languages/go.py`` and the ``go.mod`` written by the
# ``Check Go compilation and run`` step of ``lint-go``; keep them in
# sync.
_GO_MOD = "module fixture\n\ngo 1.18\n"


def _build_program(json_text: str) -> str:
    """Return a runnable Go program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Go(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=1,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        f"{preamble}\n"
        "\n"
        "import (\n"
        '\t"encoding/json"\n'
        '\t"fmt"\n'
        '\t"os"\n'
        ")\n"
        "\n"
        "func main() {\n"
        f"{result.code}\n"
        f"\tout, err := json.Marshal({_VAR_NAME})\n"
        "\tif err != nil {\n"
        "\t\tfmt.Fprintln(os.Stderr, err)\n"
        "\t\tos.Exit(1)\n"
        "\t}\n"
        "\tos.Stdout.Write(out)\n"
        "}\n"
    )


def main() -> None:
    """Round-trip the shared document through the Go backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    go = shutil.which(cmd="go") or "go"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.go",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[go, "run", "."],
                failure_label="go run error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
        extra_files={"go.mod": _GO_MOD},
    )


if __name__ == "__main__":
    main()
