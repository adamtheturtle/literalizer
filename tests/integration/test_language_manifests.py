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
from .language_specs import make_spec, sorted_languages

_DEFAULT_TYPE_CAPABILITY_FIELDS = (
    "default_set_element_type",
    "default_sequence_element_type",
    "default_dict_value_type",
    "default_dict_key_type",
    "default_ordered_map_value_type",
)


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
            "Input should be 'empty_dict_field'",
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
        (
            (
                "schema_version = 1\n[variants.non_default_kwargs]\n"
                'type_name = ""\n'
            ),
            "at least 1 character",
        ),
        (
            (
                "schema_version = 1\n"
                "[variants.declaration_style_sequence_format_overrides]\n"
                "CONST = 3\n"
            ),
            "Input should be a valid string",
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


def test_non_default_kwargs_change_the_spec() -> None:
    """Every sample value must reach the constructor and change it.

    No production annotation types these keys any more, so this is what
    catches a misspelled one: an unknown field name raises ``TypeError``
    from the constructor, and a value equal to the default builds a
    fixture identical to the one it is supposed to vary.
    """
    for lang_cls in sorted_languages():
        metadata = language_metadata(language_id=lang_cls.language_id)
        default_spec = make_spec(lang_cls=lang_cls)
        for field_name, value in metadata.non_default_kwargs.items():
            variant_spec = make_spec(
                lang_cls=lang_cls,
                **{field_name: value},
            )
            assert variant_spec != default_spec, (
                f"{metadata.path}: {field_name}={value!r} is the default"
            )


def test_default_type_kwargs_match_capability_flags() -> None:
    """Default-type sample values track the flags that enable them."""
    for lang_cls in sorted_languages():
        metadata = language_metadata(language_id=lang_cls.language_id)
        supported = {
            field_name
            for field_name, is_supported in (
                (
                    "default_set_element_type",
                    lang_cls.supports_default_set_element_type,
                ),
                (
                    "default_sequence_element_type",
                    lang_cls.supports_default_sequence_element_type,
                ),
                (
                    "default_dict_value_type",
                    lang_cls.supports_default_dict_value_type,
                ),
                (
                    "default_dict_key_type",
                    lang_cls.supports_default_dict_key_type,
                ),
                (
                    "default_ordered_map_value_type",
                    lang_cls.supports_default_ordered_map_value_type,
                ),
            )
            if is_supported
        }
        configured = set(metadata.non_default_kwargs) & set(
            _DEFAULT_TYPE_CAPABILITY_FIELDS
        )
        assert configured == supported, (
            f"{metadata.path}: default-type sample values "
            f"{sorted(configured)} do not match the supported fields "
            f"{sorted(supported)}"
        )


def test_value_variant_name_settings_travel_together() -> None:
    """The value-variant-name settings stay consistent.

    The declared ``heterogeneous_value_variant_name`` plan reads the
    strategy (and, where declared, the language version) that its
    sample name is exercised with.  A language that names one without
    the other would leave a dead setting, or a variant that cannot be
    built.
    """
    for lang_cls in sorted_languages():
        metadata = language_metadata(language_id=lang_cls.language_id)
        variants = metadata.variants
        names_variant = (
            "heterogeneous_value_variant_name" in metadata.non_default_kwargs
        )
        strategy = variants.heterogeneous_value_variant_name_strategy
        version = variants.heterogeneous_value_variant_name_language_version

        assert names_variant == (strategy is not None), metadata.path
        assert names_variant or version is None, metadata.path


def test_declaration_style_overrides_name_real_formats() -> None:
    """Substituted formats must resolve against the language's enums."""
    for lang_cls in sorted_languages():
        metadata = language_metadata(language_id=lang_cls.language_id)
        overrides = metadata.declaration_style_sequence_format_overrides
        if not overrides:
            continue
        spec = make_spec(lang_cls=lang_cls)
        style_names = {style.name for style in spec.declaration_styles}
        format_names = {fmt.name for fmt in spec.sequence_formats}
        unknown_styles = set(overrides) - style_names
        unknown_formats = set(overrides.values()) - format_names
        assert not unknown_styles, (
            f"{metadata.path}: unknown declaration styles "
            f"{sorted(unknown_styles)}"
        )
        assert not unknown_formats, (
            f"{metadata.path}: unknown sequence formats "
            f"{sorted(unknown_formats)}"
        )


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
