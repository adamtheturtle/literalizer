"""Data-driven rejections for structured native invocation contracts."""

import tomllib
from collections.abc import Callable, Mapping
from pathlib import Path

import pytest
from pydantic import TypeAdapter

import literalizer
from literalizer.languages import ALL_LANGUAGES, Java, ObjectiveC
from scripts.roundtrip_common import json_object_from_text

_MANIFEST: Mapping[str, object] = tomllib.loads(
    (Path(__file__).parent / "native_invocations.toml").read_text(
        encoding="utf-8"
    )
)
_CASES = TypeAdapter(type=tuple[dict[str, object], ...]).validate_python(
    _MANIFEST["case"]
)


@pytest.mark.parametrize(
    argnames="case",
    argvalues=_CASES,
    ids=[str(object=case["name"]) for case in _CASES],
)
def test_native_invocation_rejections(case: dict[str, object]) -> None:
    """Reject malformed recipes before emitting invalid native source."""
    spec = json_object_from_text(text=str(object=case["recipe"]))
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
        _ = literalizer.literalize_invocations(
            source=str(object=case["source"]),
            input_format=literalizer.InputFormat.JSON,
            language=ObjectiveC(
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
        _ = literalizer.literalize_invocations(
            language=ObjectiveC(),
            invocation=literalizer.NativeInvocation(
                target=literalizer.ConstructorTarget(class_name="NSObject"),
                arguments=(),
            ),
            variable_form=literalizer.NewVariable(
                name="created", modifiers=frozenset({Java.modifiers.FINAL})
            ),
        )


_UNSUPPORTED = sorted(
    (cls for cls in ALL_LANGUAGES if not cls.supports_native_invocations),
    key=lambda cls: cls.__name__,
)


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_UNSUPPORTED,
    ids=[cls.language_id for cls in _UNSUPPORTED],
)
def test_native_call_requires_capability(
    language_cls: literalizer.LanguageCls,
) -> None:
    """Every backend that opts out rejects a single native invocation."""
    invocation = literalizer.NativeInvocation(
        target=literalizer.FunctionTarget(
            name="consume",
            parameter_types=(),
            return_type=literalizer.ScalarType.VOID,
        ),
        arguments=(),
    )
    with pytest.raises(
        expected_exception=literalizer.NativeCallError,
        match="does not support native invocations",
    ):
        _ = literalizer.literalize_invocations(
            language=language_cls(), invocation=invocation
        )


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_UNSUPPORTED,
    ids=[cls.language_id for cls in _UNSUPPORTED],
)
def test_native_rows_require_capability(
    language_cls: literalizer.LanguageCls,
) -> None:
    """Bare native recipes require a backend with native support."""
    recipe: dict[str, object] = {
        "function": "consume",
        "parameter-types": [],
        "return-type": "void",
        "arguments": [],
    }
    with pytest.raises(
        expected_exception=literalizer.NativeCallError,
        match="does not support native invocations",
    ):
        _ = literalizer.literalize_invocations(
            source="[[]]",
            input_format=literalizer.InputFormat.JSON,
            language=language_cls(),
            invocation=recipe,
        )


def _invoke_dynamic(
    render: Callable[..., literalizer.LiteralizeResult], /, **options: object
) -> literalizer.LiteralizeResult:
    """Exercise runtime validation for dynamically supplied arguments."""
    return render(**options)


@pytest.mark.parametrize(
    argnames="options",
    argvalues=[
        {"source": "[[]]"},
        {"input_format": literalizer.InputFormat.JSON},
        {"per_element": False},
        {"zip_source": "[]"},
        {"zip_input_format": literalizer.InputFormat.JSON},
    ],
    ids=["source", "format", "single-row", "zip-source", "zip-format"],
)
def test_typed_invocation_rejects_recipe_options(
    options: dict[str, object],
) -> None:
    """Options for loading source rows require an invocation recipe."""
    invocation = literalizer.NativeInvocation(
        target=literalizer.FunctionTarget(
            name="consume",
            parameter_types=(),
            return_type=literalizer.ScalarType.VOID,
        ),
        arguments=(),
    )
    with pytest.raises(
        expected_exception=literalizer.NativeCallError,
        match="options require an invocation recipe",
    ):
        _ = _invoke_dynamic(
            literalizer.literalize_invocations,
            language=ObjectiveC(),
            invocation=invocation,
            **options,
        )


@pytest.mark.parametrize(
    argnames="options",
    argvalues=[
        {"source": "[[]]"},
        {"input_format": literalizer.InputFormat.JSON},
    ],
    ids=["missing-format", "missing-source"],
)
def test_invocation_recipe_requires_source_and_format(
    options: dict[str, object],
) -> None:
    """Report which inputs a recipe needs before trying to render it."""
    with pytest.raises(
        expected_exception=literalizer.NativeCallError,
        match="Invocation recipes require source and input_format",
    ):
        _ = _invoke_dynamic(
            literalizer.literalize_invocations,
            language=ObjectiveC(),
            invocation={
                "function": "consume",
                "parameter-types": [],
                "return-type": "void",
                "arguments": [],
            },
            **options,
        )
