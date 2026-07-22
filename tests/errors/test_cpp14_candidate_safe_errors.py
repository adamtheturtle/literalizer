"""C++14 candidate-safe rendering errors."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Cpp


def test_cpp14_rejects_shape_requiring_helper_carrier() -> None:
    """Unsupported mixed shapes fail instead of emitting a tool type."""
    with pytest.raises(
        UnrepresentableInputError,
        match=r"candidate-safe rendering cannot represent.*LiteralizerVariant",
    ):
        literalize(
            source='{"003": [1, {"x": true}]}',
            input_format=InputFormat.JSON,
            language=Cpp(language_version=Cpp.version_formats.CPP14),
        )
