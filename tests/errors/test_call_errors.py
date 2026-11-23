"""Error contracts for internal call checks."""

import pytest

from literalizer import (
    ExistingVariable,
    InputFormat,
    NewVariable,
    literalize_call,
)
from literalizer.exceptions import (
    UnrepresentableInputError,
    VariableNameNotSupportedError,
)
from literalizer.languages import Go, Jsonnet
from tests.integration.call_collection import default_call_case_specs
from tests.integration.call_expectations import (
    expected_call_shape_exception,
)


class _JsonnetWithoutVariableNames(Jsonnet):
    """Keep Jsonnet call syntax with result bindings disabled."""

    supports_variable_names = False


@pytest.mark.parametrize(
    argnames="variable_form",
    argvalues=[
        NewVariable(name="result", modifiers=frozenset()),
        ExistingVariable(name="result"),
    ],
)
def test_call_binding_requires_variable_name_support(
    variable_form: NewVariable | ExistingVariable,
) -> None:
    """Call syntax alone cannot enable result bindings.

    Every current callable backend supports names. The test language keeps
    that capability independent from call support.
    """
    spec = _JsonnetWithoutVariableNames()
    assert (
        expected_call_shape_exception(
            lang_cls=_JsonnetWithoutVariableNames,
            config=default_call_case_specs()[0].model_copy(
                update={"variable_form": variable_form}
            ),
            spec=spec,
        )
        is VariableNameNotSupportedError
    )
    with pytest.raises(expected_exception=VariableNameNotSupportedError):
        _ = literalize_call(
            source="1",
            input_format=InputFormat.JSON,
            language=spec,
            target_function="consume",
            parameter_names=("value",),
            variable_form=variable_form,
            per_element=False,
        )


@pytest.mark.parametrize(
    argnames=("source", "per_element"),
    argvalues=[
        ('{"items":[[],[{"name":"one"}]]}', False),
        ('[[{"items":[[],[{"name":"one"}]]}]]', True),
    ],
)
def test_go_record_call_rejects_empty_list_sibling(
    *, source: str, per_element: bool
) -> None:
    """Direct arguments have the same record-list constraints as
    literals.
    """
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="record list and its empty sibling",
    ):
        _ = literalize_call(
            source=source,
            input_format=InputFormat.JSON,
            language=Go(
                heterogeneous_strategy=Go.heterogeneous_strategies.RECORD,
            ),
            target_function="consume",
            parameter_names=("value",),
            per_element=per_element,
        )
