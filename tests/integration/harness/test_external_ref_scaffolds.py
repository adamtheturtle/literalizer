"""Typed scaffold refusals must not leave executable stale fixtures."""

import dataclasses
from functools import cached_property
from pathlib import Path
from typing import override

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import IdentifierCase, LanguageCls, SequenceFormatConfig
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import CSharp, Elm, Rust, Yaml
from tests.integration import literalize_ref_cases
from tests.integration.case_manifests import (
    REF_DEFAULT_OWNER,
    REF_OWNER,
    load_case_manifest,
)
from tests.integration.golden_outcomes import Exclusion, Rejection
from tests.integration.reference_cases import LiteralizeRefCase


class _FixedLengthCSharp(CSharp):
    """A synthetic spec with only fixed-length sequence types."""

    @cached_property
    @override
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Keep the fixed default when trying alternative formats."""
        return CSharp().sequence_format_config


@pytest.mark.parametrize(argnames="stale_fixture", argvalues=[False, True])
@pytest.mark.parametrize(
    argnames=("case_name", "lang_cls", "sequence_format", "message"),
    argvalues=[
        pytest.param(
            "literalize_ref_external_scalar_assignment",
            Elm,
            None,
            "the external destination needs a reassignable declaration",
            id="immutable_external_binding",
        ),
        pytest.param(
            "literalize_ref_external_array_assignment",
            _FixedLengthCSharp,
            None,
            "cannot change length on reassignment",
            id="fixed_only_destination",
        ),
        pytest.param(
            "literalize_ref_external_array_assignment",
            CSharp,
            "TUPLE",
            "cannot change length on reassignment",
            id="explicit_tuple",
        ),
    ],
)
def test_scaffold_refusal_through_golden_runner(
    *,
    cases_dir: Path,
    tmp_path: Path,
    file_regression: FileRegressionFixture,
    stale_fixture: bool,
    case_name: str,
    lang_cls: LanguageCls,
    sequence_format: str | None,
    message: str,
) -> None:
    """Assert a documented reference rejection through the full runner."""
    original = load_case_manifest(case_dir=cases_dir / case_name)
    case_dir = tmp_path / case_name
    case_dir.mkdir()
    _ = (case_dir / original.input.path.name).write_bytes(
        data=original.input.path.read_bytes()
    )
    manifest_source = original.path.read_text(encoding="utf-8")
    if sequence_format is not None:
        manifest_source = manifest_source.replace(
            "[ref]", f'[ref]\nsequence_format = "{sequence_format}"'
        )
    _ = (case_dir / "case.toml").write_text(
        data=manifest_source, encoding="utf-8"
    )
    manifest = load_case_manifest(case_dir=case_dir)
    assert manifest.ref is not None
    assert manifest.owner is not None
    case = LiteralizeRefCase(
        config=manifest.ref, lang_cls=lang_cls, owner=manifest.owner
    )
    assert len(case.renderings) > 0
    for rendering in case.renderings:
        rejected = dataclasses.replace(
            rendering,
            outcome=Rejection(error=UnrepresentableInputError, match=message),
        )
        golden_path = rendering.artifact(cases_dir=tmp_path).path
        if stale_fixture:
            _ = golden_path.write_text(
                data="stale fixture\n", encoding="utf-8"
            )
            with pytest.raises(
                expected_exception=pytest.fail.Exception,
                match="Unexpected success fixture",
            ):
                literalize_ref_cases.run_literalize_ref_golden_case(
                    rendering=rejected,
                    cases_dir=tmp_path,
                    file_regression=file_regression,
                )
            assert golden_path.read_text(encoding="utf-8") == "stale fixture\n"
        else:
            literalize_ref_cases.run_literalize_ref_golden_case(
                rendering=rejected,
                cases_dir=tmp_path,
                file_regression=file_regression,
            )
            assert not golden_path.exists()


def test_redefinition_checks_the_selected_declaration(cases_dir: Path) -> None:
    """An explicit immutable Rust style bypasses the mutable fallback."""
    manifest = load_case_manifest(
        case_dir=cases_dir / "literalize_ref_both_forms"
    )
    assert manifest.ref is not None
    assert manifest.owner is not None
    default = LiteralizeRefCase(
        config=manifest.ref, lang_cls=Rust, owner=manifest.owner
    )
    (mutable,) = default.renderings
    explicit = dataclasses.replace(
        default,
        config=manifest.ref.model_copy(update={"declaration_style": "LET"}),
    )
    (immutable,) = explicit.renderings
    assert not isinstance(mutable.outcome, Exclusion)
    assert (
        mutable.spec.declaration_style is not immutable.spec.declaration_style
    )
    assert isinstance(immutable.outcome, Exclusion)
    assert "does not permit redefinition" in immutable.outcome.reason


def test_external_consumer_requires_effective_call_syntax(
    cases_dir: Path,
) -> None:
    """A reference-only format cannot host a native consumer call."""
    manifest = load_case_manifest(
        case_dir=cases_dir / "external_scalar_reference"
    )
    assert manifest.ref is not None
    assert manifest.owner is not None
    case = LiteralizeRefCase(
        config=manifest.ref, lang_cls=Yaml, owner=manifest.owner
    )
    (rendering,) = case.renderings
    assert isinstance(rendering.outcome, Exclusion)
    assert "native reference consumer requires call syntax" in (
        rendering.outcome.reason
    )


def test_only_explicit_reference_spelling_is_a_prerequisite(
    cases_dir: Path,
) -> None:
    """An unsupported override excludes the explicit reference
    scenario.
    """
    manifest = load_case_manifest(
        case_dir=cases_dir / "literalize_ref_both_forms"
    )
    assert manifest.ref is not None
    case = LiteralizeRefCase(
        config=manifest.ref.model_copy(
            update={"ref_case_override": IdentifierCase.KEBAB}
        ),
        lang_cls=Rust,
        owner=REF_OWNER,
    )
    (explicit,) = case.renderings
    (default,) = dataclasses.replace(case, owner=REF_DEFAULT_OWNER).renderings
    assert isinstance(explicit.outcome, Exclusion)
    assert "unsupported reference spelling KEBAB" in explicit.outcome.reason
    assert default.ref_case is None
    assert not isinstance(default.outcome, Exclusion)
