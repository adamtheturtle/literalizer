"""Assign an external C++ reference through the public API.

An existing variable and its external reference cannot form a self-contained
golden file. New reference declarations are covered by compiling manifests.
"""

from literalizer import ExistingVariable, InputFormat, literalize
from literalizer.languages import Cpp


def test_cpp_reference_assignment() -> None:
    """An existing variable receives the rendered reference expression."""
    result = literalize(
        source='{"$ref": "ref_data"}',
        input_format=InputFormat.JSON,
        language=Cpp(),
        variable_form=ExistingVariable(name="my_data"),
        ref_key="$ref",
        ref_values={"ref_data": [1, 2]},
    )

    assert result.code == "my_data = std::move(ref_data);"
    assert result.preamble == (
        "#include <initializer_list>",
        "#include <vector>",
        "#include <utility>",
    )
