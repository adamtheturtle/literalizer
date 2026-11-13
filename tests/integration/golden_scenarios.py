"""Declare the golden-file scenarios that drive :func:`literalize`.

Every golden-file scenario renders the same way: resolve a case input,
build the golden path, build the spec, call ``literalize``, skip the
inputs the language cannot represent, and check the golden.  What
differs between them is data -- which languages take part, which case
directory each renders, what the golden is called, which spec keywords
are overridden, which variable form is bound, and which errors skip
rather than fail.

This module holds that data.  A scenario names a builder that expands
one language into its renderings; :mod:`test_literalize_golden` owns
the single runner that turns a rendering into a checked golden file.
Adding a scenario is therefore a declaration here rather than a new
test body there.
"""

import dataclasses
from collections.abc import Sequence
from pathlib import Path
from typing import Protocol, runtime_checkable

from beartype import beartype

import literalizer

from . import case_manifests, manifest_queries, scenario_skips
from .case_discovery import (
    discover_cases,
    group_cases_by_language,
    kebab_new_variable_languages,
    primed_new_variable_languages,
)
from .case_manifests import (
    KEBAB_NEW_VARIABLE_OWNER,
    PRIMED_NEW_VARIABLE_OWNER,
    OwnerName,
    variable_form_for_context,
)
from .golden_batches import (
    GOLDEN_BATCH_VERSION_LIMIT,
    GoldenGroup,
    batch_renderings,
)
from .golden_checks import (
    NO_SKIPS,
    SkipPolicy,
)
from .golden_renderings import (
    GoldenRendering,
    RenderArguments,
    compact_render,
    unprefixed_rendering,
)
from .language_metadata import language_metadata
from .language_specs import (
    find_redefinition_styles,
    make_spec,
    sorted_languages,
)
from .manifest_queries import (
    case_dir_name_for_owner,
    case_manifests_by_name,
)
from .variant_cases import group_variant_cases_by_language

_CASES_DIR = Path(__file__).parent / "cases"

_COMBINED_VARIABLE_FORM = literalizer.BothVariableForms(
    name="my_data",
    modifiers=frozenset(),
)


@runtime_checkable
class _ScenarioBuilder(Protocol):
    """A scenario builder accepting one language by keyword."""

    def __call__(
        self, *, lang_cls: literalizer.LanguageCls
    ) -> tuple[GoldenRendering, ...]:
        """Build the renderings selected for one language."""
        ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class GoldenScenario:
    """A named family of golden renderings sharing one runner.

    ``build`` takes a language by keyword and returns the renderings
    that language takes part in, empty when it takes none.
    """

    name: str
    build: _ScenarioBuilder


@beartype
def _base_renderings(
    *,
    lang_cls: literalizer.LanguageCls,
) -> tuple[GoldenRendering, ...]:
    """Render every base-suite case under the language's defaults.

    The render context -- variable form, layout, pre-indent, record null
    substitutions -- is whatever the case's manifest declares.
    """
    manifests = case_manifests_by_name(cases_dir=_CASES_DIR)
    grouped = group_cases_by_language(cases_dir=_CASES_DIR)
    renderings: list[GoldenRendering] = []
    for case_name in grouped.get(lang_cls, []):
        context = manifests[case_name].base_context
        effective_value = (
            "compact"
            if context.collection_layout is None
            else context.collection_layout
        )
        renderings.append(
            unprefixed_rendering(
                lang_cls=lang_cls,
                case_dir_name=case_name,
                golden_name=lang_cls.__name__,
                spec_source={},
                render=RenderArguments(
                    variable_form=variable_form_for_context(context=context),
                    pre_indent_level=context.pre_indent_level,
                    collection_layout=literalizer.CollectionLayout(
                        value=(effective_value)
                    ),
                    record_null_substitutions=(
                        context.resolved_record_null_substitutions()
                    ),
                    wrap_in_file=True,
                ),
                skip=scenario_skips.LANGUAGE_SKIPS,
            )
        )
    return tuple(renderings)


