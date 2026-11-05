"""Shared recipes retain the established call and native contracts."""

import subprocess
import sys
from typing import TypedDict

import pytest

from literalizer import (
    CallContext,
    ExistingVariable,
    InputFormat,
    Language,
    LanguageCls,
    NativeCallError,
    NewVariable,
    literalize_call,
    literalize_invocations,
    literalize_native_calls,
)
from literalizer.exceptions import LiteralizerError
from literalizer.languages import ALL_LANGUAGES, Clojure, ObjectiveC, Python

_LANGUAGES: list[LanguageCls] = sorted(
    ALL_LANGUAGES, key=lambda cls: cls.__name__
)

_NATIVE: dict[str, object] = {
    "function": "checkResult",
    "parameter-types": ["bool", "NSArray"],
    "return-type": "void",
    "arguments": [
        {
            "receiver": {"reference": "counter", "type": "Counter"},
            "selector": "accept:timestamp:",
            "parameter-types": ["NSString", "float"],
            "return-type": "bool",
            "arguments": [{"input": 0}, {"input": 1}],
        },
        {"zipped": True},
    ],
}

_CALL: dict[str, object] = {
    "default": {
        "target-function": "counter.accept",
        "parameter-names": ["user", "timestamp"],
        "result-function": "checkResult",
    },
    "languages": {
        "python": {"result-function": "check_result"},
        "objective-c": {"native": _NATIVE},
    },
}


class _CallOptions(TypedDict):
    """Shared typed arguments to both public APIs."""

    source: str
    input_format: InputFormat
    language: Language


class _ZippedOptions(_CallOptions):
    """A paired expected-value source."""

    zip_source: str
    zip_input_format: InputFormat


class _NativeOptions(_ZippedOptions):
    """Native placement arguments shared by the two APIs."""

    pre_indent_level: int
    initial_column: int


class _BindingOptions(_CallOptions):
    """A caller-owned result binding."""

    variable_form: NewVariable | ExistingVariable


def test_python_recipe_executes_with_paired_checks() -> None:
    """Generated checks actually call the receiver and retain row
    pairing.
    """
    result = literalize_invocations(
        source='[["user_1",100.0],["user_2",101.0]]',
        input_format=InputFormat.JSON,
        zip_source='[[true,"first"],[false,"second"]]',
        zip_input_format=InputFormat.JSON,
        language=Python(call_style=Python.call_styles["POSITIONAL"]),
        invocation=_CALL,
        pre_indent_level=1,
    )
    program = f"""
class Counter:
    def __init__(self):
        self.seen = []
    def accept(self, user, timestamp):
        self.seen.append((user, timestamp))
        return user == "user_1"
counter = Counter()
reasons = []
def check_result(actual, expected):
    assert actual is expected[0]
    reasons.append(expected[1])
def run():
{result.code}
run()
assert counter.seen == [("user_1", 100.0), ("user_2", 101.0)]
assert reasons == ["first", "second"]
"""
    _ = subprocess.run(  # noqa: S603 - execute generated test programs
        args=[sys.executable, "-c", program], check=True, capture_output=True
    )


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_LANGUAGES,
)
def test_generic_recipe_matches_existing_call_api(
    language_cls: LanguageCls,
) -> None:
    """Dispatch preserves existing backend output and rejection
    behavior.
    """
    language = language_cls()
    kwargs: _CallOptions = {
        "source": "[[1]]",
        "input_format": InputFormat.JSON,
        "language": language,
    }
    try:
        expected = literalize_call(
            **kwargs, target_function="consume", parameter_names=["value"]
        )
    except LiteralizerError as exc:
        with pytest.raises(expected_exception=type(exc)):
            literalize_invocations(
                **kwargs,
                invocation={
                    "default": {
                        "target-function": "consume",
                        "parameter-names": ["value"],
                    },
                },
            )
    else:
        assert (
            literalize_invocations(
                **kwargs,
                invocation={
                    "default": {
                        "target-function": "consume",
                        "parameter-names": ["value"],
                    },
                },
            )
            == expected
        )


@pytest.mark.parametrize(argnames="bare", argvalues=[False, True])
def test_native_override_preserves_typed_rendering(*, bare: bool) -> None:
    """Native overrides and existing bare recipes use the same
    renderer.
    """
    kwargs: _NativeOptions = {
        "source": '[["user_1",100.0]]',
        "input_format": InputFormat.JSON,
        "zip_source": '[[true,"first"]]',
        "zip_input_format": InputFormat.JSON,
        "language": ObjectiveC(),
        "pre_indent_level": 2,
        "initial_column": 3,
    }
    assert literalize_invocations(
        **kwargs, invocation=_NATIVE if bare else _CALL
    ) == literalize_native_calls(**kwargs, invocation=_NATIVE)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_LANGUAGES,
)
@pytest.mark.parametrize(argnames="existing", argvalues=[False, True])
def test_constructor_recipe_reuses_backend_syntax(
    language_cls: LanguageCls, *, existing: bool
) -> None:
    """Bindings use backend constructors and declaration/assignment
    rules.
    """
    language = language_cls()
    form = (
        ExistingVariable(name="counter")
        if existing
        else NewVariable(name="counter", modifiers=frozenset())
    )
    kwargs: _BindingOptions = {
        "source": "[[]]",
        "input_format": InputFormat.JSON,
        "language": language,
        "variable_form": form,
    }
    target = language.format_constructor_target("Counter")
    invocation: dict[str, object] = {
        "default": {"constructor-class": "Counter", "parameter-names": []},
    }
    try:
        expected = literalize_call(
            **kwargs, target_function=target, parameter_names=[]
        )
    except LiteralizerError as exc:
        with pytest.raises(expected_exception=type(exc)):
            literalize_invocations(**kwargs, invocation=invocation)
    else:
        assert (
            literalize_invocations(**kwargs, invocation=invocation) == expected
        )


