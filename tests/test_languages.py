"""Language-specific tests for literalizer converter."""

import dataclasses
from typing import ClassVar

from literalizer import (
    InputFormat,
    literalize,
    literalize_call,
)
from literalizer.languages import (
    Dart,
    Haskell,
)


def test_haskell_explicit_epoch_datetime_uses_int_constructor() -> None:
    """Explicit Haskell epoch datetimes use the integer constructor.

    Issue #2519 migrated the production-language string-assertion tests
    in this module to golden-file cases, but this one cannot ride the
    golden harness for two independent reasons, so it stays a focused
    public-API pytest test (like the Dart ``skip_null_dict_values``
    cases below):

    * It is the only thing that exercises the
      :attr:`~literalizer._literalize.LiteralizeResult.code` arm that
      joins ``body_preamble`` / ``pre_declaration_comments`` ahead of
      the declaration.  That arm only fires when ``wrap_in_file`` is
      ``False`` (otherwise the file wrapper absorbs the preamble), but
      every golden-file harness path calls ``literalize`` with
      ``wrap_in_file=True``, so no generated golden can reach it.
    * It pins the Haskell ``format_datetime`` override that fires only
      when ``datetime_format == EPOCH`` *and* ``numeric_style ==
      EXPLICIT``.  No variant axis crosses ``datetime_format`` with
      ``numeric_style``, so there is no golden configuration that
      activates the override.
    """
    result = literalize(
        source="ts: 2024-01-15T12:30:00+00:00\nname: hi\n",
        input_format=InputFormat.YAML,
        language=Haskell(
            datetime_format=Haskell.datetime_formats.EPOCH,
            numeric_style=Haskell.numeric_styles.EXPLICIT,
        ),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )

    assert not result.preamble
    assert result.code == (
        "data Val = HStr String | HMap [(String, Val)] | HInt Integer\n"
        "HMap [\n"
        '    ("ts", HInt 1705321800),\n'
        '    ("name", HStr "hi")\n'
        "    ]"
    )


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


def test_haskell_unknown_ref_values_keep_strip_behavior() -> None:
    """Haskell recursively strips unknown refs from nested dicts."""
    result = literalize_call(
        source='[[{"inner": {"$ref": "myList"}}]]',
        input_format=InputFormat.JSON,
        language=Haskell(),
        target_function="process",
        parameter_names=["data"],
        ref_values={"other": True},
    )

    assert result.source_data == [[{}]]
    assert result.types_present == frozenset({str, list, dict})
    assert result.body_preamble == (
        "data Val = HStr String | HList [Val] | HMap [(String, Val)]",
    )


def test_haskell_unknown_ref_values_strip_top_level_ref() -> None:
    """Haskell strips unknown top-level refs even when ref_values is
    set.
    """
    result = literalize_call(
        source='{"$ref": "myList"}',
        input_format=InputFormat.JSON,
        language=Haskell(),
        target_function="process",
        parameter_names=["data"],
        per_element=False,
        ref_values={"other": 1},
    )

    assert result.types_present == frozenset({list})
    assert result.body_preamble == ("data Val = HList [Val]",)


def test_haskell_without_ref_values_strips_top_level_ref() -> None:
    """Haskell's historical top-level ref strip behavior is retained."""
    result = literalize_call(
        source='{"$ref": "myList"}',
        input_format=InputFormat.JSON,
        language=Haskell(),
        target_function="process",
        parameter_names=["data"],
        per_element=False,
    )

    assert result.types_present == frozenset({list})
    assert result.body_preamble == ("data Val = HList [Val]",)


def test_haskell_without_ref_values_strips_per_element_ref() -> None:
    """Haskell per-element preamble inference skips ref marker
    elements.
    """
    result = literalize_call(
        source='[{"$ref": "myList"}]',
        input_format=InputFormat.JSON,
        language=Haskell(),
        target_function="process",
        parameter_names=["data"],
    )

    assert result.types_present == frozenset({list})
    assert result.body_preamble == ("data Val = HList [Val]",)
