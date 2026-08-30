"""Focused coverage for bound-reference parent context analysis."""

# pylint: disable=import-private-name

import json

from literalizer._literalize import (
    _bound_ref_parent_contexts,  # pyright: ignore[reportPrivateUsage]
    _contextual_bound_ref_values,  # pyright: ignore[reportPrivateUsage]
)


def test_contextual_bound_ref_values_widens_nested_mapping_value() -> None:
    """A float sibling in a nested mapping widens its integer
    reference.
    """
    assert _contextual_bound_ref_values(
        source=json.loads(
            s='{"outer":{"ref":{"$ref":"integer_value"},"float":1.5}}'
        ),
        resolved=json.loads(s='{"outer":{"ref":1,"float":1.5}}'),
        bound_refs={"integer_value": 1},
        ref_key="$ref",
    ) == {"integer_value": 1.0}


def test_contextual_bound_ref_values_ignores_unknown_list_reference() -> None:
    """An unbound marker cannot contribute a declaration to widen."""
    assert not _contextual_bound_ref_values(
        source=json.loads(s='[{"$ref":"unknown"},1.5]'),
        resolved=json.loads(s="[1,1.5]"),
        bound_refs={},
        ref_key="$ref",
    )


def test_bound_ref_parent_contexts_recurses_through_containers() -> None:
    """Nested list and mapping markers retain their immediate parents."""
    contexts = _bound_ref_parent_contexts(
        source=json.loads(
            s='[[{"$ref":"list_value"}],{"nested":{"$ref":"map_value"}}]'
        ),
        resolved=json.loads(s='[[1],{"nested":2}]'),
        bound_refs={"list_value": 10, "map_value": 20},
        ref_key="$ref",
    )
    assert contexts == {
        "list_value": [10],
        "map_value": {"nested": 20},
    }


def test_bound_ref_parent_contexts_stops_at_short_resolved_list() -> None:
    """A truncated resolved list cannot provide a missing parent slot."""
    assert not _bound_ref_parent_contexts(
        source=json.loads(s='[{"$ref":"value"}]'),
        resolved=json.loads(s="[]"),
        bound_refs={"value": 1},
        ref_key="$ref",
    )
