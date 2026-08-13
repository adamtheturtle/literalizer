"""Bound-ref declarations honor the requested collection layout."""

from literalizer import (
    CollectionLayout,
    InputFormat,
    literalize_call,
)
from literalizer.languages import Python


def test_call_bound_ref_declaration_uses_multiline_layout() -> None:
    """The call composer forwards layout into each ref declaration."""
    result = literalize_call(
        source='[[{"$ref": "x"}]]',
        input_format=InputFormat.JSON,
        language=Python(),
        target_function="f",
        parameter_names=["value"],
        ref_key="$ref",
        bound_refs={"x": [[1, 2], [3, 4]]},
        wrap_in_file=True,
        collection_layout=CollectionLayout.MULTILINE,
    )

    assert (
        "x = (\n"
        "    (\n"
        "        1,\n"
        "        2,\n"
        "    ),\n"
        "    (\n"
        "        3,\n"
        "        4,\n"
        "    ),\n"
        ")"
    ) in result.code
