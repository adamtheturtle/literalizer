"""Validation tests for Rust ``record_struct_name_prefix`` and
``record_shape_names`` constructor parameters.
"""

import pytest

from literalizer.exceptions import InvalidRecordNameError
from literalizer.languages import Rust


@pytest.mark.parametrize(
    argnames="prefix",
    argvalues=["record", "9Record", "", "My-Record"],
)
def test_invalid_prefix_raises(prefix: str) -> None:
    """``record_struct_name_prefix`` must be a non-empty PascalCase
    identifier.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Rust(record_struct_name_prefix=prefix)


@pytest.mark.parametrize(
    argnames="name",
    argvalues=["task", "My-Task", "9Task", "Self"],
)
def test_invalid_shape_name_raises(name: str) -> None:
    """Values in ``record_shape_names`` must be PascalCase identifiers
    that are not Rust reserved keywords.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Rust(record_shape_names={frozenset({"id", "name"}): name})


def test_shape_name_collides_with_enum_name_raises() -> None:
    """A mapped struct name that matches
    ``heterogeneous_value_enum_name`` is rejected because the two
    declarations would share a Rust type identifier.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Rust(
            heterogeneous_value_enum_name="Task",
            record_shape_names={frozenset({"id", "name"}): "Task"},
        )


def test_shape_name_collides_with_auto_generated_raises() -> None:
    """A mapped struct name that matches the auto-generated
    ``{prefix}{N}`` pattern is rejected because the user-named record
    would clash with an index-named record at render time.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Rust(record_shape_names={frozenset({"id", "name"}): "Record0"})


def test_duplicate_shape_names_raises() -> None:
    """Two distinct key-sets cannot map to the same struct name."""
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Rust(
            record_shape_names={
                frozenset({"id", "name"}): "Task",
                frozenset({"id", "title"}): "Task",
            },
        )
