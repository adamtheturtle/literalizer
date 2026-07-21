"""Input-fixture coverage policy for the language-variant matrix."""

from pathlib import Path

from beartype import beartype

from .case_discovery import discover_cases
from .variant_types import CaseInput

_CASES_DIR = Path(__file__).parent / "cases"


@beartype
def _ci(*, case_dir_name: str, suffix: str) -> CaseInput:
    """Shorthand for :class:`CaseInput` to keep the table compact."""
    return CaseInput(case_dir_name=case_dir_name, suffix=suffix)


INT_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="int_list", suffix=""),
    _ci(case_dir_name="int_list_large", suffix="_large"),
    _ci(case_dir_name="int_list_with_zero", suffix="_zero"),
    _ci(case_dir_name="scalar_int", suffix=""),
    _ci(case_dir_name="scalar_int_large", suffix=""),
)

FLOAT_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="float_list", suffix=""),
    _ci(case_dir_name="float_scientific_notation", suffix="_s"),
    _ci(case_dir_name="float_special_values", suffix="_v"),
    _ci(case_dir_name="nested_float_list", suffix="_n"),
    _ci(case_dir_name="scalar_float", suffix=""),
)

BASIC_COLLECTIONS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="simple_sequence", suffix=""),
    _ci(case_dir_name="simple_dict", suffix="_dict"),
    _ci(case_dir_name="set", suffix="_set"),
)

ADT_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="simple_dict", suffix=""),
    _ci(case_dir_name="float_special_values", suffix="_v"),
    _ci(case_dir_name="float_list", suffix="_float"),
    _ci(case_dir_name="binary", suffix="_binary"),
    _ci(case_dir_name="scalar_date", suffix="_date"),
    _ci(case_dir_name="scalar_datetime", suffix="_datetime"),
)

HETEROGENEOUS_INPUTS: tuple[CaseInput, ...] = tuple(
    _ci(case_dir_name=d, suffix=s)
    for d, s in (
        ("dict_mixed_scalars", ""),
        ("mixed_type_dicts_in_sequence", ""),
        ("nested_mixed_types", "_sibling"),
        ("nested_mixed_inner", "_inner"),
        ("nested_mixed_dict", ""),
        ("dict_all_scalar_types", ""),
        ("nested_sequences", ""),
        ("dict_mixed_int_widths", ""),
        ("ordered_map", ""),
        ("heterogeneous_list_with_string", ""),
        ("dict_with_list_value", "_list_val"),
        ("multiline_sibling_list_widening", "_sibling_widening"),
        ("record_basic", ""),
        ("record_pure_scalars", ""),
        ("record_nested_container", ""),
        ("record_sequence", ""),
        ("record_two_shapes", ""),
        ("record_nested_record", ""),
        ("record_list_of_records", ""),
        ("tuple_record_field", ""),
        ("tuple_record_seq_sibling", ""),
        ("tuple_int_key_dict_value", ""),
        ("tuple_top_level", ""),
        ("tuple_record_sequence", ""),
        ("tuple_pair_record_field", ""),
        ("tuple_pair_top_level", ""),
        ("tuple_triple_record_field", ""),
        ("tuple_triple_top_level", ""),
    )
)

# The ``heterogeneous_strategy`` axis additionally covers
# ``int_key_dict`` and ``empty_dict`` so the RECORD strategy walks the
# two non-record-eligible dict shapes through ``record_shape_for_dict``:
# ``int_key_dict`` exercises the non-string-key branch and ``empty_dict``
# exercises the empty-dict branch.  Languages that cannot represent
# integer keys raise ``UnrepresentableInputError`` and are skipped; the
# rest render both as plain maps, identical to the default output.
HETEROGENEOUS_STRATEGY_INPUTS: tuple[CaseInput, ...] = (
    *HETEROGENEOUS_INPUTS,
    _ci(case_dir_name="int_key_dict", suffix=""),
    _ci(case_dir_name="empty_dict", suffix=""),
)

# These compiler-verified regressions exercise recursive object-variant
# container carriers. Keep them on their focused axis rather than expanding
# every language's heterogeneous matrix.
OBJECT_VARIANT_CONTAINER_INPUTS: tuple[CaseInput, ...] = tuple(
    _ci(case_dir_name=case_dir_name, suffix="")
    for case_dir_name in (
        "object_variant_mixed_scalar_empty_list",
        "object_variant_integer_widening_tiers",
        "object_variant_null_only_map",
        "object_variant_nested_tables_mixed_int_widths",
        "object_variant_empty_and_nonempty_maps",
        "object_variant_null_only_list",
        "object_variant_scalar_empty_map",
        "object_variant_nested_empty_list_table",
        "object_variant_all_wrapped_children",
    )
)

