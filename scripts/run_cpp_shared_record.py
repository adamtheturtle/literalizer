"""C++ cross-file record-declaration check (issue #3748).

Literalize both documents in :mod:`scripts.shared_record_common` under
``Cpp(heterogeneous_strategy=RECORD, record_map_value_typing=WIDE)``,
build one translation unit from the *declaring* document's
``LiteralizerRecordValue`` alias and ``struct`` declarations plus both
documents' ``std::vector`` literals, then inspect both documents' native
values after compilation with ``clang++``. The dependent document's
widened maps are all strings, so under the default ``NARROW`` typing
they would render
``std::map<std::string, std::string>`` and fail to convert to the
declaring document's alias-typed field.

This lives here, driven by a step of the ``lint-cpp`` job in
``.github/workflows/lint.yml``, because that job is where the C++
toolchain (``clang++``) is already installed.
"""

import shutil
from pathlib import Path

import click

from literalizer import (
    InputFormat,
    Language,
    LanguageCls,
    NewVariable,
    literalize,
    literalize_call,
    literalize_call_with_declarations,
)
from literalizer.languages import Cpp
from scripts import roundtrip_common, shared_record_common

_LABEL = "C++ shared-record"
_CONSUMER_PATH = Path(__file__).with_name(name="cpp_shared_record.cpp")
_COMPOSED_CONSUMER_PATH = Path(__file__).with_name(
    name="cpp_composed_record.hpp"
)


def _build_data_sources() -> dict[str, str]:
    """Render the shared declarations and both data bindings."""
    language = Cpp(
        heterogeneous_strategy=Cpp.heterogeneous_strategies.RECORD,
        record_map_value_typing=Cpp.record_map_value_typings.WIDE,
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
    # literals bind to the ``LiteralizerRecordValue`` alias and
    # ``Record0`` declaration it brings, which is the property under
    # test.
    return {
        "record_data.hpp": "\n".join(
            (*declaring.preamble, *declaring.body_preamble)
        ),
        "record_bindings.inc": f"{declaring.code}\n{dependent.code}\n",
    }


def _build_composed_program(*, language: Language, reverse: bool) -> str:
    """Compose independent records and pass one by reference twice."""
    declarations = [
        literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(name=name, modifiers=frozenset()),
        )
        for name, source in (
            ("first_data", '{"name": "first", "values": [1, 2]}'),
            ("second_data", '{"name": "second", "values": [3]}'),
        )
    ]
    if reverse:
        declarations.reverse()
    call = literalize_call(
        source=(
            '[[{"$ref": "first_data"}, {"$ref": "second_data"}, '
            '{"$ref": "first_data"}]]'
        ),
        input_format=InputFormat.JSON,
        language=language,
        target_function="consume",
        parameter_names=("first", "second", "repeated"),
        per_element=True,
        ref_key="$ref",
    )
    result = literalize_call_with_declarations(
        language=language,
        declarations=declarations,
        call=call,
        extra_body_preamble=(),
        extra_class_preamble=(),
        extra_preamble=('#include "cpp_composed_record.hpp"',),
    )
    return result.code


def _check_composed_records(*, clangxx: str) -> None:
    """Verify both declaration orders with every supported C++ dialect."""
    consumer_files = {
        _COMPOSED_CONSUMER_PATH.name: _COMPOSED_CONSUMER_PATH.read_text(
            encoding="utf-8"
        )
    }
    language_cls: LanguageCls = Cpp
    for version, standard in (
        (Cpp.version_formats.CPP14, "c++14"),
        (Cpp.version_formats.CPP17, "c++17"),
        (Cpp.version_formats.CPP20, "c++20"),
    ):
        language = language_cls(
            language_version=version,
            heterogeneous_strategy=Cpp.heterogeneous_strategies.RECORD,
            module_name="main",
        )
        for reverse in (False, True):
            roundtrip_common.execute(
                label=f"C++ {standard} composed records reverse={reverse}",
                source_filename="main.cpp",
                program=_build_composed_program(
                    language=language, reverse=reverse
                ),
                steps=[
                    roundtrip_common.Step(
                        args=[
                            clangxx,
                            f"-std={standard}",
                            "-Werror",
                            "main.cpp",
                            "-o",
                            "main",
                        ],
                        failure_label="clang++ composition error",
                    ),
                    roundtrip_common.Step(
                        args=["./main"],
                        failure_label="composition runtime error",
                    ),
                ],
                excluded_keys=(),
                expected_json=(
                    '{"names": ["first", "second"], "values": [1, 2, 3]}'
                ),
                extra_files=consumer_files,
            )


@click.command()
def main() -> None:
    """Compile both documents against one set of declarations."""
    clangxx = shutil.which(cmd="clang++")
    if clangxx is None or clangxx == "":
        clangxx = "clang++"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.cpp",
        program=_CONSUMER_PATH.read_text(encoding="utf-8"),
        steps=[
            roundtrip_common.Step(
                args=[
                    clangxx,
                    "-std=c++20",
                    "-Werror",
                    "main.cpp",
                    "-o",
                    "main",
                ],
                failure_label="clang++ error",
            ),
            roundtrip_common.Step(
                args=["./main"],
                failure_label="run error",
            ),
        ],
        excluded_keys=(),
        expected_json=shared_record_common.OK_DOCUMENT,
        extra_files=_build_data_sources(),
    )
    _check_composed_records(clangxx=clangxx)


if __name__ == "__main__":
    main()
