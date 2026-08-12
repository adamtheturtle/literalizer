"""Tests for capability-selected round-trip inputs."""

import json

import pytest

from literalizer import RoundTripCapability
from literalizer.languages import ALL_LANGUAGES, Rust
from scripts.roundtrip_common import (
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


def test_every_language_declares_round_trip_capabilities() -> None:
    """Capability discovery uses required metadata, never a fallback."""
    for language_cls in ALL_LANGUAGES:
        capabilities = language_cls.variant_metadata.round_trip_capabilities
        assert isinstance(capabilities, frozenset)
        assert all(
            isinstance(item, RoundTripCapability) for item in capabilities
        )


def test_rust_opts_into_supported_adversarial_groups() -> None:
    """Rust selects groups accepted by its default string formatter."""
    assert Rust.variant_metadata.round_trip_capabilities == frozenset(
        {
            RoundTripCapability.I64_BOUNDARIES,
            RoundTripCapability.INTERPOLATION_STRINGS,
            RoundTripCapability.EMBEDDED_NUL,
        }
    )
