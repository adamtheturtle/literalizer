"""Parser errors retain causes that require a supplied failure."""

import pytest
from tomlkit.exceptions import TOMLKitError

from literalizer import InputFormat, LanguageCls, literalize
from literalizer.exceptions import TOMLParseError


def test_toml_error_without_position(
    monkeypatch: pytest.MonkeyPatch,
    language_cls: LanguageCls,
) -> None:
    """A parser failure without location metadata retains its cause."""
    cause = TOMLKitError("unpositioned failure")

    def fail_parse(*, string: str) -> None:
        """Simulate a parser failure without line and column metadata."""
        del string
        raise cause

    monkeypatch.setattr(target="tomlkit.parse", name=fail_parse)
    with pytest.raises(expected_exception=TOMLParseError) as caught:
        _ = literalize(
            source="a = 1",
            input_format=InputFormat.TOML,
            language=language_cls(),
        )
    assert caught.value.line is None
    assert caught.value.column is None
    assert caught.value.__cause__ is cause
