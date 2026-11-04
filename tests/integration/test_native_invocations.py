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
from .native_invocation_cases import native_invocation_cases

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
    argvalues=native_invocation_cases(cases_dir=_CASES),
)
def test_native_invocation_golden(
    manifest: CaseManifest,
    language: literalizer.LanguageCls,
    version: enum.Enum,
    golden_path: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Generate a real class consumer, not function-pointer stand-ins."""
    steps = json.loads(s=manifest.input.path.read_text(encoding="utf-8"))
    spec = language(language_version=version)
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
            pre_indent_level=2,
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
        fragments.append(result.code)
    assert manifest.native_invocation is not None
    program = manifest.native_invocation.consumer_template.format(
        code="\n".join(fragments)
    )
    file_regression.check(contents=program, fullpath=golden_path)
