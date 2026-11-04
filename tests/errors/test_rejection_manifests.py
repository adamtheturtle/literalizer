"""Validation tests for the declared rejection manifests."""

from pathlib import Path

import pytest
from beartype import beartype
from pydantic import BaseModel, TypeAdapter

from literalizer.languages import ALL_LANGUAGES
from tests.errors.rejection_cases import selected_languages
from tests.errors.rejection_manifests import (
    GOLDEN_NAME,
    MANIFEST_NAME,
    REJECTIONS_DIR,
    RejectionManifestError,
    load_rejection_manifest,
    load_rejection_manifests,
)
from tests.toml_cases import load_toml_cases


class _ManifestErrorCase(BaseModel, extra="forbid", frozen=True):
    """One named manifest-owned regression scenario."""

    name: str
    manifest: str
    message: str


class _Cases(BaseModel, extra="forbid", frozen=True):
    """The complete declarative regression corpus."""

    cases: tuple[_ManifestErrorCase, ...]


_CASES = TypeAdapter(type=_Cases).validate_python(
    load_toml_cases(name="rejection_manifest_validation")
)

_NO_EXTRA = ""
_CONSTRUCTOR = 'api = "constructor"'


@beartype
def _manifest(
    *,
    selection: str,
    extra: str,
    call: str,
) -> str:
    """Return a manifest with one part of a valid one replaced."""
    return (
        "schema_version = 1\n"
        'summary = "example"\n'
        'exceptions = ["IncompatibleFormatsError"]\n'
        f"{selection}\n{extra}\n[call]\n{call}\n"
    )


@beartype
def _write_manifest(*, tmp_path: Path, manifest: str) -> Path:
    """Create one temporary rejection directory and return its
    manifest.
    """
    rejection_dir = tmp_path / "example"
    rejection_dir.mkdir()
    manifest_path = rejection_dir / MANIFEST_NAME
    _ = manifest_path.write_text(data=manifest, encoding="utf-8")
    return manifest_path


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.cases, ids=lambda case: case.name
)
def test_invalid_manifest_is_rejected(
    case: _ManifestErrorCase, tmp_path: Path
) -> None:
    """Every declared inconsistency fails when the manifest loads."""
    manifest_path = _write_manifest(tmp_path=tmp_path, manifest=case.manifest)
    with pytest.raises(
        expected_exception=RejectionManifestError, match=case.message
    ):
        _ = load_rejection_manifest(manifest_path=manifest_path)


def test_directory_without_manifests_is_rejected(tmp_path: Path) -> None:
    """A rejections directory holding nothing is a mistake, not an
    empty suite.
    """
    with pytest.raises(
        expected_exception=RejectionManifestError,
        match=f"no {MANIFEST_NAME} found",
    ):
        _ = load_rejection_manifests(rejections_dir=tmp_path)


def test_every_rejection_directory_holds_exactly_its_two_files() -> None:
    """No rejection carries a stray file, and none is missing a
    golden.
    """
    expected = {MANIFEST_NAME, GOLDEN_NAME}
    for manifest in load_rejection_manifests(rejections_dir=REJECTIONS_DIR):
        found = {path.name for path in manifest.path.parent.iterdir()}
        assert found == expected, manifest.name


def test_every_rejection_directory_is_declared() -> None:
    """Every directory under ``rejections`` declares a manifest."""
    declared = {
        manifest.path.parent
        for manifest in load_rejection_manifests(
            rejections_dir=REJECTIONS_DIR,
        )
    }
    found = {path for path in REJECTIONS_DIR.iterdir() if path.is_dir()}
    assert found == declared


def test_scenario_without_gates_admits_every_language(tmp_path: Path) -> None:
    """New languages join a scenario without a manifest edit."""
    manifest = load_rejection_manifest(
        manifest_path=_write_manifest(
            tmp_path=tmp_path,
            manifest=_manifest(
                selection="",
                extra=_NO_EXTRA,
                call=_CONSTRUCTOR,
            ),
        ),
    )
    assert set(selected_languages(manifest=manifest)) == set(ALL_LANGUAGES)
