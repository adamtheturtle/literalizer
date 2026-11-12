"""Callable references do not require argument data or implementations."""

from collections.abc import Callable

import pytest

from literalizer import (
    Language,
    LanguageCls,
    NativeCallError,
    describe_callable,
)
from literalizer.exceptions import LiteralizerError
from literalizer.languages import ALL_LANGUAGES, JavaScript, ObjectiveC, Python

_LANGUAGES = sorted(ALL_LANGUAGES, key=lambda cls: cls.__name__)


@pytest.mark.parametrize(
    argnames=("language", "expected"),
    argvalues=[
        (Python(), "allow_request ( user_id, timestamp) -> bool"),
        (JavaScript(), "allowRequest ( user_id, timestamp) -> bool"),
        (ObjectiveC(), "allowRequestFromUser:timestamp: -> BOOL"),
    ],
)
def test_shared_description(language: Language, expected: str) -> None:
    """Overrides replace spelling while the recipe stays unchanged."""
    recipe: dict[str, object] = {
        "default": {
            "name": "allow_request",
            "parameter-names": ["user_id", "timestamp"],
            "return-annotation": "bool",
            "space-before-paren": True,
            "space-after-paren": True,
        },
        "languages": {
            "javascript": {"name": "allowRequest"},
            "objective-c": {
                "selector": "allowRequestFromUser:timestamp:",
                "return-annotation": "BOOL",
            },
        },
    }
    assert describe_callable(language=language, description=recipe) == expected
    assert recipe["default"] == {
        "name": "allow_request",
        "parameter-names": ["user_id", "timestamp"],
        "return-annotation": "bool",
        "space-before-paren": True,
        "space-after-paren": True,
    }


@pytest.mark.parametrize(
    argnames=("description", "expected"),
    argvalues=[
        ({"name": "tasks", "parameter-names": []}, "tasks()"),
        ({"name": "cost", "parameter-names": ["task"]}, "cost(task)"),
    ],
)
@pytest.mark.parametrize(argnames="language_cls", argvalues=_LANGUAGES)
def test_direct_description(
    description: dict[str, object], expected: str, language_cls: LanguageCls
) -> None:
    """Compact callable references are portable display contracts."""
    assert (
        describe_callable(language=language_cls(), description=description)
        == expected
    )


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=[cls for cls in _LANGUAGES if cls.supports_native_invocations],
)
def test_zero_argument_selector(language_cls: LanguageCls) -> None:
    """Native-capable backends can describe a selector without
    arguments.
    """
    assert (
        describe_callable(
            language=language_cls(),
            description={
                "name": "tasks",
                "parameter-names": [],
                "selector": "tasks",
            },
        )
        == "tasks"
    )


@pytest.mark.parametrize(
    argnames="override",
    argvalues=[
        {"name": ""},
        {"name": "bad name"},
        {"name": "name\nother"},
        {"parameter-names": "task"},
        {"parameter-names": [2]},
        {"parameter-names": ["bad name"]},
        {"return-annotation": "bool\rvoid"},
        {"space-before-paren": "true"},
        {"space-after-paren": 1},
        {"typo": True},
    ],
)
@pytest.mark.parametrize(argnames="language_cls", argvalues=_LANGUAGES)
def test_invalid_description(
    override: dict[str, object], language_cls: LanguageCls
) -> None:
    """Invalid metadata fails even when no sample values exist."""
    with pytest.raises(expected_exception=LiteralizerError):
        _ = describe_callable(
            language=language_cls(),
            description={"name": "consume", "parameter-names": [], **override},
        )


@pytest.mark.parametrize(
    argnames="selector", argvalues=["consume:", "bad name"]
)
@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=[cls for cls in _LANGUAGES if cls.supports_native_invocations],
)
def test_invalid_native_selector(
    selector: str, language_cls: LanguageCls
) -> None:
    """Selector grammar and arity are checked where native messages
    apply.
    """
    with pytest.raises(expected_exception=NativeCallError):
        _ = describe_callable(
            language=language_cls(),
            description={
                "name": "consume",
                "parameter-names": [],
                "selector": selector,
            },
        )


