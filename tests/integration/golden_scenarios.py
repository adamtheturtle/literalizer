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
import enum
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path

from beartype import beartype

import literalizer
from literalizer._types import ValueInput
from literalizer.exceptions import (
    HeterogeneousCollectionError,
    IncompatibleFormatsError,
    NullInCollectionError,
    UnrepresentableEmptyDictError,
    UnrepresentableInputError,
    UnrepresentableIntegerError,
    UnrepresentableSpecialFloatError,
)

from .case_discovery import (
    build_heterogeneous_strategy_combined_cases,
    build_indent_cases,
    build_no_variable_form_cases,
    build_pre_indent_cases,
    build_statement_terminator_combined_cases,
    group_cases_by_language,
    group_combined_cases_by_language,
    kebab_new_variable_languages,
    primed_new_variable_languages,
)
from .case_manifests import (
    KEBAB_NEW_VARIABLE_OWNER,
    PRIMED_NEW_VARIABLE_OWNER,
    OwnerName,
    case_dir_name_for_owner,
    case_manifests_by_name,
    variable_form_for_context,
)
from .golden_checks import (
    NO_SKIPS,
    SkipPolicy,
    SkipReason,
    SkipReasons,
)
from .language_specs import (
    find_redefinition_styles,
    make_spec,
    sorted_languages,
)
from .variant_cases import group_variant_cases_by_language

_CASES_DIR = Path(__file__).parent / "cases"

_COMBINED_VARIABLE_FORM = literalizer.BothVariableForms(
    name="my_data",
    modifiers=frozenset(),
)


LANGUAGE_SKIP_REASONS: SkipReasons = (
    SkipReason(
        error=UnrepresentableIntegerError,
        reason="cannot represent integer in this input",
        unlink=True,
    ),
    SkipReason(
        error=UnrepresentableEmptyDictError,
        reason="cannot represent an empty dict",
        unlink=True,
    ),
    SkipReason(
        error=HeterogeneousCollectionError,
        reason="cannot represent this heterogeneous input",
        unlink=True,
    ),
    SkipReason(
        error=NullInCollectionError,
        reason="cannot represent null in a collection",
        unlink=True,
    ),
    SkipReason(
        error=UnrepresentableInputError,
        reason="cannot represent this input",
        unlink=True,
    ),
)

VARIANT_SKIP_REASONS: SkipReasons = (
    SkipReason(
        error=UnrepresentableIntegerError,
        reason="cannot represent integer in this input",
        unlink=True,
    ),
    SkipReason(
        error=UnrepresentableEmptyDictError,
        reason="cannot represent an empty dict",
        unlink=True,
    ),
    SkipReason(
        error=NullInCollectionError,
        reason="rejects null elements in this input",
        unlink=False,
    ),
    SkipReason(
        error=HeterogeneousCollectionError,
        reason="cannot represent this heterogeneous input",
        unlink=True,
    ),
    SkipReason(
        error=IncompatibleFormatsError,
        reason="combination cannot represent this input",
        unlink=True,
    ),
    SkipReason(
        error=UnrepresentableSpecialFloatError,
        reason="cannot represent special floats in this input",
        unlink=True,
    ),
    SkipReason(
        error=UnrepresentableInputError,
        reason="cannot represent this input",
        unlink=True,
    ),
)


@beartype
def _reasons_for(
    *,
    reasons: SkipReasons,
    errors: tuple[type[Exception], ...],
) -> SkipReasons:
    """Return the entries of *reasons* covering exactly *errors*.

    A scenario that should skip on fewer errors than a table lists
    narrows the table rather than restating a reason, so the message
    for an error stays written once.
    """
    return tuple(entry for entry in reasons if entry.error in errors)


# Rendering the paired fixture under a non-default heterogeneous
# strategy skips only where the strategy cannot represent it; every
# other error is a real failure, so the table is narrowed rather than
# reused whole.
_STRATEGY_SKIP_REASONS: SkipReasons = _reasons_for(
    reasons=LANGUAGE_SKIP_REASONS,
    errors=(HeterogeneousCollectionError,),
)


LANGUAGE_SKIPS: SkipPolicy = SkipPolicy(
    reasons=LANGUAGE_SKIP_REASONS,
    suffix="",
)
"""An input the language itself cannot represent skips."""

