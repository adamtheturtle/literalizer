"""TOML-driven validation for invalid native-input recipes."""

import re
from pathlib import Path

import pytest
from pydantic import BaseModel, TypeAdapter

from tests.toml_cases import load_toml_cases

from .rejection_manifests import (
    RejectionManifestError,
    load_rejection_manifest,
)


class _RecipeError(BaseModel, extra="forbid", frozen=True):
    """A malformed call recipe and its validation diagnostic."""

    name: str
    call: str
    message: str


class _RecipeErrors(BaseModel, extra="forbid", frozen=True):
    """The declarative recipe validation corpus."""

    cases: tuple[_RecipeError, ...]


_CASES = TypeAdapter(type=_RecipeErrors).validate_python(
    load_toml_cases(name="invalid_input_recipe_errors")
)


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.cases, ids=lambda case: case.name
)
def test_invalid_input_recipe(case: _RecipeError, tmp_path: Path) -> None:
    """Invalid construction requests fail before invoking Literalizer."""
    manifest_path = tmp_path / "rejection.toml"
    _ = manifest_path.write_text(
        data=(
            'schema_version = 1\nsummary = "invalid recipe"\n'
            'exceptions = ["InvalidValueInputError"]\n[call]\n' + case.call
        ),
        encoding="utf-8",
    )
    with pytest.raises(
        expected_exception=RejectionManifestError,
        match=re.escape(pattern=case.message),
    ):
        _ = load_rejection_manifest(manifest_path=manifest_path)
