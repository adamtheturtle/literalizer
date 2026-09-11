"""Tests for mapping-key classification from source names."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from literalizer.exceptions import InvalidDictKeyError
from literalizer.languages import Dhall, Json5, Jsonnet, Nix, Toml

if TYPE_CHECKING:
    from literalizer._language import DictFormatConfig, OrderedMapFormatConfig


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[Dhall(), Json5(), Jsonnet(), Nix(), Toml()],
)
def test_bare_mapping_key_uses_source_name(
    language: Dhall | Json5 | Jsonnet | Nix | Toml,
) -> None:
    """Bare-key eligibility does not decode the rendered key."""
    configs: tuple[DictFormatConfig | OrderedMapFormatConfig, ...] = (
        language.dict_format_config,
        language.ordered_map_format_config,
    )

    for config in configs:
        assert (
            config.format_key(
                raw_key="source_key", formatted_key='"not valid"'
            )
            == "source_key"
        )


@pytest.mark.parametrize(
    argnames=("language", "expected"),
    argvalues=[
        (Dhall(), "`not valid`"),
        (Json5(), '"misleading"'),
        (Jsonnet(), '"misleading"'),
        (Nix(), '"misleading"'),
        (Toml(), '"misleading"'),
    ],
)
def test_non_bare_mapping_key_uses_source_name(
    language: Dhall | Json5 | Jsonnet | Nix | Toml,
    expected: str,
) -> None:
    """A rendered identifier does not make the source key bare."""
    assert (
        language.dict_format_config.format_key(
            raw_key="not valid", formatted_key='"misleading"'
        )
        == expected
    )


@pytest.mark.parametrize(argnames="language", argvalues=[Dhall(), Nix()])
def test_invalid_mapping_key_checks_source_name(
    language: Dhall | Nix,
) -> None:
    """Key validation runs against raw source characters."""
    with pytest.raises(expected_exception=InvalidDictKeyError):
        _ = language.dict_format_config.format_key(
            raw_key="line\nbreak", formatted_key='"safe-looking"'
        )