VARIANT_SKIPS: SkipPolicy = SkipPolicy(
    reasons=VARIANT_SKIP_REASONS,
    suffix="",
)
"""An input the variant's spec cannot represent skips."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class SpecSource:
    """Where a rendering's spec for one language version comes from.

    ``pinned`` carries a spec that already fixes its own language
    version -- what a format variant expands to -- and leaves
    ``overrides`` unused.  Every other scenario names the keywords its
    spec overrides and lets one spec be built per version.
    """

    pinned: literalizer.Language | None
    overrides: Mapping[str, object]


@beartype
def default_spec_source() -> SpecSource:
    """Return the source of a spec carrying no overrides."""
    return SpecSource(pinned=None, overrides={})


@beartype
def overridden_spec_source(*, overrides: Mapping[str, object]) -> SpecSource:
    """Return the source of a spec built with *overrides*."""
    return SpecSource(pinned=None, overrides=overrides)


@beartype
def pinned_spec_source(*, spec: literalizer.Language) -> SpecSource:
    """Return the source of an already-built, version-pinned spec."""
    return SpecSource(pinned=spec, overrides={})


@dataclasses.dataclass(frozen=True, kw_only=True)
class RenderArguments:
    """The ``literalize`` arguments a rendering varies."""

    variable_form: literalizer.VariableForm | None
    pre_indent_level: int
    collection_layout: literalizer.CollectionLayout
    record_null_substitutions: Mapping[str, ValueInput] | None


@beartype
def compact_render(
    *,
    variable_form: literalizer.VariableForm | None,
) -> RenderArguments:
    """Return the render arguments nearly every scenario shares.

    Most scenarios bind a variable form at the left margin, render
    compactly, and substitute nothing into record nulls; the handful
    that vary one of those name all four instead of restating the
    defaults at every construction site.
    """
    return RenderArguments(
        variable_form=variable_form,
        pre_indent_level=0,
        collection_layout=literalizer.CollectionLayout.COMPACT,
        record_null_substitutions=None,
    )


@dataclasses.dataclass(frozen=True, kw_only=True)
class GoldenRendering:
    """One language's rendering of one case against one golden name."""

    lang_cls: literalizer.LanguageCls
    case_dir_name: str
    golden_name: str
    spec_source: SpecSource
    render: RenderArguments
    fixture_prefix: str
    skip: SkipPolicy

    @property
    def versions(self) -> tuple[enum.Enum, ...]:
        """Return the language versions this rendering covers.

        A pinned spec names the one version it was built for; anything
        else renders a golden per member of the language's
        ``VersionFormats``.
        """
        pinned = self.spec_source.pinned
        if pinned is not None:
            return (pinned.language_version,)
        return tuple(self.lang_cls.VersionFormats)

    def spec_for(self, *, version: enum.Enum) -> literalizer.Language:
        """Return the spec this rendering uses for *version*."""
        pinned = self.spec_source.pinned
        if pinned is not None:
            return pinned
        return make_spec(
            lang_cls=self.lang_cls,
            language_version=version,
            **self.spec_source.overrides,
        )


@beartype
def unprefixed_rendering(
    *,
    lang_cls: literalizer.LanguageCls,
    case_dir_name: str,
    golden_name: str,
    spec_source: SpecSource,
    render: RenderArguments,
    skip: SkipPolicy,
) -> GoldenRendering:
    """Return a rendering whose golden carries no fixture preamble.

    Only the format variants put a preamble in front of the rendered
    code, so every other scenario says what it renders rather than
    restating that it has none.
    """
    return GoldenRendering(
        lang_cls=lang_cls,
        case_dir_name=case_dir_name,
        golden_name=golden_name,
        spec_source=spec_source,
        render=render,
        fixture_prefix="",
        skip=skip,
    )


@dataclasses.dataclass(frozen=True, kw_only=True)
class GoldenScenario:
    """A named family of golden renderings sharing one runner.

    ``build`` takes a language by keyword and returns the renderings
    that language takes part in, empty when it takes none.
    """

    name: str
    build: Callable[..., tuple[GoldenRendering, ...]]


