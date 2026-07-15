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
from literalizer.languages import ALL_LANGUAGES


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
def with_per_fixture_module_name(
    *,
    spec: literalizer.Language,
    golden_path: Path,
) -> literalizer.Language:
    """Apply the language-owned per-fixture module naming policy."""
    metadata = spec.variant_metadata
    template = metadata.fixture_module_name_template
    if template is None:
        return spec
    module_name = template.format(
        parent=golden_path.parent.name,
        stem=_logical_stem(path=golden_path),
    )
    if metadata.fixture_module_name_lowercase:
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
    version: enum.Enum,
) -> Path:
    """Return the on-disk path for a golden fixture file.

    Every golden filename embeds a ``@<version>`` tag derived from a
    member of the language's ``VersionFormats`` enum so adding a second
    version member automatically produces a parallel set of golden
    files.  The tag uses the member's lower-cased ``name`` (e.g.
    ``PY39`` -> ``py39``).

    Languages declare whether the entire filename must be lower-cased
    (for example, so it is also a valid module identifier).  The logical
    name retains its original casing in pytest IDs and error messages.
    """
    version_tag = version.name.lower()
    filename = f"{name}@{version_tag}{extension}"
    if lang_cls.variant_metadata.golden_filename_lowercase:
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
