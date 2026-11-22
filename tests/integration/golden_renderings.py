"""Rendering records and spec/path helpers shared by golden consumers."""

import dataclasses
import enum
from collections.abc import Mapping
from pathlib import Path

from beartype import beartype

import literalizer
from literalizer import ValueInput

from .golden_artifacts import GoldenArtifact
from .golden_outcomes import SUCCESS, Rejection, Success
from .language_specs import make_golden_artifact, make_spec
from .literal_expectations import literal_rejection
from .literal_rejection_manifest import (
    LITERAL_REJECTION_MANIFEST,
    authored_literal_rejection,
)
from .manifest_values import ComposedConsumer

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
    consumer: str | ComposedConsumer | None

    @property
    def wrap_in_file(self) -> bool:
        """Wrap directly when the rendering has no declarations to compose."""
        return (
            self.render.wrap_in_file
            and len(self.extra_preamble) == 0
            and not self.initialize_variable
            and not isinstance(self.consumer, ComposedConsumer)
        )

    @property
    def specs(self) -> tuple[literalizer.Language, ...]:
        """Return each effective language version this rendering covers.

        A pinned spec is used unchanged. Constructor overrides expand
        across supported versions, keeping only the iteration matching
        the effective version when an option raises the version floor.
        Scheduling, rendering and fixture ownership all use this view.
        """
        source = self.spec_source
        if isinstance(source, literalizer.Language):
            return (source,)
        specs: list[literalizer.Language] = []
        for version in self.lang_cls.VersionFormats:
            spec = make_spec(
                lang_cls=self.lang_cls,
                language_version=version,
                **source,
            )
            if spec.language_version is version:
                specs.append(spec)
        return tuple(specs)

    def outcome(self, *, spec: literalizer.Language) -> Success | Rejection:
        """Resolve strict outcomes before rendering the selected
        options.
        """
        authored = authored_literal_rejection(
            case_name=self.case_dir_name,
            lang_cls=self.lang_cls,
            spec=spec,
            render=self.render,
            manifest_path=LITERAL_REJECTION_MANIFEST,
        )
        if authored is not None:
            return authored
        rejection = literal_rejection(
            spec=spec,
            lang_cls=self.lang_cls,
            variable_form=(
                self.render.variable_form
                if spec.supports_variable_names
                else None
            ),
            case_dir=self.golden_parent,
            substitutions=self.render.record_null_substitutions,
            wrap_in_file=self.wrap_in_file,
        )
        return SUCCESS if rejection is None else rejection

    def artifact(self, *, version: enum.Enum) -> GoldenArtifact:
        """Resolve this fixture for one effective version."""
        return make_golden_artifact(
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
) -> GoldenRendering:
    """Return a rendering needing no supporting preamble or initialization."""
    return GoldenRendering(
        consumer=None,
        lang_cls=lang_cls,
        case_dir_name=case_dir_name,
        golden_name=golden_name,
        golden_parent=_CASES_DIR / case_dir_name,
        spec_source=spec_source,
        render=render,
        extra_preamble=(),
        initialize_variable=False,
        apply_fixture_module_name=True,
    )
