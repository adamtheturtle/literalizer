"""TOML-driven tests for capability-selected round-trip inputs."""

import json

import pytest
from pydantic import BaseModel, TypeAdapter

from literalizer import RoundTripCapability
from literalizer.languages import ALL_LANGUAGES
from scripts.roundtrip_common import input_for_capabilities
from tests.toml_cases import load_toml_cases


class _CapabilityCase(BaseModel, extra="forbid", frozen=True):
    """One capability and the corpus keys it contributes."""

    capability: RoundTripCapability
    expected_keys: frozenset[str]
    expected_values: dict[str, int]


class _RoundTripCases(BaseModel, extra="forbid", frozen=True):
    """The complete declarative round-trip capability audit."""

    capability_cases: tuple[_CapabilityCase, ...]
    audited_languages: dict[str, frozenset[RoundTripCapability]]


_CASES = TypeAdapter(type=_RoundTripCases).validate_python(
    load_toml_cases(name="roundtrip_capabilities")
)


@pytest.mark.parametrize(
    argnames="case",
    argvalues=_CASES.capability_cases,
    ids=lambda case: case.capability.value,
)
def test_capability_adds_only_its_cases(case: _CapabilityCase) -> None:
    """One capability supplies its declared keys and exact values."""
    base = json.loads(
        s=input_for_capabilities(capabilities=frozenset()),
    )
    selected = json.loads(
        s=input_for_capabilities(capabilities=frozenset({case.capability})),
    )
    assert selected.keys() - base.keys() == case.expected_keys
    assert {
        key: selected[key] for key in case.expected_values
    } == case.expected_values


def test_every_language_declares_round_trip_capabilities() -> None:
    """Capability discovery uses required metadata, never a fallback."""
    for language_cls in ALL_LANGUAGES:
        capabilities = language_cls.variant_metadata.round_trip_capabilities
        assert isinstance(capabilities, frozenset)
        assert all(
            isinstance(item, RoundTripCapability) for item in capabilities
        )


def test_audited_languages_declare_their_supported_groups() -> None:
    """Each audited backend declares exactly its TOML-recorded groups."""
    for language_cls in ALL_LANGUAGES:
        name = language_cls.__name__
        expected = _CASES.audited_languages.get(name, frozenset())
        declared = language_cls.variant_metadata.round_trip_capabilities
        assert declared == expected, name
