"""Typed scaffold refusals must not leave executable stale fixtures."""

from functools import cached_property
from pathlib import Path
from typing import override

import pytest
from pydantic import BaseModel
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import SequenceFormatConfig
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import CSharp
from tests.enum_members import enum_member_by_name
from tests.integration import literalize_ref_cases
from tests.integration.case_manifests import (
    RefCaseSpec,
    load_case_manifest,
)
from tests.integration.language_specs import make_golden_path, make_spec
from tests.integration.manifest_values import (
    ManifestLanguage,
)
from tests.integration.ref_consumers import external_assignment_spec
from tests.integration.reference_cases import LiteralizeRefCase, RefRendering
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
    configuration: dict[str, object]
    raw_data: dict[str, str]
    message: str


class _Cases(BaseModel, extra="forbid", frozen=True):
    """External-reference scaffold inputs declared in TOML."""

    refusals: tuple[_RefusalCase, ...]
    arities: tuple[_ArityCase, ...]


_CASES = _Cases.model_validate(
    obj=load_toml_cases(name="external_reference_scaffolds")
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
        lang_cls=case.language,
        version=version,
    )
    _ = golden_path.write_text(data=case.stale_contents, encoding="utf-8")
    outcome = pytest.skip.Exception if regenerate else pytest.fail.Exception
    with pytest.raises(expected_exception=outcome):
        literalize_ref_cases.run_literalize_ref_golden_case(
            rendering=RefRendering(
                config=config,
                lang_cls=case.language,
                spec=make_spec(
                    lang_cls=case.language, language_version=version
                ),
                golden_name=case.golden_name,
                ref_case=None,
            ),
            cases_dir=tmp_path,
            file_regression=file_regression,
            pytest_config=regeneration_config,
        )
    assert golden_path.exists() is not regenerate


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.arities, ids=lambda case: case.name
)
def test_fixed_length_destination_refuses_different_arity(
    case: _ArityCase,
) -> None:
    """Fixed-only formats cannot change native type."""
    spec = _FixedLengthCSharp()
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


@pytest.mark.parametrize(argnames="regenerate", argvalues=[False, True])
@pytest.mark.parametrize(argnames="stale_fixture", argvalues=[False, True])
def test_explicit_tuple_arity_refusal_through_golden_runner(
    *,
    tmp_path: Path,
    file_regression: FileRegressionFixture,
    regenerate: bool,
    regeneration_config: pytest.Config,
    stale_fixture: bool,
) -> None:
    """A manifest-selected tuple refuses reassignment without leaving a
    runnable fixture.
    """
    case_dir = tmp_path / "external"
    case_dir.mkdir()
    _ = (case_dir / "input.json").write_text(
        data='{"$ref": "shared"}\n', encoding="utf-8"
    )
    _ = (case_dir / "case.toml").write_text(
        data=(
            "schema_version = 1\n"
            'owner = "literalize-ref-default"\n'
            "[ref]\n"
            'variable_form = "existing"\n'
            'sequence_format = "TUPLE"\n'
            "[ref.external_declarations]\n"
            'my_data = "[0]"\n'
            'shared = "[1, 2]"\n'
        ),
        encoding="utf-8",
    )
    manifest = load_case_manifest(case_dir=case_dir)
    assert manifest.ref is not None
    assert manifest.owner is not None
    case = LiteralizeRefCase(
        config=manifest.ref, lang_cls=CSharp, owner=manifest.owner
    )
    assert len(case.renderings) > 0
    for rendering in case.renderings:
        golden_path = rendering.golden_path(cases_dir=tmp_path)
        if stale_fixture:
            _ = golden_path.write_text(
                data="stale fixture\n", encoding="utf-8"
            )
        outcome = (
            pytest.fail.Exception
            if stale_fixture and not regenerate
            else pytest.skip.Exception
        )
        with pytest.raises(expected_exception=outcome) as caught:
            literalize_ref_cases.run_literalize_ref_golden_case(
                rendering=rendering,
                cases_dir=tmp_path,
                file_regression=file_regression,
                pytest_config=regeneration_config,
            )
        refusal = caught.value.__context__
        assert isinstance(refusal, UnrepresentableInputError)
        assert "cannot change length on reassignment" in str(object=refusal)
        assert golden_path.exists() is (stale_fixture and not regenerate)
        if golden_path.exists():
            assert golden_path.read_text(encoding="utf-8") == "stale fixture\n"
