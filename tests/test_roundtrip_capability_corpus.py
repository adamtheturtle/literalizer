"""Tests for capability-selected round-trip inputs."""

import json

import pytest

from scripts.roundtrip_common import (
    RoundTripCapability,
    input_for_capabilities,
)


@pytest.mark.parametrize(
    argnames=("capability", "expected_keys"),
    argvalues=[
        (
            RoundTripCapability.I64_BOUNDARIES,
            {"i64_min", "i64_min_adjacent", "i64_max_adjacent", "i64_max"},
        ),
        (
            RoundTripCapability.INTERPOLATION_STRINGS,
            {
                "string_hash_interpolation",
                "string_braced_dollar_interpolation",
                "string_dollar_interpolation",
                "string_backticks",
                "string_at",
            },
        ),
        (RoundTripCapability.CONTROL_STRINGS, {"string_controls"}),
        (RoundTripCapability.EMBEDDED_NUL, {"string_embedded_nul"}),
    ],
)
def test_capability_adds_only_its_cases(
    capability: RoundTripCapability,
    expected_keys: set[str],
) -> None:
    """Selecting one capability neither skips nor leaks another group."""
    base = json.loads(
        s=input_for_capabilities(capabilities=frozenset()),
    )
    selected = json.loads(
        s=input_for_capabilities(capabilities=frozenset({capability})),
    )
    assert selected.keys() - base.keys() == expected_keys


def test_integer_boundaries_are_exact() -> None:
    """The integer group includes both i64 endpoints and neighbors."""
    selected = json.loads(
        s=input_for_capabilities(
            capabilities=frozenset({RoundTripCapability.I64_BOUNDARIES}),
        ),
    )
    assert selected["i64_min"] == -(2**63)
    assert selected["i64_min_adjacent"] == -(2**63) + 1
    assert selected["i64_max_adjacent"] == 2**63 - 2
    assert selected["i64_max"] == 2**63 - 1
