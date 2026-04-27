"""Helpers for building and caching :class:`literalizer.Language` specs.

Each ``lang_cls()`` call rebuilds ``@beartype``-wrapped closures inside
the formatter factories; sharing one instance per ``(class, kwargs)``
combination cuts thousands of redundant builds across collection and
test execution.
"""

import enum
import functools
from pathlib import Path

from beartype import beartype

import literalizer
from literalizer.languages import ALL_LANGUAGES, Erlang


@beartype
def erlang_module_name(golden_path: Path) -> str:
    """Return the Erlang module name for *golden_path*.

    Produces a deterministic, per-fixture name so every compiled
    ``.erl`` file in CI has a unique module declaration without needing
    ``sed`` rewriting.
    """
    dir_name = golden_path.parent.name
    stem = golden_path.stem
    return f"fixture_{dir_name}_{stem}".lower()


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


_ERLANG_CLS: type = Erlang


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
    golden_path: Path | None = None,
    **kwargs: object,
) -> literalizer.Language:
    """Return a cached instance of *lang_cls* for the given kwargs.

    Languages whose ``wrap_in_file`` introduces a named scope take a
    ``module_name`` constructor argument; default it to ``"check"`` so
    fixture output matches the historic golden files.  When
    *golden_path* is supplied and the language is Erlang, a
    per-fixture module name is derived from the path instead.
    """
    has_module_name = "module_name" in getattr(
        lang_cls, "__dataclass_fields__", {}
    )
    if has_module_name and "module_name" not in kwargs:
        if golden_path is not None and lang_cls is _ERLANG_CLS:
            kwargs["module_name"] = erlang_module_name(golden_path)
        else:
            kwargs["module_name"] = lang_cls.module_name_case.convert(
                name="check"
            )
    return cached_spec(
        lang_cls=lang_cls,
        kwargs_items=frozenset(kwargs.items()),
    )
