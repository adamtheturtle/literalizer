"""Tests for collection opener helpers."""

import pytest

from literalizer._formatters.collection_openers import (
    sequence_surrogate_set_open,
)
from literalizer._language import Language
from literalizer._types import Value
from literalizer.languages import Cpp, Haxe, Nim, Raku


def test_sequence_surrogate_set_open_delegates() -> None:
    """The semantic marker preserves its wrapped opener's behavior."""

    def opener(items: list[Value]) -> str:
        """Return an opener string that exposes the delegated items."""
        return f"sequence({len(items)})"

    marked_opener = sequence_surrogate_set_open(opener)

    assert marked_opener([1, "two", None]) == "sequence(3)"


def test_cpp_sequence_surrogate_set_helpers_remain_consistent() -> None:
    """C++'s rejected surrogate still has internally consistent typing."""
    language = Cpp()
    nested_set: Value = {1, 2}

    assert language.set_format_config.set_open([1, "two"]).startswith(
        "std::vector<std::variant<"
    )
    assert language.set_format_config.set_open([nested_set, "two"]).startswith(
        "std::vector<std::variant<std::vector<"
    )
    assert "#include <variant>" in language.data_dependent_preamble(
        [nested_set, "two"]
    )
    assert "#include <variant>" in language.data_dependent_preamble({1, "two"})

    cpp14 = Cpp(language_version=Cpp.version_formats.CPP14)
    outer: Value = [nested_set, "two"]
    assert id(outer) in cpp14.heterogeneous_behavior.compute_wrap_ids(outer)


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[Cpp(), Haxe(), Nim(), Raku()],
)
def test_sequence_surrogate_set_entries_delegate(language: Language) -> None:
    """Rejected sequence surrogates retain their entry formatter
    contract.
    """
    assert language.format_set_entry(1, "one") == "one"
