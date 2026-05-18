"""Negative-path checks for ``literalize_call``.

Positive-path checks for individual language behaviors (Haskell ref
inference, Python kebab-non-support, Raku kebab support, etc.) live
in :mod:`tests.test_languages`.
"""

import re

import pytest

from literalizer import (
    BothVariableForms,
    IdentifierCase,
    InputFormat,
    NewVariable,
    literalize,
    literalize_call,
)
from literalizer.exceptions import (
    CallArgNotSupportedError,
    CallsNotSupportedByLanguageError,
    CallsNotSupportedByToolError,
    CommentSourceLengthMismatchError,
    CommentSourceMultilineError,
    DottedCallTargetNotSupportedError,
    ParameterCountMismatchError,
    PerElementNotListError,
    UnsupportedCallShapeError,
    UnsupportedIdentifierCaseError,
    VariableNameNotSupportedError,
    WrapInFileWithoutVariableNotSupportedError,
    ZipSourceWithoutInputFormatError,
    ZipValuesLengthMismatchError,
    ZipValuesWithoutCallTransformError,
)
from literalizer.languages import (
    Bash,
    Cobol,
    Dhall,
    Elm,
    Haskell,
    Hcl,
    JavaScript,
    Jsonnet,
    Nix,
    Python,
    Racket,
    Tcl,
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


def test_literalize_call_dotted_target_unsupported_raises() -> None:
    """Dotted ``target_function`` raises for languages without support."""
    with pytest.raises(
        expected_exception=DottedCallTargetNotSupportedError,
        match=(
            r"^Hcl does not support dotted call targets: "
            r"'module\.fn'$"
        ),
    ):
        literalize_call(
            source="[[1]]",
            input_format=InputFormat.JSON,
            language=Hcl(),
            target_function="module.fn",
            parameter_names=["a"],
        )


def test_literalize_call_dotted_target_unsupported_per_element_false() -> None:
    """Dotted ``target_function`` raises on the per_element=False path."""
    with pytest.raises(
        expected_exception=DottedCallTargetNotSupportedError,
        match=(
            r"^Hcl does not support dotted call targets: "
            r"'module\.fn'$"
        ),
    ):
        literalize_call(
            source="[1, 2]",
            input_format=InputFormat.JSON,
            language=Hcl(),
            target_function="module.fn",
            parameter_names=["data"],
            per_element=False,
        )


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


def test_literalize_call_comment_source_length_mismatch_raises() -> None:
    """``comment_source`` must have one entry per generated call."""
    with pytest.raises(
        expected_exception=CommentSourceLengthMismatchError,
        match=(
            r"^comment_source has 2 entry\(ies\) but 3 call\(s\) were "
            r"generated; the lengths must match$"
        ),
    ):
        literalize_call(
            source="[[1], [2], [3]]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["value"],
            comment_source=["first", "second"],
        )


def test_literalize_call_comment_source_multiline_entry_raises() -> None:
    """A ``comment_source`` entry may not span multiple lines."""
    with pytest.raises(
        expected_exception=CommentSourceMultilineError,
        match=(
            r"^comment_source entry at index 1 contains a newline; "
            r"trailing comments must be single-line$"
        ),
    ):
        literalize_call(
            source="[[1], [2]]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["value"],
            comment_source=["fine", "broken\ncomment"],
        )


def test_literalize_call_comment_source_unsupported_language_raises() -> None:
    """A non-empty ``comment_source`` is rejected for a language whose
    call-sequence form cannot carry a trailing comment.
    """
    with pytest.raises(
        expected_exception=UnsupportedCallShapeError,
        match=(
            r"^Jsonnet cannot represent this call shape: comment_source "
            r"trailing comments cannot be preserved in this language's "
            r"call-sequence form$"
        ),
    ):
        literalize_call(
            source="[[1], [2]]",
            input_format=InputFormat.JSON,
            language=Jsonnet(),
            target_function="process",
            parameter_names=["value"],
            comment_source=["note", ""],
        )


def test_literalize_call_empty_comment_source_allowed_everywhere() -> None:
    """All-empty ``comment_source`` emits no comment, so it is allowed
    even for a language that cannot carry a trailing comment.
    """
    result = literalize_call(
        source="[[1], [2]]",
        input_format=InputFormat.JSON,
        language=Jsonnet(),
        target_function="process",
        parameter_names=["value"],
        comment_source=["", ""],
    )
    assert result.code == "process(value=1)\nprocess(value=2)"


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


def test_literalize_call_wrap_in_file_standalone_comments_raises() -> None:
    """``wrap_in_file=True`` rejects standalone comments when the target
    language cannot represent them in wrapped output.
    """
    source = "# header\n- 1\n- 2\n"
    with pytest.raises(
        expected_exception=UnsupportedCallShapeError,
        match=(
            r"^Haskell cannot represent this call shape: standalone "
            r"comments cannot be preserved when wrapping calls in this "
            r"language$"
        ),
    ):
        literalize_call(
            source=source,
            input_format=InputFormat.YAML,
            language=Haskell(),
            target_function="process",
            parameter_names=["value"],
            wrap_in_file=True,
        )


def test_literalize_call_ref_case_unsupported_raises() -> None:
    """``ref_case`` outside the language's ``supported_ref_cases``
    raises.
    """
    with pytest.raises(
        expected_exception=UnsupportedIdentifierCaseError,
        match=r"^Python does not support identifier case 'KEBAB'$",
    ):
        literalize_call(
            source='[[{"$ref": "user_obj"}, 42]]',
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["data", "count"],
            ref_case=IdentifierCase.KEBAB,
        )


def test_literalize_ref_case_unsupported_raises() -> None:
    """``ref_case`` outside the language's ``supported_ref_cases``
    raises.
    """
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
            variable_form=BothVariableForms(name="x"),
            wrap_in_file=True,
        )


