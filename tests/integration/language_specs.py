"""Helpers for building and caching :class:`literalizer.Language` specs.

Each ``lang_cls()`` call rebuilds ``@beartype``-wrapped closures inside
the formatter factories; sharing one instance per ``(class, kwargs)``
combination cuts thousands of redundant builds across collection and
test execution.
"""

import dataclasses
import enum
import functools
from collections.abc import Iterator, Mapping
from pathlib import Path

from beartype import beartype

import literalizer
from literalizer._language import redefinition_config
from literalizer.languages import ALL_LANGUAGES

from .fixture_names import fixture_module_name, nested_golden_path
from .golden_artifacts import GoldenArtifact
from .language_metadata import language_metadata


@beartype
def with_per_fixture_module_name(
    *,
    spec: literalizer.Language,
    golden_path: Path,
) -> literalizer.Language:
    """Apply the test-owned per-fixture module naming policy."""
    golden = language_metadata(language_id=spec.language_id).golden
    if not golden.per_fixture_module_name:
        return spec
    module_name = fixture_module_name(golden_path=golden_path)
    if golden.fixture_module_name_lowercase:
        module_name = module_name.lower()
    return dataclasses.replace(spec, module_name=module_name)


@beartype
def find_redefinition_styles(
    spec: literalizer.Language,
) -> list[enum.Enum]:
    """Return all declaration styles that support redefinition."""
    return [
        style
        for style in spec.declaration_styles
        if redefinition_config(style).supports_redefinition
    ]


@beartype
def lang_cls_name(cls: literalizer.LanguageCls) -> str:
    """Return the class name for sorting."""
    return cls.__name__


@beartype
def make_golden_path(
    *,
    parent: Path,
    name: str,
    lang_cls: literalizer.LanguageCls,
    version: enum.Enum,
) -> Path:
    """Return the on-disk path for a golden fixture file.

    The effective language version appears in the nested fixture's
    directory or in the flat filename's ``@<version>`` suffix.
    """
    version_tag = version.name.lower()
    golden = language_metadata(language_id=lang_cls.language_id).golden
    stem = name.lower() if golden.filename_lowercase else name
    nested_path = nested_golden_path(
        case_dir=parent,
        stem=stem,
        language_name=lang_cls.__name__,
        language_id=lang_cls.language_id,
        version=version_tag,
        extension=lang_cls.extension,
    )
    if nested_path is not None:
        return nested_path
    filename = f"{stem}@{version_tag}{lang_cls.extension}"
    if golden.filename_lowercase:
        filename = filename.lower()
    return parent / filename


@beartype
def make_golden_artifact(
    *,
    parent: Path,
    name: str,
    lang_cls: literalizer.LanguageCls,
    version: enum.Enum,
) -> GoldenArtifact:
    """Resolve a generated artifact for the effective language version."""
    return GoldenArtifact(
        path=make_golden_path(
            parent=parent, name=name, lang_cls=lang_cls, version=version
        ),
        language=lang_cls,
        version=version,
    )


@functools.cache
@beartype
def sorted_languages() -> list[literalizer.LanguageCls]:
    """Return all languages sorted by class name."""
    return sorted(ALL_LANGUAGES, key=lang_cls_name)


@functools.cache
@beartype
def cached_spec(
    *,
    lang_cls: literalizer.LanguageCls,
    kwargs_items: frozenset[tuple[str, object]],
) -> literalizer.Language:
    """Return a cached instance of *lang_cls* built from
    *kwargs_items*.
    """
    return lang_cls(**dict(kwargs_items))


@beartype
def make_spec(
    *,
    lang_cls: literalizer.LanguageCls,
    **kwargs: object,
) -> literalizer.Language:
    """Build a language spec, reusing cached constructor arguments.

    Languages whose ``wrap_in_file`` introduces a named scope take a
    ``module_name`` constructor argument; default it to the native spelling
    of ``"main"`` so fixture output matches the historic golden files.
    Mapping-valued overrides bypass the cache because they cannot be
    part of its key.
    """
    if lang_cls.supports_module_name and "module_name" not in kwargs:
        kwargs["module_name"] = lang_cls.module_name_case.convert(name="main")
    if any(isinstance(value, Mapping) for value in kwargs.values()):
        return lang_cls(**kwargs)
    return cached_spec(
        lang_cls=lang_cls,
        kwargs_items=frozenset(kwargs.items()),
    )


@beartype
def reference_case_for_declaration_style(
    *, lang_cls: literalizer.LanguageCls, spec: literalizer.Language
) -> literalizer.IdentifierCase:
    """Follow the native naming convention of a generated declaration."""
    names = language_metadata(
        language_id=lang_cls.language_id
    ).variants.declaration_style_variable_names
    name = names.get(spec.declaration_style.name)
    if name is None:
        return spec.identifier_cases[0]
    return next(
        case
        for case in sorted(
            lang_cls.supported_ref_cases, key=lambda case: case.value
        )
        if case.convert(name="my_data") == name
    )


@beartype
def modifier_entries(
    *, lang_cls: literalizer.LanguageCls, spec: literalizer.Language
) -> Iterator[tuple[str, frozenset[enum.Enum]]]:
    """List individual modifiers followed by declared combinations."""
    for member in spec.modifiers:
        yield member.name.lower(), frozenset({member})
    for combo in lang_cls.modifier_combinations:
        yield combo.name, combo.modifiers
