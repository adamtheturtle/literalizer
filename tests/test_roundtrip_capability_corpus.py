"""Tests for capability-selected round-trip inputs."""

import json

import pytest

from literalizer import RoundTripCapability
from literalizer.languages import ALL_LANGUAGES
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


def test_audited_languages_declare_their_supported_groups() -> None:
    """Each audited backend declares exactly the groups its runner passes.

    This table is the audited record behind the per-language
    declarations: every entry was verified by running the language's
    ``scripts/run_<lang>_roundtrip.py`` against the group's corpus on a
    real toolchain.  A language absent from the table has not been
    audited yet and must declare no capabilities.

    Exclusions are one of these verified failure classes:

    * ``control_strings`` -- most formatters would emit a raw C0 byte,
      so ``literalize`` fails hard with ``UnrepresentableStringError``
      (covered by ``tests/errors`` ``string_raw_control_character``).
    * ``i64_boundaries`` -- a runtime whose only number type is an IEEE
      double (JavaScript-hosted Elm, the 32-bit Haxe ``Int`` plus
      ``Float`` fallback, Jsonnet, PureScript, Wren, cJSON-backed C)
      collapses 64-bit endpoints; TypeScript fails hard with
      ``UnrepresentableIntegerError``.
    * ``embedded_nul`` -- a language that cannot escape a zero byte
      fails hard (``string_nul_byte`` in ``tests/errors``); the
      ``dhall-to-json`` and Haxe JSON printers emit the byte raw, Wren
      truncates the emitted document, the SystemVerilog string type
      drops the byte, and cJSON truncates at the terminator.
    * ``interpolation_strings`` -- Crystal's ``%(...)`` percent literal
      and Odin's backtick raw string cannot carry their own delimiters,
      so their ``json_type`` renderings fail-hard with
      ``UnrepresentableInputError``.
    """
    i64 = RoundTripCapability.I64_BOUNDARIES
    interpolation = RoundTripCapability.INTERPOLATION_STRINGS
    controls = RoundTripCapability.CONTROL_STRINGS
    nul = RoundTripCapability.EMBEDDED_NUL
    audited: dict[str, frozenset[RoundTripCapability]] = {
        "Bash": frozenset({i64, interpolation}),
        "C": frozenset({interpolation}),
        "CSharp": frozenset({i64, interpolation, nul}),
        "Clojure": frozenset({i64, interpolation, nul}),
        "Cpp": frozenset({i64, interpolation, nul}),
        "Crystal": frozenset({i64, nul}),
        "D": frozenset({i64, interpolation, nul}),
        "Dart": frozenset({i64, interpolation, nul}),
        "Dhall": frozenset({i64, interpolation}),
        "Elixir": frozenset({i64, interpolation, nul}),
        "Elm": frozenset({interpolation, controls, nul}),
        "Erlang": frozenset({i64, interpolation, nul}),
        "FSharp": frozenset({i64, interpolation, nul}),
        "Fortran": frozenset({i64, interpolation, controls, nul}),
        "Go": frozenset({i64, interpolation, nul}),
        "Groovy": frozenset({i64, interpolation, nul}),
        "Haskell": frozenset({i64, interpolation, controls, nul}),
        "Haxe": frozenset({interpolation}),
        "Java": frozenset({i64, interpolation, nul}),
        "JavaScript": frozenset({interpolation, nul}),
        "Json5": frozenset({i64, interpolation, controls, nul}),
        "Jsonnet": frozenset({interpolation, controls, nul}),
        "Kotlin": frozenset({i64, interpolation, nul}),
        "Lua": frozenset({i64, interpolation, nul}),
        "Mojo": frozenset({i64, interpolation, nul}),
        "Nim": frozenset({i64, interpolation, nul}),
        "ObjectiveC": frozenset({i64, interpolation, nul}),
        "Odin": frozenset({i64, nul}),
        "Perl": frozenset({i64, interpolation, nul}),
        "Php": frozenset({i64, interpolation, nul}),
        "PureScript": frozenset({interpolation, controls, nul}),
        "Racket": frozenset({i64, interpolation, nul}),
        "Ruby": frozenset({i64, interpolation, nul}),
        "Rust": frozenset({i64, interpolation, nul}),
        "Scala": frozenset({i64, interpolation, nul}),
        "Sml": frozenset({i64, interpolation, controls, nul}),
        "Swift": frozenset({i64, interpolation, controls, nul}),
        "SystemVerilog": frozenset({i64, interpolation}),
        "Tcl": frozenset({i64, interpolation, nul}),
        "Toml": frozenset({i64, interpolation, controls, nul}),
        "TypeScript": frozenset({interpolation, nul}),
        "V": frozenset({i64, interpolation, nul}),
        "VisualBasic": frozenset({i64, interpolation, controls, nul}),
        "Wren": frozenset({interpolation}),
        "Yaml": frozenset({i64, interpolation, controls, nul}),
    }
    for language_cls in ALL_LANGUAGES:
        name = language_cls.__name__
        expected = audited.get(name, frozenset())
        declared = language_cls.variant_metadata.round_trip_capabilities
        assert declared == expected, name