def test_result_wrapper_matches_existing_transform() -> None:
    """The fixed positional check retains the former consumer output."""
    language = Python()

    def check(context: CallContext, /) -> str:
        """Retain the previous caller-authored transform as a
        comparison.
        """
        return f"check_result({context.call}, {context.zipped})"

    kwargs: _ZippedOptions = {
        "source": '[["user_1",100.0]]',
        "input_format": InputFormat.JSON,
        "zip_source": '[[true,"first"]]',
        "zip_input_format": InputFormat.JSON,
        "language": language,
    }
    assert literalize_invocations(
        **kwargs, invocation=_CALL
    ) == literalize_call(
        **kwargs,
        target_function="counter.accept",
        parameter_names=["user", "timestamp"],
        call_transform=check,
    )


@pytest.mark.parametrize(
    argnames=("recipe", "message"),
    argvalues=[
        ({"languages": {}}, "missing"),
        ({"default": {}, "typo": 1}, "unknown"),
        ({"default": {}, "languages": {"pyhton": {}}}, "Unknown invocation"),
        ({"default": {"parameter-names": []}}, "exactly one"),
        (
            {
                "default": {
                    "parameter-names": [],
                    "target-function": "f",
                    "constructor-class": "C",
                }
            },
            "exactly one",
        ),
        (
            {
                "default": {
                    "target-function": "f",
                    "parameter-names": [],
                    "typo": 1,
                }
            },
            "unknown",
        ),
        ({"default": [], "languages": {}}, "string-keyed"),
        ({"default": {}, "languages": {"python": []}}, "string-keyed"),
        ({"default": {"target-function": 1, "parameter-names": []}}, "string"),
        (
            {"default": {"target-function": "f", "parameter-names": "value"}},
            "list",
        ),
        (
            {"default": {"target-function": "f", "parameter-names": [1]}},
            "string",
        ),
        ({"default": {"native": {}, "target-function": "f"}}, "unknown"),
    ],
)
def test_invalid_shared_recipes(
    recipe: dict[str, object], message: str
) -> None:
    """Malformed metadata is rejected before input rendering."""
    with pytest.raises(expected_exception=NativeCallError, match=message):
        literalize_invocations(
            source="[[]]",
            input_format=InputFormat.JSON,
            language=Python(),
            invocation=recipe,
        )


@pytest.mark.parametrize(argnames="indent", argvalues=[-1, 0])
def test_invalid_generic_placement(indent: int) -> None:
    """Unsupported placement must never be silently ignored."""
    with pytest.raises(
        expected_exception=NativeCallError, match="nonnegative indent"
    ):
        literalize_invocations(
            source="[[]]",
            input_format=InputFormat.JSON,
            language=Python(),
            invocation={
                "default": {"target-function": "f", "parameter-names": []}
            },
            pre_indent_level=indent,
            initial_column=0 if indent < 0 else 1,
        )


@pytest.mark.parametrize(
    argnames=("zip_source", "message"),
    argvalues=[(None, "requires zipped"), ("[]", "length")],
)
def test_expected_values_are_required_and_paired(
    zip_source: str | None, message: str
) -> None:
    """Checks cannot drop missing or mismatched expected results."""
    with pytest.raises(expected_exception=LiteralizerError, match=message):
        literalize_invocations(
            source='[["user",1.0]]',
            input_format=InputFormat.JSON,
            language=Python(),
            invocation=_CALL,
            zip_source=zip_source,
            zip_input_format=None if zip_source is None else InputFormat.JSON,
        )


def test_empty_checked_calls_still_require_expected_source() -> None:
    """An empty input cannot hide an incomplete expected-value contract."""
    with pytest.raises(
        expected_exception=NativeCallError, match="requires zipped"
    ):
        literalize_invocations(
            source="[]",
            input_format=InputFormat.JSON,
            language=Python(),
            invocation=_CALL,
        )


def test_checker_rejects_non_expression_call_backend() -> None:
    """A positional checker cannot be guessed for a prefix-call backend."""
    with pytest.raises(
        expected_exception=NativeCallError, match="positional expression"
    ):
        literalize_invocations(
            source="[[1]]",
            input_format=InputFormat.JSON,
            zip_source="[true]",
            zip_input_format=InputFormat.JSON,
            language=Clojure(),
            invocation={
                "default": {
                    "target-function": "consume",
                    "parameter-names": ["value"],
                    "result-function": "check_result",
                },
            },
        )
