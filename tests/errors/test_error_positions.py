"""Real TOML parser failures can omit position metadata."""

import pytest
from tomlkit.exceptions import KeyAlreadyPresent

from literalizer import InputFormat, LanguageCls, literalize
from literalizer._parsing import require_decoded_value
from literalizer.exceptions import TOMLParseError


def test_toml_error_without_position(language_cls: LanguageCls) -> None:
    """Duplicate keys preserve a parser cause without position
    metadata.
    """
    with pytest.raises(
        expected_exception=TOMLParseError,
        match='Key "a" already exists',
    ) as caught:
        _ = literalize(
            source="table = {a = 1, a = 1}\n",
            input_format=InputFormat.TOML,
            language=language_cls(),
        )
    assert caught.value.line is None
    assert caught.value.column is None
    assert isinstance(caught.value.__cause__, KeyAlreadyPresent)


def test_decoded_value_rejects_unsupported_values() -> None:
    """Reject unsupported values at the decoder boundary."""
    with pytest.raises(
        expected_exception=TypeError, match="unsupported value"
    ):
        _ = require_decoded_value(data=object())