@beartype
def _default_module_name_renderings(
    *,
    lang_cls: literalizer.LanguageCls,
) -> tuple[GoldenRendering, ...]:
    """Render declared inputs with the constructor's module-name default.

    These specs bypass both the test default in ``make_spec`` and the
    per-fixture naming policy, so the golden pins the public default.
    """
    manifests = case_manifests_by_name(cases_dir=_CASES_DIR)
    return tuple(
        GoldenRendering(
            consumer_template=None,
            lang_cls=lang_cls,
            case_dir_name=case_name,
            golden_name=f"{lang_cls.__name__}_default_module_name",
            golden_parent=_CASES_DIR.parent / "default_module_names",
            spec_source=lang_cls(language_version=version),
            render=compact_render(
                variable_form=literalizer.NewVariable(
                    name="my_data",
                    modifiers=frozenset(),
                ),
            ),
            extra_preamble=(),
            initialize_variable=False,
            apply_fixture_module_name=False,
            skip=NO_SKIPS,
        )
        for case_name, manifest in manifests.items()
        if "default-module-name" in manifest.suites
        and manifest.selection.admits_language(lang_cls=lang_cls)
        for version in lang_cls.VersionFormats
    )


@beartype
def _new_variable_renderings(
    *,
    lang_cls: literalizer.LanguageCls,
    languages: Sequence[literalizer.LanguageCls],
    owner: OwnerName,
    variable_name: str,
) -> tuple[GoldenRendering, ...]:
    """Declare *variable_name* in every language whose syntax admits
    it.
    """
    if lang_cls not in languages:
        return ()
    return (
        unprefixed_rendering(
            lang_cls=lang_cls,
            case_dir_name=case_dir_name_for_owner(
                cases_dir=_CASES_DIR,
                owner=owner,
            ),
            golden_name=lang_cls.__name__,
            spec_source={},
            render=compact_render(
                variable_form=literalizer.NewVariable(
                    name=variable_name,
                    modifiers=frozenset(),
                ),
            ),
            skip=NO_SKIPS,
        ),
    )


@beartype
def _kebab_new_variable_renderings(
    *,
    lang_cls: literalizer.LanguageCls,
) -> tuple[GoldenRendering, ...]:
    """Hyphen-friendly languages preserve a hyphenated declaration
    name.
    """
    return _new_variable_renderings(
        lang_cls=lang_cls,
        languages=kebab_new_variable_languages(),
        owner=KEBAB_NEW_VARIABLE_OWNER,
        variable_name="a-b",
    )


@beartype
def _primed_new_variable_renderings(
    *,
    lang_cls: literalizer.LanguageCls,
) -> tuple[GoldenRendering, ...]:
    """Prime-friendly languages preserve a primed declaration name."""
    return _new_variable_renderings(
        lang_cls=lang_cls,
        languages=primed_new_variable_languages(),
        owner=PRIMED_NEW_VARIABLE_OWNER,
        variable_name="a'",
    )


@beartype
def _combined_renderings(
    *, lang_cls: literalizer.LanguageCls
) -> tuple[GoldenRendering, ...]:
    """Combine declaration and assignment under each supported style."""
    styles = find_redefinition_styles(spec=make_spec(lang_cls=lang_cls))
    return tuple(
        unprefixed_rendering(
            lang_cls=lang_cls,
            case_dir_name=case_name,
            golden_name=(
                f"{lang_cls.__name__}_combined"
                if style is styles[0]
                else (
                    f"{lang_cls.__name__}_combined_declaration_style"
                    f"_{style.name.lower()}"
                )
            ),
            spec_source={"declaration_style": style},
            render=compact_render(variable_form=_COMBINED_VARIABLE_FORM),
            skip=scenario_skips.LANGUAGE_SKIPS,
        )
        for case_name, case_language in discover_cases(
            cases_dir=_CASES_DIR, suite="combined"
        )
        if case_language is lang_cls
        for style in styles
    )


@beartype
def _variant_renderings(
    *,
    lang_cls: literalizer.LanguageCls,
) -> tuple[GoldenRendering, ...]:
    """Render each format variant's own spec against its own case.

    Plans expand ordinary options across supported versions and keep
    explicit version choices pinned. Each variant already carries its
    effective version, so the rendering uses that spec unchanged.
    """
    grouped = group_variant_cases_by_language()
    return tuple(
        GoldenRendering(
            lang_cls=lang_cls,
            case_dir_name=variant_case.case_dir_name,
            golden_name=variant_case.golden_name,
            golden_parent=_CASES_DIR / variant_case.case_dir_name,
            spec_source=variant_case.variant.spec,
            render=RenderArguments(
                variable_form=variant_case.variable_form,
                pre_indent_level=variant_case.pre_indent_level,
                collection_layout=variant_case.variant.collection_layout,
                record_null_substitutions=(
                    variant_case.variant.record_null_substitutions
                ),
                wrap_in_file=variant_case.variant.wrap_in_file,
            ),
            consumer_template=variant_case.consumer_template,
            extra_preamble=variant_case.variant.extra_preamble,
            initialize_variable=variant_case.variant.initialize_variable,
            apply_fixture_module_name=variant_case.apply_fixture_module_name,
            skip=(
                scenario_skips.VARIANT_MAPPING_KEY_SKIPS
                if "InvalidDictKeyError" in variant_case.expected_errors
                else scenario_skips.VARIANT_SKIPS
            ),
        )
        for variant_case in grouped.get(lang_cls, [])
    )


