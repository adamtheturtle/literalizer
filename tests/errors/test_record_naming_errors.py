"""Validation tests for the ``record_struct_name_prefix`` and
``record_shape_names`` constructor parameters.
"""

import pytest

from literalizer.exceptions import InvalidRecordNameError
from literalizer.languages import Cpp, Go, Java, Kotlin, Rust, Scala


@pytest.mark.parametrize(
    argnames="name",
    argvalues=["task", "My-Task", "9Task"],
)
def test_cpp_invalid_shape_name_raises(name: str) -> None:
    """Externally declared C++ record names must be PascalCase."""
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Cpp(record_shape_names={frozenset({"id", "name"}): name})


def test_cpp_shape_name_collides_with_auto_generated_raises() -> None:
    """An external C++ type cannot take a generated ``RecordN`` name."""
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Cpp(record_shape_names={frozenset({"id", "name"}): "Record0"})


def test_cpp_duplicate_shape_names_raises() -> None:
    """Distinct C++ record shapes need distinct external type names."""
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Cpp(
            record_shape_names={
                frozenset({"id", "name"}): "Task",
                frozenset({"id", "title"}): "Task",
            },
        )


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


@pytest.mark.parametrize(
    argnames="name",
    argvalues=["task", "My-Task", "9Task"],
)
def test_go_invalid_shape_name_raises(name: str) -> None:
    """Values in Go's ``record_shape_names`` must be PascalCase
    identifiers.

    Go has no PascalCase reserved keyword (every Go keyword is
    lowercase), so the PascalCase check is the only name-shape gate.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Go(record_shape_names={frozenset({"id", "name"}): name})


def test_go_shape_name_collides_with_auto_generated_raises() -> None:
    """A mapped struct name that matches the auto-generated
    ``{prefix}{N}`` pattern is rejected because the user-named record
    would clash with an index-named record at render time.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Go(record_shape_names={frozenset({"id", "name"}): "Record0"})


def test_go_duplicate_shape_names_raises() -> None:
    """Two distinct key-sets cannot map to the same Go struct name."""
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Go(
            record_shape_names={
                frozenset({"id", "name"}): "Task",
                frozenset({"id", "title"}): "Task",
            },
        )


@pytest.mark.parametrize(
    argnames="name",
    argvalues=["task", "My-Task", "9Task"],
)
def test_kotlin_invalid_shape_name_raises(name: str) -> None:
    """Values in Kotlin's ``record_shape_names`` must be PascalCase
    identifiers.

    Kotlin has no PascalCase reserved keyword (every Kotlin keyword is
    lowercase), so the PascalCase check is the only name-shape gate.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Kotlin(record_shape_names={frozenset({"id", "name"}): name})


def test_kotlin_shape_name_collides_with_auto_generated_raises() -> None:
    """A mapped struct name that matches the auto-generated
    ``{prefix}{N}`` pattern is rejected because the user-named record
    would clash with an index-named record at render time.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Kotlin(record_shape_names={frozenset({"id", "name"}): "Record0"})


def test_kotlin_duplicate_shape_names_raises() -> None:
    """Two distinct key-sets cannot map to the same Kotlin struct
    name.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Kotlin(
            record_shape_names={
                frozenset({"id", "name"}): "Task",
                frozenset({"id", "title"}): "Task",
            },
        )


@pytest.mark.parametrize(
    argnames="name",
    argvalues=["task", "My-Task", "9Task"],
)
def test_java_invalid_shape_name_raises(name: str) -> None:
    """Values in Java's ``record_shape_names`` must be PascalCase
    identifiers.

    Java has no PascalCase reserved keyword (every Java keyword is
    lowercase), so the PascalCase check is the only name-shape gate.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Java(record_shape_names={frozenset({"id", "name"}): name})


def test_java_shape_name_collides_with_module_name_raises() -> None:
    """A mapped record name that matches ``module_name`` is rejected
    because Java records are emitted as top-level types alongside the
    ``class {module_name}`` wrapper, so the two declarations would
    share an identifier.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Java(
            module_name="Task",
            record_shape_names={frozenset({"id", "name"}): "Task"},
        )


def test_java_shape_name_collides_with_auto_generated_raises() -> None:
    """A mapped record name that matches the auto-generated
    ``{prefix}{N}`` pattern is rejected because the user-named record
    would clash with an index-named record at render time.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Java(record_shape_names={frozenset({"id", "name"}): "Record0"})


def test_java_duplicate_shape_names_raises() -> None:
    """Two distinct key-sets cannot map to the same Java record
    name.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Java(
            record_shape_names={
                frozenset({"id", "name"}): "Task",
                frozenset({"id", "title"}): "Task",
            },
        )


@pytest.mark.parametrize(
    argnames="name",
    argvalues=["task", "My-Task", "9Task"],
)
def test_scala_invalid_shape_name_raises(name: str) -> None:
    """Values in Scala's ``record_shape_names`` must be PascalCase
    identifiers.

    Scala has no PascalCase reserved keyword (every Scala keyword is
    lowercase), so the PascalCase check is the only name-shape gate.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Scala(record_shape_names={frozenset({"id", "name"}): name})


def test_scala_shape_name_collides_with_auto_generated_raises() -> None:
    """A mapped struct name that matches the auto-generated
    ``{prefix}{N}`` pattern is rejected because the user-named record
    would clash with an index-named record at render time.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Scala(record_shape_names={frozenset({"id", "name"}): "Record0"})


def test_scala_duplicate_shape_names_raises() -> None:
    """Two distinct key-sets cannot map to the same Scala struct
    name.
    """
    with pytest.raises(expected_exception=InvalidRecordNameError):
        Scala(
            record_shape_names={
                frozenset({"id", "name"}): "Task",
                frozenset({"id", "title"}): "Task",
            },
        )
