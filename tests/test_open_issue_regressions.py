"""Regression coverage for compiler-validity issues #2960--#2969."""

from collections.abc import Iterable

import pytest

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Java, Kotlin, Nim, Scala, Swift, Zig

_DECLARATION_AND_LITERAL = 2


def _render(*, source: str, language: Language) -> str:
    """Render a wrapped declaration for one compact JSON input."""
    return literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=language,
        wrap_in_file=True,
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
    ).declaration_code


def test_java_mixed_width_integer_array_widens_to_long() -> None:
    """A later long literal widens the Java array element type (#2960)."""
    rendered = _render(source="[1, 1099511627776]", language=Java())

    assert "new long[]{" in rendered
    assert "1099511627776L" in rendered


@pytest.mark.parametrize(
    argnames=("language", "expected"),
    argvalues=[
        (
            Java(heterogeneous_strategy=Java.heterogeneous_strategies.RECORD),
            ("record Record0(int x)", "record Record1(String x)"),
        ),
        (
            Swift(
                heterogeneous_strategy=Swift.heterogeneous_strategies.RECORD,
            ),
            (
                "struct Record0 { let x: Int }",
                "struct Record1 { let x: String }",
            ),
        ),
        (
            Zig(heterogeneous_strategy=Zig.heterogeneous_strategies.RECORD),
            ("struct { x: i64 }", "struct { x: []const u8 }"),
        ),
    ],
)
def test_record_strategy_splits_conflicting_field_types(
    language: Language,
    expected: Iterable[str],
) -> None:
    """Same-key records with incompatible fields use distinct types."""
    rendered = _render(source='[{"x": 1}, {"x": "s"}]', language=language)

    for declaration in expected:
        assert declaration in rendered
    assert "Record0" in rendered
    assert "Record1" in rendered


def test_java_nested_record_variant_list_uses_top_element_type() -> None:
    """A nested list spanning split records uses the Java top type."""
    rendered = _render(
        source='{"items": [{"x": 1}, {"x": "s"}]}',
        language=Java(
            heterogeneous_strategy=Java.heterogeneous_strategies.RECORD,
        ),
    )

    assert "record Record0(Object[] items)" in rendered
    assert "new Object[]{" in rendered


@pytest.mark.parametrize(
    argnames=("language", "source", "escaped"),
    argvalues=[
        (
            Zig(heterogeneous_strategy=Zig.heterogeneous_strategies.RECORD),
            '[{"error": "x"}]',
            '@"error"',
        ),
        (
            Nim(heterogeneous_strategy=Nim.heterogeneous_strategies.RECORD),
            '[{"type": "a"}]',
            "`type`",
        ),
        (
            Scala(
                heterogeneous_strategy=Scala.heterogeneous_strategies.RECORD,
            ),
            '[{"type": "a"}]',
            "`type`",
        ),
    ],
)
def test_record_strategy_escapes_keyword_fields(
    language: Language,
    source: str,
    escaped: str,
) -> None:
    """Keyword keys use the target language's identifier escape."""
    rendered = _render(source=source, language=language)

    assert rendered.count(escaped) == _DECLARATION_AND_LITERAL


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        Scala(heterogeneous_strategy=Scala.heterogeneous_strategies.TUPLE),
        Kotlin(heterogeneous_strategy=Kotlin.heterogeneous_strategies.TUPLE),
    ],
)
def test_tuple_strategy_splits_outer_records_for_nested_shape(
    language: Language,
) -> None:
    """Differently typed nested fields get distinct outer records."""
    rendered = _render(
        source='[{"input": {"a": 1}}, {"input": {"b": 2}}]',
        language=language,
    )

    assert "Record0(input" in rendered
    assert "Record2(input" in rendered
    assert "Record0(input = Record1" in rendered
    assert "Record2(input = Record3" in rendered


def test_nim_object_variant_rejects_scalar_container_sequence() -> None:
    """Nim rejects a list its scalar-only variant cannot unify (#2965)."""
    language = Nim(
        heterogeneous_strategy=Nim.heterogeneous_strategies.OBJECT_VARIANT,
    )

    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="mixes scalar and container elements",
    ):
        _render(source="[1, []]", language=language)