@beartype
def _statement_terminator_renderings(
    *, lang_cls: literalizer.LanguageCls
) -> tuple[GoldenRendering, ...]:
    """Combine both variable forms under each non-default terminator."""
    spec = make_spec(lang_cls=lang_cls)
    styles = find_redefinition_styles(spec=spec)
    if len(styles) == 0:
        return ()
    case_names = manifest_queries.case_dir_names_for_role(
        cases_dir=_CASES_DIR, role=case_manifests.STATEMENT_TERMINATOR_ROLE
    )
    return tuple(
        unprefixed_rendering(
            lang_cls=lang_cls,
            case_dir_name=case_name,
            golden_name=(
                f"{lang_cls.__name__}_statement_terminator_style"
                f"_{terminator.name.lower()}_{case_name}"
            ),
            spec_source={
                "statement_terminator_style": terminator,
                "declaration_style": styles[0],
            },
            render=compact_render(variable_form=_COMBINED_VARIABLE_FORM),
            skip=NO_SKIPS,
        )
        for terminator in spec.statement_terminator_styles
        if terminator is not spec.statement_terminator_style
        for case_name in case_names
    )


@beartype
def _heterogeneous_strategy_renderings(
    *, lang_cls: literalizer.LanguageCls
) -> tuple[GoldenRendering, ...]:
    """Combine both variable forms under each non-default strategy.

    Name the strategy in skips when it cannot represent its paired input.
    """
    spec = make_spec(lang_cls=lang_cls)
    styles = find_redefinition_styles(spec=spec)
    if len(styles) == 0:
        return ()
    return tuple(
        unprefixed_rendering(
            lang_cls=lang_cls,
            case_dir_name=manifest_queries.case_dir_name_for_role(
                cases_dir=_CASES_DIR,
                role=manifest_queries.heterogeneous_strategy_role(
                    strategy_name=strategy.name
                ),
            ),
            golden_name=(
                f"{lang_cls.__name__}_heterogeneous_strategy"
                f"_{strategy.name.lower()}_combined"
            ),
            spec_source={
                "heterogeneous_strategy": strategy,
                "declaration_style": styles[0],
            },
            render=compact_render(variable_form=_COMBINED_VARIABLE_FORM),
            skip=SkipPolicy(
                reasons=scenario_skips.STRATEGY_SKIP_REASONS,
                suffix=f" under {strategy.name}",
            ),
        )
        for strategy in spec.heterogeneous_strategies
        if strategy is not spec.heterogeneous_strategy
    )


@beartype
def _pre_indent_renderings(
    *, lang_cls: literalizer.LanguageCls
) -> tuple[GoldenRendering, ...]:
    """Render each modifier combination at a non-zero pre-indent.

    Include the comment-scalar fixture when the language declares it.
    Keep container renderings before comment renderings for stable IDs.
    """
    container = manifest_queries.case_dir_name_for_role(
        cases_dir=_CASES_DIR, role=case_manifests.PRE_INDENT_CONTAINER_ROLE
    )
    comment = manifest_queries.case_dir_name_for_role(
        cases_dir=_CASES_DIR,
        role=case_manifests.PRE_INDENT_COMMENT_SCALAR_ROLE,
    )
    contexts = [(container, "")]
    if language_metadata(
        language_id=lang_cls.language_id
    ).variants.pre_indent_comment_scalar:
        contexts.append((comment, f"_{comment}"))
    return tuple(
        unprefixed_rendering(
            lang_cls=lang_cls,
            case_dir_name=case_dir_name,
            golden_name=f"{lang_cls.__name__}_pre_indent_1_{combo.name}{suffix}",
            spec_source={},
            render=RenderArguments(
                variable_form=literalizer.NewVariable(
                    name="my_data", modifiers=combo.modifiers
                ),
                pre_indent_level=1,
                collection_layout=literalizer.CollectionLayout.COMPACT,
                record_null_substitutions=None,
                wrap_in_file=True,
            ),
            skip=SkipPolicy(
                reasons=scenario_skips.LANGUAGE_SKIP_REASONS,
                suffix=" at non-zero pre-indent",
            ),
        )
        for case_dir_name, suffix in contexts
        for combo in lang_cls.modifier_combinations
    )


