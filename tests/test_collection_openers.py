"""Tests for collection opener helpers.

These call an opener directly with values assembled in Python, which
is what makes them useful: the typing they check has to hold for a
shape the language then refuses, so there is no output for a golden
file to hold (issue #4699).
"""

import pytest

from literalizer._formatters.collection_openers import (
    sequence_surrogate_set_open,
)
from literalizer._language import Language
from literalizer._types import Scalar, Value
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

    def make_set(*items: Scalar) -> Value:
        """Return a recursively typed scalar set."""
        result: set[Scalar] = set(items)
        return result

    language = Cpp()
    nested_set = make_set(1, 2)

    assert (
        language.set_format_config.set_open([1, "two"])
        == "std::vector<std::variant<int, std::string>>{"
    )
    assert (
        language.set_format_config.set_open([nested_set, "two"])
        == "std::vector<std::variant<std::vector<int>, std::string>>{"
    )
    assert language.data_dependent_preamble([nested_set, "two"]) == (
        "#include <variant>",
    )
    assert language.data_dependent_preamble(make_set(1, "two")) == (
        "#include <variant>",
    )

    cpp14 = Cpp(language_version=Cpp.version_formats.CPP14)
    outer: Value = [nested_set, "two"]
    assert cpp14.heterogeneous_behavior.compute_wrap_ids(outer) == frozenset(
        {id(outer)}
    )


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[Cpp(), Haxe(), Nim(), Raku()],
)
def test_sequence_surrogate_set_entries_delegate(language: Language) -> None:
    """Rejected sequence surrogates retain their entry formatter
    contract.
    """
    assert language.format_set_entry(1, "one") == "one"
