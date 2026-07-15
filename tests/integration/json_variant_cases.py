"""Focused JSON-mode cases that do not fit the generic variant matrix.

The main variant matrix is capability-driven.  These cases deliberately
exercise particular interactions in particular language implementations, so
keeping them in a separate, declarative table makes that test policy visible
without teaching the matrix orchestrator about every language class.
"""

import dataclasses
import enum

from beartype import beartype

import literalizer
from literalizer.languages import (
    C,
    Cobol,
    Cpp,
    Crystal,
    CSharp,
    Elm,
    FSharp,
    Gleam,
    Haskell,
    Java,
    Kotlin,
    Nim,
    OCaml,
    Odin,
    PureScript,
    Rust,
    Scala,
    Zig,
)

from .language_specs import make_spec
from .variant_types import (
    Variant,
    VariantCase,
    enum_member_by_name,
    wrap_variable_form,
)


class _VariableFormKind(enum.Enum):
    """Variable form used by a focused regression case."""

    NEW = enum.auto()
    BOTH = enum.auto()
    EXISTING = enum.auto()


@dataclasses.dataclass(frozen=True, kw_only=True)
class _ExtraCase:
    """Declarative description of one focused JSON-mode regression."""

    lang_cls: literalizer.LanguageCls
    name: str
    json_type: str
    case_dir_name: str
    variable_form: _VariableFormKind
    declaration_style: str | None
    datetime_format: str | None
    bytes_format: str | None


_BOTH = _VariableFormKind.BOTH
_EXISTING = _VariableFormKind.EXISTING


