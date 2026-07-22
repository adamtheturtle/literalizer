"""C++14's automatic native-only heterogeneous rendering policy."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Cpp


def _cpp14() -> Cpp:
    """Return C++14 with its default candidate-safe policy."""
    return Cpp(language_version=Cpp.version_formats.CPP14)


def test_cpp14_default_renders_heterogeneous_list_as_native_tuple() -> None:
    """A fixed scalar sequence needs no literalizer helper carrier."""
    result = literalize(
        source='[1, "two"]',
        input_format=InputFormat.JSON,
        language=_cpp14(),
    )

    assert "std::make_tuple(" in result.code
    assert "#include <tuple>" in result.preamble
    assert "LiteralizerVariant" not in result.code
    assert "LiteralizerVariant" not in "\n".join(result.preamble)
    assert "std::variant" not in result.code


def test_cpp14_default_renders_valid_object_as_record() -> None:
    """Naturally named object keys select a generated aggregate."""
    result = literalize(
        source='{"id": 1, "name": "Ada"}',
        input_format=InputFormat.JSON,
        language=_cpp14(),
    )

    assert result.code.startswith("Record0{")
    assert any("struct Record0 {" in line for line in result.preamble)
    assert "LiteralizerVariant" not in "\n".join(result.preamble)


def test_cpp14_default_keeps_non_identifier_key_as_standard_map() -> None:
    """A map key cannot silently become an invalid C++ field name."""
    result = literalize(
        source='{"003": "map value"}',
        input_format=InputFormat.JSON,
        language=_cpp14(),
    )

    assert result.code.startswith("std::map<std::string, std::string>{")
    assert "Record" not in result.code
    assert all("struct Record" not in line for line in result.preamble)


def test_cpp14_default_rejects_shape_requiring_helper_carrier() -> None:
    """Unsupported mixed shapes fail rather than emitting a tool type."""
    with pytest.raises(
        UnrepresentableInputError,
        match=r"candidate-safe rendering cannot represent.*LiteralizerVariant",
    ):
        literalize(
            source='{"003": [1, {"x": true}]}',
            input_format=InputFormat.JSON,
            language=_cpp14(),
        )
