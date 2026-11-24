"""Go cross-file record-declaration check (issues #3748 and #7219).

Literalize both documents in :mod:`scripts.shared_record_common` under
``Go(heterogeneous_strategy=RECORD, record_map_value_typing=WIDE)``,
then compile both sets of slice literals against each document's
``struct`` declarations in turn. The documents contain mixed and
string-only maps, which must both use ``map[string]any``. Each program
emits both documents' native values for comparison with the original JSON.

The ``lint-go`` job in ``.github/workflows/lint.yml`` runs this check.
"""

import shutil

import click

from literalizer import LiteralizeResult
from literalizer.languages import Go
from scripts import roundtrip_common, shared_record_common

_LABEL = "Go shared-record"
_EXPECTED_JSON = (
    f'{{"declaring": {shared_record_common.DECLARING_DOCUMENT},'
    f'"dependent": {shared_record_common.DEPENDENT_DOCUMENT}}}'
)

# ``go 1.18`` matches ``Go.language_version`` in
# ``src/literalizer/languages/go.py`` and the ``go.mod`` written by the
# ``Check Go compilation and run`` step of ``lint-go``; keep them in
# sync.
_GO_MOD = "module fixture\n\ngo 1.18\n"


def _build_program(
    *,
    declarations_from: LiteralizeResult,
    declaring: LiteralizeResult,
    dependent: LiteralizeResult,
) -> str:
    """Build a runnable Go program with just the selected preamble."""
    package_clause, *declarations = (
        *declarations_from.preamble,
        *declarations_from.body_preamble,
    )
    declared = "\n".join(declarations)
    return (
        f"{package_clause}\n"
        "\n"
        "import (\n"
        '\t"encoding/json"\n'
        '\t"os"\n'
        ")\n"
        "\n"
        f"{declared}\n"
        "\n"
        "func main() {\n"
        f"{declaring.code}\n"
        f"{dependent.code}\n"
        "\trecords := map[string][]Record0{\n"
        f'\t\t"declaring": {shared_record_common.DECLARING_VAR_NAME_CAMEL},\n'
        f'\t\t"dependent": {shared_record_common.DEPENDENT_VAR_NAME_CAMEL},\n'
        "\t}\n"
        "\tdocuments := make(map[string][]map[string]any, len(records))\n"
        "\tfor document, rows := range records {\n"
        "\t\tvalues := make([]map[string]any, 0, len(rows))\n"
        "\t\tfor _, row := range rows {\n"
        "\t\t\tvalues = append(values, map[string]any{\n"
        '\t\t\t\t"name": row.Name,\n'
        '\t\t\t\t"attributes": row.Attributes,\n'
        "\t\t\t})\n"
        "\t\t}\n"
        "\t\tdocuments[document] = values\n"
        "\t}\n"
        "\tencoder := json.NewEncoder(os.Stdout)\n"
        "\tif err := encoder.Encode(documents); err != nil {\n"
        "\t\tpanic(err)\n"
        "\t}\n"
        "}\n"
    )


@click.command()
def main() -> None:
    """Check both documents in each declaration order."""
    language = Go(
        heterogeneous_strategy=Go.heterogeneous_strategies.RECORD,
        record_map_value_typing=Go.record_map_value_typings.WIDE,
    )
    declaring = roundtrip_common.literalize_new_variable(
        language=language,
        json_text=shared_record_common.DECLARING_DOCUMENT,
        var_name=shared_record_common.DECLARING_VAR_NAME_CAMEL,
        pre_indent_level=1,
    )
    dependent = roundtrip_common.literalize_new_variable(
        language=language,
        json_text=shared_record_common.DEPENDENT_DOCUMENT,
        var_name=shared_record_common.DEPENDENT_VAR_NAME_CAMEL,
        pre_indent_level=1,
    )
    go = shutil.which(cmd="go")
    if go is None or go == "":
        go = "go"
    steps = [
        roundtrip_common.Step(
            args=[go, "vet", "./..."],
            failure_label="go vet error",
        ),
        roundtrip_common.Step(
            args=[go, "run", "./..."],
            failure_label="go run error",
        ),
    ]
    for declaration_label, declarations_from in (
        ("mixed-map declaration", declaring),
        ("string-only declaration", dependent),
    ):
        roundtrip_common.execute(
            label=f"{_LABEL} ({declaration_label})",
            source_filename="main.go",
            program=_build_program(
                declarations_from=declarations_from,
                declaring=declaring,
                dependent=dependent,
            ),
            steps=steps,
            excluded_keys=(),
            expected_json=_EXPECTED_JSON,
            extra_files={"go.mod": _GO_MOD},
        )


if __name__ == "__main__":
    main()
