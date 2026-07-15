"""Focused JSON-mode cases that cannot be capability-generated.

Generic JSON inputs, option crosses, and combined variable forms belong to
the main variant matrix.  This module contains only regression cases for
language-specific implementation paths.
"""

import dataclasses

from beartype import beartype

import literalizer
from literalizer.languages import Cobol

from .language_specs import make_spec
from .variant_types import (
    Variant,
    VariantCase,
    enum_member_by_name,
    wrap_variable_form,
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class _FocusedCase:
    """Declarative description of one focused JSON-mode regression."""

    lang_cls: literalizer.LanguageCls
    name: str
    json_type: str
    case_dir_name: str


_FOCUSED_CASES: tuple[_FocusedCase, ...] = (
    # COBOL literals have no escapes, so CJSON splices non-printable bytes
    # into this string as hexadecimal literals.
    _FocusedCase(
        lang_cls=Cobol,
        name="Cobol_json_type_cjson_string_bytes",
        json_type="CJSON",
        case_dir_name="cobol_cjson_string_bytes",
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
            variable_form=wrap_variable_form(),
        )
        for case in _FOCUSED_CASES
    ]
