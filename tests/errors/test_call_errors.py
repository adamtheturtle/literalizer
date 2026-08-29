"""Call refusals a rejection manifest cannot declare.

Most of ``literalize_call``'s negative paths are declared in
``tests/errors/rejections`` and run by ``test_rejections.py``.  What is
left here needs something a manifest has no field for: a
``call_transform`` callable, a ``zip_source`` beside it, a bare
``ValueError`` rather than a ``literalizer.exceptions`` type, an
explicit ``variable_form=None``, or a call made straight to an
internal check.
"""

import inspect
import re

import pytest

from literalizer import (
    BothVariableForms,
    InputFormat,
    literalize,
    literalize_call,
)
from literalizer._language import validate_call_parameter_names
from literalizer.exceptions import (
    PerElementNotListError,
    UnsupportedCallShapeError,
    WrapInFileWithoutVariableNotSupportedError,
    ZipInputFormatWithoutSourceError,
    ZipSourceWithoutInputFormatError,
    ZipValuesLengthMismatchError,
    ZipValuesWithoutCallTransformError,
)
from literalizer.languages import Elm, Haskell, Python, Tcl


def test_call_parameter_validation_requires_language_metaclass() -> None:
    """Malformed internal language objects fail immediately."""
    validator = inspect.unwrap(func=validate_call_parameter_names)
    with pytest.raises(
        expected_exception=TypeError,
        match="requires a LanguageCls language",
    ):
        validator(language=object(), names=(), reject_reserved=True)


def test_literalize_call_transform_rejected_for_non_substitution_style() -> (
    None
):
    """``call_transform`` is unsupported for prefix/postfix/command
    call styles whose language-native wrapper cannot be synthesized
    from a context-aware transform.
    """
    with pytest.raises(
        expected_exception=UnsupportedCallShapeError,
        match=(
            r"^Tcl cannot represent this call shape: call_transform is "
            r"only supported for languages whose call form is an "
            r"expression that can be wrapped"
        ),
    ):
        literalize_call(
            source="[[1]]",
            input_format=InputFormat.JSON,
            language=Tcl(),
            target_function="process",
            parameter_names=["value"],
            call_transform=lambda ctx: f"emit({ctx.call})",
        )


def test_literalize_call_zip_source_length_mismatch_raises() -> None:
    """``zip_source`` must parse to one element per generated call."""
    with pytest.raises(
        expected_exception=ZipValuesLengthMismatchError,
        match=(
            r"^zip_source parsed to 3 element\(s\) but 2 call\(s\) were "
            r"generated; the lengths must match$"
        ),
    ):
        literalize_call(
            source="[[1], [2]]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["value"],
            call_transform=lambda ctx: f"emit({ctx.call}, {ctx.zipped})",
            zip_source="[true, false, true]",
            zip_input_format=InputFormat.JSON,
        )


def test_literalize_call_zip_source_without_transform_raises() -> None:
    """``zip_source`` values are only reachable through
    ``call_transform``.
    """
    with pytest.raises(
        expected_exception=ZipValuesWithoutCallTransformError,
        match=(
            r"^zip_source was supplied without a call_transform; the "
            r"paired values would be unused$"
        ),
    ):
        literalize_call(
            source="[[1], [2]]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["value"],
            zip_source="[true, false]",
            zip_input_format=InputFormat.JSON,
        )


def test_literalize_call_zip_source_without_input_format_raises() -> None:
    """``zip_source`` cannot be parsed without a ``zip_input_format``."""
    with pytest.raises(
        expected_exception=ZipSourceWithoutInputFormatError,
        match=(
            r"^zip_source was supplied without a zip_input_format; the "
            r"companion source cannot be parsed without its format$"
        ),
    ):
        literalize_call(
            source="[[1], [2]]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["value"],
            call_transform=lambda ctx: f"emit({ctx.call}, {ctx.zipped})",
            zip_source="[true, false]",
        )


def test_literalize_call_zip_input_format_without_source_raises() -> None:
    """``zip_input_format`` cannot be silently ignored."""
    with pytest.raises(
        expected_exception=ZipInputFormatWithoutSourceError,
        match=(
            r"^zip_input_format was supplied without a zip_source; there is "
            r"no companion source to parse$"
        ),
    ):
        literalize_call(
            source="[[1]]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["value"],
            zip_input_format=InputFormat.JSON,
        )


def test_literalize_call_zip_source_per_element_non_list_raises() -> None:
    """``per_element=True`` requires ``zip_source`` to parse to a list."""
    with pytest.raises(
        expected_exception=PerElementNotListError,
        match=(
            r"^per_element=True requires zip_source to parse to a "
            r"top-level list, got str$"
        ),
    ):
        literalize_call(
            source="[[1], [2]]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["value"],
            call_transform=lambda ctx: f"emit({ctx.call}, {ctx.zipped})",
            zip_source='"not a list"',
            zip_input_format=InputFormat.JSON,
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
        literalize(
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
        literalize(
            source="42",
            input_format=InputFormat.JSON,
            language=Haskell(),
            variable_form=None,
            wrap_in_file=True,
        )
