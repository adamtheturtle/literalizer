"""C++14 heterogeneous value-carrier rendering coverage."""

from literalizer import InputFormat, literalize
from literalizer.languages import Cpp


def test_cpp14_custom_value_carrier_preserves_nested_maps_and_nulls() -> None:
    """Nested heterogeneous map values use the configured carrier name."""
    result = literalize(
        source='[{"id":1,"meta":{"done":false,"note":null}},'
        '{"id":null,"meta":{"done":"yes","note":2}}]',
        input_format=InputFormat.JSON,
        language=Cpp(
            language_version=Cpp.version_formats.CPP14,
            heterogeneous_value_variant_name="TaskValue",
        ),
    )

    assert "TaskValue" in result.code
    assert "nullptr" in result.code
    assert "LiteralizerVariant" not in result.code
    assert "struct TaskValue {" in result.preamble
    assert "#include <memory>" in result.preamble
