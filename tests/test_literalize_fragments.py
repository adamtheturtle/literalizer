"""Tests for intentionally incomplete literal fragments."""

from literalizer import CollectionLayout, InputFormat, literalize
from literalizer._json_native_document import format_json_native_document_fast
from literalizer._types import OrderedMap, Scalar, Value
from literalizer.languages import Python, Rust


def test_binary_without_sequence_delimiters() -> None:
    """YAML binary renders when the enclosing sequence is omitted."""
    result = literalize(
        source="- !!binary SGVsbG8=\n",
        input_format=InputFormat.YAML,
        language=Python(),
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=None,
    )
    assert result.code == '"48656c6c6f",'


def test_json_native_fast_path_rejects_nested_ordered_map() -> None:
    """A nested ordered mapping falls back to the shared renderer."""
    language = Rust(json_type=Rust.json_types.SERDE_JSON_VALUE)
    data: dict[Scalar, Value] = {}
    data["ordered"] = OrderedMap()
    assert (
        format_json_native_document_fast(
            language=language,
            data=data,
            line_prefix="",
            include_delimiters=True,
            collection_layout=CollectionLayout.COMPACT,
        )
        is None
    )
