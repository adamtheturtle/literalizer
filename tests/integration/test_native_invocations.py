"""Executable fixtures for caller-owned native message signatures."""

import enum
import json
from pathlib import Path
from typing import Literal

import pytest
from pydantic import BaseModel, TypeAdapter
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer

from .case_manifests import CaseManifest
from .golden_checks import check_golden
from .native_invocation_cases import native_invocation_cases
from .source_profiles import source_format_marks, source_profiles

type _MetadataTypeName = Literal["str", "int", "bool"]

_METADATA_TYPES: dict[_MetadataTypeName, type[object]] = {
    "str": str,
    "int": int,
    "bool": bool,
}


class _ExpectedMetadata(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """Public composition metadata retained with a compiling consumer."""

    source_data: literalizer.ValueInput
    required_types: frozenset[_MetadataTypeName]
    excluded_types: frozenset[_MetadataTypeName]
    is_call_statement: bool
    uses_existing_variable: bool


_EXPECTED_METADATA = TypeAdapter(type=_ExpectedMetadata)


_CASES = Path(__file__).parent / "cases"


@pytest.mark.parametrize(
    argnames=("manifest", "language", "version", "golden_path"),
    argvalues=[
        pytest.param(*case, marks=source_format_marks(lang_cls=case[1]))
        for case in native_invocation_cases(cases_dir=_CASES)
    ],
)
def test_native_invocation_golden(
    manifest: CaseManifest,
    language: literalizer.LanguageCls,
    version: enum.Enum,
    golden_path: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Retain every native recipe and metadata assertion in both
    profiles.
    """
    for profile in source_profiles(
        spec=language(language_version=version),
        lang_cls=language,
        name=golden_path.name,
    ):
        _native_invocation_golden(
            manifest=manifest,
            golden_path=golden_path.with_name(name=profile.name),
            file_regression=file_regression,
            spec=profile.spec,
        )


def _native_invocation_golden(
    manifest: CaseManifest,
    golden_path: Path,
    file_regression: FileRegressionFixture,
    spec: literalizer.Language,
) -> None:
    """Generate a real class consumer, not function-pointer stand-ins."""
    steps = json.loads(s=manifest.input.path.read_text(encoding="utf-8"))
    fragments: list[str] = []
    for step in steps:
        variable = step.get("variable")
        form = None
        if variable is not None:
            form = (
                literalizer.ExistingVariable(name=variable)
                if step.get("existing", False)
                else literalizer.NewVariable(
                    name=variable, modifiers=frozenset()
                )
            )
        zipped = step.get("zipped")
        placement = step.get("source_context")
        source_context = (
            literalizer.SourceContext(**placement)
            if placement is not None
            and vars(spec).get("source_format")
            is literalizer.SourceFormat.CANONICAL
            else None
        )
        if "literal" in step or "literal_source" in step:
            result = literalizer.literalize(
                source=step.get(
                    "literal_source", json.dumps(obj=step.get("literal"))
                ),
                input_format=literalizer.InputFormat[
                    step.get("literal_format", "JSON")
                ],
                language=spec,
                include_delimiters=step.get("include_delimiters", True),
                variable_form=form,
                pre_indent_level=2 if source_context is None else 0,
                source_context=source_context,
            )
        else:
            result = literalizer.literalize_native_calls(
                source=json.dumps(obj=step["rows"]),
                input_format=literalizer.InputFormat.JSON,
                language=spec,
                per_element=step.get("per_element", True),
                invocation=step["invocation"],
                variable_form=form,
                zip_source=None if zipped is None else json.dumps(obj=zipped),
                zip_input_format=None
                if zipped is None
                else literalizer.InputFormat.JSON,
                pre_indent_level=2 if source_context is None else 0,
                source_context=source_context,
            )
        metadata = step.get("expected_metadata")
        if metadata is not None:
            expected = _EXPECTED_METADATA.validate_python(metadata)
            assert result.source_data == expected.source_data
            required = {
                _METADATA_TYPES[name] for name in expected.required_types
            }
            excluded = {
                _METADATA_TYPES[name] for name in expected.excluded_types
            }
            assert required <= result.types_present
            assert excluded.isdisjoint(result.types_present)
            assert result.is_call_statement == expected.is_call_statement
            assert (
                result.uses_existing_variable
                == expected.uses_existing_variable
            )
        fragments.append(
            step.get("prefix", "") + result.code + step.get("suffix", "")
        )
    assert manifest.native_invocation is not None
    program = manifest.native_invocation.consumer_template.format(
        code="\n".join(fragments)
    )
    check_golden(
        contents=program,
        extension=golden_path.suffix,
        golden_path=golden_path,
        file_regression=file_regression,
    )
