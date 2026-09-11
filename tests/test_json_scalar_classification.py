"""Tests for JSON scalar classification from source values."""

from literalizer.languages import OCaml, Scala


def test_scala_circe_integer_constructor_uses_source_range() -> None:
    """Circe constructor selection does not parse the rendered integer."""
    language = Scala(json_type=Scala.json_types.CIRCE)

    assert language.format_sequence_entry(1, "BigInt(1)") == (
        "Json.fromInt(BigInt(1))"
    )
    assert language.format_sequence_entry(2**31, "1") == "Json.fromLong(1)"
    assert language.format_sequence_entry(2**63, "1L") == (
        "Json.fromBigInt(1L)"
    )


def test_scala_circe_beyond_i64_collection_keeps_per_value_width() -> None:
    """Circe needs no inner integer widening once entries become JSON."""
    language = Scala(json_type=Scala.json_types.CIRCE)

    assert language.format_integer_beyond_i64 is not None
    assert language.format_integer_beyond_i64(1) == "1"
    assert language.format_integer_beyond_i64(2**63) == (
        'BigInt("9223372036854775808")'
    )


def test_ocaml_yojson_wrapper_uses_source_value() -> None:
    """Yojson pass-through and scalar tags do not parse rendered text."""
    language = OCaml(json_type=OCaml.json_types.YOJSON_SAFE_T)
    source_bool = True

    assert language.format_sequence_entry(1, '`String "misleading"') == (
        '`Int `String "misleading"'
    )
    assert language.format_sequence_entry(source_bool, "not prewrapped") == (
        "not prewrapped"
    )
    assert language.format_sequence_entry([], "not prewrapped") == (
        "not prewrapped"
    )
    assert language.format_sequence_entry(2**62, "not prewrapped") == (
        "not prewrapped"
    )
