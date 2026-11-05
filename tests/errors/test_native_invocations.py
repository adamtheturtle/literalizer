"""Data-driven rejections for structured native invocation contracts."""

import json
import tomllib
from pathlib import Path

import pytest

import literalizer
from literalizer.languages import Java, ObjectiveC, Python

_CASES = tomllib.loads(
    (Path(__file__).parent / "native_invocations.toml").read_text(
        encoding="utf-8"
    )
)["case"]


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES, ids=[case["name"] for case in _CASES]
)
def test_native_invocation_rejections(case: dict[str, object]) -> None:
    """Reject malformed recipes before emitting invalid native source."""
    spec = json.loads(s=str(object=case["recipe"]))
    bind = case.get("bind")
    variable = (
        None
        if bind is None
        else literalizer.NewVariable(
            name=str(object=bind), modifiers=frozenset()
        )
    )
    zip_source = case.get("zip_source")
    with pytest.raises(
        expected_exception=literalizer.LiteralizerError,
        match=str(object=case["match"]),
    ):
        _ = literalizer.literalize_native_calls(
            source=str(object=case["source"]),
            input_format=literalizer.InputFormat.JSON,
            language=Python()
            if case.get("language") == "python"
            else ObjectiveC(
                native_continuation_indent=int(
                    str(object=case.get("continuation_indent", 1))
                ),
                native_column_limit=int(
                    str(object=case.get("column_limit", 80))
                ),
            ),
            invocation=spec,
            variable_form=variable,
            zip_source=None if zip_source is None else str(object=zip_source),
            zip_input_format=literalizer.InputFormat.JSON
            if zip_source is not None or case.get("zip_format_only") is True
            else None,
            pre_indent_level=int(str(object=case.get("indent", 0))),
            initial_column=int(str(object=case.get("initial_column", 0))),
        )


@pytest.mark.parametrize(
    argnames="value", argvalues=[object(), {(): "invalid key"}]
)
def test_opaque_native_recipe_literals_are_rejected(value: object) -> None:
    """Python-only values outside serialized data also receive diagnostics."""
    with pytest.raises(
        expected_exception=literalizer.NativeCallError, match="Native literal"
    ):
        _ = literalizer.native_invocation_from_data(
            spec={
                "function": "consume",
                "parameter-types": ["id"],
                "return-type": "void",
                "arguments": [{"literal": value}],
            },
            values=[],
        )


def test_native_binding_rejects_foreign_modifiers() -> None:
    """Reject modifiers owned by another language."""
    with pytest.raises(
        expected_exception=literalizer.NativeCallError,
        match="do not accept modifiers",
    ):
        _ = literalizer.literalize_native_call(
            language=ObjectiveC(),
            invocation=literalizer.NativeInvocation(
                target=literalizer.ConstructorTarget(class_name="NSObject"),
                arguments=(),
            ),
            variable_form=literalizer.NewVariable(
                name="created", modifiers=frozenset({Java.modifiers.FINAL})
            ),
        )


def test_native_capability_can_be_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A backend can opt out even when it provides the native
    callbacks.
    """
    monkeypatch.setattr(
        target=ObjectiveC, name="supports_native_invocations", value=False
    )
    with pytest.raises(
        expected_exception=literalizer.NativeCallError,
        match="does not support",
    ):
        _ = literalizer.literalize_native_call(
            language=ObjectiveC(),
            invocation=literalizer.NativeInvocation(
                target=literalizer.ConstructorTarget(class_name="NSObject"),
                arguments=(),
            ),
        )
