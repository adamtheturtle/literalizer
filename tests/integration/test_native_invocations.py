"""Compile-ready goldens for caller-owned native message signatures."""

import enum
import json
from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer

from .case_manifests import CaseManifest
from .native_invocation_cases import native_invocation_cases

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
        fragments.append(result.code)
    assert manifest.native_invocation is not None
    program = manifest.native_invocation.consumer_template.format(
        code="\n".join(fragments)
    )
    file_regression.check(contents=program, fullpath=golden_path)
