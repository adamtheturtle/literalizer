"""Known ref values participate in nested container opener inference."""

import pytest

from literalizer import CollectionLayout, InputFormat, literalize
from literalizer.languages import Go


@pytest.mark.parametrize(
    argnames=("source", "expected_opener"),
    argvalues=[
        ('[{"$ref": "x"}]', "[]int{"),
        ('{"a": {"$ref": "x"}}', "map[string]int{"),
        (
            '{"outer": {"a": {"$ref": "x"}}}',
            "map[string]map[string]int{",
        ),
    ],
)
@pytest.mark.parametrize(
    argnames="collection_layout",
    argvalues=[CollectionLayout.COMPACT, CollectionLayout.MULTILINE],
)
def test_known_ref_value_drives_container_opener(
    source: str,
    expected_opener: str,
    collection_layout: CollectionLayout,
) -> None:
    """Ref marker dictionaries never determine a typed opener."""
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=Go(),
        ref_key="$ref",
        ref_values={"x": 1},
        collection_layout=collection_layout,
    )

    assert result.code.startswith(expected_opener)