@pytest.mark.parametrize(argnames="language_cls", argvalues=_LANGUAGES)
def test_missing_field(language_cls: LanguageCls) -> None:
    """Required parameter metadata is never inferred."""
    with pytest.raises(expected_exception=LiteralizerError):
        _ = describe_callable(
            language=language_cls(), description={"name": "accept"}
        )


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=[
        cls for cls in _LANGUAGES if not cls.supports_native_invocations
    ],
)
def test_selector_capability(language_cls: LanguageCls) -> None:
    """Positional backends cannot silently emit message selectors."""
    with pytest.raises(
        expected_exception=NativeCallError, match="native message selectors"
    ):
        _ = describe_callable(
            language=language_cls(),
            description={
                "name": "consume",
                "parameter-names": [],
                "selector": "consume",
            },
        )


def _rename(value: str) -> str:
    """Keep renamed function names valid for languages requiring lowercase."""
    return "renamed_" + value


@pytest.mark.parametrize(
    argnames=("shared", "name_renamer", "parameter_renamer", "expected"),
    argvalues=[
        (False, _rename, None, "renamed_accept_value(item_name) -> bool"),
        (True, _rename, None, "renamed_accept_value(item_name) -> bool"),
        (False, None, _rename, "accept_value(renamed_item_name) -> bool"),
        (True, None, _rename, "accept_value(renamed_item_name) -> bool"),
        (
            True,
            _rename,
            _rename,
            "renamed_accept_value(renamed_item_name) -> bool",
        ),
    ],
)
@pytest.mark.parametrize(argnames="language_cls", argvalues=_LANGUAGES)
def test_renamers(
    language_cls: LanguageCls,
    *,
    shared: bool,
    name_renamer: Callable[[str], str] | None,
    parameter_renamer: Callable[[str], str] | None,
    expected: str,
) -> None:
    """Caller naming policies transform canonical names without
    mutation.
    """
    default: dict[str, object] = {
        "name": "accept_value",
        "parameter-names": ["item_name"],
        "return-annotation": "bool",
    }
    description = {"default": default} if shared else default
    assert (
        describe_callable(
            language=language_cls(),
            description=description,
            name_renamer=name_renamer,
            parameter_renamer=parameter_renamer,
        )
        == expected
    )
    assert default == {
        "name": "accept_value",
        "parameter-names": ["item_name"],
        "return-annotation": "bool",
    }


@pytest.mark.parametrize(
    argnames=("override", "expected"),
    argvalues=[
        ({"name": "acceptValue"}, "acceptValue(ITEM_NAME) -> BOOL"),
        (
            {"parameter-names": ["requestURL"]},
            "ACCEPT_VALUE(requestURL) -> BOOL",
        ),
        (
            {"name": "acceptValue", "parameter-names": ["requestURL"]},
            "acceptValue(requestURL) -> BOOL",
        ),
        ({"selector": "acceptValue:"}, "acceptValue: -> BOOL"),
    ],
)
def test_overrides_after_renaming(
    override: dict[str, object], expected: str
) -> None:
    """Language-specific spellings, selectors and annotations remain exact."""
    assert (
        describe_callable(
            language=ObjectiveC(),
            description={
                "default": {
                    "name": "accept_value",
                    "parameter-names": ["item_name"],
                    "return-annotation": "BOOL",
                },
                "languages": {"objective-c": override},
            },
            name_renamer=str.upper,
            parameter_renamer=str.upper,
        )
        == expected
    )


def _invalid_name(value: str) -> str:
    """Return an invalid identifier through a well-typed callback."""
    return value + " invalid"


@pytest.mark.parametrize(
    argnames="field", argvalues=["name", "parameter-names"]
)
@pytest.mark.parametrize(argnames="language_cls", argvalues=_LANGUAGES)
def test_invalid_renamed_identifier(
    field: str, language_cls: LanguageCls
) -> None:
    """Callback results receive the same validation as explicit names."""
    with pytest.raises(expected_exception=LiteralizerError):
        _ = describe_callable(
            language=language_cls(),
            description={"name": "consume", "parameter-names": ["value"]},
            name_renamer=_invalid_name if field == "name" else None,
            parameter_renamer=_invalid_name
            if field == "parameter-names"
            else None,
        )
