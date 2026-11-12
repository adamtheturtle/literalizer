"""``literalize`` golden-file case configuration and runner for ``$ref``
support.

Each ``cases/literalize_ref_*`` directory declares in its own ``case.toml``
how it is driven through :func:`literalizer.literalize` with a ``ref_case``
set to the language's default identifier case.  The runner
(``run_literalize_ref_golden_case``) is shared by
``test_literalize_ref_golden_file``.
"""

import copy
import dataclasses
import enum
import functools
import json
from pathlib import Path

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer.exceptions import (
    CallArgNotSupportedError,
    CallsNotSupportedByLanguageError,
    CallsNotSupportedByToolError,
    ExistingVariableNotSelfContainedError,
    HeterogeneousCollectionError,
    IncompatibleFormatsError,
    InvalidDictKeyError,
    NullInCollectionError,
    ReservedVariableNameError,
    UnrepresentableInputError,
    VariableNameNotSupportedError,
)
from tests.enum_members import enum_member_by_name

from .case_manifests import (
    REF_DEFAULT_OWNER,
    REF_OWNER,
    OwnerName,
    RefCaseSpec,
    case_input,
    ref_case_specs,
)
from .golden_checks import (
    GoldenSkips,
    SkipPolicy,
    SkipReason,
    check_golden,
)
from .language_metadata import language_metadata
from .language_specs import (
    find_redefinition_styles,
    make_golden_path,
    make_spec,
    reference_case_for_declaration_style,
    sorted_languages,
    with_per_fixture_module_name,
)
from .ref_consumers import (
    compose_external_ref_fixture,
    external_assignment_spec,
    ref_fixture_contents,
)
from .reference_inputs import bound_ref_inputs, parse_ref_input
from .variant_cases import Variant, variants_for_axis
from .variant_context import config_with_variant_layout

CASES_DIR = Path(__file__).parent / "cases"

# A ``$ref`` case is written once for every language, so an input a
# language cannot represent, or a ref identifier it will not spell,
# skips rather than fails.
_REF_SKIPS: SkipPolicy = SkipPolicy(
    reasons=(
        SkipReason(
            error=CallsNotSupportedByLanguageError,
            reason="has no generated consumer call syntax",
            unlink=True,
        ),
        SkipReason(
            error=CallsNotSupportedByToolError,
            reason="cannot generate consumer calls",
            unlink=True,
        ),
        SkipReason(
            error=IncompatibleFormatsError,
            reason="reference input is incompatible with the selected formats",
            unlink=True,
        ),
        SkipReason(
            error=ReservedVariableNameError,
            reason="rejects a declared reference identifier",
            unlink=True,
        ),
        SkipReason(
            error=VariableNameNotSupportedError,
            reason="cannot declare the reference binding",
            unlink=True,
        ),
        SkipReason(
            error=ExistingVariableNotSelfContainedError,
            reason=(
                "cannot wrap an assignment without its destination declaration"
            ),
            unlink=True,
        ),
        SkipReason(
            error=NullInCollectionError,
            reason="cannot represent null in this collection",
            unlink=True,
        ),
        SkipReason(
            error=HeterogeneousCollectionError,
            reason="cannot represent this heterogeneous input",
            unlink=True,
        ),
        SkipReason(
            error=UnrepresentableInputError,
            reason="cannot represent this heterogeneous input",
            unlink=True,
        ),
        SkipReason(
            error=CallArgNotSupportedError,
            reason="rejected ref identifier",
            unlink=True,
        ),
        SkipReason(
            error=InvalidDictKeyError,
            reason="cannot represent a dictionary key",
            unlink=True,
        ),
    ),
    suffix="",
)


@dataclasses.dataclass(frozen=True)
class LiteralizeRefCase:
    """A parameterized literalize-ref golden-file test case."""

    config: RefCaseSpec
    lang_cls: literalizer.LanguageCls


@functools.cache
@beartype
def discover_literalize_ref_cases(
    *, owner: OwnerName
) -> list[LiteralizeRefCase]:
    """Return reference cases for the selected API owner.

    Explicit reference cases require a supported reference spelling and,
    for combined forms, a redefinition style. Default cases exercise the
    public defaults without imposing those explicit options.
    """
    return [
        LiteralizeRefCase(config=config, lang_cls=lang_cls)
        for config in ref_case_specs(cases_dir=CASES_DIR, owner=owner)
        if not config.variant_only
        for lang_cls in sorted_languages()
        if config.admits_language(lang_cls=lang_cls)
        if owner == REF_DEFAULT_OWNER
        or config.variable_form != "both"
        or bool(find_redefinition_styles(spec=make_spec(lang_cls=lang_cls)))
        if owner == REF_DEFAULT_OWNER
        or config.ref_case_for(lang_cls=lang_cls) is None
        or config.ref_case_for(lang_cls=lang_cls)
        in lang_cls.supported_ref_cases
    ]


