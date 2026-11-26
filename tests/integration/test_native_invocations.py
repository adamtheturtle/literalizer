"""Executable fixtures for caller-owned native message signatures."""

import dataclasses
import enum
import json
from pathlib import Path
from typing import TYPE_CHECKING, Literal, NotRequired, TypedDict

import pytest
from pydantic import BaseModel, TypeAdapter
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer.languages import ObjectiveC, Python

from .native_invocation_cases import (
    NativeInvocationCase,
    native_invocation_cases,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

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


class _Step(TypedDict):
    """An authored call step and its rendering options."""

    invocation: dict[str, object]
    rows: NotRequired[object]
    zipped: NotRequired[object]
    options: NotRequired[dict[str, str | int | bool]]
    variable: NotRequired[str]
    existing: NotRequired[bool]
    single: NotRequired[bool]
    per_element: NotRequired[bool]
    pre_indent_level: NotRequired[int]
    initial_column: NotRequired[int]
    prefix_initial_column: NotRequired[bool]
    expected_metadata: NotRequired[dict[str, object]]


_CASES = Path(__file__).parent / "cases"
_STEPS = TypeAdapter(type=list[_Step])


def _load_steps(*, path: Path) -> list[_Step]:
    """Read the authored steps for a native invocation case."""
    return _STEPS.validate_json(path.read_text(encoding="utf-8"), strict=True)


@pytest.mark.parametrize(
    argnames=("case", "api"),
    argvalues=[
        pytest.param(case, api, id=f"{case.test_id}-{api}")
        for case in native_invocation_cases(cases_dir=_CASES)
        for api in (
            ("native",)
            if all(
                step.get("single", False)
                for step in _load_steps(path=case.manifest.input.path)
            )
            else ("shared", "bare")
        )
    ],
)
def test_native_invocation_golden(
    *,
    api: Literal["native", "shared", "bare"],
    case: NativeInvocationCase,
    file_regression: FileRegressionFixture,
) -> None:
    """Generate a real class consumer, not function-pointer stand-ins."""
    manifest = case.manifest
    steps = _load_steps(path=manifest.input.path)
    spec = case.spec
    fragments: list[literalizer.LiteralizeResult] = []
    options: Mapping[str, object] = vars(spec)
    for step in steps:
        kwargs: dict[str, object] = {}
        for name, value in step.get("options", {}).items():
            current = options[name]
            kwargs[name] = (
                type(current)[value]
                if isinstance(current, enum.Enum) and isinstance(value, str)
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
        initial_column = step.get("initial_column", 0)
        if step.get("single", False):
            result = literalizer.literalize_call(
                language=step_spec,
                invocation=literalizer.native_invocation_from_data(
                    spec=step["invocation"], values=()
                ),
                variable_form=form,
                initial_column=initial_column,
                pre_indent_level=step.get("pre_indent_level", 2),
            )
        else:
            assert "rows" in step
            invocation: dict[str, object] = step["invocation"]
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
            result = literalizer.literalize_call(
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
                initial_column=initial_column,
            )
        expected_metadata = step.get("expected_metadata")
        if expected_metadata is not None:
            expected = _ExpectedMetadata.model_validate(obj=expected_metadata)
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
        prefix_initial_column = step.get("prefix_initial_column", False)
        prefix = " " * initial_column if prefix_initial_column else ""
        fragments.append(
            dataclasses.replace(
                result, declaration_code=prefix + result.declaration_code
            )
        )
    consumer = manifest.native_invocation
    assert consumer is not None
    last_call = fragments.pop()
    program = literalizer.literalize_call_with_declarations(
        language=dataclasses.replace(spec, module_name="main"),
        declarations=fragments,
        call=dataclasses.replace(
            last_call,
            declaration_code=(
                f"{last_call.declaration_code}\n{consumer.after_calls.rstrip()}"
            ),
        ),
        extra_body_preamble=(
            ()
            if consumer.before_calls is None
            else (consumer.before_calls.rstrip(),)
        ),
        extra_preamble=(consumer.file_declarations.rstrip(),),
    )
    file_regression.check(
        contents=program.code + "\n", fullpath=case.artifact.path
    )


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
    result = literalizer.literalize_call(
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
        _ = literalizer.literalize_call(
            language=_LegacyNativeBackend(),
            invocation=literalizer.NativeInvocation(
                target=literalizer.ConstructorTarget(class_name="NSObject"),
                arguments=(),
            ),
            initial_column=1,
        )


def test_deprecated_invocation_entry_point() -> None:
    """The released renderer accepts typed invocations and recipes."""
    language = ObjectiveC()
    recipe = {"constructor": "NSObject"}
    invocation = literalizer.native_invocation_from_data(
        spec=recipe, values=()
    )
    with pytest.warns(
        expected_warning=DeprecationWarning, match="Use literalize_call"
    ):
        typed = literalizer.literalize_invocations(
            language=language, invocation=invocation
        )
    assert typed == literalizer.literalize_call(
        language=language, invocation=invocation
    )
    with pytest.warns(
        expected_warning=DeprecationWarning, match="Use literalize_call"
    ):
        from_recipe = literalizer.literalize_invocations(
            source="[[]]",
            input_format=literalizer.InputFormat.JSON,
            language=language,
            invocation=recipe,
        )
    assert from_recipe == literalizer.literalize_call(
        source="[[]]",
        input_format=literalizer.InputFormat.JSON,
        language=language,
        invocation=recipe,
    )
