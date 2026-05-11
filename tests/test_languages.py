"""Language-specific tests for literalizer converter."""

import dataclasses
import datetime
import json
import re
from typing import ClassVar

import pytest

from literalizer import (
    InputFormat,
    NewVariable,
    literalize,
    literalize_call,
)
from literalizer.exceptions import (
    NullInCollectionError,
    UnrepresentableSpecialFloatError,
)
from literalizer.languages import (
    Cobol,
    Dart,
    Fortran,
    Gleam,
    Haskell,
    Java,
    Jsonnet,
    Matlab,
    Mojo,
    Python,
    R,
    Rust,
    Sml,
)

COBOL = Cobol(
    date_format=Cobol.date_formats.ISO,
    datetime_format=Cobol.datetime_formats.ISO,
    bytes_format=Cobol.bytes_formats.HEX,
    sequence_format=Cobol.sequence_formats.SEQUENCE,
)
FORTRAN = Fortran(
    date_format=Fortran.date_formats.ISO,
    datetime_format=Fortran.datetime_formats.ISO,
    bytes_format=Fortran.bytes_formats.HEX,
    sequence_format=Fortran.sequence_formats.LIST,
    module_name="check",
)


def test_python_datetime_whole_hour_offset_omits_minutes() -> None:
    """Whole-hour timezone offsets do not include zero minutes."""
    result = Python(
        date_format=Python.date_formats.PYTHON,
        datetime_format=Python.datetime_formats.PYTHON,
    ).format_datetime(
        datetime.datetime(
            year=2024,
            month=1,
            day=1,
            hour=12,
            tzinfo=datetime.timezone(offset=datetime.timedelta(hours=5)),
        )
    )

    assert result == (
        "datetime.datetime("
        "year=2024, "
        "month=1, "
        "day=1, "
        "hour=12, "
        "minute=0, "
        "second=0, "
        "tzinfo=datetime.timezone("
        "offset=datetime.timedelta(hours=5)"
        ")"
        ")"
    )


def test_r_formats_named_dict_entries() -> None:
    """R dict entries with names are formatted without raising."""
    result = literalize(
        source="{name: value}",
        input_format=InputFormat.YAML,
        language=R(empty_dict_key=R.empty_dict_keys.ERROR),
        variable_form=None,
    )

    assert result.code == 'list(\n    "name" = "value"\n)'


def test_haskell_explicit_epoch_datetime_uses_int_constructor() -> None:
    """Explicit Haskell epoch datetimes use the integer constructor."""
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


def test_sml_negative_epoch_datetime_parenthesizes_int_constructor() -> None:
    """Negative SML epoch datetimes wrap the converted integer."""
    result = literalize(
        source="1900-01-01T00:00:00+00:00",
        input_format=InputFormat.YAML,
        language=Sml(datetime_format=Sml.datetime_formats.EPOCH),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_data"),
    )

    assert result.code == (
        "datatype val_t =\n"
        "    SInt of LargeInt.int\n"
        "val my_data : val_t = SInt (~2208988800)"
    )


def test_rust_epoch_datetime_tagged_enum_uses_integer_variant() -> None:
    """Epoch datetimes use the integer variant in heterogeneous Rust
    data.
    """
    result = literalize(
        source="ts: 2024-01-15T12:30:00+00:00\nname: hi\n",
        input_format=InputFormat.YAML,
        language=Rust(
            datetime_format=Rust.datetime_formats.EPOCH,
            heterogeneous_strategy=Rust.heterogeneous_strategies.TAGGED_ENUM,
        ),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )

    assert result.preamble == (
        "use std::collections::HashMap;",
        "enum Value {",
        "    I64(i64),",
        "    Str(&'static str),",
        "}",
    )
    assert result.code == (
        "HashMap::from([\n"
        '    ("ts", Value::I64(1705321800)),\n'
        '    ("name", Value::Str("hi")),\n'
        "])"
    )