@dataclasses.dataclass(frozen=True, kw_only=True)
class GoldenGroup:
    """One scenario's renderings for one language.

    Grouping by language keeps the pytest axis at roughly the number of
    languages rather than the number of golden files; each rendering
    inside runs as its own sub-test.
    """

    scenario_name: str
    lang_cls: literalizer.LanguageCls
    renderings: tuple[GoldenRendering, ...]

    @property
    def test_id(self) -> str:
        """Return the pytest ID identifying this group."""
        return f"{self.scenario_name}-{self.lang_cls.__name__}"


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
        renderings.append(
            unprefixed_rendering(
                lang_cls=lang_cls,
                case_dir_name=case_name,
                golden_name=lang_cls.__name__,
                spec_source=default_spec_source(),
                render=RenderArguments(
                    variable_form=variable_form_for_context(context=context),
                    pre_indent_level=context.pre_indent_level,
                    collection_layout=literalizer.CollectionLayout(
                        value=context.collection_layout or "compact"
                    ),
                    record_null_substitutions=(
                        context.record_null_substitutions
                    ),
                ),
                skip=LANGUAGE_SKIPS,
            )
        )
    return tuple(renderings)


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
            spec_source=default_spec_source(),
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
    *,
    lang_cls: literalizer.LanguageCls,
) -> tuple[GoldenRendering, ...]:
    """Combine a declaration and an assignment in one file.

    One rendering per redefinition-supporting declaration style, which
    is what :func:`discover_combined_cases` already pairs with its
    golden name.
    """
    grouped = group_combined_cases_by_language(cases_dir=_CASES_DIR)
    return tuple(
        unprefixed_rendering(
            lang_cls=lang_cls,
            case_dir_name=combined_case.case_name,
            golden_name=combined_case.golden_file_name,
            spec_source=overridden_spec_source(
                overrides={
                    "declaration_style": combined_case.declaration_style,
                },
            ),
            render=compact_render(variable_form=_COMBINED_VARIABLE_FORM),
            skip=LANGUAGE_SKIPS,
        )
        for combined_case in grouped.get(lang_cls, [])
    )


@beartype
def _variant_renderings(
    *,
    lang_cls: literalizer.LanguageCls,
) -> tuple[GoldenRendering, ...]:
    """Render each format variant's own spec against its own case.

    A variant pins the language version its spec was built for, so the
    rendering carries the spec rather than the keywords to rebuild it.
    """
    grouped = group_variant_cases_by_language()
    return tuple(
        GoldenRendering(
            lang_cls=lang_cls,
            case_dir_name=variant_case.case_dir_name,
            golden_name=variant_case.variant_name,
            spec_source=pinned_spec_source(spec=variant_case.variant.spec),
            render=RenderArguments(
                variable_form=variant_case.variable_form,
                pre_indent_level=variant_case.pre_indent_level,
                collection_layout=variant_case.variant.collection_layout,
                record_null_substitutions=(
                    variant_case.variant.record_null_substitutions
                ),
            ),
            fixture_prefix=variant_case.variant.fixture_prefix,
            skip=VARIANT_SKIPS,
        )
        for variant_case in grouped.get(lang_cls, [])
    )


@beartype
def _first_redefinition_style(
    *,
    lang_cls: literalizer.LanguageCls,
) -> enum.Enum:
    """Return the declaration style a combined rendering declares
    with.

    Both scenarios that reach here are built only for languages with at
    least one redefinition-supporting style.
    """
    styles = find_redefinition_styles(spec=make_spec(lang_cls=lang_cls))
    return styles[0]


@beartype
def _statement_terminator_renderings(
    *,
    lang_cls: literalizer.LanguageCls,
) -> tuple[GoldenRendering, ...]:
    """Combine both variable forms under a non-default statement
    terminator.
    """
    return tuple(
        unprefixed_rendering(
            lang_cls=lang_cls,
            case_dir_name=case.case_dir_name,
            golden_name=case.name,
            spec_source=overridden_spec_source(
                overrides={
                    "statement_terminator_style": (
                        case.statement_terminator_style
                    ),
                    "declaration_style": _first_redefinition_style(
                        lang_cls=lang_cls
                    ),
                },
            ),
            render=compact_render(variable_form=_COMBINED_VARIABLE_FORM),
            skip=NO_SKIPS,
        )
        for case in build_statement_terminator_combined_cases()
        if case.lang_cls is lang_cls
    )


