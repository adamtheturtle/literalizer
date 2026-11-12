"""Rendering records and spec/path helpers shared by golden consumers."""

import dataclasses
import enum
from collections.abc import Mapping
from pathlib import Path

from beartype import beartype

import literalizer
from literalizer import ValueInput

from .golden_checks import SkipPolicy
from .language_specs import make_golden_path, make_spec

_CASES_DIR = Path(__file__).parent / "cases"


type SpecSource = literalizer.Language | Mapping[str, object]
"""A pinned language spec or constructor overrides for every version."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class RenderArguments:
    """The ``literalize`` arguments a rendering varies."""

    variable_form: literalizer.VariableForm | None
    pre_indent_level: int
    collection_layout: literalizer.CollectionLayout
    record_null_substitutions: Mapping[str, ValueInput] | None
    wrap_in_file: bool


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
        wrap_in_file=True,
    )


@dataclasses.dataclass(frozen=True, kw_only=True)
class GoldenRendering:
    """One language's rendering of one case against one golden name."""

    lang_cls: literalizer.LanguageCls
    case_dir_name: str
    golden_name: str
    golden_parent: Path
    spec_source: SpecSource
    render: RenderArguments
    extra_preamble: tuple[str, ...]
    initialize_variable: bool
    apply_fixture_module_name: bool
    skip: SkipPolicy
    consumer_template: str | None

    @property
    def versions(self) -> tuple[enum.Enum, ...]:
        """Return the language versions this rendering covers.

        A pinned spec names the one version it was built for; anything
        else renders a golden per member of the language's
        ``VersionFormats``.
        """
        pinned = self.spec_source
        if isinstance(pinned, literalizer.Language):
            return (pinned.language_version,)
        return tuple(self.lang_cls.VersionFormats)

    def spec_for(self, *, version: enum.Enum) -> literalizer.Language:
        """Return the spec this rendering uses for *version*."""
        pinned = self.spec_source
        if isinstance(pinned, literalizer.Language):
            return pinned
        return make_spec(
            lang_cls=self.lang_cls,
            language_version=version,
            **pinned,
        )

    @property
    def specs(self) -> tuple[literalizer.Language, ...]:
        """Return the effective specs exercised by the golden runner.

        An override may require a newer language version (for example,
        Java records require JDK16). Keep only the iteration for that
        effective version, so earlier versions cannot own phantom files.
        """
        specs: list[literalizer.Language] = []
        for version in self.versions:
            spec = self.spec_for(version=version)
            if spec.language_version is version:
                specs.append(spec)
        return tuple(specs)

    def golden_path(self, *, version: enum.Enum) -> Path:
        """Return this rendering's fixture path for one effective
        version.
        """
        return make_golden_path(
            parent=self.golden_parent,
            name=self.golden_name,
            lang_cls=self.lang_cls,
            version=version,
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
    """Return a rendering needing no supporting preamble or initialization."""
    return GoldenRendering(
        consumer_template=None,
        lang_cls=lang_cls,
        case_dir_name=case_dir_name,
        golden_name=golden_name,
        golden_parent=_CASES_DIR / case_dir_name,
        spec_source=spec_source,
        render=render,
        extra_preamble=(),
        initialize_variable=False,
        apply_fixture_module_name=True,
        skip=skip,
    )
