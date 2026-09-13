"""Reference discovery ignores markers whose names are not strings."""

from .literalize_ref_cases import collect_ref_names


def test_nonstring_ref_names() -> None:
    """Malformed markers do not declare phantom bound reference names."""
    assert collect_ref_names(
        data=[{"$ref": 1}, {"$ref": None}, {"$ref": "actual"}],
        ref_key="$ref",
    ) == ["actual"]
