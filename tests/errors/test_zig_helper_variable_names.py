"""Zig bindings cannot shadow the helpers used by their output mode."""

import dataclasses

import pytest

from literalizer import (
    ExistingVariable,
    InputFormat,
    Language,
    NewVariable,
    literalize,
    literalize_call,
)
from literalizer.exceptions import ReservedVariableNameError
from literalizer.languages import Zig


@pytest.mark.parametrize(
    argnames=("language", "name"),
    argvalues=[
        (Zig(), "ZVal"),
        (Zig(), "ZKV"),
        (Zig(json_type=Zig.JsonTypes["STD_JSON_VALUE"]), "std"),
        (Zig(json_type=Zig.JsonTypes["STD_JSON_VALUE"]), "allocator"),
    ],
)
@pytest.mark.parametrize(argnames="wrap_in_file", argvalues=[False, True])
@pytest.mark.parametrize(argnames="existing", argvalues=[False, True])
def test_root_helper_name_is_rejected(
    *,
    language: Language,
    name: str,
    wrap_in_file: bool,
    existing: bool,
) -> None:
    """Declarations and assignments share the mode's occupied names."""
    variable_form = (
        ExistingVariable(name=name)
        if existing
        else NewVariable(name=name, modifiers=frozenset())
    )
    with pytest.raises(expected_exception=ReservedVariableNameError):
        _ = literalize(
            source='{"a":1}',
            input_format=InputFormat.JSON,
            language=language,
            variable_form=variable_form,
            wrap_in_file=wrap_in_file,
        )


@pytest.mark.parametrize(
    argnames=("language", "name"),
    argvalues=[
        (Zig(), "ZVal"),
        (Zig(), "ZKV"),
        (Zig(json_type=Zig.JsonTypes["STD_JSON_VALUE"]), "std"),
        (Zig(json_type=Zig.JsonTypes["STD_JSON_VALUE"]), "allocator"),
    ],
)
@pytest.mark.parametrize(argnames="wrap_in_file", argvalues=[False, True])
@pytest.mark.parametrize(argnames="call_argument", argvalues=[False, True])
def test_reference_helper_name_is_rejected(
    *,
    language: Language,
    name: str,
    wrap_in_file: bool,
    call_argument: bool,
) -> None:
    """Bound references use the same name checks as root bindings."""
    source = '{"$ref":"' + name + '"}'
    bound_refs = {name: {"a": 1}}
    if call_argument:
        with pytest.raises(expected_exception=ReservedVariableNameError):
            _ = literalize_call(
                source=source,
                input_format=InputFormat.JSON,
                language=language,
                target_function="process",
                parameter_names=["value"],
                per_element=False,
                ref_key="$ref",
                bound_refs=bound_refs,
                wrap_in_file=wrap_in_file,
            )
    else:
        with pytest.raises(expected_exception=ReservedVariableNameError):
            _ = literalize(
                source=source,
                input_format=InputFormat.JSON,
                language=language,
                variable_form=NewVariable(
                    name="my_data", modifiers=frozenset()
                ),
                ref_key="$ref",
                bound_refs=bound_refs,
                wrap_in_file=wrap_in_file,
            )


def test_replaced_spec_drops_previous_mode_reservations() -> None:
    """Derived binding metadata follows the options in a spec copy."""
    default = dataclasses.replace(
        Zig(json_type=Zig.JsonTypes["STD_JSON_VALUE"]), json_type=None
    )
    record = dataclasses.replace(
        Zig(), heterogeneous_strategy=Zig.HeterogeneousStrategies["RECORD"]
    )
    json = dataclasses.replace(
        Zig(), json_type=Zig.JsonTypes["STD_JSON_VALUE"]
    )
    assert default.reserved_variable_identifiers == (
        Zig().reserved_variable_identifiers
    )
    assert record.reserved_variable_identifiers == (
        Zig(
            heterogeneous_strategy=Zig.HeterogeneousStrategies["RECORD"]
        ).reserved_variable_identifiers
    )
    assert json.reserved_variable_identifiers == (
        Zig(
            json_type=Zig.JsonTypes["STD_JSON_VALUE"]
        ).reserved_variable_identifiers
    )
    assert json.reserved_identifiers == record.reserved_identifiers
