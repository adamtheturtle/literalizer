"""Focused JSON-mode cases that cannot be capability-generated.

Generic JSON inputs, option crosses, and combined variable forms belong to
the main variant matrix.  This module contains only regression cases for
language-specific implementation paths.
"""

import dataclasses
import enum

from beartype import beartype

import literalizer
from literalizer.languages import Cobol, Haskell, OCaml, Odin, PureScript

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
    EXISTING = enum.auto()


@dataclasses.dataclass(frozen=True, kw_only=True)
class _FocusedCase:
    """Declarative description of one focused JSON-mode regression."""

    lang_cls: literalizer.LanguageCls
    name: str
    json_type: str
    case_dir_name: str
    variable_form: _VariableFormKind


_EXISTING = _VariableFormKind.EXISTING


_FOCUSED_CASES: tuple[_FocusedCase, ...] = (
    # These immutable-language assignments take bespoke JSON-mode paths:
    # each renders a valid binding rather than a conventional reassignment.
    _FocusedCase(
        lang_cls=Haskell,
        name="Haskell_json_type_aeson_value_existing",
        json_type="AESON_VALUE",
        case_dir_name="dict_with_list_value",
        variable_form=_EXISTING,
    ),
    _FocusedCase(
        lang_cls=OCaml,
        name="OCaml_json_type_yojson_safe_t_existing",
        json_type="YOJSON_SAFE_T",
        case_dir_name="dict_with_list_value",
        variable_form=_EXISTING,
    ),
    _FocusedCase(
        lang_cls=PureScript,
        name="PureScript_json_type_argonaut_json_existing",
        json_type="ARGONAUT_JSON",
        case_dir_name="dict_with_list_value",
        variable_form=_EXISTING,
    ),
    # Odin emits a real assignment, so its file wrapper must inject the
    # declaration that makes an ExistingVariable fixture self-contained.
    _FocusedCase(
        lang_cls=Odin,
        name="Odin_json_type_json_value_existing",
        json_type="JSON_VALUE",
        case_dir_name="dict_with_list_value",
        variable_form=_EXISTING,
    ),
    # COBOL literals have no escapes, so CJSON splices non-printable bytes
    # into this string as hexadecimal literals.
    _FocusedCase(
        lang_cls=Cobol,
        name="Cobol_json_type_cjson_string_bytes",
        json_type="CJSON",
        case_dir_name="cobol_cjson_string_bytes",
        variable_form=_VariableFormKind.NEW,
    ),
)


@beartype
def _build_spec(*, case: _FocusedCase) -> literalizer.Language:
    """Build the language spec described by *case*."""
    default_spec = make_spec(lang_cls=case.lang_cls)
    return make_spec(
        lang_cls=case.lang_cls,
        json_type=enum_member_by_name(
            enum_cls=default_spec.json_types,
            name=case.json_type,
        ),
    )


@beartype
def _build_variable_form(
    *, kind: _VariableFormKind
) -> literalizer.VariableForm:
    """Build the variable form selected by *kind*."""
    if kind is _VariableFormKind.NEW:
        return wrap_variable_form()
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
        for case in _FOCUSED_CASES
    ]