@dataclasses.dataclass(frozen=True)
class LiteralizeRefVariantCase:
    """A reference scenario paired with an effective language variant."""

    config: RefCaseSpec
    variant: Variant
    ref_case: literalizer.IdentifierCase | None

    @property
    def golden_name(self) -> str:
        """Retain whether the public API receives an explicit ref case."""
        suffix = "ref_default" if self.ref_case is None else "ref"
        return f"{self.variant.name}_{suffix}"


@beartype
def _reference_variant_case(
    *, config: RefCaseSpec, variant: Variant, owner: OwnerName
) -> LiteralizeRefVariantCase | None:
    """Retain selected options and reject unsupported reference styles."""
    lang_cls = variant.lang_cls
    if not config.admits_language(lang_cls=lang_cls):
        return None
    ref_case = config.ref_case_for(lang_cls=lang_cls)
    if ref_case is not None and ref_case not in lang_cls.supported_ref_cases:
        return None
    spec = _ref_language_options(
        config=config, lang_cls=lang_cls, spec=variant.spec
    )
    if (
        config.variable_form == "both"
        and spec.declaration_style not in find_redefinition_styles(spec=spec)
    ):
        return None
    # A selected declaration variant is an explicit choice. The base
    # suite's automatic mutable-style fallback must not relabel it.
    names = language_metadata(
        language_id=lang_cls.language_id
    ).variants.declaration_style_variable_names
    reference_case = config.ref_case_for(lang_cls=lang_cls)
    if owner == REF_DEFAULT_OWNER:
        reference_case = None
    elif reference_case is None:
        reference_case = reference_case_for_declaration_style(
            lang_cls=lang_cls, spec=spec
        )
    selected_config = config_with_variant_layout(
        config=config, layout=variant.collection_layout
    ).model_copy(
        update={
            "declaration_style": spec.declaration_style.name,
            "variable_name": names.get(
                spec.declaration_style.name, config.variable_name
            ),
            "ref_case_override": reference_case,
        }
    )
    return LiteralizeRefVariantCase(
        config=selected_config,
        variant=dataclasses.replace(variant, spec=spec),
        ref_case=reference_case,
    )


@functools.cache
@beartype
def build_literalize_ref_variant_cases() -> list[LiteralizeRefVariantCase]:
    """Discover reference variants through the existing typed axis
    plans.
    """
    return [
        case
        for owner in (REF_OWNER, REF_DEFAULT_OWNER)
        for config in ref_case_specs(cases_dir=CASES_DIR, owner=owner)
        for entry in config.variants
        for variant in variants_for_axis(axis_key=entry.axis)
        if (
            case := _reference_variant_case(
                config=config, variant=variant, owner=owner
            )
        )
        is not None
    ]


@beartype
def _ref_language_options(
    *,
    config: RefCaseSpec,
    lang_cls: literalizer.LanguageCls,
    spec: literalizer.Language,
) -> literalizer.Language:
    """Apply the output modes explicitly selected by a reference case."""
    for name, enum_cls, choice in (
        (
            "variable_type_hints",
            lang_cls.VariableTypeHints,
            config.variable_type_hints,
        ),
        (
            "heterogeneous_strategy",
            lang_cls.HeterogeneousStrategies,
            config.heterogeneous_strategy,
        ),
        ("sequence_format", lang_cls.SequenceFormats, config.sequence_format),
        (
            "declaration_style",
            lang_cls.DeclarationStyles,
            config.declaration_style,
        ),
        ("json_type", lang_cls.JsonTypes, config.json_type),
        ("dict_format", lang_cls.DictFormats, config.dict_format),
    ):
        if choice is not None:
            spec = dataclasses.replace(
                spec,
                **{name: enum_member_by_name(enum_cls=enum_cls, name=choice)},
            )
    if config.default_sequence_element_type is not None:
        spec = dataclasses.replace(
            spec,
            default_sequence_element_type=config.default_sequence_element_type,
        )
    return spec


@beartype
def ref_language_versions(
    *, config: RefCaseSpec, lang_cls: literalizer.LanguageCls
) -> tuple[enum.Enum, ...]:
    """Return each effective target version once after applying
    options.
    """
    return tuple(
        dict.fromkeys(
            _ref_language_options(
                config=config,
                lang_cls=lang_cls,
                spec=make_spec(lang_cls=lang_cls, language_version=version),
            ).language_version
            for version in lang_cls.VersionFormats
        )
    )


