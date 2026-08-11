"""Invalid-dict-key error contract for languages with key restrictions.

R, Dhall, and Nix reject certain dict keys (empty strings or control
characters). The errors are language behaviors, independent of the
input format, so each case is parameterized over the formats that can
express the key (here, JSON and the flow-style YAML form, which both
``ruamel.yaml`` and the YAML parser accept).
"""

import json
import re

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import InvalidDictKeyError
from literalizer.languages import Dhall, Matlab, Nix, R

_EMPTY_KEY_DICT: dict[str, str] = {"": "value"}
_CONTROL_CHAR_KEY_DICT: dict[str, str] = {"\x01": "value"}


def _yaml_flow(obj: dict[str, str]) -> str:
    """Serialize *obj* as flow-form text accepted by both JSON and
    YAML.
    """
    return json.dumps(obj=obj) + "\n"


@pytest.mark.parametrize(
    argnames="input_format",
    argvalues=[InputFormat.JSON, InputFormat.YAML],
    ids=["json", "yaml"],
)
def test_r_empty_dict_key_raises(*, input_format: InputFormat) -> None:
    """R rejects an empty dict key by default."""
    expected_msg = re.escape(
        pattern='R does not support the dict key "". '
        "Use empty_dict_key=R.EmptyDictKey.POSITIONAL to emit them "
        "as unnamed list elements instead."
    )
    with pytest.raises(
        expected_exception=InvalidDictKeyError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=_yaml_flow(obj=_EMPTY_KEY_DICT),
            input_format=input_format,
            language=R(),
            pre_indent_level=0,
            include_delimiters=True,
        )


@pytest.mark.parametrize(argnames="key", argvalues=["", "1a", "a b", "a\x01b"])
def test_matlab_invalid_struct_field_name_raises(*, key: str) -> None:
    """MATLAB rejects keys that cannot name struct fields."""
    expected_msg = re.escape(
        pattern=(
            f"MATLAB does not support the struct field name {key!r}. "
            "Field names must start with a letter and contain only letters, "
            "digits, and underscores."
        )
    )
    with pytest.raises(
        expected_exception=InvalidDictKeyError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=json.dumps(obj={key: "value"}),
            input_format=InputFormat.JSON,
            language=Matlab(),
            pre_indent_level=0,
            include_delimiters=True,
        )


@pytest.mark.parametrize(
    argnames="input_format",
    argvalues=[InputFormat.JSON, InputFormat.YAML],
    ids=["json", "yaml"],
)
def test_dhall_empty_dict_key_raises(*, input_format: InputFormat) -> None:
    """Dhall raises InvalidDictKeyError for empty-string dict keys."""
    expected_msg = re.escape(
        pattern='Dhall does not support the dict key "". '
        "Backtick-quoted labels must be non-empty and contain only "
        "printable ASCII (no backticks or control characters)."
    )
    with pytest.raises(
        expected_exception=InvalidDictKeyError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=_yaml_flow(obj=_EMPTY_KEY_DICT),
            input_format=input_format,
            language=Dhall(),
            pre_indent_level=0,
            include_delimiters=True,
        )


@pytest.mark.parametrize(
    argnames="input_format",
    argvalues=[InputFormat.JSON, InputFormat.YAML],
    ids=["json", "yaml"],
)
def test_dhall_control_char_dict_key_raises(
    *,
    input_format: InputFormat,
) -> None:
    """Dhall rejects control characters in dict keys."""
    expected_msg = re.escape(
        pattern='Dhall does not support the dict key "\\u{0001}". '
        "Backtick-quoted labels must be non-empty and contain only "
        "printable ASCII (no backticks or control characters)."
    )
    with pytest.raises(
        expected_exception=InvalidDictKeyError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=_yaml_flow(obj=_CONTROL_CHAR_KEY_DICT),
            input_format=input_format,
            language=Dhall(),
            pre_indent_level=0,
            include_delimiters=True,
        )


@pytest.mark.parametrize(
    argnames="input_format",
    argvalues=[InputFormat.JSON, InputFormat.YAML],
    ids=["json", "yaml"],
)
def test_nix_control_char_dict_key_raises(
    *,
    input_format: InputFormat,
) -> None:
    """Nix rejects control characters in dict keys."""
    expected_msg = re.escape(
        pattern='Nix does not support the dict key "\x01". '
        "Attribute names must be non-empty and must not contain "
        "control characters."
    )
    with pytest.raises(
        expected_exception=InvalidDictKeyError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=_yaml_flow(obj=_CONTROL_CHAR_KEY_DICT),
            input_format=input_format,
            language=Nix(),
            pre_indent_level=0,
            include_delimiters=True,
        )
