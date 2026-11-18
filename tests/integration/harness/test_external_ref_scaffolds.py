"""Typed scaffold refusals must not leave executable stale fixtures."""

import dataclasses
from functools import cached_property
from pathlib import Path
from typing import override

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import LanguageCls, SequenceFormatConfig
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import CSharp, Elm
from tests.integration import literalize_ref_cases
from tests.integration.case_manifests import load_case_manifest
from tests.integration.golden_outcomes import Rejection
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
        golden_path = rendering.golden_path(cases_dir=tmp_path)
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
