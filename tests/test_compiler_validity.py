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
from literalizer.exceptions import (
    HeterogeneousSiblingListsError,
    UnrepresentableInputError,
    UnrepresentableIntegerError,
)
from literalizer.languages import (
    C,
    Cobol,
    Cpp,
    Crystal,
    D,
    Go,
    Java,
    Kotlin,
    Nim,
    Odin,
    Python,
    R,
    Rust,
    Scala,
    Swift,
    V,
    Zig,
)

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


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        C(heterogeneous_strategy=C.heterogeneous_strategies.RECORD),
        Cpp(heterogeneous_strategy=Cpp.heterogeneous_strategies.RECORD),
        D(heterogeneous_strategy=D.heterogeneous_strategies.RECORD),
        Nim(heterogeneous_strategy=Nim.heterogeneous_strategies.RECORD),
        V(heterogeneous_strategy=V.heterogeneous_strategies.RECORD),
    ],
)
def test_record_strategy_rejects_unholdable_record_variants(
    language: Language,
) -> None:
    """Homogeneous sequences reject records needing distinct types."""
    with pytest.raises(expected_exception=HeterogeneousSiblingListsError):
        _render(source='[{"x": 1}, {"x": "s"}]', language=language)


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        Crystal(
            heterogeneous_strategy=Crystal.heterogeneous_strategies.RECORD,
        ),
        Odin(heterogeneous_strategy=Odin.heterogeneous_strategies.RECORD),
    ],
)
def test_record_strategy_emits_holdable_record_variants(
    language: Language,
) -> None:
    """Top-typed sequences retain records with incompatible fields."""
    rendered = _render(
        source='[{"x": 1}, {"x": "s"}]',
        language=language,
    )

    assert "Record0" in rendered
    assert "Record1" in rendered


@pytest.mark.parametrize(
    argnames=("language", "escape"),
    argvalues=[
        (Crystal(), r"\0"),
        (D(), r"\0"),
        (Go(), r"\x00"),
        (Nim(), r"\0"),
        (Odin(), r"\0"),
        (Python(), r"\0"),
        (V(), r"\0"),
    ],
)
def test_string_literals_escape_nul(
    language: Language,
    escape: str,
) -> None:
    """A zero byte uses target-language escape syntax."""
    rendered = _render(source='{"x": "\\u0000"}', language=language)

    assert "\0" not in rendered
    assert escape in rendered


@pytest.mark.parametrize(argnames="language", argvalues=[R(), Cobol()])
def test_string_literals_reject_unrepresentable_nul(
    language: Language,
) -> None:
    """Targets without embedded zero bytes reject the value."""
    with pytest.raises(expected_exception=UnrepresentableInputError):
        _render(source='{"x": "\\u0000"}', language=language)


@pytest.mark.parametrize(
    argnames=("language", "source", "type_name", "literal_marker"),
    argvalues=[
        (
            Cpp(),
            "[9223372036854775807, 9223372036854775808]",
            "std::vector<unsigned long long>",
            "ULL",
        ),
        (
            Go(),
            "[9223372036854775807, 9223372036854775808]",
            "[]uint64",
            "uint64(",
        ),
        (
            Go(),
            '{"a": 9223372036854775807, "b": 9223372036854775808}',
            "map[string]uint64",
            "uint64(",
        ),
        (
            Rust(),
            "[9223372036854775807, 9223372036854775808]",
            "vec![",
            "i128",
        ),
        (
            Rust(),
            '{"a": 9223372036854775807, "b": 9223372036854775808}',
            "HashMap::from",
            "i128",
        ),
        (
            Scala(),
            "[9223372036854775807, 9223372036854775808]",
            "List[BigInt]",
            "BigInt(",
        ),
        (
            Scala(),
            '{"a": 9223372036854775807, "b": 9223372036854775808}',
            "Map[String, BigInt]",
            "BigInt(",
        ),
        (
            Kotlin(),
            '{"a": 9223372036854775807, "b": 9223372036854775808}',
            "mapOf<String, BigInteger>",
            "BigInteger(",
        ),
    ],
)
def test_integer_collections_widen_past_signed_64_bit(
    language: Language,
    source: str,
    type_name: str,
    literal_marker: str,
) -> None:
    """The container type and every integer use one wider type."""
    rendered = _render(source=source, language=language)

    assert type_name in rendered
    assert rendered.count(literal_marker) >= _DECLARATION_AND_LITERAL


@pytest.mark.parametrize(argnames="language", argvalues=[V(), Zig()])
def test_integers_above_unsigned_64_bit_are_rejected(
    language: Language,
) -> None:
    """Targets capped at ``u64`` reject larger integer values."""
    with pytest.raises(expected_exception=UnrepresentableIntegerError):
        _render(source="1267650600228229401496703205376", language=language)


def test_go_rejects_negative_and_unsigned_width_integer_mix() -> None:
    """Go rejects a collection with no common integer type."""
    with pytest.raises(expected_exception=UnrepresentableIntegerError):
        _render(source=f"[-1, {2**63}]", language=Go())


