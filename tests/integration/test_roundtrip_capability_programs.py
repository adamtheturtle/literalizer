"""Capability corpora survive public rendering and native execution."""

import enum
import json
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
from pydantic import BaseModel, TypeAdapter

from literalizer import (
    InputFormat,
    NewVariable,
    RoundTripCapability,
    literalize,
)
from literalizer.languages import Python
from scripts.roundtrip_common import input_for_capabilities, verify

from .language_specs import make_spec


class _CapabilityCase(BaseModel, extra="forbid", frozen=True):
    """A capability's independent key and boundary-value expectations."""

    capability: RoundTripCapability
    expected_keys: frozenset[str]
    expected_values: dict[str, int]


_CASES = TypeAdapter(type=tuple[_CapabilityCase, ...]).validate_python(
    tomllib.loads(
        Path(__file__)
        .with_name(name="roundtrip_capability_cases.toml")
        .read_text(encoding="utf-8")
    )["capability_cases"]
)


@pytest.mark.parametrize(
    argnames="version", argvalues=list(Python.VersionFormats)
)
@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES, ids=lambda case: case.capability.value
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
    verify(
        label=f"{case.capability.value}-{version.name}",
        produced_json=completed.stdout,
        exclude_keys=(),
        expected_json=source,
    )
    base = json.loads(s=input_for_capabilities(capabilities=frozenset()))
    reconstructed = json.loads(s=completed.stdout)
    assert reconstructed.keys() - base.keys() == case.expected_keys
    assert {
        key: reconstructed[key] for key in case.expected_values
    } == case.expected_values