DICT_FORMAT_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="simple_dict", suffix=""),
    _ci(case_dir_name="dict_with_list_value", suffix="_list_val"),
)

DEFAULT_DICT_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="empty_dict", suffix=""),
    _ci(case_dir_name="simple_dict", suffix=""),
)

_NUMERIC_INPUTS: tuple[CaseInput, ...] = (
    _ci(case_dir_name="int_list", suffix=""),
    _ci(case_dir_name="int_list_large", suffix="_large"),
    _ci(case_dir_name="int_list_with_zero", suffix="_zero"),
    _ci(case_dir_name="scalar_int", suffix=""),
    _ci(case_dir_name="scalar_int_large", suffix=""),
    _ci(case_dir_name="float_list", suffix="_float"),
    _ci(case_dir_name="float_scientific_notation", suffix="_float_s"),
    _ci(case_dir_name="float_special_values", suffix="_float_v"),
    _ci(case_dir_name="nested_float_list", suffix="_float_n"),
    _ci(case_dir_name="scalar_float", suffix="_float_scalar"),
)


# Per-axis input table.  Each axis names the input case directories it
# should run against; coverage is added or removed by editing this table
# alone.  The cross product of every axis's variants with its inputs
# yields the full set of golden-file test cases.
AXIS_INPUTS: dict[str, tuple[CaseInput, ...]] = {
    "date": (
        _ci(case_dir_name="scalar_date", suffix=""),
        _ci(case_dir_name="date_list", suffix=""),
        _ci(case_dir_name="date_set", suffix=""),
    ),
    "datetime": (
        _ci(case_dir_name="scalar_datetime", suffix=""),
        _ci(case_dir_name="scalar_datetime_naive", suffix="_naive"),
        _ci(case_dir_name="scalar_datetime_non_utc", suffix="_non_utc"),
        _ci(case_dir_name="datetime_list", suffix=""),
    ),
    "sequence": (
        _ci(case_dir_name="simple_sequence", suffix=""),
        _ci(case_dir_name="pair_sequence", suffix="_pair"),
        _ci(case_dir_name="triple_sequence", suffix="_triple"),
        _ci(case_dir_name="simple_sequence", suffix="_varname"),
        _ci(case_dir_name="float_list", suffix="_float"),
        _ci(case_dir_name="null_list", suffix="_null"),
        _ci(case_dir_name="binary_list", suffix="_binary"),
    ),
    "set": (
        _ci(case_dir_name="set", suffix=""),
        _ci(case_dir_name="int_set", suffix=""),
        _ci(case_dir_name="mixed_set", suffix=""),
        _ci(case_dir_name="empty_set", suffix=""),
        _ci(case_dir_name="set_mixed_int_widths", suffix=""),
    ),
    "default_set_element_type": (
        _ci(case_dir_name="empty_set", suffix=""),
        _ci(case_dir_name="set", suffix=""),
    ),
    "default_sequence_element_type": (
        _ci(case_dir_name="empty_sequence", suffix=""),
        _ci(case_dir_name="simple_sequence", suffix=""),
    ),
    "json_type": (
        _ci(case_dir_name="dict_with_list_value", suffix=""),
        _ci(case_dir_name="nested_mixed_inner", suffix="_nested_mixed"),
        _ci(case_dir_name="dates", suffix="_dates"),
        _ci(case_dir_name="dict_with_nulls", suffix="_nulls"),
        _ci(case_dir_name="date_set", suffix="_date_set"),
        _ci(case_dir_name="ordered_map", suffix="_ordered_map"),
        _ci(case_dir_name="scalar_datetime_naive", suffix="_datetime_naive"),
        _ci(case_dir_name="binary", suffix="_binary"),
        _ci(case_dir_name="scalar_float", suffix="_float"),
        _ci(case_dir_name="scalar_time", suffix="_time"),
        _ci(case_dir_name="scalar_int_large", suffix="_long"),
        _ci(case_dir_name="scalar_int_very_large", suffix="_bigint"),
        _ci(case_dir_name="bool_list", suffix="_bool_list"),
        _ci(case_dir_name="scalar_null", suffix="_null"),
        _ci(case_dir_name="json_string_escaping", suffix="_string_escaping"),
        _ci(
            case_dir_name="scalar_int_negative_large",
            suffix="_negative_large",
        ),
        _ci(case_dir_name="float_special_values", suffix="_float_specials"),
    ),
    "json_type_bytes_cross": (_ci(case_dir_name="binary", suffix=""),),
    "json_type_datetime_cross": (
        _ci(case_dir_name="scalar_datetime", suffix=""),
        _ci(case_dir_name="scalar_datetime_naive", suffix="_naive"),
    ),
    "json_type_declaration_cross": (
        _ci(case_dir_name="dict_with_list_value", suffix=""),
    ),
    "default_dict_value_type": DEFAULT_DICT_INPUTS,
    "default_dict_key_type": DEFAULT_DICT_INPUTS,
    "empty_dict_key": (_ci(case_dir_name="simple_dict", suffix=""),),
    "default_ordered_map_value_type": (
        _ci(case_dir_name="ordered_map", suffix=""),
    ),
    "comment": (_ci(case_dir_name="comments", suffix=""),),
    "type_hints": tuple(
        _ci(case_dir_name=d, suffix="")
        for d in (
            "type_hints",
            "scalar_date",
            "scalar_datetime",
            # ``scalar_time`` pins the ``case datetime.time():`` scalar
            # type-hint arm under non-default (``ALWAYS``)
            # ``variable_type_hints``, replacing the
            # ``test_datetime_time_always_type_hint_renders`` shim
            # (issue #2518).  The Python-only ``_structural_type_id``
            # time arm cannot ride this all-languages axis (it would
            # force non-compiling Kotlin nested-time-list output); it
            # keeps a focused pytest test instead.
            "scalar_time",
            "binary",
            "mixed_type_dicts_in_sequence",
            "empty_dicts_in_sequence",
            "float_list",
            "int_list",
            "empty_list",
            "int_set",
            "mixed_set",
            "empty_set",
            "set_mixed_int_widths",
            "list_mixed_int_widths",
            "map_mixed_int_widths",
            "mixed_number_list",
            "nested_sequence",
            "dict_with_list_value",
            "ordered_map_in_sequence",
        )
    ),
    "type_hints_cross": tuple(
        _ci(case_dir_name=d, suffix="")
        for d in (
            "int_list",
            "int_list_large",
            "pair_sequence",
            "empty_list",
            "scalar_date",
            "scalar_datetime",
            "simple_dict",
            "int_set",
            "bool_list",
            "float_list",
        )
    ),
    "declaration_style": tuple(
        _ci(case_dir_name=d, suffix="")
        for d in (
            "simple_sequence",
            "simple_dict",
            "empty_list",
            "empty_dict",
            "int_list",
            "int_key_dict",
            "scalar_int",
            "scalar_int_large",
            "scalar_float",
            "scalar_bool",
            "scalar_string",
            "scalar_null",
            "scalar_date",
            "scalar_datetime",
            "time_dict",
            "binary",
            "set_mixed_int_widths",
            "list_mixed_int_widths",
            "map_mixed_int_widths",
        )
    ),
    "dict_format": DICT_FORMAT_INPUTS,
    "dict_entry_style": DICT_FORMAT_INPUTS,
    "float_format": FLOAT_INPUTS,
    "integer_format": INT_INPUTS,
    "numeric_literal_suffix": _NUMERIC_INPUTS,
    "numeric_separator": _NUMERIC_INPUTS,
    "string_format": (
        _ci(case_dir_name="string_list", suffix=""),
        _ci(case_dir_name="string_with_backslash", suffix=""),
        _ci(case_dir_name="simple_dict", suffix="_dict"),
        _ci(case_dir_name="binary", suffix="_binary"),
        _ci(case_dir_name="scalar_string", suffix=""),
        _ci(case_dir_name="time_list", suffix="_time"),
        # Pins the non-ASCII branch of each non-default string format:
        # Perl ``DOUBLE_UTF8`` adds ``use utf8;`` and emits literal
        # characters (#2600), and every other multi-format language's
        # alternate quoting style is exercised against the same input.
        _ci(case_dir_name="string_unicode", suffix=""),
    ),
    "string_format_date_cross": (_ci(case_dir_name="scalar_date", suffix=""),),
    "string_format_datetime_cross": (
        _ci(case_dir_name="scalar_datetime", suffix="_dt"),
    ),
    "bytes_format": (_ci(case_dir_name="binary", suffix=""),),
    "trailing_comma": BASIC_COLLECTIONS,
    "statement_terminator_style": BASIC_COLLECTIONS,
    "collection_layout": tuple(
        _ci(case_dir_name=d, suffix="")
        for d in (
            "dict_with_list_value",
            "nested",
            "nested_mixed_set",
            "multiline_sibling_list_widening",
        )
    ),
    "statement_terminator_style_decl": (
        _ci(case_dir_name="simple_sequence", suffix=""),
    ),
    "sequence_decl": (
        _ci(case_dir_name="int_list", suffix=""),
        # A one-element list pins the single-element-tuple trailing
        # comma in both the type annotation and the value (e.g. Rust
        # ``static my_data: (i32,) = (1,);``); a multi-element input
        # cannot exercise that carve-out.
        _ci(case_dir_name="int_list_single", suffix=""),
    ),
    "set_decl": (_ci(case_dir_name="set_mixed_int_widths", suffix=""),),
    "dict_decl": (_ci(case_dir_name="int_key_dict", suffix=""),),
    "type_name": ADT_INPUTS,
    "constructor_prefix": ADT_INPUTS,
    "numeric_style": (
        _ci(case_dir_name="int_list", suffix=""),
        _ci(case_dir_name="int_list_large", suffix="_large"),
        _ci(case_dir_name="int_list_with_zero", suffix="_zero"),
        _ci(case_dir_name="float_list", suffix=""),
        _ci(case_dir_name="float_special_values", suffix=""),
        _ci(case_dir_name="mixed_number_list", suffix=""),
        _ci(case_dir_name="scalars", suffix=""),
    ),
    "c_field_name": (
        _ci(case_dir_name="simple_dict", suffix=""),
        _ci(case_dir_name="simple_sequence", suffix=""),
    ),
    "constructor_name": (_ci(case_dir_name="simple_dict", suffix=""),),
    "heterogeneous_strategy": (
        *HETEROGENEOUS_STRATEGY_INPUTS,
        # ``heterogeneous_time_string`` carries a time and a string in
        # one list to pin the ``datetime.time`` arm of each language's
        # heterogeneous-variant signature builder under its non-default
        # wrap-as-variant strategies (Rust tagged enum, Dhall union
        # type, Nim object variant).  It replaces the
        # ``test_datetime_time_heterogeneous_variant_renders`` shim
        # (issue #2518).
        _ci(case_dir_name="heterogeneous_time_string", suffix=""),
    ),
    "object_variant_containers": OBJECT_VARIANT_CONTAINER_INPUTS,
    "heterogeneous_strategy_datetime_cross": (
        _ci(case_dir_name="dict_all_scalar_types", suffix=""),
    ),
    "heterogeneous_value_enum_name": HETEROGENEOUS_INPUTS,
    "record_shape_names": (
        _ci(case_dir_name="record_named_shape", suffix=""),
        _ci(case_dir_name="record_named_nested_record", suffix=""),
    ),
    "heterogeneous_value_union_name": HETEROGENEOUS_INPUTS,
    "heterogeneous_value_variant_name": HETEROGENEOUS_INPUTS,
    "record_unify_optional_fields": (
        _ci(case_dir_name="record_optional_unify", suffix=""),
    ),
    "record_nonrecord_dict_field": (
        _ci(case_dir_name="record_nonrecord_dict_field", suffix=""),
    ),
    "record_keyword_field": (
        _ci(case_dir_name="record_keyword_field", suffix=""),
    ),
    "record_quoted_field": (
        _ci(case_dir_name="record_quoted_field", suffix=""),
    ),
    "record_field_type_split": (
        _ci(case_dir_name="record_field_type_split", suffix=""),
    ),
    "record_nested_map_fallback": (
        _ci(case_dir_name="record_nested_map_fallback", suffix=""),
    ),
    "nested_map_widening": (
        _ci(case_dir_name="nested_map_widening", suffix=""),
    ),
    "string_embedded_nul": (
        _ci(case_dir_name="string_embedded_nul", suffix=""),
    ),
    "empty_map_narrowing": (
        _ci(case_dir_name="empty_map_narrowing", suffix=""),
    ),
    "tagged_enum_empty_container": (
        _ci(case_dir_name="tagged_enum_empty_list", suffix=""),
        _ci(case_dir_name="tagged_enum_empty_map", suffix=""),
    ),
    "empty_container_type_hint": (
        _ci(case_dir_name="tagged_enum_empty_map", suffix=""),
    ),
    "dhall_nested_map_widening": (
        _ci(case_dir_name="dhall_nested_map_widening", suffix=""),
    ),
    "record_epoch_i32_overflow": (
        _ci(case_dir_name="record_epoch_datetime_i32_overflow", suffix=""),
    ),
    "record_numeric_cross": (_ci(case_dir_name="record_wide_int", suffix=""),),
    "integer_width_strategy": (
        _ci(case_dir_name="record_wide_int", suffix=""),
        _ci(case_dir_name="int_list", suffix=""),
        _ci(case_dir_name="dict_wide_int_key", suffix=""),
    ),
    "language_version": tuple(
        _ci(case_dir_name=case_dir_name, suffix="")
        for case_dir_name in dict.fromkeys(
            case_dir_name
            for case_dir_name, _ in discover_cases(cases_dir=_CASES_DIR)
        )
    ),
    "language_version_cross_dict_type": (
        _ci(case_dir_name="empty_dict", suffix=""),
        _ci(case_dir_name="empty_ordered_map", suffix=""),
    ),
    "bool_format": (
        _ci(case_dir_name="scalar_bool", suffix=""),
        _ci(case_dir_name="bool_list", suffix=""),
        _ci(case_dir_name="nested_bool_list", suffix=""),
    ),
}
