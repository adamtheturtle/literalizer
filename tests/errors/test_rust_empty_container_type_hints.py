"""Validation of Rust empty-container type hints."""

from collections.abc import Mapping

import pytest

from literalizer import InputFormat, NewVariable, literalize, literalize_call
from literalizer.languages import Rust


def _literalize(
    *,
    source: str,
    hints: Mapping[tuple[str | int, ...], str],
) -> None:
    """Literalize *source* with the supplied Rust empty-container
    hints.
    """
    literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=Rust(
            heterogeneous_strategy=Rust.heterogeneous_strategies.TAGGED_ENUM,
            empty_container_type_hints=hints,
        ),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )


@pytest.mark.parametrize(
    argnames=("source", "hints", "match"),
    argvalues=[
        (
            "[1, {}]",
            {(1,): ""},
            "must be a non-empty string",
        ),
        (
            "[1, {}]",
            {(): "HashMap<String, String>"},
            "does not target an empty list or map",
        ),
    ],
)
def test_empty_container_type_hint_rejects_invalid_target(
    source: str,
    hints: Mapping[tuple[str | int, ...], str],
    match: str,
) -> None:
    """Hints must name a concrete type and target an empty container."""
    with pytest.raises(expected_exception=ValueError, match=match):
        _literalize(source=source, hints=hints)


@pytest.mark.parametrize(
    argnames=("source", "hints", "match"),
    argvalues=[
        (
            "[1, [], []]",
            {(1,): "Vec<String>", (2,): "Vec<bool>"},
            "one concrete empty-list type",
        ),
        (
            "[1, {}, {}]",
            {
                (1,): "HashMap<String, String>",
                (2,): "HashMap<String, bool>",
            },
            "one concrete empty-map type",
        ),
    ],
)
def test_tagged_enum_rejects_conflicting_empty_container_types(
    source: str,
    hints: Mapping[tuple[str | int, ...], str],
    match: str,
) -> None:
    """A tagged enum has one inner type for each container variant."""
    with pytest.raises(expected_exception=ValueError, match=match):
        _literalize(source=source, hints=hints)


def test_call_hints_apply_only_to_arguments_containing_their_path() -> None:
    """A hint for one call argument does not reject another argument."""
    result = literalize_call(
        source="[[[1, {}], 42]]",
        input_format=InputFormat.JSON,
        language=Rust(
            heterogeneous_strategy=Rust.heterogeneous_strategies.TAGGED_ENUM,
            empty_container_type_hints={(1,): "HashMap<String, String>"},
        ),
        target_function="process",
        parameter_names=["values", "count"],
    )
    assert "    Map(HashMap<String, String>)," in result.preamble
    assert "process(" in result.declaration_code
