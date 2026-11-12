"""Executable fixtures for caller-owned native message signatures."""

import dataclasses
import enum
import json
from pathlib import Path
from typing import Literal

import pytest
from pydantic import BaseModel
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer.languages import ObjectiveC, Python

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


_CASES = Path(__file__).parent / "cases"


@pytest.mark.parametrize(
    argnames="api", argvalues=["native", "shared", "bare"]
)
@pytest.mark.parametrize(
    argnames=("manifest", "language", "version", "golden_path"),
    argvalues=native_invocation_cases(cases_dir=_CASES),
)
def test_native_invocation_golden(
    *,
    api: Literal["native", "shared", "bare"],
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
        kwargs: dict[str, object] = {}
        for name, value in step.get("options", {}).items():
            current = vars(spec)[name]
            kwargs[name] = (
                type(current)[value]
                if isinstance(current, enum.Enum)
                else value
            )
        step_spec = dataclasses.replace(spec, **kwargs)
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
        if step.get("single", False):
            result = literalizer.literalize_native_call(
                language=step_spec,
                invocation=literalizer.native_invocation_from_data(
                    spec=step["invocation"], values=()
                ),
                variable_form=form,
                initial_column=step.get("initial_column", 0),
                pre_indent_level=step.get("pre_indent_level", 2),
            )
        else:
            invocation = step["invocation"]
            render = literalizer.literalize_native_calls
            if api != "native":
                render = literalizer.literalize_invocations
                if api == "shared":
                    invocation = {
                        "default": {
                            "target-function": "counter.accept",
                            "parameter-names": ["user", "timestamp"],
                            "result-function": "checkResult",
                        },
                        "languages": {
                            "python": {"result-function": "check_result"},
                            step_spec.pygments_name: {"native": invocation},
                        },
                    }
            result = render(
                source=json.dumps(obj=step["rows"]),
                input_format=literalizer.InputFormat.JSON,
                language=step_spec,
                per_element=step.get("per_element", True),
                invocation=invocation,
                variable_form=form,
                zip_source=None if zipped is None else json.dumps(obj=zipped),
                zip_input_format=None
                if zipped is None
                else literalizer.InputFormat.JSON,
                pre_indent_level=step.get("pre_indent_level", 2),
                initial_column=step.get("initial_column", 0),
            )
        metadata = step.get("expected_metadata")
        if metadata is not None:
            expected = _ExpectedMetadata.model_validate(obj=metadata)
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
        prefix = (
            " " * step.get("initial_column", 0)
            if step.get("prefix_initial_column", False)
            else ""
        )
        fragments.append(prefix + result.code)
    assert manifest.native_invocation is not None
    program = manifest.native_invocation.consumer_template.format(
        code="\n".join(fragments)
    )
    file_regression.check(contents=program, fullpath=golden_path)


def test_original_objective_c_native_callback() -> None:
    """Existing consumers can still invoke the original backend hook."""
    invocation = literalizer.NativeInvocation(
        target=literalizer.FunctionTarget(
            name="notify",
            parameter_types=(),
            return_type=literalizer.ScalarType.VOID,
        ),
        arguments=(),
    )
    assert (
        ObjectiveC.render_native_invocation(ObjectiveC(), invocation)
        == "notify()"
    )


class _LegacyNativeBackend(Python):
    """An existing native backend implementing only the original
    callback.
    """

    supports_native_invocations = True

    @staticmethod
    def render_native_invocation(
        _language: literalizer.Language,
        _invocation: literalizer.NativeInvocation,
        /,
    ) -> str:
        """Emit caller-owned syntax through the original callback."""
        return "legacyExpression()"

    @staticmethod
    def native_type_name(_native_type: object, /) -> str:
        """Supply the existing callback's binding type contract."""
        return "NativeValue"


def test_native_legacy_callback_still_works() -> None:
    """Existing backend callbacks need not implement positioned
    rendering.
    """
    result = literalizer.literalize_native_call(
        language=_LegacyNativeBackend(),
        invocation=literalizer.NativeInvocation(
            target=literalizer.ConstructorTarget(class_name="NSObject"),
            arguments=(),
        ),
        variable_form=literalizer.NewVariable(
            name="value", modifiers=frozenset()
        ),
    )
    assert result.declaration_code == "NativeValue value = legacyExpression();"
    with pytest.raises(
        expected_exception=literalizer.NativeCallError,
        match="does not support initial_column",
    ):
        _ = literalizer.literalize_native_call(
            language=_LegacyNativeBackend(),
            invocation=literalizer.NativeInvocation(
                target=literalizer.ConstructorTarget(class_name="NSObject"),
                arguments=(),
            ),
            initial_column=1,
        )
