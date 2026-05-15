"""Validation tests for Rust ``record_struct_name_prefix`` and
``record_shape_names`` constructor parameters.
"""

import pytest

from literalizer.exceptions import InvalidRecordNameError
from literalizer.languages import Rust


def test_invalid_prefix_lowercase_raises() -> None:
    """A lowercase prefix is not PascalCase and is rejected."""
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Rust(record_struct_name_prefix="record")


def test_invalid_prefix_starts_with_digit_raises() -> None:
    """A prefix that does not start with an uppercase letter is
    rejected.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Rust(record_struct_name_prefix="9Record")


def test_invalid_prefix_empty_raises() -> None:
    """An empty prefix would emit anonymous ``0``, ``1`` names and is
    rejected.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Rust(record_struct_name_prefix="")


def test_invalid_shape_name_lowercase_raises() -> None:
    """A lowercase mapped struct name is not PascalCase and is
    rejected.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Rust(
            record_shape_names={frozenset({"id", "name"}): "task"},
        )


def test_invalid_shape_name_with_hyphen_raises() -> None:
    """A mapped struct name with non-identifier characters is rejected."""
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Rust(
            record_shape_names={frozenset({"id", "name"}): "My-Task"},
        )


def test_shape_name_collides_with_rust_keyword_raises() -> None:
    """``Self`` is a Rust reserved keyword and cannot be used as a
    generated struct name.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Rust(
            record_shape_names={frozenset({"id", "name"}): "Self"},
        )


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


def test_duplicate_shape_names_raises() -> None:
    """Two distinct key-sets cannot map to the same struct name."""
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Rust(
            record_shape_names={
                frozenset({"id", "name"}): "Task",
                frozenset({"id", "title"}): "Task",
            },
        )
