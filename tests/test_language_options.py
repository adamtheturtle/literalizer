"""Tests for the typed :class:`~literalizer.LanguageOptions` builder.

These are focused public-API pytest tests rather than golden-file
integration cases (cf. the exceptions documented in
``tests/test_languages.py``).  The point of
:meth:`~literalizer.LanguageCls.configured` is *static* type-safety for
downstream code that resolves a language class from a runtime string
and then applies generic options; it adds no new rendering behavior,
so it produces output identical to direct construction and has no
golden axis of its own.  The construction shapes below are written the
way the downstream ``sphinx-literalizer`` extension needs them -- a
``dict[str, LanguageCls]`` resolved by a runtime string, then
``configured`` with one generic options object -- so that this module
being type-checked by the project's mypy/pyright/pyrefly/ty suite *is*
the regression test for the type hole this API closes.
"""

from literalizer import (
    InputFormat,
    Language,
    LanguageCls,
    LanguageOptions,
    NewVariable,
    literalize,
)
from literalizer.languages import Clojure, Python

_REGISTRY: dict[str, LanguageCls] = {
    "python": Python,
    "clojure": Clojure,
}


def _render(*, language: Language) -> str:
    """Literalize a fixed document so two configurations can be
    compared by their rendered output.
    """
    return literalize(
        source="greeting: hi\n",
        input_format=InputFormat.YAML,
        language=language,
        variable_form=NewVariable(name="data"),
    ).code


def test_runtime_resolved_class_configured_matches_direct() -> None:
    """A language resolved from a runtime string and built through
    ``configured`` renders identically to direct construction.

    This is the downstream pattern: only ``LanguageCls`` is known at
    the call site, and the options arrive as one generic object.
    """
    language_cls: LanguageCls = _REGISTRY["python"]
    configured = language_cls.configured(
        options=LanguageOptions(string_format="SINGLE"),
    )

    direct = Python(string_format=Python.string_formats.SINGLE)

    assert _render(language=configured) == _render(language=direct)


def test_empty_options_match_language_defaults() -> None:
    """An empty :class:`~literalizer.LanguageOptions` reproduces the
    language's own defaults.
    """
    configured = Clojure.configured(options=LanguageOptions())

    assert _render(language=configured) == _render(language=Clojure())


def test_plain_str_option_is_passed_through() -> None:
    """A plain-``str`` option (here ``indent``) reaches the concrete
    per-language field.
    """
    configured = Python.configured(options=LanguageOptions(indent="\t"))

    direct = Python(indent="\t")

    assert _render(language=configured) == _render(language=direct)
