"""Validation tests for case-local golden coverage manifests."""

from pathlib import Path

import pytest

import literalizer

from .case_manifests import (
    CaseManifestError,
    RenderContext,
    VariableFormName,
    case_manifests_by_name,
    load_case_manifest,
    variable_form_for_context,
)
from .variant_cases import build_variant_cases, validate_unique_variant_targets


def _write_case(
    *, tmp_path: Path, manifest: str, input_name: str = "input.yaml"
) -> Path:
    """Create one temporary case directory and return its path."""
    case_dir = tmp_path / "example"
    case_dir.mkdir()
    (case_dir / input_name).write_text(data="value: 1\n", encoding="utf-8")
    (case_dir / "case.toml").write_text(data=manifest, encoding="utf-8")
    return case_dir


@pytest.mark.parametrize(
    argnames=("manifest", "message"),
    argvalues=[
        ('schema_version = 2\nsuites = ["base"]\n', "schema_version"),
        ('schema_version = "1"\nsuites = ["base"]\n', "Input should be 1"),
        (
            'schema_version = 1\nsuites = ["base"]\nextra = true\n',
            "Extra inputs are not permitted",
        ),
        (
            'schema_version = 1\nowner = "mystery"\n',
            "Input should be 'literalize-call'",
        ),
        (
            (
                'schema_version = 1\nsuites = ["base"]\n'
                '[[variants]]\naxis = "made_up"\n'
            ),
            "unknown variant axis",
        ),
        (
            (
                'schema_version = 1\nsuites = ["base"]\n'
                '[[variants]]\naxis = "date"\n'
                '[[variants]]\naxis = "date"\n'
            ),
            "duplicate logical variant case",
        ),
        (
            'schema_version = 1\nsuites = ["base", "base"]\n',
            "suites contains a duplicate entry",
        ),
        (
            ('schema_version = 1\nsuites = ["base"]\nowner = "variant"\n'),
            "suites and owner are mutually exclusive",
        ),
        (
            "schema_version = 1\n",
            "declare suites or a specialized owner",
        ),
        (
            ('schema_version = 1\nsuites = ["combined"]\n[base_context]\n'),
            "base_context requires participation in the base suite",
        ),
    ],
)
def test_invalid_manifest_is_actionable(
    tmp_path: Path,
    manifest: str,
    message: str,
) -> None:
    """Invalid schema data reports the manifest and specific problem."""
    case_dir = _write_case(tmp_path=tmp_path, manifest=manifest)
    with pytest.raises(expected_exception=CaseManifestError, match=message):
        load_case_manifest(case_dir=case_dir)


def test_invalid_toml_is_actionable(tmp_path: Path) -> None:
    """TOML syntax errors retain the manifest path and parser detail."""
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest="schema_version = [\n",
    )
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="invalid TOML",
    ):
        load_case_manifest(case_dir=case_dir)


def test_missing_manifest_is_actionable(tmp_path: Path) -> None:
    """A case directory cannot silently participate without a manifest."""
    case_dir = tmp_path / "example"
    case_dir.mkdir()
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="manifest is missing",
    ):
        load_case_manifest(case_dir=case_dir)


def test_manifest_inventory_is_keyed_in_directory_order(
    tmp_path: Path,
) -> None:
    """The shared inventory preserves stable case-directory ordering."""
    for name in ("second", "first"):
        case_dir = tmp_path / name
        case_dir.mkdir()
        (case_dir / "input.yaml").write_text(
            data="value: 1\n",
            encoding="utf-8",
        )
        (case_dir / "case.toml").write_text(
            data='schema_version = 1\nsuites = ["base"]\n',
            encoding="utf-8",
        )

    manifests = case_manifests_by_name(cases_dir=tmp_path)
    assert tuple(manifests) == ("first", "second")
    assert manifests["first"].case_dir == tmp_path / "first"


def test_declared_input_must_exist(tmp_path: Path) -> None:
    """An explicit input cannot silently fall back to another file."""
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest=(
            'schema_version = 1\ninput = "input.json"\nsuites = ["base"]\n'
        ),
    )
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="declared input does not exist",
    ):
        load_case_manifest(case_dir=case_dir)


def test_render_context_is_loaded(tmp_path: Path) -> None:
    """Simple rendering arguments deserialize into the typed context."""
    expected_pre_indent_level = 2
    case_dir = _write_case(
        tmp_path=tmp_path,
        manifest=(
            "schema_version = 1\n"
            'suites = ["base", "combined"]\n'
            "[base_context]\n"
            'variable_form = "existing"\n'
            'collection_layout = "multiline"\n'
            "pre_indent_level = 2\n"
            "[base_context.record_null_substitutions]\n"
            "missing = -1\n"
        ),
    )
    context = load_case_manifest(case_dir=case_dir).base_context
    assert context.variable_form == "existing"
    assert context.collection_layout == "multiline"
    assert context.pre_indent_level == expected_pre_indent_level
    assert context.record_null_substitutions == {"missing": -1}


@pytest.mark.parametrize(
    argnames=("name", "expected_type"),
    argvalues=[
        ("new", literalizer.NewVariable),
        ("existing", literalizer.ExistingVariable),
        ("both", literalizer.BothVariableForms),
    ],
)
def test_variable_form_for_context(
    name: VariableFormName,
    expected_type: type[literalizer.VariableForm],
) -> None:
    """Every manifest variable form maps to its public API
    representation.
    """
    variable_form = variable_form_for_context(
        context=RenderContext(variable_form=name)
    )
    assert isinstance(variable_form, expected_type)


def test_duplicate_golden_target_is_actionable() -> None:
    """Resolved path collisions fail instead of disappearing into a
    set.
    """
    example = build_variant_cases()[0]
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="duplicate golden target",
    ):
        validate_unique_variant_targets(cases=[example, example])