_COLLAPSED_DART_MAP_COUNT = 2


@dataclasses.dataclass(frozen=True, kw_only=True)
class _DartSkipNulls(Dart):
    """Dart subclass that skips null dict values.

    The widening bug in
    :func:`~literalizer._literalize._compute_dict_open_override` only
    manifests when a language combines a value-type-sensitive
    ``dict_open`` (produced by
    :func:`~literalizer._formatters.collection_openers.typed_dict_open`)
    with ``skip_null_dict_values=True``.  No production language pairs
    those two today — the ``typed_dict_open`` languages (Dart, CSharp,
    Kotlin, Scala, Go) all keep nulls, while the
    ``skip_null_dict_values=True`` languages (Java, Lua, Toml, Wren)
    all use ``fixed_dict_open`` whose constant opener never triggers
    widening.

    That is also why these tests live here rather than in the
    ``tests/integration/cases/`` golden-file suite, which iterates over
    :data:`~literalizer.languages.ALL_LANGUAGES` and has no way to
    inject a test-only language.
    """

    skip_null_dict_values: ClassVar[bool] = True


def test_dart_skip_nulls_widens_across_null_masked_types() -> None:
    """Widening fires when null-masked dict value types differ.

    With ``skip_null_dict_values=True``, filtering ``None`` out of
    ``{"a": None, "b": 1}`` and ``{"a": "hello", "b": None}`` leaves
    dicts whose remaining value types diverge (``int`` vs. ``String``).
    The override must widen so both dicts share a ``dynamic`` opener.
    """
    source = '[{"a": null, "b": 1}, {"a": "hello", "b": null}]'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=_DartSkipNulls(),
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


def test_dart_skip_nulls_widens_when_one_dict_collapses_to_empty() -> None:
    """Widening fires when one dict collapses to ``{}`` and another is
    typed.

    ``{"a": None}`` filters to ``{}`` (fallback opener), while
    ``{"x": 1}`` filters to ``{"x": 1}`` (``<String, int>``).  The
    override must widen both to the fallback so the sequence is
    consistent.
    """
    source = '[{"a": null}, {"x": 1}]'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=_DartSkipNulls(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )

    assert result.code == (
        "<Map<String, dynamic>>[\n"
        "    <String, dynamic>{},\n"
        '    <String, dynamic>{"x": 1},\n'
        "]"
    )


def test_dart_skip_nulls_no_widening_when_all_dicts_collapse_to_empty() -> (
    None
):
    """No override is needed when every dict collapses to ``{}``.

    Two all-null dicts filter to ``{}`` each.  Both render with the
    fallback ``<String, dynamic>{`` opener on their own, so widening
    would be a no-op.
    """
    source = '[{"a": null}, {"b": null}]'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=_DartSkipNulls(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )

    assert (
        result.code.count("<String, dynamic>{}") == _COLLAPSED_DART_MAP_COUNT
    )


def test_dart_skip_nulls_no_widening_when_filtered_dicts_match() -> None:
    """No override is needed when filtered dicts all share one opener.

    Null masks hide keys ``a`` and ``b`` in each dict, leaving only
    ``{"n": 1}`` and ``{"n": 2}`` — both ``<String, int>``.  Widening
    would be redundant; each dict renders with its own inferred opener.
    """
    source = '[{"a": null, "n": 1}, {"b": null, "n": 2}]'
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=_DartSkipNulls(),
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


def test_matlab_dict_key_with_quote() -> None:
    """MATLAB struct keys containing double quotes are decoded correctly.

    The ``_decode_matlab_string_expr`` helper must handle ``""`` inside a
    double-quoted string, which represents a literal ``"`` character.
    """
    yaml_string = '{"hello \\"world\\"": 1}\n'
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=Matlab(
            date_format=Matlab.date_formats.ISO,
            datetime_format=Matlab.datetime_formats.ISO,
            bytes_format=Matlab.bytes_formats.HEX,
            sequence_format=Matlab.sequence_formats.CELL_ARRAY,
        ),
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=None,
    )

    assert result.code == "'hello \"world\"', 1"


