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
from pathlib import Path

import click

from literalizer import InputFormat, literalize
from literalizer.languages import Rust
from scripts import roundtrip_common, shared_record_common

_LABEL = "Rust shared-record"


_CONSUMER_PATH = Path(__file__).with_name(name="rust_shared_record.rs")


def _build_sources() -> dict[str, str]:
    """Render the shared library and both data expressions."""
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD,
        record_map_value_typing=Rust.record_map_value_typings.WIDE,
    )
    declaring = literalize(
        source=shared_record_common.DECLARING_DOCUMENT,
        input_format=InputFormat.JSON,
        language=language,
    )
    dependent = literalize(
        source=shared_record_common.DEPENDENT_DOCUMENT,
        input_format=InputFormat.JSON,
        language=language,
    )
    # Both documents use only the declaring document's exported types.
    return {
        "record_data.rs": "\n".join(
            (*declaring.preamble, *declaring.body_preamble)
        ),
        "declaring_data.rs": declaring.code,
        "dependent_data.rs": dependent.code,
    }


@click.command()
def main() -> None:
    """Compile both documents against one set of declarations."""
    rustc = shutil.which(cmd="rustc")
    if rustc is None or rustc == "":
        rustc = "rustc"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.rs",
        program=_CONSUMER_PATH.read_text(encoding="utf-8"),
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
        extra_files=_build_sources(),
    )


if __name__ == "__main__":
    main()