def test_literalize_variable_names_not_supported_raises() -> None:
    """``variable_form`` raises for languages without variable-name
    support.
    """
    with pytest.raises(
        expected_exception=VariableNameNotSupportedError,
        match=r"^Yaml does not support variable names: 'x'$",
    ):
        literalize(
            source="42",
            input_format=InputFormat.JSON,
            language=Yaml(),
            variable_form=BothVariableForms(name="x"),
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


def test_literalize_call_variable_form_multiple_calls_raises() -> None:
    """``variable_form`` with a ``per_element`` source of more than one
    element is rejected.

    A single name can bind only one call result, so a source producing
    several calls leaves it ambiguous which call's result to bind.
    """
    with pytest.raises(
        expected_exception=UnsupportedCallShapeError,
        match=(
            r"variable_form binds a single call result, but this input "
            r"produces 2 calls"
        ),
    ):
        literalize_call(
            source="[1, 2]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["value"],
            per_element=True,
            variable_form=NewVariable(name="result"),
        )


def test_literalize_call_variable_form_zero_calls_raises() -> None:
    """``variable_form`` with an empty ``per_element`` source is
    rejected.

    An empty top-level list produces no calls, so there is no result
    for the variable to bind.
    """
    with pytest.raises(
        expected_exception=UnsupportedCallShapeError,
        match=(
            r"variable_form binds a single call result, but this input "
            r"produces 0 calls"
        ),
    ):
        literalize_call(
            source="[]",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="process",
            parameter_names=["value"],
            per_element=True,
            variable_form=NewVariable(name="result"),
        )


def test_literalize_call_variable_form_statement_language_raises() -> None:
    """``variable_form`` on a language whose call form is a statement
    rather than an expression is rejected.

    Cobol's ``CALL`` is a statement: there is no expression to bind to
    a variable.
    """
    with pytest.raises(
        expected_exception=UnsupportedCallShapeError,
        match=(
            r"calls in this language are statements, not expressions, "
            r"so the call result cannot be bound to a variable"
        ),
    ):
        literalize_call(
            source="42",
            input_format=InputFormat.JSON,
            language=Cobol(),
            target_function="MAKE-WIDGET",
            parameter_names=["count"],
            per_element=False,
            variable_form=NewVariable(name="RESULT"),
        )


def test_literalize_call_variable_form_unsupported_variable_names_raises() -> (
    None
):
    """``variable_form`` on a language without ``supports_variable_names``
    raises ``VariableNameNotSupportedError``.
    """
    with pytest.raises(
        expected_exception=VariableNameNotSupportedError,
    ):
        literalize_call(
            source="42",
            input_format=InputFormat.JSON,
            language=Jsonnet(),
            target_function="make_widget",
            parameter_names=["count"],
            per_element=False,
            variable_form=NewVariable(name="result"),
        )


def test_literalize_call_both_variable_forms_unsupported_raises() -> None:
    """``BothVariableForms`` is unconditionally rejected for
    ``literalize_call`` because rendering both halves would invoke the
    target function twice.
    """
    with pytest.raises(
        expected_exception=UnsupportedCallShapeError,
        match=(
            r"BothVariableForms is not supported for literalize_call: "
            r"rendering both a declaration and an assignment would "
            r"invoke the target function twice"
        ),
    ):
        literalize_call(
            source="42",
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="make_widget",
            parameter_names=["count"],
            per_element=False,
            variable_form=BothVariableForms(name="result"),
        )


def test_literalize_call_bound_refs_with_variable_form_raises() -> None:
    """``bound_refs`` combined with ``variable_form`` is rejected:
    ``bound_refs`` declares the call's input refs, not a binding for
    the call result, and the declaration-composition path cannot apply
    a language's call-result binding file scaffold.
    """
    with pytest.raises(
        expected_exception=UnsupportedCallShapeError,
        match=(
            r"variable_form cannot be combined with bound_refs; "
            r"bound_refs declares the call's input refs, not a "
            r"binding for the call result"
        ),
    ):
        literalize_call(
            source='{"$ref": "my_list"}',
            input_format=InputFormat.JSON,
            language=Python(),
            target_function="make_widget",
            parameter_names=["data"],
            per_element=False,
            wrap_in_file=True,
            bound_refs={"my_list": [1, 2, 3]},
            variable_form=NewVariable(name="result"),
        )
