"""Custom Zig JSON configurations retain their public rendering
policies.
"""

from typing import ClassVar

from literalizer import InputFormat, literalize
from literalizer.languages import Zig


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
