"""Negative-path checks for ``literalize_call``."""

import re
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Mapping

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
    DottedCallStubNotSupportedError,
    DottedCallTargetNotSupportedError,
    FreeFunctionCallNotSupportedError,
    ParameterCountMismatchError,
    PerElementNotListError,
    UnsupportedCallShapeError,
    UnsupportedIdentifierCaseError,
    VariableNameNotSupportedError,
    WrapInFileWithoutVariableNotSupportedError,
)
from literalizer.languages import (
    Bash,
    Dhall,
    Elm,
    Haskell,
    Hcl,
    JavaScript,
    Nix,
    Python,
    Racket,
    Raku,
    Wren,
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


def test_literalize_call_dotted_target_supported_language() -> None:
    """Dotted ``target_function`` succeeds when the language supports
    it.
    """
    result = literalize_call(
        source="[[1]]",
        input_format=InputFormat.JSON,
        language=Python(),
        target_function="module.fn",
        parameter_names=["a"],
    )
    assert result.code == "module.fn(a=1)"


def test_literalize_call_dotted_stub_unsupported_raises() -> None:
    """Dotted ``call_transform`` wrapper raises for languages without
    support.
    """
    with pytest.raises(
        expected_exception=DottedCallStubNotSupportedError,
        match=(
            r"^Haskell does not support dotted call stubs: "
            r"'tracer\.emit'$"
        ),
    ):
        literalize_call(
            source="[[1]]",
            input_format=InputFormat.JSON,
            language=Haskell(),
            target_function="process",
            parameter_names=["value"],
            call_transform=lambda c: f"tracer.emit({c})",
        )


def test_literalize_call_free_function_unsupported_raises() -> None:
    """A bare ``call_transform`` wrapper name with no dot raises for
    languages without free function call syntax.
    """
    with pytest.raises(
        expected_exception=FreeFunctionCallNotSupportedError,
        match=(
            r"^Wren has no free function call syntax for call stub: "
            r"'emit'$"
        ),
    ):
        literalize_call(
            source="[[1]]",
            input_format=InputFormat.JSON,
            language=Wren(),
            target_function="Throttler.process",
            parameter_names=["value"],
            call_transform=lambda c: f"emit({c})",
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


def test_literalize_accepts_syntactic_non_idiomatic_ref_case() -> None:
    """Cases legal in the language but absent from the idiomatic
    preference list are accepted and rendered.

    Python's ``identifier_cases`` lists only ``SNAKE``, ``UPPER_SNAKE``,
    and ``PASCAL``; ``CAMEL`` is non-idiomatic but still a syntactically
    legal Python identifier.  Validation uses ``supported_ref_cases``,
    which exposes ``CAMEL``.
    """
    assert Python().identifier_cases == (
        IdentifierCase.SNAKE,
        IdentifierCase.UPPER_SNAKE,
        IdentifierCase.PASCAL,
    )
    assert Python().supported_ref_cases == frozenset(
        {
            IdentifierCase.SNAKE,
            IdentifierCase.UPPER_SNAKE,
            IdentifierCase.PASCAL,
            IdentifierCase.CAMEL,
        },
    )

    result = literalize(
        source='{"$ref": "user_obj"}',
        input_format=InputFormat.JSON,
        language=Python(),
        ref_case=IdentifierCase.CAMEL,
    )

    assert result.declaration_code == "userObj"


def test_literalize_kebab_friendly_language_accepts_kebab_ref_case() -> None:
    """Kebab-friendly languages render kebab-form refs as legal
    symbols.
    """
    assert Raku().supported_ref_cases == frozenset(
        {
            IdentifierCase.SNAKE,
            IdentifierCase.UPPER_SNAKE,
            IdentifierCase.PASCAL,
            IdentifierCase.CAMEL,
            IdentifierCase.KEBAB,
        },
    )

    result = literalize(
        source='{"$ref": "user_obj"}',
        input_format=InputFormat.JSON,
        language=Raku(),
        ref_case=IdentifierCase.KEBAB,
    )

    assert result.declaration_code == "$user-obj"


def test_supported_ref_cases_independent_of_identifier_cases() -> None:
    """``supported_ref_cases`` is not derived from ``identifier_cases``.

    The two attributes answer different questions -- syntactic validity
    vs. stylistic preference -- and one is not a function of the other.
    """
    python = Python()
    assert frozenset(python.identifier_cases) != python.supported_ref_cases
    assert frozenset(python.identifier_cases) <= python.supported_ref_cases

    raku = Raku()
    assert frozenset(raku.identifier_cases) != raku.supported_ref_cases
    assert frozenset(raku.identifier_cases) <= raku.supported_ref_cases


def test_literalize_call_unknown_ref_values_keep_strip_behavior() -> None:
    """Unknown refs still do not contribute marker dict types."""
    result = literalize_call(
        source='[[{"$ref": "myList"}]]',
        input_format=InputFormat.JSON,
        language=Haskell(),
        target_function="process",
        parameter_names=["data"],
        ref_values={},
    )

    assert result.types_present == frozenset({list})
    assert result.body_preamble == ("data Val = HList [Val]",)


def test_literalize_call_unknown_ref_values_strip_top_level_ref() -> None:
    """Unknown refs are stripped even when other ref values are
    supplied.
    """
    result = literalize_call(
        source='{"$ref": "myList"}',
        input_format=InputFormat.JSON,
        language=Haskell(),
        target_function="process",
        parameter_names=["data"],
        per_element=False,
        ref_values={"other": 1},
    )

    assert result.types_present == frozenset({list})
    assert result.body_preamble == ("data Val = HList [Val]",)


def test_literalize_call_unknown_refs_strip_from_nested_preamble() -> None:
    """Unknown nested refs do not shape preamble type inference."""
    ref_values: Mapping[str, int] = {"known": 42}
    result = literalize_call(
        source=(
            '[[{"$ref": "known"}, {"$ref": "missing"}, '
            '{"inner": {"$ref": "missing"}}]]'
        ),
        input_format=InputFormat.JSON,
        language=Haskell(),
        target_function="process",
        parameter_names=["a", "b", "c"],
        ref_values=ref_values,
    )

    assert result.body_preamble == (
        "data Val = HInt Integer | HStr String | HList [Val] | HMap "
        "[(String, Val)]",
        "instance Num Val where\n"
        "    fromInteger = HInt\n"
        '    _ + _ = error "not implemented"\n'
        '    _ * _ = error "not implemented"\n'
        '    abs _ = error "not implemented"\n'
        '    signum _ = error "not implemented"\n'
        "    negate (HInt n) = HInt (negate n)\n"
        '    negate _ = error "not implemented"',
    )


def test_literalize_call_without_ref_values_strips_top_level_ref() -> None:
    """The historical top-level ref strip behavior is retained."""
    result = literalize_call(
        source='{"$ref": "myList"}',
        input_format=InputFormat.JSON,
        language=Haskell(),
        target_function="process",
        parameter_names=["data"],
        per_element=False,
    )

    assert result.types_present == frozenset({list})
    assert result.body_preamble == ("data Val = HList [Val]",)


def test_literalize_call_without_ref_values_strips_per_element_ref() -> None:
    """Per-element preamble inference skips ref marker elements."""
    result = literalize_call(
        source='[{"$ref": "myList"}]',
        input_format=InputFormat.JSON,
        language=Haskell(),
        target_function="process",
        parameter_names=["data"],
    )

    assert result.types_present == frozenset({list})
    assert result.body_preamble == ("data Val = HList [Val]",)


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


def test_literalize_variable_names_supported_renders() -> None:
    """``variable_form`` succeeds for languages with variable-name
    support.
    """
    result = literalize(
        source="42",
        input_format=InputFormat.JSON,
        language=Python(),
        variable_form=BothVariableForms(name="x"),
        wrap_in_file=True,
    )
    assert result.code == "x = 42\nx = 42"
