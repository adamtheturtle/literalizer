"""C++ cross-file record-declaration check (issue #3748).

Literalize both documents in :mod:`scripts.shared_record_common` under
``Cpp(heterogeneous_strategy=RECORD, record_map_value_typing=WIDE)``,
build one translation unit from the *declaring* document's
``LiteralizerRecordValue`` alias and ``struct`` declarations plus both
documents' ``std::vector`` literals, and compile and run it with
``clang++``.  The dependent document's widened maps are all strings, so
under the default ``NARROW`` typing they would render
``std::map<std::string, std::string>`` and fail to convert to the
declaring document's alias-typed field.

This lives here, driven by a step of the ``lint-cpp`` job in
``.github/workflows/lint.yml``, because that job is where the C++
toolchain (``clang++``) is already installed.
"""

import shutil

from literalizer.languages import Cpp
from scripts import roundtrip_common, shared_record_common

_LABEL = "C++ shared-record"


def _build_program() -> str:
    """Return a runnable C++ program built from both documents."""
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
    preamble = "\n".join((*declaring.preamble, *declaring.body_preamble))
    ok_document = shared_record_common.OK_DOCUMENT
    return (
        f"{preamble}\n"
        "#include <iostream>\n"
        "int main() {\n"
        f"{declaring.code}\n"
        f"{dependent.code}\n"
        f"    (void){shared_record_common.DECLARING_VAR_NAME_SNAKE};\n"
        f"    (void){shared_record_common.DEPENDENT_VAR_NAME_SNAKE};\n"
        f'    std::cout << R"json({ok_document})json";\n'
        "    return 0;\n"
        "}\n"
    )


def main() -> None:
    """Compile both documents against one set of declarations."""
    program = _build_program()
    clangxx = shutil.which(cmd="clang++") or "clang++"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.cpp",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[clangxx, "-std=c++20", "main.cpp", "-o", "main"],
                failure_label="clang++ error",
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
