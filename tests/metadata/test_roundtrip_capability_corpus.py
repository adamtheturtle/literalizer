"""Audit required per-language round-trip capability declarations."""

from pydantic import BaseModel, TypeAdapter

from literalizer import RoundTripCapability
from literalizer.languages import ALL_LANGUAGES
from tests.toml_cases import load_toml_cases


class _RoundTripCases(BaseModel, extra="forbid", frozen=True):
    """The complete declarative round-trip capability audit."""

    audited_languages: dict[str, frozenset[RoundTripCapability]]


_CASES = TypeAdapter(type=_RoundTripCases).validate_python(
    load_toml_cases(name="roundtrip_capabilities")
)


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
