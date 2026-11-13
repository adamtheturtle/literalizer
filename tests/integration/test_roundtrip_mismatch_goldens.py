"""Mismatch controls consume values from complete native golden
programs.
"""

import enum
import json
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
from pydantic import BaseModel

from literalizer.languages import Python
from scripts.roundtrip_common import verify

from .language_specs import make_golden_path


class _MismatchCase(BaseModel, extra="forbid", frozen=True):
    """An independent expectation that the native value must reject."""

    name: str
    expected_json: str
    exclude_keys: tuple[str, ...]


class _Cases(BaseModel, extra="forbid", frozen=True):
    """Every former handwritten JSON mismatch control."""

    mismatches: tuple[_MismatchCase, ...]


_CASES = _Cases.model_validate(
    obj=tomllib.loads(
        Path(__file__)
        .with_name(name="roundtrip_mismatch_cases.toml")
        .read_text(encoding="utf-8")
    )
)
_EMIT = (
    "import json,runpy,sys; "
    "print(json.dumps(runpy.run_path(sys.argv[1])['my_data'][sys.argv[2]]))"
)


@pytest.mark.parametrize(
    argnames="version", argvalues=list(Python.VersionFormats)
)
@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.mismatches, ids=lambda case: case.name
)
def test_native_golden_roundtrip_mismatch(
    case: _MismatchCase,
    version: enum.Enum,
    cases_dir: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Native values pass their input oracle and fail changed expectations."""
    case_dir = cases_dir / "roundtrip_verifier_mismatches"
    path = make_golden_path(
        parent=case_dir,
        name="Python",
        lang_cls=Python,
        version=version,
    )
    completed = subprocess.run(  # noqa: S603 - execute complete native fixtures
        args=[sys.executable, "-I", "-c", _EMIT, str(object=path), case.name],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    source = json.loads(
        s=(case_dir / "input.json").read_text(encoding="utf-8")
    )
    assert set(source) == {control.name for control in _CASES.mismatches}
    verify(
        label="native-input-control",
        produced_json=completed.stdout,
        exclude_keys=case.exclude_keys,
        expected_json=json.dumps(obj=source[case.name]),
    )
    with pytest.raises(expected_exception=SystemExit) as exc_info:
        verify(
            label="negative-control",
            produced_json=completed.stdout,
            exclude_keys=case.exclude_keys,
            expected_json=case.expected_json,
        )
    assert exc_info.value.code == 1
    assert "negative-control: round-trip mismatch" in capsys.readouterr().err