@pytest.mark.parametrize(
    argnames=("language", "source"),
    argvalues=[
        (Rust(), '[{}, {"x": 1}]'),
        (
            Rust(
                heterogeneous_strategy=Rust.heterogeneous_strategies.TAGGED_ENUM,
            ),
            "[1, []]",
        ),
        (
            Rust(
                heterogeneous_strategy=Rust.heterogeneous_strategies.TAGGED_ENUM,
            ),
            "[1, {}]",
        ),
        (
            Nim(
                heterogeneous_strategy=Nim.heterogeneous_strategies.OBJECT_VARIANT,
            ),
            '{"a": {"x": 1}, "b": {"x": 1099511627776}}',
        ),
        (
            Nim(
                heterogeneous_strategy=Nim.heterogeneous_strategies.OBJECT_VARIANT,
            ),
            '[{}, {"x": 1}]',
        ),
        (
            Nim(
                heterogeneous_strategy=Nim.heterogeneous_strategies.OBJECT_VARIANT,
            ),
            "[null]",
        ),
        (
            Nim(
                heterogeneous_strategy=Nim.heterogeneous_strategies.OBJECT_VARIANT,
            ),
            "[1, {}]",
        ),
        (V(), "[[], [1]]"),
        (V(), '[{}, {"x": 1}]'),
        (V(), "[null]"),
        (V(), '{"a": null}'),
        (
            V(heterogeneous_strategy=V.heterogeneous_strategies.INTERFACE),
            "[true, 1]",
        ),
        (
            V(heterogeneous_strategy=V.heterogeneous_strategies.INTERFACE),
            '{"a": true, "b": 1}',
        ),
        (
            V(heterogeneous_strategy=V.heterogeneous_strategies.INTERFACE),
            "[1, []]",
        ),
        (
            V(heterogeneous_strategy=V.heterogeneous_strategies.INTERFACE),
            "[1, {}]",
        ),
        (
            V(heterogeneous_strategy=V.heterogeneous_strategies.INTERFACE),
            '[[1], ["s"]]',
        ),
        (
            V(heterogeneous_strategy=V.heterogeneous_strategies.INTERFACE),
            '{"a": [1], "b": ["s"]}',
        ),
    ],
)
def test_untypable_container_shapes_are_rejected(
    language: Language,
    source: str,
) -> None:
    """A target compiler never receives a collection with no safe type."""
    with pytest.raises(expected_exception=UnrepresentableInputError):
        _render(source=source, language=language)


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
        (
            Python(
                heterogeneous_strategy=Python.heterogeneous_strategies.RECORD,
            ),
            '[{"class": 1}]',
            "class_",
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
    argnames=("language", "escaped"),
    argvalues=[
        (
            Kotlin(
                heterogeneous_strategy=Kotlin.heterogeneous_strategies.RECORD,
            ),
            "`a-b`",
        ),
        (
            Scala(
                heterogeneous_strategy=Scala.heterogeneous_strategies.RECORD,
            ),
            "`a-b`",
        ),
        (
            Zig(heterogeneous_strategy=Zig.heterogeneous_strategies.RECORD),
            '@"a-b"',
        ),
    ],
)
def test_record_strategy_quotes_non_bare_field_names(
    language: Language,
    escaped: str,
) -> None:
    """Languages with quoted identifiers preserve punctuation in keys."""
    rendered = _render(source='[{"a-b": 1}]', language=language)

    assert rendered.count(escaped) == _DECLARATION_AND_LITERAL


@pytest.mark.parametrize(
    argnames=("language", "key"),
    argvalues=[
        (
            C(heterogeneous_strategy=C.heterogeneous_strategies.RECORD),
            "switch",
        ),
        (
            C(heterogeneous_strategy=C.heterogeneous_strategies.RECORD),
            "a-b",
        ),
        (
            Cpp(heterogeneous_strategy=Cpp.heterogeneous_strategies.RECORD),
            "class",
        ),
        (
            Cpp(heterogeneous_strategy=Cpp.heterogeneous_strategies.RECORD),
            "a-b",
        ),
        (
            Crystal(
                heterogeneous_strategy=Crystal.heterogeneous_strategies.RECORD,
            ),
            "a-b",
        ),
        (
            D(heterogeneous_strategy=D.heterogeneous_strategies.RECORD),
            "a-b",
        ),
        (
            Java(
                heterogeneous_strategy=Java.heterogeneous_strategies.RECORD,
            ),
            "a-b",
        ),
        (
            Odin(
                heterogeneous_strategy=Odin.heterogeneous_strategies.RECORD,
            ),
            "proc",
        ),
        (
            Odin(
                heterogeneous_strategy=Odin.heterogeneous_strategies.RECORD,
            ),
            "a-b",
        ),
        (
            Python(
                heterogeneous_strategy=Python.heterogeneous_strategies.RECORD,
            ),
            "a-b",
        ),
        (
            Swift(
                heterogeneous_strategy=Swift.heterogeneous_strategies.RECORD,
            ),
            "a-b",
        ),
        (
            V(heterogeneous_strategy=V.heterogeneous_strategies.RECORD),
            "a-b",
        ),
        (
            Kotlin(
                heterogeneous_strategy=Kotlin.heterogeneous_strategies.RECORD,
            ),
            r"a\nb",
        ),
        (
            Scala(
                heterogeneous_strategy=Scala.heterogeneous_strategies.RECORD,
            ),
            r"a\nb",
        ),
        (
            Zig(heterogeneous_strategy=Zig.heterogeneous_strategies.RECORD),
            r"a\nb",
        ),
    ],
)
def test_record_strategy_rejects_unquotable_field_names(
    language: Language,
    key: str,
) -> None:
    """A record key must have a compiling target-language identifier."""
    source = f'[{{"{key}": 1}}]'

    with pytest.raises(expected_exception=UnrepresentableInputError):
        _render(source=source, language=language)


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


def test_nim_object_variant_accepts_a_non_list_container() -> None:
    """Nim object variants still support heterogeneous maps."""
    language = Nim(
        heterogeneous_strategy=Nim.heterogeneous_strategies.OBJECT_VARIANT,
    )

    rendered = _render(source='{"a": 1, "b": "s"}', language=language)

    assert "ValueKind = enum" in rendered


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