def test_cobol_level_number_cap() -> None:
    """COBOL level numbers are capped at 49 for deeply nested
    structures.
    """
    yaml_string = (
        "a:\n"
        "  b:\n"
        "    c:\n"
        "      d:\n"
        "        e:\n"
        "          f:\n"
        "            g:\n"
        "              h:\n"
        "                i:\n"
        "                  value: deep\n"
    )
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=COBOL,
        pre_indent_level=1,
        include_delimiters=True,
        variable_form=None,
    )

    assert result.code == (
        "\n"
        "        05 F-A.\n"
        "10 F-B.\n"
        "15 F-C.\n"
        "20 F-D.\n"
        "25 F-E.\n"
        "30 F-F.\n"
        "35 F-G.\n"
        "40 F-H.\n"
        "45 F-I.\n"
        '49 F-VALUE PIC X(4) VALUE "deep".\n'
        "    "
    )


def test_fortran_continuation_with_escaped_quote_and_comment() -> None:
    """Line continuation handles escaped quotes before inline comments."""
    yaml_string = "host: it's here  # a comment\nport: 80  # another\n"
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=FORTRAN,
        pre_indent_level=0,
        variable_form=NewVariable(name="cfg"),
        include_delimiters=True,
    )

    assert result.code == (
        "type(fval_t) :: cfg\n"
        "cfg = fmap([fval_t :: &\n"
        "    fentry('host', fstr('it''s here')), &  ! a comment\n"
        "    fentry('port', fint(80_int64)) &  ! another\n"
        "])"
    )


def test_cobol_key_name_trailing_hyphen_after_truncation() -> None:
    """COBOL data names must not end with a hyphen after truncation."""
    long_key = "a-b-c-d-e-f-g-h-i-j-k-l-m-n-o"
    yaml_string = f'"{long_key}": 1\n'
    result = literalize(
        source=yaml_string,
        input_format=InputFormat.YAML,
        language=COBOL,
        pre_indent_level=1,
        include_delimiters=True,
        variable_form=None,
    )
    for line in result.code.splitlines():
        stripped = line.strip()
        if stripped.startswith("05 F-"):
            name = stripped.split()[1]
            assert not name.endswith("-")