_EXTRA_CASES: tuple[_ExtraCase, ...] = (
    _ExtraCase(
        lang_cls=Rust,
        name="Rust_json_type_serde_json_value_combined",
        json_type="SERDE_JSON_VALUE",
        case_dir_name="dict_with_list_value",
        variable_form=_BOTH,
        declaration_style="LET_MUT",
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Rust,
        name="Rust_json_type_serde_json_value_lazy_static",
        json_type="SERDE_JSON_VALUE",
        case_dir_name="dict_with_list_value",
        variable_form=_VariableFormKind.NEW,
        declaration_style="LAZY_STATIC",
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Crystal,
        name="Crystal_json_type_json_any_combined",
        json_type="JSON_ANY",
        case_dir_name="dict_with_list_value",
        variable_form=_BOTH,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Java,
        name="Java_json_type_jackson_json_node_combined",
        json_type="JACKSON_JSON_NODE",
        case_dir_name="dict_with_list_value",
        variable_form=_BOTH,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Scala,
        name="Scala_json_type_circe_combined",
        json_type="CIRCE",
        case_dir_name="dict_with_list_value",
        variable_form=_BOTH,
        declaration_style="VAR",
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=CSharp,
        name="CSharp_json_type_json_node_combined",
        json_type="SYSTEM_TEXT_JSON_NODE",
        case_dir_name="dict_with_list_value",
        variable_form=_BOTH,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Nim,
        name="Nim_json_type_json_node_combined",
        json_type="JSON_NODE",
        case_dir_name="dict_with_list_value",
        variable_form=_BOTH,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Zig,
        name="Zig_json_type_std_json_value_combined",
        json_type="STD_JSON_VALUE",
        case_dir_name="dict_with_list_value",
        variable_form=_BOTH,
        declaration_style="VAR",
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Haskell,
        name="Haskell_json_type_aeson_value_existing",
        json_type="AESON_VALUE",
        case_dir_name="dict_with_list_value",
        variable_form=_EXISTING,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Odin,
        name="Odin_json_type_json_value_existing",
        json_type="JSON_VALUE",
        case_dir_name="dict_with_list_value",
        variable_form=_EXISTING,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=OCaml,
        name="OCaml_json_type_yojson_safe_t_existing",
        json_type="YOJSON_SAFE_T",
        case_dir_name="dict_with_list_value",
        variable_form=_EXISTING,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    # The shared JSON inputs contain no False value, so this pins OCaml's
    # YOJSON_SAFE_T false-literal branch.
    _ExtraCase(
        lang_cls=OCaml,
        name="OCaml_json_type_yojson_safe_t_bool_list",
        json_type="YOJSON_SAFE_T",
        case_dir_name="bool_list",
        variable_form=_VariableFormKind.NEW,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Kotlin,
        name="Kotlin_json_type_kotlinx_json_element_combined",
        json_type="KOTLINX_JSON_ELEMENT",
        case_dir_name="dict_with_list_value",
        variable_form=_BOTH,
        declaration_style="VAR",
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Cpp,
        name="Cpp_json_type_nlohmann_json_combined",
        json_type="NLOHMANN_JSON",
        case_dir_name="dict_with_list_value",
        variable_form=_BOTH,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=C,
        name="C_json_type_cjson_combined",
        json_type="CJSON",
        case_dir_name="dict_with_list_value",
        variable_form=_BOTH,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Cobol,
        name="Cobol_json_type_cjson_combined",
        json_type="CJSON",
        case_dir_name="dict_with_list_value",
        variable_form=_BOTH,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    # COBOL literals have no escapes, so CJSON splices non-printable bytes
    # into this string as hexadecimal literals.
    _ExtraCase(
        lang_cls=Cobol,
        name="Cobol_json_type_cjson_string_bytes",
        json_type="CJSON",
        case_dir_name="cobol_cjson_string_bytes",
        variable_form=_VariableFormKind.NEW,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=FSharp,
        name="FSharp_json_type_json_node_combined",
        json_type="SYSTEM_TEXT_JSON_NODE",
        case_dir_name="dict_with_list_value",
        variable_form=_BOTH,
        declaration_style="LET_MUTABLE",
        datetime_format=None,
        bytes_format=None,
    ),
    # These inputs pin JSON-node scalar branches that the combined case does
    # not reach, including epoch conversion under JSON mode.
    _ExtraCase(
        lang_cls=FSharp,
        name="FSharp_json_type_json_node_null",
        json_type="SYSTEM_TEXT_JSON_NODE",
        case_dir_name="scalar_null",
        variable_form=_VariableFormKind.NEW,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=FSharp,
        name="FSharp_json_type_json_node_bool_list",
        json_type="SYSTEM_TEXT_JSON_NODE",
        case_dir_name="bool_list",
        variable_form=_VariableFormKind.NEW,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=FSharp,
        name="FSharp_json_type_json_node_epoch_dt",
        json_type="SYSTEM_TEXT_JSON_NODE",
        case_dir_name="scalar_datetime",
        variable_form=_VariableFormKind.NEW,
        declaration_style=None,
        datetime_format="EPOCH",
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Gleam,
        name="Gleam_json_type_gleam_json_json_datetime_epoch",
        json_type="GLEAM_JSON_JSON",
        case_dir_name="scalar_datetime_naive",
        variable_form=_VariableFormKind.NEW,
        declaration_style=None,
        datetime_format="EPOCH",
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Gleam,
        name="Gleam_json_type_gleam_json_json_bytes_base64",
        json_type="GLEAM_JSON_JSON",
        case_dir_name="binary",
        variable_form=_VariableFormKind.NEW,
        declaration_style=None,
        datetime_format=None,
        bytes_format="BASE64",
    ),
    _ExtraCase(
        lang_cls=Gleam,
        name="Gleam_json_type_gleam_json_json_combined",
        json_type="GLEAM_JSON_JSON",
        case_dir_name="dict_with_list_value",
        variable_form=_BOTH,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Nim,
        name="Nim_json_type_json_node_let",
        json_type="JSON_NODE",
        case_dir_name="dict_with_list_value",
        variable_form=_VariableFormKind.NEW,
        declaration_style="LET",
        datetime_format=None,
        bytes_format=None,
    ),
    # The shared JSON inputs do not cover Elm's False constructor, negative
    # numeric wrapping, special floats, or its cross-format JSON paths.
    _ExtraCase(
        lang_cls=Elm,
        name="Elm_json_type_json_encode_value_bool_list",
        json_type="JSON_ENCODE_VALUE",
        case_dir_name="bool_list",
        variable_form=_VariableFormKind.NEW,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Elm,
        name="Elm_json_type_json_encode_value_negative_int",
        json_type="JSON_ENCODE_VALUE",
        case_dir_name="scalar_int_negative_large",
        variable_form=_VariableFormKind.NEW,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Elm,
        name="Elm_json_type_json_encode_value_float_specials",
        json_type="JSON_ENCODE_VALUE",
        case_dir_name="float_special_values",
        variable_form=_VariableFormKind.NEW,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=Elm,
        name="Elm_json_type_json_encode_value_base64",
        json_type="JSON_ENCODE_VALUE",
        case_dir_name="binary",
        variable_form=_VariableFormKind.NEW,
        declaration_style=None,
        datetime_format=None,
        bytes_format="BASE64",
    ),
    _ExtraCase(
        lang_cls=Elm,
        name="Elm_json_type_json_encode_value_epoch",
        json_type="JSON_ENCODE_VALUE",
        case_dir_name="scalar_datetime",
        variable_form=_VariableFormKind.NEW,
        declaration_style=None,
        datetime_format="EPOCH",
        bytes_format=None,
    ),
    _ExtraCase(
        lang_cls=PureScript,
        name="PureScript_json_type_argonaut_json_existing",
        json_type="ARGONAUT_JSON",
        case_dir_name="dict_with_list_value",
        variable_form=_EXISTING,
        declaration_style=None,
        datetime_format=None,
        bytes_format=None,
    ),
)


@beartype
def _build_spec(*, case: _ExtraCase) -> literalizer.Language:
    """Build the language spec described by *case*."""
    default_spec = make_spec(lang_cls=case.lang_cls)
    kwargs: dict[str, object] = {
        "json_type": enum_member_by_name(
            enum_cls=default_spec.json_types,
            name=case.json_type,
        )
    }
    if case.declaration_style is not None:
        kwargs["declaration_style"] = enum_member_by_name(
            enum_cls=default_spec.declaration_styles,
            name=case.declaration_style,
        )
    if case.datetime_format is not None:
        kwargs["datetime_format"] = enum_member_by_name(
            enum_cls=default_spec.datetime_formats,
            name=case.datetime_format,
        )
    if case.bytes_format is not None:
        kwargs["bytes_format"] = enum_member_by_name(
            enum_cls=default_spec.bytes_formats,
            name=case.bytes_format,
        )
    return make_spec(lang_cls=case.lang_cls, **kwargs)


@beartype
def _build_variable_form(
    *, kind: _VariableFormKind
) -> literalizer.VariableForm:
    """Build the variable form selected by *kind*."""
    match kind:
        case _VariableFormKind.NEW:
            return wrap_variable_form()
        case _VariableFormKind.BOTH:
            return literalizer.BothVariableForms(
                name="my_data",
                modifiers=frozenset(),
            )
        case _VariableFormKind.EXISTING:
            return literalizer.ExistingVariable(name="my_data")


@beartype
def build_json_variant_cases() -> list[VariantCase]:
    """Build focused language-specific JSON-mode regression cases."""
    return [
        VariantCase(
            variant_name=case.name,
            variant=Variant(
                name=case.name,
                spec=_build_spec(case=case),
                lang_cls=case.lang_cls,
                collection_layout=literalizer.CollectionLayout.COMPACT,
            ),
            case_dir_name=case.case_dir_name,
            variable_form=_build_variable_form(kind=case.variable_form),
        )
        for case in _EXTRA_CASES
    ]
