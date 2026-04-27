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
from typing import Any, cast

from beartype import beartype

import literalizer
from literalizer.languages import (
    ALL_LANGUAGES,
    Crystal,
    Erlang,
    Haskell,
    Scala,
)

# Languages whose constructor takes a ``module_name`` argument.
# :func:`make_spec` auto-fills it with ``"check"`` so fixture output
# matches the historic golden files unless the caller overrides.
_MODULE_NAME_LANGUAGES: frozenset[literalizer.LanguageCls] = frozenset(
    cls
    for cls in ALL_LANGUAGES
    if "module_name" in getattr(cls, "__dataclass_fields__", {})
)

# Languages whose CI lint job batches every fixture into one
# compilation unit and so needs a per-fixture top-level name to
# avoid collisions. The other ``module_name`` languages (C, C++,
# Java, Fortran, etc.) keep the historic ``"check"`` default because
# their CI hosts (``cpp_main.o`` calling ``check_()``,
# ``CheckJavaSyntax`` etc.) are wired to that exact name.
_BATCHED_NAMED_WRAPPER_LANGUAGES: frozenset[literalizer.LanguageCls] = (
    frozenset({Erlang, Scala, Crystal, Haskell})
)


@beartype
def _per_fixture_module_name(
    *,
    lang_cls: literalizer.LanguageCls,
    golden_path: Path,
) -> str | None:
    """Return the per-fixture wrapper name for *golden_path*, or
    ``None`` if *lang_cls* does not opt into ``module_name``.
    """
    if lang_cls not in _BATCHED_NAMED_WRAPPER_LANGUAGES:
        return None
    stem = f"{golden_path.parent.name}_{golden_path.stem}".lower()
    prefix = "fixture_" if lang_cls is Erlang else "Fixture_"
    return f"{prefix}{stem}"


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
    if lang_cls in _MODULE_NAME_LANGUAGES and "module_name" not in kwargs:
        kwargs["module_name"] = "check"
    return cached_spec(
        lang_cls=lang_cls,
        kwargs_items=frozenset(kwargs.items()),
    )


@beartype
def make_spec_for_golden(
    *,
    lang_cls: literalizer.LanguageCls,
    golden_path: Path,
    **kwargs: object,
) -> literalizer.Language:
    """Like :func:`make_spec` but auto-derives the ``module_name``
    constructor argument from *golden_path* for the four batched-CI
    languages.

    The four batched-CI languages (Erlang, Scala, Crystal, Haskell)
    each compile every fixture in one process, so each fixture needs
    a unique top-level name to avoid clashes. The name is a
    deterministic prefix + lower-cased path stem so the CI shell
    scripts can derive the same name from the file path without
    parsing the source. Other languages get :func:`make_spec`'s
    default ``"check"``.
    """
    name = _per_fixture_module_name(
        lang_cls=lang_cls,
        golden_path=golden_path,
    )
    if name is not None and "module_name" not in kwargs:
        kwargs["module_name"] = name
    return make_spec(lang_cls=lang_cls, **kwargs)


@beartype
def with_per_fixture_module_name(
    *,
    spec: literalizer.Language,
    golden_path: Path,
) -> literalizer.Language:
    """Return *spec* with ``module_name`` overridden for *golden_path*.

    Used when the test already has a configured spec (e.g. a variant
    with non-default formats) and only needs the ``module_name``
    swapped for the per-fixture batched-CI name. Returns *spec*
    unchanged for languages that do not opt into ``module_name``.
    """
    name = _per_fixture_module_name(
        lang_cls=cast("literalizer.LanguageCls", type(spec)),
        golden_path=golden_path,
    )
    if name is None:
        return spec
    # ``dataclasses.replace`` is typed for ``DataclassInstance`` but
    # ``literalizer.Language`` is a Protocol; every concrete language
    # is a frozen dataclass at runtime, so the call is sound.
    return cast(
        "literalizer.Language",
        dataclasses.replace(cast("Any", spec), module_name=name),
    )
