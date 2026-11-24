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

from literalizer import (
    InputFormat,
    NewVariable,
    literalize,
    literalize_call,
    literalize_call_with_declarations,
)
from literalizer.languages import Rust
from scripts import roundtrip_common, shared_record_common

_LABEL = "Rust shared-record"


_CONSUMER_PATH = Path(__file__).with_name(name="rust_shared_record.rs")
_COMPOSED_CONSUMER_PATH = Path(__file__).with_name(
    name="rust_composed_record.rs"
)


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


def _build_composed_program(*, reverse: bool, include_ref_values: bool) -> str:
    """Compose separate records and a call with a repeated reference."""
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD,
    )
    declarations = {
        name: literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(name=name, modifiers=frozenset()),
        )
        for name, source in (
            ("first_data", '{"name":"first","values":[1,2]}'),
            ("second_data", '{"name":"second","values":[3]}'),
        )
    }
    call = literalize_call(
        source=(
            '[[{"$ref":"first_data"},{"$ref":"second_data"},'
            '{"$ref":"first_data"}]]'
        ),
        input_format=InputFormat.JSON,
        language=language,
        target_function="consume",
        parameter_names=("first", "second", "repeated"),
        per_element=True,
        ref_key="$ref",
        ref_values=(
            {name: result.source_data for name, result in declarations.items()}
            if include_ref_values
            else None
        ),
    )
    bindings = tuple(declarations.values())
    return literalize_call_with_declarations(
        language=language,
        declarations=bindings[::-1] if reverse else bindings,
        call=call,
        extra_preamble=(f'include!("{_COMPOSED_CONSUMER_PATH.name}");',),
    ).code


def _check_composed_records(*, rustc: str) -> None:
    """Run both declaration orders with and without reference hints."""
    consumer = _COMPOSED_CONSUMER_PATH.read_text(encoding="utf-8")
    steps = [
        roundtrip_common.Step(
            args=[rustc, "--edition", "2021", "-D", "warnings", "main.rs"],
            failure_label="Rust composition rustc error",
        ),
        roundtrip_common.Step(
            args=["./main"], failure_label="Rust composition runtime error"
        ),
    ]
    for reverse in (False, True):
        for include_ref_values in (False, True):
            roundtrip_common.execute(
                label=(
                    f"Rust composed records reverse={reverse}, "
                    f"ref_values={include_ref_values}"
                ),
                source_filename="main.rs",
                program=_build_composed_program(
                    reverse=reverse, include_ref_values=include_ref_values
                ),
                steps=steps,
                excluded_keys=(),
                expected_json=shared_record_common.OK_DOCUMENT,
                extra_files={_COMPOSED_CONSUMER_PATH.name: consumer},
            )


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
    _check_composed_records(rustc=rustc)


if __name__ == "__main__":
    main()