def test_java_list_rejects_null_elements() -> None:
    """Java's ``List.of()`` does not accept null elements."""
    spec = Java(
        sequence_format=Java.sequence_formats.LIST,
    )
    expected_msg = re.escape(
        pattern="Java's List.of() does not accept null elements"
        " (got 3 items, including null). "
        "Use sequence_format=ARRAY instead."
    )
    with pytest.raises(
        expected_exception=NullInCollectionError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=json.dumps(obj=[1, None, "hello"]),
            input_format=InputFormat.JSON,
            language=spec,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


def test_gleam_call_stub_more_than_26_parameters() -> None:
    """Gleam type-var generation falls back to numeric suffixes past
    the 26-letter alphabet.

    Calls with 27 parameters exercise ``_gleam_type_var``'s numeric
    suffix branch, emitting ``z`` for the last single-letter slot and
    ``a1`` for the next one in the generated stub signature.
    """
    parameter_names = [f"p{i}" for i in range(27)]
    yaml_row = "\n".join(f"  - {i}" for i in range(27))
    source = f"---\n-\n{yaml_row}\n"
    result = literalize_call(
        source=source,
        input_format=InputFormat.YAML,
        language=Gleam(),
        target_function="process",
        parameter_names=parameter_names,
        wrap_in_file=True,
    )
    assert (
        "pub fn process("
        "_p0: a, _p1: b, _p2: c, _p3: d, _p4: e, _p5: f, _p6: g, "
        "_p7: h, _p8: i, _p9: j, _p10: k, _p11: l, _p12: m, _p13: n, "
        "_p14: o, _p15: p, _p16: q, _p17: r, _p18: s, _p19: t, "
        "_p20: u, _p21: v, _p22: w, _p23: x, _p24: y, _p25: z, "
        "_p26: a1) -> Nil { Nil }"
    ) in result.code


@pytest.mark.parametrize(
    argnames="yaml_value",
    argvalues=[".inf", "-.inf", ".nan"],
    ids=["positive_infinity", "negative_infinity", "nan"],
)
def test_gleam_special_floats_raise(yaml_value: str) -> None:
    """Gleam raises ``UnrepresentableSpecialFloatError`` for non-finite
    floats.

    Gleam targets Erlang, which has no expression that evaluates to a
    non-finite float, so the literalizer surfaces this at literalize
    time rather than producing output that panics at ``gleam run``.
    """
    with pytest.raises(expected_exception=UnrepresentableSpecialFloatError):
        literalize(
            source=f"- {yaml_value}\n",
            input_format=InputFormat.YAML,
            language=Gleam(),
        )


def test_mojo_variant_call_slot_with_unmappable_scalar_falls_back() -> None:
    """A Mojo VARIANT call slot containing an unmappable scalar (e.g.
    ``None``) falls back to the generic ``[*Ts: AnyType]`` stub.

    ``None`` is not in Mojo's call-arg scalar mapping, so
    ``_value_to_mojo_type`` returns ``None`` for it.  The typed-param
    helper detects the unresolved slot type and bails to the generic
    signature instead of emitting ``Variant[...]``.  This exercises the
    ``None in slot_types`` fallback branch.
    """
    source = "---\n- null\n- hello\n"
    variant_strategy = next(
        strategy
        for strategy in Mojo.heterogeneous_strategies
        if strategy.name == "VARIANT"
    )
    spec = Mojo(heterogeneous_strategy=variant_strategy)
    result = literalize_call(
        source=source,
        input_format=InputFormat.YAML,
        language=spec,
        target_function="process",
        parameter_names=["value"],
        per_element=True,
        wrap_in_file=True,
    )
    assert "def process[*Ts: AnyType](*args: *Ts):" in result.code


def test_mojo_variant_homogeneous_slot_skipped_in_wrap_ids() -> None:
    """A homogeneous all-scalar VARIANT slot contributes no wrap ids.

    With a 2-param Mojo VARIANT call where slot 0 diverges
    (``String, Int, Bool``) but slot 1 is uniformly ``String``, the
    cross-call wrap-id helper wraps slot-0 values but leaves slot-1
    values untouched.  This exercises the ``len(slot_types) <= 1``
    short-circuit in ``_mojo_cross_call_scalar_wrap_ids``.
    """
    source = "---\n- - hello\n  - a\n- - 42\n  - b\n- - true\n  - c\n"
    variant_strategy = next(
        strategy
        for strategy in Mojo.heterogeneous_strategies
        if strategy.name == "VARIANT"
    )
    spec = Mojo(heterogeneous_strategy=variant_strategy)
    result = literalize_call(
        source=source,
        input_format=InputFormat.YAML,
        language=spec,
        target_function="process",
        parameter_names=["divergent", "uniform"],
        per_element=True,
        wrap_in_file=True,
    )
    assert 'process(Value(String("hello")), "a")' in result.code
    assert 'process(Value(42), "b")' in result.code
    assert 'process(Value(True), "c")' in result.code


def test_jsonnet_wrap_calls_with_declarations_prepends_bindings() -> None:
    """Non-empty declarations are placed before the wrapped call
    expression.

    Jsonnet ``local`` bindings are invalid inside an array literal, so
    ``wrap_calls_with_declarations`` emits them before the
    ``wrap_in_file`` output rather than splicing them inside the array.
    """
    spec = Jsonnet()
    result = spec.wrap_calls_with_declarations(
        declarations=("local x = 1;",),
        calls="[x]",
        body_preamble=(),
    )
    assert result == "local x = 1;\n[x]"
