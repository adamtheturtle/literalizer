"""Negative-path checks for ``literalize_call``."""

import re

import pytest

from literalizer import (
    BothVariableForms,
    IdentifierCase,
    InputFormat,
    literalize,
    literalize_call,
)
from literalizer.exceptions import (
    CallArgNotSupportedError,
    CallsNotSupportedByLanguageError,
    CallsNotSupportedByToolError,
    DottedCallsNotSupportedError,
    ParameterCountMismatchError,
    PerElementNotListError,
    UnsupportedIdentifierCaseError,
    VariableNamesNotSupportedError,
)
from literalizer.languages import (
    Bash,
    Dart,
    Dhall,
    Hcl,
    JavaScript,
    Nix,
    Python,
    Racket,
    Yaml,
)


def test_dhall_literalize_call_rejects_non_scalar_arg() -> None:
    """Dhall call argument wrapping is restricted to scalar values."""
    with pytest.raises(
        expected_exception=CallArgNotSupportedError,
        match="Dhall call stubs only support scalar arguments",
    ):
        literalize_call(
            source="[[[]]]",
            input_format=InputFormat.JSON,
            language=Dhall(),
            target_function="consume",
            parameter_names=["value"],
        )


def test_literalize_call_per_element_non_list_raises() -> None:
    """Literalize_call raises PerElementNotListError for non-list."""
    with pytest.raises(
        expected_exception=PerElementNotListError,
        match=r"^per_element=True requires a top-level list, got str$",
    ):
        literalize_call(
            source='"hello"',
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["value"],
            per_element=True,
        )


def test_literalize_call_parameter_count_too_few_raises() -> None:
    """Literalize_call raises when fewer parameter_names than values."""
    with pytest.raises(
        expected_exception=ParameterCountMismatchError,
        match=r"^Expected 1 parameters but got 2 values$",
    ):
        literalize_call(
            source="[[1, 2]]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["a"],
        )


def test_literalize_call_parameter_count_too_many_raises() -> None:
    """Literalize_call raises when more parameter_names than values."""
    with pytest.raises(
        expected_exception=ParameterCountMismatchError,
        match=r"^Expected 3 parameters but got 2 values$",
    ):
        literalize_call(
            source="[[1, 2]]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["a", "b", "c"],
        )


def test_literalize_call_parameter_count_mismatch_object_style() -> None:
    """Literalize_call raises ParameterCountMismatchError for object
    styles.
    """
    with pytest.raises(
        expected_exception=ParameterCountMismatchError,
        match=r"^Expected 2 parameters but got 1 values$",
    ):
        literalize_call(
            source="[[1]]",
            input_format=InputFormat.JSON,
            language=JavaScript(),
            target_function="process",
            parameter_names=["a", "b"],
        )


def test_literalize_call_parameter_count_mismatch_prefix_style() -> None:
    """Literalize_call raises ParameterCountMismatchError for prefix
    styles.
    """
    with pytest.raises(
        expected_exception=ParameterCountMismatchError,
        match=r"^Expected 2 parameters but got 1 values$",
    ):
        literalize_call(
            source="[[1]]",
            input_format=InputFormat.JSON,
            language=Racket(),
            target_function="process",
            parameter_names=["a", "b"],
        )


def test_literalize_call_parameter_count_mismatch_later_row() -> None:
    """Literalize_call raises when a later row has a mismatched count."""
    with pytest.raises(
        expected_exception=ParameterCountMismatchError,
        match=r"^Expected 2 parameters but got 1 values$",
    ):
        literalize_call(
            source="[[1, 2], [3]]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["a", "b"],
        )


def test_literalize_call_language_without_calls_raises() -> None:
    """Literalize_call raises for a data-format language with no calls."""
    with pytest.raises(
        expected_exception=CallsNotSupportedByLanguageError,
        match=r"^Yaml has no function call syntax$",
    ):
        literalize_call(
            source="[[1, 2]]",
            input_format=InputFormat.JSON,
            language=Yaml(),
            target_function="f",
            parameter_names=["a", "b"],
        )


def test_literalize_call_language_without_calls_per_element_false() -> None:
    """Literalize_call raises for a data-format language without calls."""
    with pytest.raises(
        expected_exception=CallsNotSupportedByLanguageError,
        match=r"^Yaml has no function call syntax$",
    ):
        literalize_call(
            source="[1, 2]",
            input_format=InputFormat.JSON,
            language=Yaml(),
            target_function="f",
            parameter_names=["data"],
            per_element=False,
        )


def test_literalize_call_tool_unsupported_language_raises() -> None:
    """Literalize_call raises when call rendering is not implemented."""
    with pytest.raises(
        expected_exception=CallsNotSupportedByToolError,
        match=(
            r"^literalizer does not support function call rendering "
            r"for Nix$"
        ),
    ):
        literalize_call(
            source="[[1, 2]]",
            input_format=InputFormat.JSON,
            language=Nix(),
            target_function="f",
            parameter_names=["a", "b"],
        )


