"""Callable references do not require argument data or implementations."""

import pytest

from literalizer import Language, NativeCallError, describe_callable
from literalizer.exceptions import LiteralizerError
from literalizer.languages import JavaScript, ObjectiveC, Python


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
        (
            {"name": "tasks", "parameter-names": [], "selector": "tasks"},
            "tasks",
        ),
    ],
)
def test_direct_description(
    description: dict[str, object], expected: str
) -> None:
    """Compact references and zero-argument selectors are supported."""
    assert (
        describe_callable(language=ObjectiveC(), description=description)
        == expected
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
        {"selector": "accept:"},
        {"selector": "bad name"},
        {"return-annotation": "bool\rvoid"},
        {"space-before-paren": "true"},
        {"space-after-paren": 1},
        {"typo": True},
    ],
)
def test_invalid_description(override: dict[str, object]) -> None:
    """Invalid metadata fails even when no sample values exist."""
    with pytest.raises(expected_exception=LiteralizerError):
        _ = describe_callable(
            language=ObjectiveC(),
            description={"name": "accept", "parameter-names": [], **override},
        )


def test_missing_field() -> None:
    """Required parameter metadata is never inferred."""
    with pytest.raises(expected_exception=LiteralizerError):
        _ = describe_callable(
            language=Python(), description={"name": "accept"}
        )


def test_selector_capability() -> None:
    """Positional backends cannot silently emit message selectors."""
    with pytest.raises(
        expected_exception=NativeCallError, match="native message selectors"
    ):
        _ = describe_callable(
            language=Python(),
            description={
                "name": "accept",
                "parameter-names": [],
                "selector": "accept",
            },
        )
