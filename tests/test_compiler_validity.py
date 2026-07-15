"""Regression coverage for compiler-valid literal generation."""

from collections.abc import Iterable

import pytest

from literalizer import (
    CollectionLayout,
    InputFormat,
    Language,
    NewVariable,
    literalize,
)
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import D, Java, Kotlin, Nim, Scala, Swift, V, Zig

_DECLARATION_AND_LITERAL = 2


def _render(
    *,
    source: str,
    language: Language,
    collection_layout: CollectionLayout = CollectionLayout.COMPACT,
) -> str:
    """Render a wrapped declaration for one compact JSON input."""
    return literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=language,
        collection_layout=collection_layout,
        wrap_in_file=True,
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
    ).declaration_code


def test_java_mixed_width_integer_array_widens_to_long() -> None:
    """A later long literal widens the Java array element type."""
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
        (
            Kotlin(
                heterogeneous_strategy=Kotlin.heterogeneous_strategies.RECORD,
            ),
            (
                "data class Record0(val x: Int)",
                "data class Record1(val x: String)",
            ),
        ),
        (
            Scala(
                heterogeneous_strategy=Scala.heterogeneous_strategies.RECORD,
            ),
            (
                "case class Record0(x: Int)",
                "case class Record1(x: String)",
            ),
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
    argnames=("language", "source", "escaped", "expected_count"),
    argvalues=[
        (
            Zig(heterogeneous_strategy=Zig.heterogeneous_strategies.RECORD),
            '[{"error": "x"}]',
            '@"error"',
            _DECLARATION_AND_LITERAL,
        ),
        (
            Nim(heterogeneous_strategy=Nim.heterogeneous_strategies.RECORD),
            '[{"type": "a"}]',
            "`type`",
            _DECLARATION_AND_LITERAL,
        ),
        (
            Scala(
                heterogeneous_strategy=Scala.heterogeneous_strategies.RECORD,
            ),
            '[{"type": "a"}]',
            "`type`",
            _DECLARATION_AND_LITERAL,
        ),
        (
            Java(
                heterogeneous_strategy=Java.heterogeneous_strategies.RECORD,
            ),
            '[{"class": 1}]',
            "class_",
            1,
        ),
        (
            Swift(
                heterogeneous_strategy=Swift.heterogeneous_strategies.RECORD,
            ),
            '[{"class": 1}]',
            "`class`",
            1,
        ),
        (
            Kotlin(
                heterogeneous_strategy=Kotlin.heterogeneous_strategies.RECORD,
            ),
            '[{"when": 1}]',
            "`when`",
            _DECLARATION_AND_LITERAL,
        ),
        (
            D(heterogeneous_strategy=D.heterogeneous_strategies.RECORD),
            '[{"class": 1}]',
            "class_",
            1,
        ),
        (
            V(heterogeneous_strategy=V.heterogeneous_strategies.RECORD),
            '[{"type": 1}]',
            "@type",
            _DECLARATION_AND_LITERAL,
        ),
    ],
)
def test_record_strategy_escapes_keyword_fields(
    language: Language,
    source: str,
    escaped: str,
    expected_count: int,
) -> None:
    """Keyword keys use the target language's identifier escape."""
    rendered = _render(source=source, language=language)

    assert rendered.count(escaped) == expected_count


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
    """Nim rejects a list its scalar-only variant cannot unify."""
    language = Nim(
        heterogeneous_strategy=Nim.heterogeneous_strategies.OBJECT_VARIANT,
    )

    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="mixes scalar and container elements",
    ):
        _render(source="[1, []]", language=language)


def test_nim_object_variant_rejects_null_only_map() -> None:
    """Nim rejects a map whose values infer only ``typeof(nil)``."""
    language = Nim(
        heterogeneous_strategy=Nim.heterogeneous_strategies.OBJECT_VARIANT,
    )

    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="values are all null",
    ):
        _render(source='{"a": null}', language=language)


@pytest.mark.parametrize(
    argnames=("source", "layout"),
    argvalues=[
        ("[1, 1099511627776]", CollectionLayout.COMPACT),
        ("[1, 1099511627776]", CollectionLayout.MULTILINE),
        ('{"a": 1, "b": 1099511627776}', CollectionLayout.COMPACT),
        ('{"a": 1, "b": 1099511627776}', CollectionLayout.MULTILINE),
    ],
)
def test_v_mixed_width_integer_collections_widen_every_value(
    source: str,
    layout: CollectionLayout,
) -> None:
    """V lists and maps cast every mixed-width integer to ``i64``."""
    rendered = _render(
        source=source,
        language=V(),
        collection_layout=layout,
    )

    assert "i64(1)" in rendered
    assert "i64(1099511627776)" in rendered
