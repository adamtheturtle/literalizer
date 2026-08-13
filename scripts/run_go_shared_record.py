"""Go cross-file record-declaration check (issue #3748).

Literalize both documents in :mod:`scripts.shared_record_common` under
``Go(heterogeneous_strategy=RECORD, record_map_value_typing=WIDE)``,
build one program from the *declaring* document's ``struct``
declarations plus both documents' slice literals, and run it with ``go
run``.  The dependent document's widened maps are all strings, so under
the default ``NARROW`` typing they would render ``map[string]string``
and fail to compile against the declaring document's ``map[string]any``
field.

This lives here, driven by a step of the ``lint-go`` job in
``.github/workflows/lint.yml``, because that job is where the Go
toolchain is already available.
"""

import shutil

from literalizer.languages import Go
from scripts import roundtrip_common, shared_record_common

_LABEL = "Go shared-record"

# ``go 1.18`` matches ``Go.language_version`` in
# ``src/literalizer/languages/go.py`` and the ``go.mod`` written by the
# ``Check Go compilation and run`` step of ``lint-go``; keep them in
# sync.
_GO_MOD = "module fixture\n\ngo 1.18\n"


def _build_program() -> str:
    """Return a runnable Go program built from both documents."""
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
    # Only the declaring document's preamble is emitted; the dependent
    # literals bind to the ``Record0`` declaration it brings, which is
    # the property under test.  Go wants the import block between the
    # package clause and any declaration, so that preamble is split
    # rather than emitted in one piece.
    package_clause, *declarations = (
        *declaring.preamble,
        *declaring.body_preamble,
    )
    declared = "\n".join(declarations)
    ok_document = shared_record_common.OK_DOCUMENT
    return (
        f"{package_clause}\n"
        "\n"
        'import "fmt"\n'
        "\n"
        f"{declared}\n"
        "\n"
        "func main() {\n"
        f"{declaring.code}\n"
        f"{dependent.code}\n"
        f"\t_ = {shared_record_common.DECLARING_VAR_NAME_CAMEL}\n"
        f"\t_ = {shared_record_common.DEPENDENT_VAR_NAME_CAMEL}\n"
        f"\tfmt.Print(`{ok_document}`)\n"
        "}\n"
    )


def main() -> None:
    """Compile both documents against one set of declarations."""
    program = _build_program()
    go = shutil.which(cmd="go") or "go"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.go",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[go, "vet", "./..."],
                failure_label="go vet error",
            ),
            roundtrip_common.Step(
                args=[go, "run", "./..."],
                failure_label="go run error",
            ),
        ],
        excluded_keys=(),
        expected_json=shared_record_common.OK_DOCUMENT,
        extra_files={"go.mod": _GO_MOD},
    )


if __name__ == "__main__":
    main()
