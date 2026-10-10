"""Public contracts for Zig JSON configurations and native references."""

from typing import ClassVar

import pytest

from literalizer import InputFormat, literalize, literalize_call
from literalizer._types import Value
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Zig


@pytest.mark.parametrize(
    argnames="bound_value",
    argvalues=[
        {1: "value"},
        {True: "value"},
        {1.5: "value"},
        {"nested": {1: "value"}},
        {"nested": {True: "value"}},
        {"nested": {1.5: "value"}},
        [{"nested": {1: "value"}}],
        [{"nested": {True: "value"}}],
        [{"nested": {1.5: "value"}}],
    ],
)
def test_zig_json_bound_call_rejects_non_string_keys(
    bound_value: Value,
) -> None:
    """Bound call declarations retain the JSON object-key restriction."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="Zig cannot represent dict key of type",
    ):
        _ = literalize_call(
            source='{"$ref": "shared"}',
            input_format=InputFormat.JSON,
            language=Zig(json_type=Zig.JsonTypes["STD_JSON_VALUE"]),
            target_function="process",
            parameter_names=["value"],
            per_element=False,
            ref_key="$ref",
            bound_refs={"shared": bound_value},
            wrap_in_file=True,
        )


def test_zig_json_subclass_retains_null_field_policy() -> None:
    """A caller-defined null policy still applies to complete
    documents.
    """

    class SkipNullZig(Zig):
        """A custom Zig configuration that omits null dictionary
        values.
        """

        skip_null_dict_values: ClassVar[bool] = True

    language = SkipNullZig(json_type=SkipNullZig.JsonTypes["STD_JSON_VALUE"])
    actual = literalize(
        source='{"drop": null, "keep": 1}',
        input_format=InputFormat.JSON,
        language=language,
    )
    expected = literalize(
        source='{"keep": 1}',
        input_format=InputFormat.JSON,
        language=language,
    )
    assert actual.code == expected.code