@beartype
def _heterogeneous_strategy_renderings(
    *,
    lang_cls: literalizer.LanguageCls,
) -> tuple[GoldenRendering, ...]:
    """Combine both variable forms under a non-default heterogeneous
    strategy.

    A strategy may not represent the paired fixture in every language
    (Kotlin ``TUPLE`` has no native tuple for a four-element array), so
    the strategy is named in the skip and two strategies failing on the
    same input stay distinguishable.
    """
    return tuple(
        unprefixed_rendering(
            lang_cls=lang_cls,
            case_dir_name=case.case_dir_name,
            golden_name=case.name,
            spec_source=overridden_spec_source(
                overrides={
                    "heterogeneous_strategy": case.heterogeneous_strategy,
                    "declaration_style": _first_redefinition_style(
                        lang_cls=lang_cls
                    ),
                },
            ),
            render=compact_render(variable_form=_COMBINED_VARIABLE_FORM),
            skip=SkipPolicy(
                reasons=_STRATEGY_SKIP_REASONS,
                suffix=f" under {case.heterogeneous_strategy.name}",
            ),
        )
        for case in build_heterogeneous_strategy_combined_cases()
        if case.lang_cls is lang_cls
    )


@beartype
def _pre_indent_renderings(
    *,
    lang_cls: literalizer.LanguageCls,
) -> tuple[GoldenRendering, ...]:
    """Declare a new variable at a non-zero ``pre_indent_level``.

    Regression coverage for the bug where the first line of a
    multi-line value was inserted after ``=`` with the indent baked in,
    producing extra spaces between ``=`` and the value and shifting
    continuation lines by an extra indent.
    """
    return tuple(
        unprefixed_rendering(
            lang_cls=lang_cls,
            case_dir_name=case.case_dir_name,
            golden_name=case.name,
            spec_source=default_spec_source(),
            render=RenderArguments(
                variable_form=literalizer.NewVariable(
                    name="my_data",
                    modifiers=case.modifiers,
                ),
                pre_indent_level=case.pre_indent_level,
                collection_layout=literalizer.CollectionLayout.COMPACT,
                record_null_substitutions=None,
            ),
            skip=SkipPolicy(
                reasons=LANGUAGE_SKIP_REASONS,
                suffix=" at non-zero pre-indent",
            ),
        )
        for case in build_pre_indent_cases()
        if case.lang_cls is lang_cls
    )


@beartype
def _no_variable_form_renderings(
    *,
    lang_cls: literalizer.LanguageCls,
) -> tuple[GoldenRendering, ...]:
    """Render a bare value at file scope, with no variable form.

    Locks in issue #2138: languages whose
    :attr:`~literalizer._language.Language.supports_no_variable_wrap_in_file`
    is ``True`` must produce valid file-scope output for a bare value;
    opt-out languages are rejected upstream with
    :class:`~literalizer.exceptions.WrapInFileWithoutVariableNotSupportedError`.
    """
    return tuple(
        unprefixed_rendering(
            lang_cls=lang_cls,
            case_dir_name=case.case_dir_name,
            golden_name=case.name,
            spec_source=default_spec_source(),
            render=compact_render(variable_form=None),
            skip=NO_SKIPS,
        )
        for case in build_no_variable_form_cases()
        if case.lang_cls is lang_cls
    )


@beartype
def _indent_renderings(
    *,
    lang_cls: literalizer.LanguageCls,
) -> tuple[GoldenRendering, ...]:
    """Render one case under an indent no language defaults to.

    Locks in issue #2084: every spec carries an ``indent`` field, but
    until #2087 most languages hard-coded their indentation in the
    ``wrap_in_file`` / preamble helpers.  Pinning the result means a
    future regression that re-introduces a literal ``"    "`` (or
    two-space, or a tab) cannot pass silently.
    """
    return tuple(
        unprefixed_rendering(
            lang_cls=lang_cls,
            case_dir_name=case.case_dir_name,
            golden_name=case.name,
            spec_source=overridden_spec_source(
                overrides={"indent": case.indent},
            ),
            render=compact_render(
                variable_form=literalizer.NewVariable(
                    name="my_data",
                    modifiers=frozenset(),
                ),
            ),
            skip=NO_SKIPS,
        )
        for case in build_indent_cases()
        if case.lang_cls is lang_cls
    )


GOLDEN_SCENARIOS: tuple[GoldenScenario, ...] = (
    GoldenScenario(name="base", build=_base_renderings),
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
            if renderings:
                groups.append(
                    GoldenGroup(
                        scenario_name=scenario.name,
                        lang_cls=lang_cls,
                        renderings=renderings,
                    )
                )
    return tuple(groups)
