"""C++ nested ARRAY validation coverage."""

from literalizer import InputFormat, literalize
from literalizer.languages import Cpp


def test_compatible_nested_array_values_are_accepted() -> None:
    """Equivalent nested array element shapes remain representable."""
    literalize(
        source='{"groups": [[{"id": 1}], [{"id": 2}]]}',
        input_format=InputFormat.JSON,
        language=Cpp(sequence_format=Cpp.sequence_formats.ARRAY),
    )