@beartype
def ref_golden_path(
    *,
    config: RefCaseSpec,
    lang_cls: literalizer.LanguageCls,
    golden_name: str,
    cases_dir: Path,
    version: enum.Enum,
) -> Path:
    """Locate an ordinary or variant reference consumer fixture."""
    return make_golden_path(
        parent=cases_dir / config.case_dir_name,
        name=config.golden_name(name=golden_name),
        lang_cls=lang_cls,
        version=version,
    )


@beartype
def run_literalize_ref_golden_case(
    *,
    config: RefCaseSpec,
    lang_cls: literalizer.LanguageCls,
    spec: literalizer.Language,
    golden_name: str,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    ref_case: literalizer.IdentifierCase | None,
    version: enum.Enum,
    pytest_config: pytest.Config,
) -> None:
    """Run a literalize ``$ref`` golden-file case against *golden_name*.

    When *ref_case* is set, the ref identifier is spelled idiomatically
    for each language.  Each referenced identifier is supplied through
    ``bound_refs`` so a single :func:`literalizer.literalize` call
    emits the binding before its first use and the golden file is a
    complete unit that compiles, with per-language declaration
    sequencing.
    """
    spec = _ref_language_options(config=config, lang_cls=lang_cls, spec=spec)
    input_info = case_input(case_dir=cases_dir / config.case_dir_name)
    input_path = input_info.path
    input_source = input_path.read_text(encoding="utf-8")
    golden_path = ref_golden_path(
        config=config,
        lang_cls=lang_cls,
        golden_name=golden_name,
        cases_dir=cases_dir,
        version=version,
    )
    spec = with_per_fixture_module_name(spec=spec, golden_path=golden_path)
    if (
        config.variable_form == "both"
        and config.declaration_style is None
        and spec.declaration_style not in find_redefinition_styles(spec=spec)
    ):
        spec = dataclasses.replace(
            spec, declaration_style=find_redefinition_styles(spec=spec)[0]
        )
    variable_form_obj: literalizer.VariableForm | None = (
        config.resolved_variable_form()
    )
    if isinstance(variable_form_obj, literalizer.NewVariable):
        variable_form_obj = dataclasses.replace(
            variable_form_obj,
            modifiers=frozenset(
                enum_member_by_name(enum_cls=spec.modifiers, name=name)
                for name in config.variable_modifiers
            ),
        )
    with GoldenSkips(
        policy=_REF_SKIPS,
        golden_path=golden_path,
        prefix=lang_cls.__name__,
        config=pytest_config,
    ):
        try:
            _ = literalizer.literalize(
                source='{"key": "value"}',
                input_format=literalizer.InputFormat.JSON,
                language=spec,
                variable_form=variable_form_obj,
                wrap_in_file=(
                    len(config.external_declarations) == 0
                    and config.consumer is None
                ),
            )
        except VariableNameNotSupportedError:
            variable_form_obj = None
        raw_data = parse_ref_input(
            input_format=input_info.input_format,
            input_source=input_source,
        )
        spec = external_assignment_spec(
            spec=spec, config=config, raw_data=raw_data
        )
        bound_refs_input = bound_ref_inputs(
            config=config,
            raw_data=raw_data,
            lang_cls=lang_cls,
        )
        effective_bound_refs = None
        if len(bound_refs_input) > 0 and config.external_declarations == {}:
            effective_bound_refs = bound_refs_input
        effective_ref_values = None
        if config.explicit_ref_value_sources is not None:
            effective_ref_values = {
                name: json.loads(s=source)
                for name, source in (config.explicit_ref_value_sources.items())
            }
        original_ref_values = copy.deepcopy(x=effective_ref_values)
        result = literalizer.literalize(
            source=input_source,
            input_format=input_info.input_format,
            language=spec,
            variable_form=variable_form_obj,
            wrap_in_file=(
                len(config.external_declarations) == 0
                and config.consumer is None
            ),
            ref_case=ref_case,
            bound_refs=(effective_bound_refs),
            ref_values=(effective_ref_values),
            ref_key=config.ref_key,
            include_delimiters=config.include_delimiters,
            pre_indent_level=config.pre_indent_level,
            collection_layout=literalizer.CollectionLayout(
                value=config.collection_layout
            ),
        )
        assert effective_ref_values == original_ref_values, (  # noqa: S101
            "literalize mutated caller-owned ref_values"
        )
        if (
            len(config.external_declarations) > 0
            or config.consumer is not None
        ):
            result = compose_external_ref_fixture(
                config=config,
                spec=spec,
                result=result,
                raw_data=raw_data,
            )
    check_golden(
        contents=ref_fixture_contents(
            code=result.code,
            spec=spec,
            lang_cls=lang_cls,
            ref_case=ref_case,
        ),
        golden_path=golden_path,
        file_regression=file_regression,
    )
