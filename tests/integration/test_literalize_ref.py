"""Tests for ``{"$ref": "name"}`` marker support in
:func:`literalizer.literalize`.
"""

import pytest

import literalizer
from literalizer.exceptions import UnsupportedIdentifierCaseError
from literalizer.languages import Python

from .literalize_ref_cases import _inject_stubs_before_variable


def test_ref_without_ref_case_treated_as_literal() -> None:
    """Without ref_case, $ref dicts are treated as ordinary literal
    dicts.
    """
    result = literalizer.literalize(
        source='{"$ref": "my_var"}',
        input_format=literalizer.InputFormat.JSON,
        language=Python(),
    )
    assert result.bare_code == '{\n    "$ref": "my_var",\n}'


def test_ref_with_mixed_list() -> None:
    """$ref among non-ref elements in a list renders as bare
    identifier.
    """
    result = literalizer.literalize(
        source='[{"$ref": "x"}, 1, 2]',
        input_format=literalizer.InputFormat.JSON,
        language=Python(),
        ref_case=literalizer.IdentifierCase.SNAKE,
    )
    assert result.bare_code == "(\n    x,\n    1,\n    2,\n)"


def test_ref_with_case_conversion() -> None:
    """Ref_case converts the identifier name."""
    result = literalizer.literalize(
        source='{"$ref": "myVar"}',
        input_format=literalizer.InputFormat.JSON,
        language=Python(),
        ref_case=literalizer.IdentifierCase.SNAKE,
    )
    assert result.bare_code == "my_var"


def test_ref_deep_nesting() -> None:
    """$ref at arbitrary depth renders as bare identifier."""
    result = literalizer.literalize(
        source='{"a": {"b": {"c": {"$ref": "deep"}}}}',
        input_format=literalizer.InputFormat.JSON,
        language=Python(),
        ref_case=literalizer.IdentifierCase.SNAKE,
    )
    assert result.bare_code == '{\n    "a": {"b": {"c": deep}},\n}'


def test_unsupported_ref_case_raises() -> None:
    """Passing an unsupported ref_case raises
    UnsupportedIdentifierCaseError.
    """
    with pytest.raises(expected_exception=UnsupportedIdentifierCaseError):
        literalizer.literalize(
            source='{"$ref": "my_var"}',
            input_format=literalizer.InputFormat.JSON,
            language=Python(),
            ref_case=literalizer.IdentifierCase.KEBAB,
        )


def test_inject_stubs_returns_code_unchanged_when_variable_absent() -> None:
    """No injection occurs when the variable name is absent from the code.

    Guards the fall-through path in ``_inject_stubs_before_variable``
    for languages whose generated code does not contain the variable
    name in a form the search can locate.
    """
    code = "x = 1\ny = 2\n"
    result = _inject_stubs_before_variable(
        code=code,
        variable_name="my_data",
        stub_codes=["stub_var = 'value'"],
    )
    assert result == code
