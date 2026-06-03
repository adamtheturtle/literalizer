"""Configuration for Sphinx."""

import importlib.metadata
from pathlib import Path

from packaging.specifiers import SpecifierSet
from sphinx_pyproject import SphinxConfig

from literalizer.languages import ALL_LANGUAGES

_pyproject_file = Path(__file__).parent.parent.parent / "pyproject.toml"
_pyproject_config = SphinxConfig(
    pyproject_file=_pyproject_file,
    config_overrides={"version": None},
)

project = _pyproject_config.name
author = _pyproject_config.author

extensions = [
    "sphinx_copybutton",
    "sphinx_jinja",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_substitution_extensions",
    "sphinxcontrib.spelling",
    "sphinxcontrib.towncrier.ext",
]

# Render the unreleased ``newsfragments/`` entries into
# ``docs/source/unreleased.rst`` so the Sphinx spelling, doc-build and
# link-checking gates cover the prose before it is assembled into
# CHANGELOG.rst at release time.  ``include_empty=True`` makes the page
# show the "No significant changes." placeholder line between releases
# instead of an empty section (which would otherwise be a document
# with no body).
towncrier_draft_autoversion_mode = "draft"
towncrier_draft_include_empty = True
towncrier_draft_working_directory = f"{_pyproject_file.parent}"

templates_path = ["_templates"]

# Build the heterogeneous-strategy support matrix from the language
# registry so the table in ``heterogeneous-strategies.rst`` (rendered via
# the ``sphinx_jinja`` extension) cannot drift from the
# ``heterogeneous_strategies`` enum on each language class.  Every
# language supports ``ERROR``; only the richer strategies are listed, and
# a language exposing nothing else is omitted.
_strategies_by_language = {
    language.__name__: [
        member.name
        for member in language.HeterogeneousStrategies
        if member.name != "ERROR"
    ]
    for language in ALL_LANGUAGES
}
jinja_contexts = {
    "heterogeneous_strategies": {
        "languages": [
            {
                "name": name,
                "strategies": ", ".join(f"``{member}``" for member in members),
            }
            for name, members in sorted(_strategies_by_language.items())
            if members
        ],
    },
}

# Ambiguous cross-references from identically-named nested classes
# (DateFormat, DatetimeFormat, BytesFormat) across language modules.
suppress_warnings = ["ref.python"]

project_copyright = f"%Y, {author}"

copybutton_exclude = ".linenos, .gp"

project_metadata = importlib.metadata.metadata(distribution_name=project)
requires_python = project_metadata["Requires-Python"]
specifiers = SpecifierSet(specifiers=requires_python)
(specifier,) = specifiers
if specifier.operator != ">=":
    msg = (
        f"We only support '>=' for Requires-Python, got {specifier.operator}."
    )
    raise ValueError(msg)
minimum_python_version = specifier.version

html_theme = "furo"
html_title = project
html_show_copyright = False
html_show_sphinx = False
html_show_sourcelink = False
html_theme_options = {
    "sidebar_hide_name": False,
    "source_repository": "https://github.com/adamtheturtle/literalizer/",
    "source_branch": "main",
    "source_directory": "docs/source/",
}

htmlhelp_basename = "literalizerdoc"

spelling_word_list_filename = "../../spelling_private_dict.txt"

linkcheck_ignore = [
    r"https://dhall-lang\.org/",
    r"https://json5\.org/",
]
linkcheck_retries = 5

rst_prolog = f"""
.. |project| replace:: {project}
.. |minimum-python-version| replace:: {minimum_python_version}
.. |github-owner| replace:: adamtheturtle
.. |github-repository| replace:: literalizer
"""
