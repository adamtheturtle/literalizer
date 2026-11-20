"""Error contracts for internal call checks."""

import pytest

from literalizer import (
    ExistingVariable,
    InputFormat,
    NewVariable,
    literalize_call,
)
from literalizer.exceptions import VariableNameNotSupportedError
from literalizer.languages import Jsonnet
from tests.integration.call_collection import default_call_case_specs
from tests.integration.call_expectations import (
    expected_call_shape_exception,
)


@pytest.mark.parametrize(
    argnames="variable_form",
    argvalues=[
        NewVariable(name="result", modifiers=frozenset()),
        ExistingVariable(name="result"),
    ],
)
def test_call_binding_requires_variable_name_support(
    variable_form: NewVariable | ExistingVariable,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Call syntax alone cannot enable result bindings.

    Every current callable backend supports names. Disable that independent
    capability to retain the rejection contract for future backends.
    """
    monkeypatch.setattr(
        target=Jsonnet, name="supports_variable_names", value=False
    )
    assert (
        expected_call_shape_exception(
            lang_cls=Jsonnet,
            config=default_call_case_specs()[0].model_copy(
                update={"variable_form": variable_form}
            ),
            spec=Jsonnet(),
        )
        is VariableNameNotSupportedError
    )
    with pytest.raises(expected_exception=VariableNameNotSupportedError):
        _ = literalize_call(
            source="1",
            input_format=InputFormat.JSON,
            language=Jsonnet(),
            target_function="consume",
            parameter_names=("value",),
            variable_form=variable_form,
            per_element=False,
        )
