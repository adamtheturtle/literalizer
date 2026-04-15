"""Regression test for ``fallback_value_type=None`` in
:func:`make_element_to_type`.

A custom Go variant with ``fallback_value_type=None`` exercises the
code path that would otherwise interpolate the string ``"None"`` into
a type template like ``map[string]{inner}``.
"""

import json
import textwrap

import literalizer
from literalizer._formatters.collection_openers import (
    make_element_to_type,
    make_type_to_opener,
    typed_dict_open,
)
from literalizer._language import DictFormatConfig
from literalizer.languages import Go


def test_none_fallback_value_type_uses_dict_open_fallback() -> None:
    """When ``fallback_value_type`` is ``None`` and dict values have
    mixed types, the dict opener must use its fallback — not interpolate
    the string ``"None"`` into the type template.
    """
    source = json.dumps(
        {
            "group_a": {"x": 1, "y": "hello"},
            "group_b": {"p": True, "q": 42},
        }
    )

    spec = Go()
    resolver = make_element_to_type(
        str_type="string",
        bool_type="bool",
        int_type="int",
        float_type="float64",
        mixed_numeric_type="float64",
        bytes_type="string",
        date_type=None,
        datetime_type=None,
        list_template="[]{inner}",
        dict_type_template="map[string]{inner}",
        fallback_value_type=None,
    )
    fallback = "map[string]any{"
    spec.dict_format_config = DictFormatConfig(
        dict_open=typed_dict_open(
            type_to_opener=make_type_to_opener(
                element_to_type=resolver,
                opener_template="map[string]{type_name}{{",
            ),
            fallback=fallback,
        ),
        close="}",
        format_entry=spec.dict_format_config.format_entry,
        empty_dict=spec.dict_format_config.empty_dict,
        preamble_lines=spec.dict_format_config.preamble_lines,
        narrowed_open=spec.dict_format_config.narrowed_open,
    )
    result = literalizer.literalize(
        source=source,
        input_format=literalizer.InputFormat.JSON,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=literalizer.NewVariable(name="my_data"),
        error_on_coercion=False,
        wrap_in_file=True,
    )
    expected = textwrap.dedent("""\
        package main

        func main() {
        my_data := map[string]any{
        \t"group_a": map[string]any{"x": 1, "y": "hello"},
        \t"group_b": map[string]any{"p": true, "q": 42},
        }
        _ = my_data
        }""")
    assert result.code == expected
