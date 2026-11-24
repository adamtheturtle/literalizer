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
from pathlib import Path

import click

from literalizer import LiteralizeResult
from literalizer.languages import Go
from scripts import roundtrip_common, shared_record_common

_LABEL = "Go shared-record"
_CONSUMER_PATH = Path(__file__).with_name(name="go_shared_record.go")
_EXPECTED_JSON = (
    f'{{"declaring": {shared_record_common.DECLARING_DOCUMENT},'
    f'"dependent": {shared_record_common.DEPENDENT_DOCUMENT}}}'
)

# ``go 1.18`` matches ``Go.language_version`` in
# ``src/literalizer/languages/go.py`` and the ``go.mod`` written by the
# ``Check Go compilation and run`` step of ``lint-go``; keep them in
# sync.
_GO_MOD = "module fixture\n\ngo 1.18\n"


def _build_data_source(
    *,
    declarations_from: LiteralizeResult,
    declaring: LiteralizeResult,
    dependent: LiteralizeResult,
) -> str:
    """Put both bindings in the package with the selected declarations."""
    return "\n".join(
        (
            *declarations_from.preamble,
            *declarations_from.body_preamble,
            declaring.code,
            dependent.code,
        )
    )


@click.command()
def main() -> None:
    """Check both documents in each declaration order."""
    language = Go(
        heterogeneous_strategy=Go.heterogeneous_strategies.RECORD,
        record_map_value_typing=Go.record_map_value_typings.WIDE,
        declaration_style=Go.declaration_styles.VAR,
    )
    declaring = roundtrip_common.literalize_new_variable(
        language=language,
        json_text=shared_record_common.DECLARING_DOCUMENT,
        var_name=shared_record_common.DECLARING_VAR_NAME_CAMEL,
        pre_indent_level=0,
    )
    dependent = roundtrip_common.literalize_new_variable(
        language=language,
        json_text=shared_record_common.DEPENDENT_DOCUMENT,
        var_name=shared_record_common.DEPENDENT_VAR_NAME_CAMEL,
        pre_indent_level=0,
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
    program = _CONSUMER_PATH.read_text(encoding="utf-8")
    for declaration_label, declarations_from in (
        ("mixed-map declaration", declaring),
        ("string-only declaration", dependent),
    ):
        roundtrip_common.execute(
            label=f"{_LABEL} ({declaration_label})",
            source_filename="main.go",
            program=program,
            steps=steps,
            excluded_keys=(),
            expected_json=_EXPECTED_JSON,
            extra_files={
                "go.mod": _GO_MOD,
                "record_data.go": _build_data_source(
                    declarations_from=declarations_from,
                    declaring=declaring,
                    dependent=dependent,
                ),
            },
        )


if __name__ == "__main__":
    main()
