"""Language-specific collection-key representation errors."""

import pytest

from literalizer import InputFormat, literalize
from literalizer._language import Language
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Java, Lua, Rust


@pytest.mark.parametrize(
    argnames=("source", "language", "message"),
    argvalues=[
        (".nan: value\n", Lua(), "Lua cannot use NaN as a mapping key"),
        ("!!set\n? .nan\n", Lua(), "Lua cannot use NaN as a set member"),
        ("1.0: value\n", Rust(), "Rust map formats cannot use float keys"),
        (
            "!!set\n? 1.0\n",
            Rust(),
            "Rust set formats cannot use float members",
        ),
        ("null: value\n", Java(), "Map.entry.*null keys"),
        ("!!set\n? null\n", Java(), "Set.of.*null elements"),
    ],
)
def test_unrepresentable_collection_key_raises(
    source: str,
    language: Language,
    message: str,
) -> None:
    """Back ends must reject values invalid as native collection keys."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match=message,
    ):
        literalize(
            source=source,
            input_format=InputFormat.YAML,
            language=language,
        )
