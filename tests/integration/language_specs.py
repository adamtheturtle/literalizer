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


@beartype
def _default_language_version(
    *, lang_cls: literalizer.LanguageCls
) -> enum.Enum:
    """Return the default ``language_version`` enum member for *lang_cls*.

    Every language dataclass declares a ``language_version`` field
    whose default points at the single active member of its
    ``VersionFormats`` enum.  Reading the default lets the golden-file
    pipeline tag each fixture with the active version without scanning
    on-disk filenames.
    """
    return make_spec(lang_cls=lang_cls).language_version


@beartype
def _logical_stem(*, path: Path) -> str:
    """Return *path*'s stem with any ``@version`` suffix removed.

    Per-fixture module names embed the stem in the generated source
    file (``-module(...)``, ``module Fixture_...``).  Version-tagged
    variants live alongside the base file but identifiers must remain
    stable across both forms so the same source can resolve to either
    path.
    """
    stem = path.stem
    return stem.rsplit(sep="@", maxsplit=1)[0] if "@" in stem else stem


@beartype
def erlang_module_name(*, golden_path: Path) -> str:
    """Return the Erlang module name for *golden_path*.

    Produces a deterministic, per-fixture name so every compiled
    ``.erl`` file in CI has a unique module declaration without needing
    ``sed`` rewriting.
    """
    dir_name = golden_path.parent.name
    stem = _logical_stem(path=golden_path)
    return f"fixture_{dir_name}_{stem}".lower()


@beartype
def scala_module_name(*, golden_path: Path) -> str:
    """Return the Scala object name for *golden_path*.

    Produces a deterministic, per-fixture name so every compiled
    ``.scala`` file in CI has a unique object declaration without needing
    ``sed`` rewriting.
    """
    dir_name = golden_path.parent.name
    stem = _logical_stem(path=golden_path)
    return f"Fixture_{dir_name}_{stem}"


@beartype
def crystal_module_name(*, golden_path: Path) -> str:
    """Return the Crystal module name for *golden_path*.

    Produces a deterministic, per-fixture name so every compiled
    ``.cr`` file in CI has a unique module declaration without needing
    shell-level wrapping or ``sed`` rewriting.
    """
    dir_name = golden_path.parent.name
    stem = _logical_stem(path=golden_path)
    return f"Fixture_{dir_name}_{stem}"


@beartype
def haskell_module_name(*, golden_path: Path) -> str:
    """Return the Haskell module name for *golden_path*.

    Produces a deterministic, per-fixture name so every compiled
    ``.hs`` file in CI has a unique module declaration without needing
    ``sed`` rewriting.
    """
    dir_name = golden_path.parent.name
    stem = _logical_stem(path=golden_path)
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
    version: enum.Enum | None = None,
) -> Path:
    """Return the on-disk path for a golden fixture file.

    Every golden filename embeds a ``@<version>`` tag derived from a
    member of the language's ``VersionFormats`` enum so adding a second
    version member automatically produces a parallel set of golden
    files.  The tag uses the member's lower-cased ``name`` (e.g.
    ``PY_3_12`` -> ``py_3_12``).

    When *version* is ``None`` the tag is derived from the language's
    default ``language_version`` field.  Callers that want to loop over
    every active version (today exactly one per language) pass the
    explicit member they are rendering.

    Gleam is special-cased: the entire file name (including the version
    tag) is mapped to its lower-case form so it remains a valid Gleam
    module identifier.  The CI Gleam-lint job drops each fixture into a
    one-shot project as a real module path (e.g. ``binary/gleam_combined``),
    which fails compilation if the file name starts with a capital
    letter or contains an upper-case character.  The name passed in
    (``Gleam_type_name_JsonVal``) keeps its original casing in pytest
    test IDs and error messages; only the on-disk file name is mapped
    down.
    """
    effective_version = (
        version
        if version is not None
        else _default_language_version(lang_cls=lang_cls)
    )
    version_tag = effective_version.name.lower()
    filename = f"{name}@{version_tag}{extension}"
    if lang_cls.__name__ == Gleam.__name__:
        filename = filename.lower()
    return parent / filename


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


@beartype
def spec_with_version(
    *,
    spec: literalizer.Language,
    version: enum.Enum,
) -> literalizer.Language:
    """Return *spec* with its ``language_version`` replaced by *version*.

    Wraps :func:`dataclasses.replace` for use on
    :class:`literalizer.Language` values, whose Protocol type does not
    statically satisfy the ``DataclassInstance`` constraint that
    ``dataclasses.replace`` requires.  Every concrete language is a
    dataclass at runtime, so the call is valid; the helper hides the
    type-checker noise behind one local cast.
    """
    kwargs_dict: dict[str, object] = {
        field.name: getattr(spec, field.name)
        for field in dataclasses.fields(spec)  # pyright: ignore[reportArgumentType]
        if field.init
    }
    kwargs_dict["language_version"] = version
    lang_cls: literalizer.LanguageCls = type(spec)  # pyright: ignore[reportAssignmentType]
    return cached_spec(
        lang_cls=lang_cls,
        kwargs_items=frozenset(kwargs_dict.items()),
    )
