"""Shared semantic verification preserves JSON value distinctions."""

import pytest
from pydantic import BaseModel, TypeAdapter

from scripts.roundtrip_common import verify
from tests.toml_cases import load_toml_cases


class _RoundtripCase(BaseModel, extra="forbid", frozen=True):
    """One named manifest-owned regression scenario."""

    name: str
    expected_json: str
    produced_json: str
    exclude_keys: tuple[str, ...]


class _Cases(BaseModel, extra="forbid", frozen=True):
    """The complete declarative regression corpus."""

    mismatches: tuple[_RoundtripCase, ...]


_CASES = TypeAdapter(type=_Cases).validate_python(
    load_toml_cases(name="roundtrip_verifier")
)


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.mismatches, ids=lambda case: case.name
)
def test_roundtrip_mismatch(
    case: _RoundtripCase, capsys: pytest.CaptureFixture[str]
) -> None:
    """Changed JSON values fail with the existing mismatch diagnostic."""
    with pytest.raises(expected_exception=SystemExit) as exc_info:
        verify(
            label="negative-control",
            produced_json=case.produced_json,
            exclude_keys=case.exclude_keys,
            expected_json=case.expected_json,
        )
    assert exc_info.value.code == 1
    assert "negative-control: round-trip mismatch" in capsys.readouterr().err
