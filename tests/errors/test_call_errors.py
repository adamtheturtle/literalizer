"""Call refusals that should remain direct tests.

Most of ``literalize_call``'s negative paths are declared in
``tests/errors/rejections`` and run by ``test_rejections.py``.  What is
left here needs something a manifest should not encode: a bare ``ValueError``
rather than a ``literalizer.exceptions`` type, an explicit
``variable_form=None``, or a call made straight to an internal check.
"""

import inspect
import re

import pytest

from literalizer import (
    BothVariableForms,
    InputFormat,
    literalize,
)
from literalizer._language import validate_call_parameter_names
from literalizer.exceptions import WrapInFileWithoutVariableNotSupportedError
from literalizer.languages import Elm, Haskell, Python


def test_call_parameter_validation_requires_language_metaclass() -> None:
    """Malformed internal language objects fail immediately."""
    validator = inspect.unwrap(func=validate_call_parameter_names)
    with pytest.raises(
        expected_exception=TypeError,
        match="requires a LanguageCls language",
    ):
        validator(language=object(), names=(), reject_reserved=True)


def test_both_variable_forms_without_wrap_in_file_raises() -> None:
    """BothVariableForms without wrap_in_file=True raises ValueError."""
    expected_msg = "BothVariableForms requires wrap_in_file=True"
    with pytest.raises(
        expected_exception=ValueError,
        match=f"^{re.escape(pattern=expected_msg)}$",
    ):
        _ = literalize(
            source="42",
            input_format=InputFormat.JSON,
            language=Python(),
            variable_form=BothVariableForms(name="x", modifiers=frozenset()),
        )


def test_both_variable_forms_without_redefinition_support_raises() -> None:
    """BothVariableForms raises when declaration_style cannot redefine."""
    expected = (
        "BothVariableForms requires a declaration_style that supports "
        "redefinition; 'ASSIGN' does not."
    )
    with pytest.raises(
        expected_exception=ValueError,
        match=rf"^{re.escape(pattern=expected)}$",
    ):
        _ = literalize(
            source="42",
            input_format=InputFormat.JSON,
            language=Elm(),
            variable_form=BothVariableForms(name="x", modifiers=frozenset()),
            wrap_in_file=True,
        )


def test_literalize_wrap_in_file_without_variable_not_supported_raises() -> (
    None
):
    """``wrap_in_file=True, variable_form=None`` raises for languages
    that cannot represent a bare value at file scope.
    """
    with pytest.raises(
        expected_exception=WrapInFileWithoutVariableNotSupportedError,
        match=(
            r"^Haskell cannot wrap a bare value \(without a variable_form\) "
            r"at file scope$"
        ),
    ):
        _ = literalize(
            source="42",
            input_format=InputFormat.JSON,
            language=Haskell(),
            variable_form=None,
            wrap_in_file=True,
        )
