"""Shared recipes retain the established call and native contracts."""

import pytest
from typing_extensions import TypedDict

from literalizer import (
    ExistingVariable,
    InputFormat,
    Language,
    LanguageCls,
    NativeCallError,
    NewVariable,
    literalize_call,
    literalize_invocations,
)
from literalizer._enums import enum_payload
from literalizer._language import (
    CallSupport,
    KeywordCallStyle,
    ObjectCallStyle,
    PositionalCallStyle,
)
from literalizer.exceptions import LiteralizerError
from literalizer.languages import ALL_LANGUAGES

_LANGUAGES: list[LanguageCls] = sorted(
    ALL_LANGUAGES, key=lambda cls: cls.__name__
)


class _BindingOptions(TypedDict, closed=True):
    """A caller-owned result binding."""

    source: str
    input_format: InputFormat
    language: Language
    variable_form: NewVariable | ExistingVariable


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
            _ = literalize_invocations(**kwargs, invocation=invocation)
    else:
        assert (
            literalize_invocations(**kwargs, invocation=invocation) == expected
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
@pytest.mark.parametrize(argnames="language_cls", argvalues=_LANGUAGES)
def test_invalid_shared_recipes(
    recipe: dict[str, object], message: str, language_cls: LanguageCls
) -> None:
    """Malformed metadata is rejected before input rendering."""
    with pytest.raises(expected_exception=NativeCallError, match=message):
        _ = literalize_invocations(
            source="[[]]",
            input_format=InputFormat.JSON,
            language=language_cls(),
            invocation=recipe,
        )


@pytest.mark.parametrize(argnames="indent", argvalues=[-1, 0])
@pytest.mark.parametrize(argnames="language_cls", argvalues=_LANGUAGES)
def test_invalid_generic_placement(
    indent: int, language_cls: LanguageCls
) -> None:
    """Unsupported placement must never be silently ignored."""
    with pytest.raises(
        expected_exception=NativeCallError, match="nonnegative indent"
    ):
        _ = literalize_invocations(
            source="[[]]",
            input_format=InputFormat.JSON,
            language=language_cls(),
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
@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=[
        cls
        for cls in _LANGUAGES
        if isinstance(
            cls().call_style_config,
            (PositionalCallStyle, KeywordCallStyle, ObjectCallStyle),
        )
        and any(
            isinstance(
                enum_payload(member=style, payload_type=object),
                PositionalCallStyle,
            )
            for style in cls.CallStyles
        )
    ],
)
def test_expected_values_are_required_and_paired(
    zip_source: str | None, message: str, language_cls: LanguageCls
) -> None:
    """Checks cannot drop missing or mismatched expected results."""
    with pytest.raises(expected_exception=LiteralizerError, match=message):
        _ = literalize_invocations(
            source="[[1]]",
            input_format=InputFormat.JSON,
            language=language_cls(),
            invocation={
                "default": {
                    "target-function": "consume",
                    "parameter-names": ["value"],
                    "result-function": "check_result",
                }
            },
            zip_source=zip_source,
            zip_input_format=None if zip_source is None else InputFormat.JSON,
        )


@pytest.mark.parametrize(argnames="language_cls", argvalues=_LANGUAGES)
def test_empty_checked_calls_still_require_expected_source(
    language_cls: LanguageCls,
) -> None:
    """An empty input cannot hide an incomplete expected-value
    contract.
    """
    with pytest.raises(
        expected_exception=NativeCallError, match="requires zipped"
    ):
        _ = literalize_invocations(
            source="[]",
            input_format=InputFormat.JSON,
            language=language_cls(),
            invocation={
                "default": {
                    "target-function": "consume",
                    "parameter-names": ["value"],
                    "result-function": "check_result",
                }
            },
        )


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=[
        cls
        for cls in _LANGUAGES
        if not isinstance(cls().call_style_config, CallSupport)
        and not any(
            isinstance(
                enum_payload(member=style, payload_type=object),
                PositionalCallStyle,
            )
            for style in cls.CallStyles
        )
    ],
)
def test_checker_rejects_non_expression_call_backend(
    language_cls: LanguageCls,
) -> None:
    """A positional checker cannot be guessed for a prefix-call
    backend.
    """
    with pytest.raises(
        expected_exception=NativeCallError, match="positional expression"
    ):
        _ = literalize_invocations(
            source="[[1]]",
            input_format=InputFormat.JSON,
            zip_source="[true]",
            zip_input_format=InputFormat.JSON,
            language=language_cls(),
            invocation={
                "default": {
                    "target-function": "consume",
                    "parameter-names": ["value"],
                    "result-function": "check_result",
                },
            },
        )


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=[cls for cls in _LANGUAGES if cls.pygments_name is not None],
)
def test_invalid_selected_override(language_cls: LanguageCls) -> None:
    """Malformed overrides fail for the backend they actually address."""
    with pytest.raises(
        expected_exception=NativeCallError, match="string-keyed"
    ):
        _ = literalize_invocations(
            source="[[]]",
            input_format=InputFormat.JSON,
            language=language_cls(),
            invocation={
                "default": {},
                "languages": {language_cls.pygments_name: []},
            },
        )
