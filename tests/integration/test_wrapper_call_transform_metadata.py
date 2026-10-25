"""Internal operand contracts for the native wrapper recipe."""

from typing import TYPE_CHECKING, Literal

import pytest
from pydantic import BaseModel, TypeAdapter

from literalizer import CallContext, InputFormat, Language
from literalizer.languages import Python, Yaml
from tests.toml_cases import load_toml_cases

from .call_cases import (
    WrapperCallTransform,
    call_transform_for_case,
    default_call_case_specs,
)
from .case_manifests import CallCaseSpec, CallTransform, CallWrapperSpec

if TYPE_CHECKING:
    from collections.abc import Callable


class _UsageCase(BaseModel, extra="forbid", frozen=True):
    """One wrapper and outer-transform operand-usage contract."""

    name: str
    arguments: tuple[Literal["call", "zipped"], ...]
    outer: str
    uses_zipped: bool


class _ErrorCase(BaseModel, extra="forbid", frozen=True):
    """One invalid direct invocation of an internal transform."""

    name: str
    language: Literal["Yaml", "Python"]
    has_zipped: bool
    per_element: bool
    message: str
    error: Literal["TypeError", "ValueError"]


class _WrapperCases(BaseModel, extra="forbid", frozen=True):
    """The internal metadata and invocation-error corpus."""

    cases: tuple[_UsageCase, ...]
    errors: tuple[_ErrorCase, ...]


_CASES = TypeAdapter(type=_WrapperCases).validate_python(
    load_toml_cases(name="wrapper_call_transforms")
)


def _config() -> CallCaseSpec:
    """Use the validated wrapper recipe from its golden fixtures."""
    return next(
        config
        for config in default_call_case_specs()
        if config.case_dir_name == "call_zip_opaque_emitted"
    )


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.cases, ids=lambda case: case.name
)
def test_wrapper_preserves_operand_usage(case: _UsageCase) -> None:
    """Outer callbacks retain usage metadata independently of native
    syntax.
    """
    config = _config().model_copy(
        update={
            "call_transform_wrapper": CallWrapperSpec(
                target="emit", arguments=case.arguments
            ),
            "transform_stub_param_names": tuple(
                f"argument{index}" for index in range(len(case.arguments))
            ),
            "call_transform": (
                CallTransform(template=case.outer)
                if len(case.outer) > 0
                else None
            ),
            "zip_source": "1",
            "zip_input_format": InputFormat.JSON,
        }
    )
    transform = call_transform_for_case(spec=Python(), config=config)
    assert isinstance(transform, WrapperCallTransform)
    assert transform.uses_zipped is case.uses_zipped


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.errors, ids=lambda case: case.name
)
def test_wrapper_rejects_invalid_invocation(case: _ErrorCase) -> None:
    """A malformed internal context fails before producing native
    source.
    """
    factories: dict[str, Callable[[], Language]] = {
        "Yaml": Yaml,
        "Python": Python,
    }
    transform = call_transform_for_case(
        spec=factories[case.language](),
        config=_config().model_copy(update={"per_element": case.per_element}),
    )
    assert transform is not None
    context = CallContext(
        call="call-value",
        index=0,
        row=(42,),
        zipped="zip-value" if case.has_zipped else None,
    )
    error = {"TypeError": TypeError, "ValueError": ValueError}[case.error]
    with pytest.raises(expected_exception=error, match=case.message):
        _ = transform(context)