def test_literalize_call_tool_unsupported_language_per_element_false() -> None:
    """Literalize_call raises for unsupported call rendering."""
    with pytest.raises(
        expected_exception=CallsNotSupportedByToolError,
        match=(
            r"^literalizer does not support function call rendering "
            r"for Nix$"
        ),
    ):
        literalize_call(
            source="[1, 2]",
            input_format=InputFormat.JSON,
            language=Nix(),
            target_function="f",
            parameter_names=["data"],
            per_element=False,
        )


def test_literalize_call_bash_rejects_list_arg() -> None:
    """Bash raises when a call argument is a list."""
    with pytest.raises(
        expected_exception=CallArgNotSupportedError,
        match=(
            r"^Bash cannot accept this value as a call argument: "
            r"list values have no inline literal form"
        ),
    ):
        literalize_call(
            source="[[[1, 2, 3]]]",
            input_format=InputFormat.JSON,
            language=Bash(),
            target_function="cmd",
            parameter_names=["items"],
        )


def test_literalize_call_bash_rejects_dict_arg() -> None:
    """Bash raises when a call argument is a dict."""
    with pytest.raises(
        expected_exception=CallArgNotSupportedError,
        match=(
            r"^Bash cannot accept this value as a call argument: "
            r"dict values have no inline literal form"
        ),
    ):
        literalize_call(
            source='[[{"k": 1}]]',
            input_format=InputFormat.JSON,
            language=Bash(),
            target_function="cmd",
            parameter_names=["m"],
        )


def test_literalize_call_bash_rejects_list_arg_per_element_false() -> None:
    """Bash's call-argument guard fires on the per_element=False path."""
    with pytest.raises(
        expected_exception=CallArgNotSupportedError,
        match=r"^Bash cannot accept this value as a call argument",
    ):
        literalize_call(
            source="[1, 2, 3]",
            input_format=InputFormat.JSON,
            language=Bash(),
            target_function="cmd",
            parameter_names=["items"],
            per_element=False,
        )


def test_literalize_call_arg_ref_parameter_count_still_validated() -> None:
    """Refs count as arguments; parameter-count mismatch still raises."""
    with pytest.raises(
        expected_exception=ParameterCountMismatchError,
        match=r"^Expected 1 parameters but got 2 values$",
    ):
        literalize_call(
            source='[[{"$ref": "a"}, {"$ref": "b"}]]',
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="f",
            parameter_names=["only"],
        )


def test_literalize_call_ref_case_unsupported_raises() -> None:
    """``ref_case`` outside the language's ``IdentifierCases`` raises."""
    with pytest.raises(
        expected_exception=UnsupportedIdentifierCaseError,
        match=r"^Python does not support identifier case 'CAMEL'$",
    ):
        literalize_call(
            source='[[{"$ref": "user_obj"}, 42]]',
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["data", "count"],
            ref_case=IdentifierCase.CAMEL,
        )


def test_literalize_ref_case_unsupported_raises() -> None:
    """``ref_case`` outside the language's ``identifier_cases`` raises."""
    with pytest.raises(
        expected_exception=UnsupportedIdentifierCaseError,
        match=r"^Python does not support identifier case 'KEBAB'$",
    ):
        literalize(
            source='{"$ref": "my_var"}',
            input_format=InputFormat.JSON,
            language=Python(),
            ref_case=IdentifierCase.KEBAB,
        )


def test_literalize_variable_name_unsupported_raises() -> None:
    """Variable forms are rejected for languages without variable
    names.
    """
    with pytest.raises(
        expected_exception=VariableNamesNotSupportedError,
        match=r"^Yaml does not support variable names$",
    ):
        literalize(
            source="42",
            input_format=InputFormat.JSON,
            language=Yaml(),
            variable_form=BothVariableForms(name="x"),
            wrap_in_file=True,
        )


def test_literalize_call_dotted_target_unsupported_raises() -> None:
    """Dotted call targets are rejected for languages that cannot render
    them.
    """
    with pytest.raises(
        expected_exception=DottedCallsNotSupportedError,
        match=r"^Hcl does not support dotted call target 'client.fetch'$",
    ):
        literalize_call(
            source="[[1]]",
            input_format=InputFormat.JSON,
            language=Hcl(),
            target_function="client.fetch",
            parameter_names=["value"],
        )


def test_both_variable_forms_without_wrap_in_file_raises() -> None:
    """BothVariableForms without wrap_in_file=True raises ValueError."""
    expected_msg = "BothVariableForms requires wrap_in_file=True"
    with pytest.raises(
        expected_exception=ValueError,
        match=f"^{re.escape(pattern=expected_msg)}$",
    ):
        literalize(
            source="42",
            input_format=InputFormat.JSON,
            language=Python(),
            variable_form=BothVariableForms(name="x"),
        )


def test_both_variable_forms_without_redefinition_support_raises() -> None:
    """BothVariableForms raises when declaration_style cannot redefine."""
    expected = (
        "BothVariableForms requires a declaration_style that supports "
        "redefinition; 'FINAL' does not."
    )
    with pytest.raises(
        expected_exception=ValueError,
        match=rf"^{re.escape(pattern=expected)}$",
    ):
        literalize(
            source="42",
            input_format=InputFormat.JSON,
            language=Dart(),
            variable_form=BothVariableForms(name="x"),
            wrap_in_file=True,
        )
