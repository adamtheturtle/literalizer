"""C++ ``json_type`` rendering coverage."""

from literalizer import InputFormat, literalize
from literalizer.languages import Cpp


def test_cpp14_json_type_bypasses_native_only_shape_validation() -> None:
    """JSON mode renders shapes that native-only C++14 rejects."""
    result = literalize(
        source='{"outer": {"alpha": 1, "beta": "two"}}',
        input_format=InputFormat.JSON,
        language=Cpp(
            language_version=Cpp.version_formats.CPP14,
            json_type=Cpp.json_types.NLOHMANN_JSON,
        ),
    )

    assert result.code == '{\n    "outer": {"alpha": 1, "beta": "two"},\n}'
    assert result.preamble == ("#include <nlohmann/json.hpp>",)
