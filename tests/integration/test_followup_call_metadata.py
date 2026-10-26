"""Native call-result operands retain their roles in follow-up stubs."""

import pytest

from literalizer import InputFormat

from .call_cases import followup_result_slots
from .case_manifests import CallCaseSpec


@pytest.mark.parametrize(
    argnames=("source", "parameters", "per_element", "expected"),
    argvalues=[
        (None, ("value",), False, frozenset[int]()),
        ('{"$ref": "my_data"}', ("value",), False, frozenset({0})),
        ('{"$ref": "seed"}', ("value",), False, frozenset[int]()),
        (
            '[[{"$ref": "my_data"}, 3]]',
            ("result", "literal"),
            True,
            frozenset({0}),
        ),
        (
            '[[3, {"$ref": "my_data"}]]',
            ("literal", "result"),
            True,
            frozenset({1}),
        ),
        ('[{"$ref": "my_data"}]', ("value",), True, frozenset({0})),
        ('[{"$ref": "my_data"}]', ("value",), False, frozenset[int]()),
        ('[[{"$ref": "my_data"}]]', ("value",), True, frozenset({0})),
        ('[[[{"$ref": "my_data"}]]]', ("value",), True, frozenset[int]()),
        (
            '{"value": {"$ref": "my_data"}}',
            ("value",),
            False,
            frozenset[int](),
        ),
        ("[]", ("value",), False, frozenset[int]()),
        ("null", ("value",), False, frozenset[int]()),
    ],
)
def test_followup_result_slots_preserve_operand_positions(
    *,
    source: str | None,
    parameters: tuple[str, ...],
    per_element: bool,
    expected: frozenset[int],
) -> None:
    """Whole values and per-element rows retain their actual argument
    roles.
    """
    config = CallCaseSpec.model_validate(
        obj={
            "target_function": "make_widget",
            "parameter_names": parameters,
            "per_element": per_element,
            "variable_form": "new",
            "followup_source": source,
        },
        context={"case_dir_name": "followup_operand_positions"},
    )
    assert (
        followup_result_slots(config=config, input_format=InputFormat.JSON)
        == expected
    )


def test_unbound_followup_has_no_call_result_operands() -> None:
    """A reference with no bound call result keeps its ordinary literal
    type.
    """
    config = CallCaseSpec.model_validate(
        obj={
            "target_function": "consume",
            "parameter_names": ["value"],
            "per_element": False,
            "followup_source": '{"$ref": "my_data"}',
        },
        context={"case_dir_name": "unbound_followup"},
    )
    assert (
        followup_result_slots(config=config, input_format=InputFormat.JSON)
        == frozenset()
    )
