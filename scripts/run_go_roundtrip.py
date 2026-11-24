"""Go JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Go
``myData := ...`` declaration, wrap it in a tiny ``main`` that prints
``json.Marshal(myData)``, run it with ``go run``, and hand the emitted
JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-go`` job in
``.github/workflows/lint.yml``, because that job is where the Go
toolchain is invoked.  It shares the same input and comparison logic as
the other per-language round-trip helpers.

The shared input's ``biginteger`` field is trimmed before
literalization: its 26-digit value overflows ``uint64`` (the widest Go
integer literal type the literalizer emits), so the literalizer raises
:class:`literalizer.exceptions.UnrepresentableIntegerError` rather than
emitting a ``uint64(...)`` conversion the Go compiler would reject.
Every other field round-trips through ``encoding/json`` losslessly
under the parsed-value comparison in :func:`roundtrip_common.verify`.
"""

import json
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

import click

from literalizer.exceptions import HeterogeneousSiblingListsError
from literalizer.languages import Go
from scripts import roundtrip_common

if TYPE_CHECKING:
    from pydantic import JsonValue

_VAR_NAME = "myData"
_LABEL = "Go"
_EXCLUDED_KEYS = ("biginteger",)
_SIBLING_CONSUMER = Path(__file__).with_name(
    name="go_record_sibling_consumer.go"
)

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
    preamble = "\n".join(
        line
        for line in (*result.preamble, *result.body_preamble)
        if line != 'import "math"'
    )
    return (
        f"{preamble}\n"
        "\n"
        "import (\n"
        '\t"encoding/json"\n'
        '\t"fmt"\n'
        '\t"math"\n'
        '\t"os"\n'
        ")\n"
        "\n"
        "func main() {\n"
        f"{result.code}\n"
        f'\tnegativeZero, ok := {_VAR_NAME}["negative_zero"].(float64)\n'
        "\tif !ok || negativeZero != 0 || !math.Signbit(negativeZero) {\n"
        '\t\tpanic("negative_zero lost its sign")\n'
        "\t}\n"
        f"\tout, err := json.Marshal({_VAR_NAME})\n"
        "\tif err != nil {\n"
        "\t\tfmt.Fprintln(os.Stderr, err)\n"
        "\t\tos.Exit(1)\n"
        "\t}\n"
        "\tos.Stdout.Write(out)\n"
        "}\n"
    )


def _check_sibling_permutations(*, go: str) -> None:
    """Check empty and null-only record siblings in both orders."""
    language = Go(heterogeneous_strategy=Go.heterogeneous_strategies.RECORD)
    consumer = _SIBLING_CONSUMER.read_text(encoding="utf-8")
    populated: dict[str, JsonValue] = {"tag": "mixed", "items": [1, "x", True]}
    sparse: tuple[dict[str, JsonValue], ...] = (
        {"tag": "empty", "items": []},
        {"tag": "nulls", "items": [None, None]},
    )
    for empty in sparse:
        for records in ([empty, populated], [populated, empty]):
            result = roundtrip_common.literalize_new_variable(
                language=language,
                json_text=json.dumps(obj=records),
                var_name=_VAR_NAME,
                pre_indent_level=1,
            )
            program = "\n".join(
                (
                    *result.preamble,
                    *result.body_preamble,
                    "func main() {",
                    result.code,
                    f"writeSiblingRecords({_VAR_NAME})",
                    "}",
                )
            )
            roundtrip_common.execute(
                label=f"{_LABEL} record siblings ({records[0]['tag']} first)",
                source_filename="main.go",
                program=program,
                steps=[
                    roundtrip_common.Step(
                        args=[go, "run", "."], failure_label="go run error"
                    ),
                ],
                excluded_keys=(),
                expected_json=json.dumps(obj={"records": records}),
                extra_files={
                    "go.mod": _GO_MOD,
                    _SIBLING_CONSUMER.name: consumer,
                },
            )


def _check_incompatible_siblings() -> None:
    """Retain the error contract for incompatible inferred record shapes."""
    language = Go(heterogeneous_strategy=Go.heterogeneous_strategies.RECORD)
    sparse: dict[str, JsonValue] = {"tag": "empty", "items": []}
    typed: dict[str, JsonValue] = {"tag": "typed", "items": [1, 2]}
    for records in ([sparse, typed], [typed, sparse]):
        try:
            _ = roundtrip_common.literalize_new_variable(
                language=language,
                json_text=json.dumps(obj=records),
                var_name=_VAR_NAME,
                pre_indent_level=1,
            )
        except HeterogeneousSiblingListsError:
            continue
        msg = (
            f"Expected Go RECORD to reject incompatible siblings: {records!r}"
        )
        raise AssertionError(msg)


@click.command()
def main() -> None:
    """Round-trip the shared document through the Go backend."""
    json_text = roundtrip_common.input_for_capabilities(
        capabilities=Go.variant_metadata.round_trip_capabilities,
    )
    program = _build_program(json_text=json_text)
    go = shutil.which(cmd="go")
    if go is None or go == "":
        go = "go"
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
        expected_json=json_text,
        extra_files={"go.mod": _GO_MOD},
    )
    _check_sibling_permutations(go=go)
    _check_incompatible_siblings()


if __name__ == "__main__":
    main()
