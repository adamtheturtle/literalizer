"""Language-specific tests for literalizer converter."""

import dataclasses
from typing import ClassVar

from literalizer import InputFormat, literalize
from literalizer.languages import Dart

# The null-filtering step in
# :func:`~literalizer._literalize._compute_dict_open_override` (the
# ``filtered_dicts`` comprehension) only runs when a language combines
# a value-type-sensitive ``dict_open`` (from
# :func:`~literalizer._formatters.collection_openers.typed_dict_open`)
# with ``skip_null_dict_values=True``. No production language pairs
# those two: the ``typed_dict_open`` languages (Dart, CSharp, Kotlin,
# Scala, Go) all keep nulls, while the ``skip_null_dict_values=True``
# languages (Java, Lua, Toml, Wren) all use ``fixed_dict_open`` whose
# constant opener never triggers widening. The golden-file suite
# iterates over :data:`~literalizer.languages.ALL_LANGUAGES` and has
# no way to inject a test-only language, so the two cases below define
# a Dart subclass inline to pin the divergent-types and matching-types
# outcomes of that filtering. The surrounding widening logic (override
# computation and the collapse-to-empty paths) is exercised by
# production golden cases with type-divergent dicts and is not
# re-asserted here.


def test_dart_skip_nulls_widens_across_null_masked_types() -> None:
    """Widening fires when null-masked dict value types differ.

    With ``skip_null_dict_values=True``, filtering ``None`` out of
    ``{"a": None, "b": 1}`` and ``{"a": "hello", "b": None}`` leaves
    dicts whose remaining value types diverge (``int`` vs. ``String``).
    The override must widen so both dicts share a ``dynamic`` opener.
    """

    @dataclasses.dataclass(frozen=True, kw_only=True)
    class DartSkipNulls(Dart):
        """Dart variant that drops null dict values."""

        skip_null_dict_values: ClassVar[bool] = True

    source = '[{"a": null, "b": 1}, {"a": "hello", "b": null}]'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=DartSkipNulls(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )

    assert result.code == (
        "<Map<String, dynamic>>[\n"
        '    <String, dynamic>{"b": 1},\n'
        '    <String, dynamic>{"a": "hello"},\n'
        "]"
    )


def test_dart_skip_nulls_no_widening_when_filtered_dicts_match() -> None:
    """No override is needed when filtered dicts all share one opener.

    Null masks hide keys ``a`` and ``b`` in each dict, leaving only
    ``{"n": 1}`` and ``{"n": 2}``, both ``<String, int>``.  Widening
    would be redundant; each dict renders with its own inferred opener.
    """

    @dataclasses.dataclass(frozen=True, kw_only=True)
    class DartSkipNulls(Dart):
        """Dart variant that drops null dict values."""

        skip_null_dict_values: ClassVar[bool] = True

    source = '[{"a": null, "n": 1}, {"b": null, "n": 2}]'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=DartSkipNulls(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )

    assert result.code == (
        "<Map<String, dynamic>>[\n"
        '    <String, int>{"n": 1},\n'
        '    <String, int>{"n": 2},\n'
        "]"
    )
