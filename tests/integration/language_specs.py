"""Helpers for building and caching :class:`literalizer.Language` specs.

Each ``lang_cls()`` call rebuilds ``@beartype``-wrapped closures inside
the formatter factories; sharing one instance per ``(class, kwargs)``
combination cuts thousands of redundant builds across collection and
test execution.
"""

import dataclasses
import enum
import functools
from pathlib import Path

from beartype import beartype

import literalizer
from literalizer.languages import (
    ALL_LANGUAGES,
    Crystal,
    Erlang,
    Gleam,
    Haskell,
    Scala,
)

from .language_versions import language_version_for


@beartype
def erlang_module_name(*, golden_path: Path) -> str:
    """Return the Erlang module name for *golden_path*.

    Produces a deterministic, per-fixture name so every compiled
    ``.erl`` file in CI has a unique module declaration without needing
    ``sed`` rewriting.
    """
    dir_name = golden_path.parent.name
    stem = golden_path.stem
    return f"fixture_{dir_name}_{stem}".lower()


@beartype
def scala_module_name(*, golden_path: Path) -> str:
    """Return the Scala object name for *golden_path*.

    Produces a deterministic, per-fixture name so every compiled
    ``.scala`` file in CI has a unique object declaration without needing
    ``sed`` rewriting.
    """
    dir_name = golden_path.parent.name
    stem = golden_path.stem
    return f"Fixture_{dir_name}_{stem}"


@beartype
def crystal_module_name(*, golden_path: Path) -> str:
    """Return the Crystal module name for *golden_path*.

    Produces a deterministic, per-fixture name so every compiled
    ``.cr`` file in CI has a unique module declaration without needing
    shell-level wrapping or ``sed`` rewriting.
    """
    dir_name = golden_path.parent.name
    stem = golden_path.stem
    return f"Fixture_{dir_name}_{stem}"


@beartype
def haskell_module_name(*, golden_path: Path) -> str:
    """Return the Haskell module name for *golden_path*.

    Produces a deterministic, per-fixture name so every compiled
    ``.hs`` file in CI has a unique module declaration without needing
    ``sed`` rewriting.
    """
    dir_name = golden_path.parent.name
    stem = golden_path.stem
    return f"Fixture_{dir_name}_{stem}"


@beartype
def with_per_fixture_module_name(
    *,
    spec: literalizer.Language,
    golden_path: Path,
) -> literalizer.Language:
    """Return *spec* with a per-fixture ``module_name`` if applicable.

    Languages whose CI lint requires unique module names (Crystal, Erlang,
    Haskell, Scala) get a deterministic name derived from *golden_path*; all
    other languages are returned unchanged.
    """
    if isinstance(spec, Crystal):
        return dataclasses.replace(
            spec,
            module_name=crystal_module_name(golden_path=golden_path),
        )
    if isinstance(spec, Erlang):
        return dataclasses.replace(
            spec,
            module_name=erlang_module_name(golden_path=golden_path),
        )
    if isinstance(spec, Haskell):
        return dataclasses.replace(
            spec,
            module_name=haskell_module_name(golden_path=golden_path),
        )
    if isinstance(spec, Scala):
        return dataclasses.replace(
            spec,
            module_name=scala_module_name(golden_path=golden_path),
        )
    return spec


@beartype
def find_redefinition_styles(
    spec: literalizer.Language,
) -> list[enum.Enum]:
    """Return all declaration styles that support redefinition."""
    return [
        style
        for style in spec.declaration_styles
        if style.value.supports_redefinition
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
    extension: str,
    lang_cls: literalizer.LanguageCls,
) -> Path:
    """Return the on-disk path for a golden fixture file.

    For most languages this is just ``parent / (name + extension)``.
    Gleam is special-cased: the file name is mapped to its lower-case
    form so it is a valid Gleam module identifier.  The CI Gleam-lint
    job drops each fixture into a one-shot project as a real module
    path (e.g. ``binary/gleam_combined``), which fails compilation if
    the file name starts with a capital letter or contains an
    upper-case character.

    The name passed in (``Gleam_type_name_JsonVal``) keeps its original
    casing in pytest test IDs and error messages; only the on-disk
    file name is mapped down.

    Languages registered in
    ``language_versions.LANGUAGE_VERSIONS`` prefer a version-tagged
    variant ``{stem}@{version}{extension}`` when one exists on disk,
    falling back to the base file otherwise.  This lets a single
    fixture diverge across compiler versions without forking every
    case.
    """
    filename = name + extension
    if lang_cls.__name__ == Gleam.__name__:
        filename = filename.lower()
    base_path = parent / filename
    version = language_version_for(lang_cls=lang_cls)
    if version is not None:
        versioned = parent / f"{base_path.stem}@{version}{extension}"
        if versioned.is_file():
            return versioned
    return base_path


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
    """Return a cached instance of *lang_cls* for the given kwargs.

    Languages whose ``wrap_in_file`` introduces a named scope take a
    ``module_name`` constructor argument; default it to ``"check"`` so
    fixture output matches the historic golden files.
    """
    if lang_cls.supports_module_name and "module_name" not in kwargs:
        kwargs["module_name"] = lang_cls.module_name_case.convert(name="main")
    return cached_spec(
        lang_cls=lang_cls,
        kwargs_items=frozenset(kwargs.items()),
    )
