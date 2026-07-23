"""C++14 heterogeneous value-carrier configuration errors."""

import pytest

from literalizer.exceptions import InvalidRecordNameError
from literalizer.languages import Cpp


@pytest.mark.parametrize(
    argnames="name",
    argvalues=["", "task-value", "1Value"],
)
def test_cpp14_rejects_invalid_value_carrier_name(name: str) -> None:
    """The generated carrier name must be a C++ identifier."""
    with pytest.raises(
        expected_exception=InvalidRecordNameError,
        match="heterogeneous_value_variant_name",
    ):
        Cpp(
            language_version=Cpp.version_formats.CPP14,
            heterogeneous_value_variant_name=name,
        )


def test_cpp14_rejects_value_carrier_record_name_collision() -> None:
    """Generated and externally declared C++ types cannot share a name."""
    with pytest.raises(
        expected_exception=InvalidRecordNameError,
        match="collides with heterogeneous_value_variant_name",
    ):
        Cpp(
            language_version=Cpp.version_formats.CPP14,
            heterogeneous_value_variant_name="TaskValue",
            record_shape_names={frozenset({"id"}): "TaskValue"},
        )
