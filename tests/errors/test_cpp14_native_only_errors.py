"""C++14 native-only rendering errors."""

import pytest

from literalizer import InputFormat, literalize, literalize_call
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Cpp


def test_cpp14_rejects_shape_requiring_helper_carrier() -> None:
    """Unsupported mixed shapes fail instead of emitting a tool type."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match=r"native-only rendering cannot represent.*LiteralizerVariant",
    ):
        literalize(
            source='{"003": [1, {"x": true}]}',
            input_format=InputFormat.JSON,
            language=Cpp(language_version=Cpp.version_formats.CPP14),
        )


def test_cpp14_rejects_call_argument_requiring_helper_carrier() -> None:
    """Calls reject arguments that would require a helper carrier."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match=r"native-only call rendering cannot represent.*LiteralizerVariant",
    ):
        literalize_call(
            source='{"first": 1, "second": "x"}',
            input_format=InputFormat.JSON,
            language=Cpp(language_version=Cpp.version_formats.CPP14),
            target_function="process",
            parameter_names=(),
            per_element=False,
        )
