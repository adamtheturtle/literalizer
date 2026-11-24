"""Rust cross-file record-declaration check (issue #3748).

Literalize both documents in :mod:`scripts.shared_record_common` under
``Rust(heterogeneous_strategy=RECORD, record_map_value_typing=WIDE)``,
compile the mixed document's public ``enum`` and ``struct``
declarations as a library, then construct and inspect both documents'
``vec![...]`` literals in a separate consumer crate.  The dependent
document's widened maps are all strings, so under the default ``NARROW``
typing they would render ``HashMap<&'static str, &'static str>`` and fail
to compile against the declaring document's ``HashMap<&'static str, Value>``
field. The mixed document supplies the declarations because it also
contains the boolean variant used by the mixed literals.

This lives here, driven by a step of the ``lint-rust`` job in
``.github/workflows/lint.yml``, because that job is where the Rust
toolchain is already available.
"""

import shutil
import textwrap

import click

from literalizer.languages import Rust
from scripts import roundtrip_common, shared_record_common

_LABEL = "Rust shared-record"


_VALUE_CHECKS = textwrap.dedent(
    text=r"""
    fn assert_row(row: &Record0, name: &str, attributes: &[(&str, Value)]) {
        assert_eq!(row.name, name);
        assert_eq!(row.attributes.len(), attributes.len(), "{name}");
        for (key, expected) in attributes {
            let actual = row.attributes.get(key).expect("missing attribute");
            match (actual, expected) {
                (Value::Str(actual), Value::Str(expected)) =>
                    assert_eq!(actual, expected, "{name}.{key}"),
                (Value::Bool(actual), Value::Bool(expected)) =>
                    assert_eq!(actual, expected, "{name}.{key}"),
                _ => panic!("{name}.{key}: wrong value type"),
            }
        }
    }
    """,
).strip()

_DOCUMENT_CHECKS = textwrap.indent(
    text=textwrap.dedent(
        text=r"""
        assert_eq!(declaring_data.len(), 2);
        assert_eq!(dependent_data.len(), 2);
        assert_row(&declaring_data[0], "row_1",
            &[("colour", Value::Str("red")),
              ("discounted", Value::Bool(true))]);
        assert_row(&declaring_data[1], "row_2",
            &[("colour", Value::Str("blue")), ("size", Value::Str("large"))]);
        assert_row(&dependent_data[0], "row_3",
            &[("colour", Value::Str("green")), ("size", Value::Str("small"))]);
        assert_row(&dependent_data[1], "row_4",
            &[("colour", Value::Str("white"))]);
        """,
    ).strip(),
    prefix="    ",
)


def _build_sources() -> tuple[str, str]:
    """Return a consumer program and its shared data-type library."""
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
    # Both documents use only the declaring document's exported types.
    preamble = "\n".join((*declaring.preamble, *declaring.body_preamble))
    ok_document = shared_record_common.OK_DOCUMENT
    program = (
        "use std::collections::HashMap;\n"
        "use record_data::{Record0, Value};\n"
        f"{_VALUE_CHECKS}\n"
        "fn main() {\n"
        f"{declaring.code}\n"
        f"{dependent.code}\n"
        f"{_DOCUMENT_CHECKS}\n"
        f'    print!("{{}}", r#"{ok_document}"#);\n'
        "}\n"
    )
    return program, preamble


@click.command()
def main() -> None:
    """Compile both documents against one set of declarations."""
    program, library = _build_sources()
    rustc = shutil.which(cmd="rustc")
    if rustc is None or rustc == "":
        rustc = "rustc"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.rs",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[
                    rustc,
                    "--edition",
                    "2021",
                    "-D",
                    "warnings",
                    "--crate-type",
                    "lib",
                    "record_data.rs",
                    "-o",
                    "librecord_data.rlib",
                ],
                failure_label="library rustc error",
            ),
            roundtrip_common.Step(
                args=[
                    rustc,
                    "--edition",
                    "2021",
                    "-D",
                    "warnings",
                    "--extern",
                    "record_data=librecord_data.rlib",
                    "main.rs",
                    "-o",
                    "main",
                ],
                failure_label="rustc error",
            ),
            roundtrip_common.Step(
                args=["./main"],
                failure_label="run error",
            ),
        ],
        excluded_keys=(),
        expected_json=shared_record_common.OK_DOCUMENT,
        extra_files={"record_data.rs": library},
    )


if __name__ == "__main__":
    main()
