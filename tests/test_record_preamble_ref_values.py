"""Record declarations survive ref-aware preamble inference."""

from __future__ import annotations

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer._language import Language  # noqa: TC001 - pytest-beartype
from literalizer.languages import Go, Kotlin


@pytest.mark.parametrize(
    argnames=("language", "declaration"),
    argvalues=[
        (
            Go(heterogeneous_strategy=Go.heterogeneous_strategies.RECORD),
            "type Record0 struct",
        ),
        (
            Kotlin(
                heterogeneous_strategy=(
                    Kotlin.heterogeneous_strategies.RECORD
                ),
            ),
            "data class Record0",
        ),
    ],
)
def test_unreferenced_ref_value_preserves_record_declaration(
    language: Language,
    declaration: str,
) -> None:
    """An unrelated ``ref_values`` entry cannot erase declarations."""
    rendered = literalize(
        source='{"main":{"x":1,"y":"s"}}',
        input_format=InputFormat.JSON,
        language=language,
        wrap_in_file=True,
        variable_form=NewVariable(name="v", modifiers=frozenset()),
        ref_values={"other": "true"},
    )

    assert declaration in rendered.code
