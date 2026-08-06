"""Validation tests for test-owned language metadata files."""

from pathlib import Path

import pytest

from .language_metadata import (
    LANGUAGES_DIR,
    LanguageMetadataError,
    language_metadata,
    language_metadata_by_id,
    load_language_metadata,
)
from .language_specs import sorted_languages


def _write_metadata(*, tmp_path: Path, contents: str) -> Path:
    """Create one temporary metadata directory and return its path."""
    (tmp_path / "example.toml").write_text(data=contents, encoding="utf-8")
    return tmp_path


@pytest.mark.parametrize(
    argnames=("contents", "message"),
    argvalues=[
        ("schema_version = 2\n", "schema_version"),
        ('schema_version = "1"\n', "Input should be 1"),
        (
            "schema_version = 1\nextra = true\n",
            "Extra inputs are not permitted",
        ),
        (
            "schema_version = 1\n[golden]\nmystery = true\n",
            "Extra inputs are not permitted",
        ),
        (
            'schema_version = 1\n[variants]\nrecord = ["made_up"]\n',
            "Input should be 'unify_optional_fields'",
        ),
        (
            (
                "schema_version = 1\n[variants]\n"
                'record = ["keyword_field", "keyword_field"]\n'
            ),
            "record contains a duplicate entry",
        ),
        (
            (
                "schema_version = 1\n[variants]\n"
                'nested_map_widening = "sometimes"\n'
            ),
            "Input should be 'none'",
        ),
        (
            'schema_version = 1\n[golden]\ncollection_layout_category = ""\n',
            "at least 1 character",
        ),
    ],
)
def test_invalid_metadata_is_actionable(
    tmp_path: Path,
    contents: str,
    message: str,
) -> None:
    """Invalid schema data reports the file and the specific problem."""
    languages_dir = _write_metadata(tmp_path=tmp_path, contents=contents)
    with pytest.raises(
        expected_exception=LanguageMetadataError,
        match=message,
    ):
        load_language_metadata(
            languages_dir=languages_dir,
            language_id="example",
        )


def test_invalid_toml_is_actionable(tmp_path: Path) -> None:
    """TOML syntax errors retain the file path and parser detail."""
    languages_dir = _write_metadata(
        tmp_path=tmp_path,
        contents="schema_version = [\n",
    )
    with pytest.raises(
        expected_exception=LanguageMetadataError,
        match="invalid TOML",
    ):
        load_language_metadata(
            languages_dir=languages_dir,
            language_id="example",
        )


def test_missing_metadata_is_actionable(tmp_path: Path) -> None:
    """A language cannot silently participate without test metadata."""
    with pytest.raises(
        expected_exception=LanguageMetadataError,
        match="no test metadata for language 'mystery'",
    ):
        load_language_metadata(
            languages_dir=tmp_path,
            language_id="mystery",
        )


def test_every_language_declares_test_metadata() -> None:
    """Each production language resolves to one metadata file."""
    for lang_cls in sorted_languages():
        metadata = language_metadata(language_id=lang_cls.language_id)
        assert metadata.language_id == lang_cls.language_id


def test_no_orphan_metadata_files() -> None:
    """Every metadata file belongs to a language in the registry."""
    declared = {lang_cls.language_id for lang_cls in sorted_languages()}
    loaded = language_metadata_by_id(languages_dir=LANGUAGES_DIR)
    assert set(loaded) == declared


def test_defaults_apply_to_a_minimal_file(tmp_path: Path) -> None:
    """A language that opts into nothing still loads its policy."""
    languages_dir = _write_metadata(
        tmp_path=tmp_path,
        contents="schema_version = 1\n",
    )
    metadata = load_language_metadata(
        languages_dir=languages_dir,
        language_id="example",
    )
    assert metadata.golden.collection_layout_category == "collection_layout"
    assert metadata.golden.filename_lowercase is False
    assert metadata.variants.nested_map_widening == "none"
    assert metadata.record_variants == frozenset()
