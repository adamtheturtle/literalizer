"""Centralized non-string dict key guard for unsupported languages.

The guard runs inside ``_format_dict_value`` and
``_format_ordered_map_value`` and rejects non-string dict keys when the
target language sets ``supports_non_string_dict_keys = False``.  The
YAML parser produces non-string dict keys natively, so the guard is
reachable through :func:`literalizer.literalize`; the helper-level tests
here exercise the contract directly.  Integration coverage for
end-to-end rejection lives in
``tests/errors/test_non_string_dict_key_literalize.py``.
"""

import re

import pytest

from literalizer import Language
from literalizer._literalize import _guard_dict_keys_supported
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Json5, Jsonnet, Python, Toml

_JSON5 = Json5(indent="  ")
_JSONNET = Jsonnet(indent="  ")
_TOML = Toml(indent="  ")
_PYTHON = Python(indent="  ")


def test_guard_raises_for_int_key_on_json5() -> None:
    """Json5 rejects non-string keys with
    ``UnrepresentableInputError``.
    """
    expected_msg = re.escape(
        pattern="Json5 cannot represent dict key of type int",
    )
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match=f"^{expected_msg}$",
    ):
        _guard_dict_keys_supported(value={1: "v"}, spec=_JSON5)


@pytest.mark.parametrize(
    argnames="spec",
    argvalues=[_JSON5, _JSONNET, _TOML],
    ids=["json5", "jsonnet", "toml"],
)
def test_guard_raises_for_bytes_key_on_unsupported(
    *,
    spec: Language,
) -> None:
    """Languages opted out raise for any non-string scalar key."""
    with pytest.raises(expected_exception=UnrepresentableInputError):
        _guard_dict_keys_supported(value={b"k": "v"}, spec=spec)


@pytest.mark.parametrize(
    argnames="spec",
    argvalues=[_JSON5, _JSONNET, _TOML],
    ids=["json5", "jsonnet", "toml"],
)
def test_guard_accepts_string_key_on_unsupported(*, spec: Language) -> None:
    """String keys pass through the guard even for opted-out languages."""
    _guard_dict_keys_supported(value={"k": "v"}, spec=spec)


def test_guard_accepts_non_string_key_on_supported() -> None:
    """Languages with the default ``True`` accept non-string keys."""
    _guard_dict_keys_supported(value={1: "v"}, spec=_PYTHON)
