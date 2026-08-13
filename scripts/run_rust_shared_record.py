"""Rust cross-file record-declaration check (issue #3748).

Literalize both documents in :mod:`scripts.shared_record_common` under
``Rust(heterogeneous_strategy=RECORD, record_map_value_typing=WIDE)``,
build one program from the *declaring* document's ``enum`` and ``struct``
declarations plus both documents' ``vec![...]`` literals, and compile and
run it with ``rustc``.  The dependent document's widened maps are all
strings, so under the default ``NARROW`` typing they would render
``HashMap<&'static str, &'static str>`` and fail to compile against the
declaring document's ``HashMap<&'static str, Value>`` field.

This lives here, driven by a step of the ``lint-rust`` job in
``.github/workflows/lint.yml``, because that job is where the Rust
toolchain is already available.
"""

import shutil

from literalizer.languages import Rust
from scripts import roundtrip_common, shared_record_common

_LABEL = "Rust shared-record"


def _build_program() -> str:
    """Return a runnable Rust program built from both documents."""
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD,
        record_map_value_typing=Rust.record_map_value_typings.WIDE,
    )
    declaring = roundtrip_common.literalize_new_variable(
        language=language,
        json_text=shared_record_common.DECLARING_DOCUMENT,
        var_name=shared_record_common.DECLARING_VAR_NAME_SNAKE,
        pre_indent_level=1,
    )
    dependent = roundtrip_common.literalize_new_variable(
        language=language,
        json_text=shared_record_common.DEPENDENT_DOCUMENT,
        var_name=shared_record_common.DEPENDENT_VAR_NAME_SNAKE,
        pre_indent_level=1,
    )
    # Only the declaring document's preamble is emitted; the dependent
    # literals bind to the ``Value`` and ``Record0`` declarations it
    # brings, which is the property under test.
    preamble = "\n".join((*declaring.preamble, *declaring.body_preamble))
    ok_document = shared_record_common.OK_DOCUMENT
    return (
        f"{preamble}\n"
        "fn main() {\n"
        f"{declaring.code}\n"
        f"{dependent.code}\n"
        f"    let _ = {shared_record_common.DECLARING_VAR_NAME_SNAKE};\n"
        f"    let _ = {shared_record_common.DEPENDENT_VAR_NAME_SNAKE};\n"
        f'    print!("{{}}", r#"{ok_document}"#);\n'
        "}\n"
    )


def main() -> None:
    """Compile both documents against one set of declarations."""
    program = _build_program()
    rustc = shutil.which(cmd="rustc") or "rustc"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.rs",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[rustc, "--edition", "2021", "main.rs", "-o", "main"],
                failure_label="rustc error",
            ),
            roundtrip_common.Step(
                args=["./main"],
                failure_label="run error",
            ),
        ],
        excluded_keys=(),
        expected_json=shared_record_common.OK_DOCUMENT,
        extra_files=None,
    )


if __name__ == "__main__":
    main()
