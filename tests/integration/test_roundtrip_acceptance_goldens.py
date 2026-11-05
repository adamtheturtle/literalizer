"""Passing comparison controls consume JSON from native golden
programs.
"""

import enum
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
from pydantic import BaseModel, TypeAdapter

from literalizer.languages import Python
from scripts.roundtrip_common import verify

from .language_specs import make_golden_path


class _AcceptanceCase(BaseModel, extra="forbid", frozen=True):
    """A complete native input and its independent comparison contract."""

    name: str
    case_name: str
    expected_json: str
    exclude_keys: tuple[str, ...]


_CASES = TypeAdapter(type=tuple[_AcceptanceCase, ...]).validate_python(
    tomllib.loads(
        Path(__file__)
        .with_name(name="roundtrip_acceptance_cases.toml")
        .read_text(encoding="utf-8")
    )["cases"]
)
_EMIT = (
    "import json,runpy,sys; "
    "print(json.dumps(runpy.run_path(sys.argv[1])['my_data']))"
)


@pytest.mark.parametrize(
    argnames="version", argvalues=list(Python.VersionFormats)
)
@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES, ids=lambda case: case.name
)
def test_native_golden_roundtrip_acceptance(
    case: _AcceptanceCase, version: enum.Enum, cases_dir: Path
) -> None:
    """Retain key exclusions and numeric equivalence for native values."""
    path = make_golden_path(
        parent=cases_dir / case.case_name,
        name="Python",
        extension=Python.extension,
        lang_cls=Python,
        version=version,
    )
    completed = subprocess.run(  # noqa: S603 - execute complete native fixtures
        args=[sys.executable, "-I", "-c", _EMIT, str(object=path)],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    verify(
        label="passing-control",
        produced_json=completed.stdout,
        exclude_keys=case.exclude_keys,
        expected_json=case.expected_json,
    )
