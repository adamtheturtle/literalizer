"""Capability corpora survive native program and document round trips."""

import enum
import json
import subprocess
import sys
import tomllib
from pathlib import Path

import json5_document
import pytest
from pydantic import BaseModel

from literalizer import (
    InputFormat,
    NewVariable,
    RoundTripCapability,
    literalize,
)
from literalizer.languages import Json5, Python
from scripts.roundtrip_common import input_for_capabilities, verify

from .language_specs import make_spec


class _CapabilityCase(BaseModel, extra="forbid", frozen=True):
    """A capability's independent key and boundary-value expectations."""

    capability: RoundTripCapability
    expected_keys: frozenset[str]
    expected_values: dict[str, int | str]


class _Cases(BaseModel, extra="forbid", frozen=True):
    """Native program cases and the control-string document case."""

    capability_cases: tuple[_CapabilityCase, ...]
    document_case: _CapabilityCase


_CASES = _Cases.model_validate(
    obj=tomllib.loads(
        Path(__file__)
        .with_name(name="roundtrip_capability_cases.toml")
        .read_text(encoding="utf-8")
    )
)


def _verify_corpus_roundtrip(
    *,
    case: _CapabilityCase,
    source: str,
    produced_json: str,
    label: str,
) -> None:
    """Check reconstructed values and the independently declared group."""
    verify(
        label=label,
        produced_json=produced_json,
        exclude_keys=(),
        expected_json=source,
    )
    base = json.loads(s=input_for_capabilities(capabilities=frozenset()))
    reconstructed = json.loads(s=produced_json)
    assert reconstructed.keys() - base.keys() == case.expected_keys
    assert {
        key: reconstructed[key] for key in case.expected_values
    } == case.expected_values


@pytest.mark.parametrize(
    argnames="version", argvalues=list(Python.VersionFormats)
)
@pytest.mark.parametrize(
    argnames="case",
    argvalues=_CASES.capability_cases,
    ids=lambda case: case.capability.value,
)
def test_capability_corpus_native_roundtrip(
    case: _CapabilityCase, version: enum.Enum
) -> None:
    """Execute each selected group and retain its exact input contract.

    Python executes the integer, interpolation and null-byte groups; each
    language's round-trip driver retains its native capability checks.
    Target versions select output syntax, while this process's interpreter
    supplies the runtime, as in the native golden comparison controls.
    """
    source = input_for_capabilities(capabilities=frozenset({case.capability}))
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=make_spec(lang_cls=Python, language_version=version),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    program = result.code + "\nimport json\nprint(json.dumps(my_data))\n"
    completed = subprocess.run(  # noqa: S603 - execute generated native program
        args=[sys.executable, "-I", "-c", program],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    _verify_corpus_roundtrip(
        case=case,
        source=source,
        label=f"{case.capability.value}-{version.name}",
        produced_json=completed.stdout,
    )


@pytest.mark.parametrize(
    argnames="version", argvalues=list(Json5.VersionFormats)
)
def test_control_corpus_document_roundtrip(version: enum.Enum) -> None:
    """Parse the generated document and retain every control character.

    JSON5 supports the complete control-string corpus that Python rejects.
    Its native parser provides the document execution oracle, as in the
    existing JSON5 round-trip driver.
    """
    case = _CASES.document_case
    assert case.capability in Json5.variant_metadata.round_trip_capabilities
    source = input_for_capabilities(capabilities=frozenset({case.capability}))
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=make_spec(lang_cls=Json5, language_version=version),
        include_delimiters=True,
        wrap_in_file=False,
    )
    _verify_corpus_roundtrip(
        case=case,
        source=source,
        label=f"{case.capability.value}-{version.name}",
        produced_json=json.dumps(obj=json5_document.loads(source=result.code)),
    )
