"""Typed scaffold refusals must not leave executable stale fixtures."""

from functools import cached_property
from pathlib import Path
from typing import override

import pytest
from pydantic import BaseModel, TypeAdapter
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import SequenceFormatConfig
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import CSharp
from tests.enum_members import enum_member_by_name
from tests.integration import literalize_ref_cases
from tests.integration.case_manifests import ManifestLanguage, RefCaseSpec
from tests.integration.language_specs import make_golden_path, make_spec
from tests.integration.literalize_ref_cases import external_assignment_spec
from tests.toml_cases import load_toml_cases


class _RefusalCase(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """A refused native scaffold and its stale fixture."""

    name: str
    directory: str
    input_name: str
    source: str
    manifest: str
    configuration: dict[str, object]
    language: ManifestLanguage
    version: str
    golden_name: str
    stale_contents: str


class _ArityCase(BaseModel, extra="forbid", frozen=True):
    """A fixed-length destination and incompatible source shape."""

    name: str
    directory: str
    explicit_choice: bool
    configuration: dict[str, object]
    raw_data: dict[str, str]
    message: str


class _Cases(BaseModel, extra="forbid", frozen=True):
    """External-reference scaffold inputs declared in TOML."""

    refusals: tuple[_RefusalCase, ...]
    arities: tuple[_ArityCase, ...]


_CASES = TypeAdapter(type=_Cases).validate_python(
    load_toml_cases(name="external_reference_scaffolds")
)


class _FixedLengthCSharp(CSharp):
    """A synthetic spec with only fixed-length sequence types."""

    @cached_property
    @override
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Keep the fixed default when trying alternative formats."""
        return CSharp().sequence_format_config


@pytest.mark.parametrize(argnames="regenerate", argvalues=[False, True])
@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.refusals, ids=lambda case: case.name
)
def test_refused_scaffold_handles_stale_fixture(
    *,
    tmp_path: Path,
    file_regression: FileRegressionFixture,
    regenerate: bool,
    regeneration_config: pytest.Config,
    case: _RefusalCase,
) -> None:
    """Verification reports stale output; regeneration removes it."""
    case_dir = tmp_path / case.directory
    case_dir.mkdir()
    _ = (case_dir / case.input_name).write_text(
        data=case.source, encoding="utf-8"
    )
    _ = (case_dir / "case.toml").write_text(
        data=case.manifest, encoding="utf-8"
    )
    config = RefCaseSpec.model_validate(
        obj=case.configuration, context={"case_dir_name": case.directory}
    )
    version = enum_member_by_name(
        enum_cls=case.language.VersionFormats, name=case.version
    )
    golden_path = make_golden_path(
        parent=case_dir,
        name=case.golden_name,
        extension=case.language.extension,
        lang_cls=case.language,
        version=version,
    )
    _ = golden_path.write_text(data=case.stale_contents, encoding="utf-8")
    outcome = pytest.skip.Exception if regenerate else pytest.fail.Exception
    with pytest.raises(expected_exception=outcome):
        literalize_ref_cases.run_literalize_ref_golden_case(
            config=config,
            lang_cls=case.language,
            spec=make_spec(lang_cls=case.language, language_version=version),
            golden_name=case.golden_name,
            cases_dir=tmp_path,
            file_regression=file_regression,
            ref_case=None,
            version=version,
            pytest_config=regeneration_config,
        )
    assert golden_path.exists() is not regenerate


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.arities, ids=lambda case: case.name
)
def test_fixed_length_destination_refuses_different_arity(
    case: _ArityCase,
) -> None:
    """Neither a forced tuple nor fixed-only formats can change native
    type.
    """
    spec = CSharp() if case.explicit_choice else _FixedLengthCSharp()
    config = RefCaseSpec.model_validate(
        obj={"sequence_format": None, **case.configuration},
        context={"case_dir_name": case.directory},
    )
    with pytest.raises(
        expected_exception=UnrepresentableInputError, match=case.message
    ):
        _ = external_assignment_spec(
            spec=spec,
            config=config,
            raw_data=dict(case.raw_data.items()),
        )