@beartype
def _no_variable_form_renderings(
    *, lang_cls: literalizer.LanguageCls
) -> tuple[GoldenRendering, ...]:
    """Render selected role inputs directly at file scope.

    Keep the scalar fixture's historical name; other shapes include
    their case name so fixtures sharing the role remain distinct.
    """
    if not lang_cls.supports_no_variable_wrap_in_file:
        return ()
    manifests = case_manifests_by_name(cases_dir=_CASES_DIR)
    return tuple(
        unprefixed_rendering(
            lang_cls=lang_cls,
            case_dir_name=case_name,
            golden_name=(
                f"{lang_cls.__name__}_no_variable_form"
                + ("" if case_name == "scalar_int" else f"_{case_name}")
            ),
            spec_source={},
            render=compact_render(variable_form=None),
            skip=NO_SKIPS,
        )
        for case_name in manifest_queries.case_dir_names_for_role(
            cases_dir=_CASES_DIR, role=case_manifests.NO_VARIABLE_FORM_ROLE
        )
        if manifests[case_name].selection.admits_language(lang_cls=lang_cls)
    )


@beartype
def _indent_renderings(
    *, lang_cls: literalizer.LanguageCls
) -> tuple[GoldenRendering, ...]:
    """Exercise the declared indent fixture with three-space
    indentation.
    """
    return (
        unprefixed_rendering(
            lang_cls=lang_cls,
            case_dir_name=manifest_queries.case_dir_name_for_role(
                cases_dir=_CASES_DIR, role=case_manifests.INDENT_ROLE
            ),
            golden_name=f"{lang_cls.__name__}_indent_three_space",
            spec_source={"indent": "   "},
            render=compact_render(
                variable_form=literalizer.NewVariable(
                    name="my_data", modifiers=frozenset()
                )
            ),
            skip=NO_SKIPS,
        ),
    )


GOLDEN_SCENARIOS: tuple[GoldenScenario, ...] = (
    GoldenScenario(name="base", build=_base_renderings),
    GoldenScenario(
        name="default_module_name",
        build=_default_module_name_renderings,
    ),
    GoldenScenario(
        name="kebab_new_variable",
        build=_kebab_new_variable_renderings,
    ),
    GoldenScenario(
        name="primed_new_variable",
        build=_primed_new_variable_renderings,
    ),
    GoldenScenario(name="combined", build=_combined_renderings),
    GoldenScenario(name="format_variant", build=_variant_renderings),
    GoldenScenario(
        name="statement_terminator_style",
        build=_statement_terminator_renderings,
    ),
    GoldenScenario(
        name="heterogeneous_strategy",
        build=_heterogeneous_strategy_renderings,
    ),
    GoldenScenario(name="pre_indent_level", build=_pre_indent_renderings),
    GoldenScenario(
        name="no_variable_form",
        build=_no_variable_form_renderings,
    ),
    GoldenScenario(name="indent", build=_indent_renderings),
)


@beartype
def golden_groups() -> tuple[GoldenGroup, ...]:
    """Return every scenario's renderings, grouped by language.

    A language a scenario does not cover yields no group rather than an
    empty test.
    """
    groups: list[GoldenGroup] = []
    for scenario in GOLDEN_SCENARIOS:
        for lang_cls in sorted_languages():
            renderings = scenario.build(lang_cls=lang_cls)
            batches = batch_renderings(
                renderings=renderings, max_versions=GOLDEN_BATCH_VERSION_LIMIT
            )
            for index, batch in enumerate(iterable=batches, start=1):
                groups.append(
                    GoldenGroup(
                        scenario_name=scenario.name,
                        lang_cls=lang_cls,
                        renderings=batch,
                        batch_index=index if len(batches) > 1 else None,
                    )
                )
    return tuple(groups)
