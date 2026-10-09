"""Public contracts for null reference knowledge and optional hints."""

from collections.abc import Mapping

import pytest

from literalizer import (
    ExistingVariable,
    InputFormat,
    ValueInput,
    literalize,
    literalize_call,
)
from literalizer.languages import Cpp, Python


@pytest.mark.parametrize(
    argnames=("ref_values", "expected_code", "expected_preamble"),
    argvalues=[
        (
            None,
            "my_data = std::move(item);",
            (
                "#include <initializer_list>",
                "#include <vector>",
                "#include <utility>",
            ),
        ),
        (
            {},
            "my_data = std::move(item);",
            (
                "#include <initializer_list>",
                "#include <vector>",
                "#include <utility>",
            ),
        ),
        (
            {"item": None},
            "my_data = item;",
            (
                "#include <initializer_list>",
                "#include <cstddef>",
                "#include <utility>",
            ),
        ),
    ],
)
def test_cpp_external_reference_assignment(
    ref_values: Mapping[str, ValueInput] | None,
    expected_code: str,
    expected_preamble: tuple[str, ...],
) -> None:
    """Known null assignments stay bare; missing metadata retains
    moves.
    """
    result = literalize(
        source='{"$ref": "item"}',
        input_format=InputFormat.JSON,
        language=Cpp(),
        variable_form=ExistingVariable(name="my_data"),
        ref_key="$ref",
        ref_values=ref_values,
    )
    assert result.code == expected_code
    assert result.preamble == expected_preamble


def test_python_known_null_reference() -> None:
    """Languages without null-specific formatting retain their
    behavior.
    """
    result = literalize(
        source='{"$ref": "item"}',
        input_format=InputFormat.JSON,
        language=Python(),
        variable_form=ExistingVariable(name="my_data"),
        ref_key="$ref",
        ref_values={"item": None},
    )
    assert (result.code, result.preamble) == ("my_data = item", ())


def test_cpp_json_null_reference_assignment() -> None:
    """A JSON null remains an owning JSON object rather than
    ``nullptr``.
    """
    result = literalize(
        source='{"$ref": "item"}',
        input_format=InputFormat.JSON,
        language=Cpp(json_type=Cpp.JsonTypes["NLOHMANN_JSON"]),
        variable_form=ExistingVariable(name="my_data"),
        ref_key="$ref",
        ref_values={"item": None},
    )
    assert result.code == "my_data = std::move(item);"
    assert result.preamble == (
        "#include <nlohmann/json.hpp>",
        "#include <utility>",
    )


@pytest.mark.parametrize(
    argnames=("bound_value", "hint", "expected_code"),
    argvalues=[
        ([1, 2], None, "consume(std::move(item));"),
        (None, [1, 2], "consume(item);"),
    ],
)
def test_cpp_null_consumption_uses_bound_value(
    bound_value: ValueInput, hint: ValueInput, expected_code: str
) -> None:
    """Actual bindings determine null ownership without replacing
    hints.
    """
    result = literalize_call(
        source='{"$ref": "item"}',
        input_format=InputFormat.JSON,
        language=Cpp(),
        target_function="consume",
        parameter_names=["value"],
        per_element=False,
        ref_key="$ref",
        bound_refs={"item": bound_value},
        ref_values={"item": hint},
        consumable_refs=frozenset({"item"}),
    )
    assert result.code == expected_code
    assert result.source_data == hint


@pytest.mark.parametrize(
    argnames=("ref_values", "expected_code"),
    argvalues=[
        (None, "consume(std::move(item));"),
        ({}, "consume(std::move(item));"),
        ({"item": None}, "consume(item);"),
    ],
)
def test_cpp_external_consumable_reference(
    ref_values: Mapping[str, ValueInput] | None, expected_code: str
) -> None:
    """Unknown external ownership retains the historical consuming
    form.
    """
    result = literalize_call(
        source='{"$ref": "item"}',
        input_format=InputFormat.JSON,
        language=Cpp(),
        target_function="consume",
        parameter_names=["value"],
        per_element=False,
        ref_key="$ref",
        ref_values=ref_values,
        consumable_refs=frozenset({"item"}),
    )
    assert result.code == expected_code
