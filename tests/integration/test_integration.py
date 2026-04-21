"""Integration tests that compare literalize_yaml output against golden
files.

Each subdirectory contains an ``input.yaml`` and one expected-output file
per supported language, using the real file extension for that language.

Golden files contain syntactically valid programs so that pre-commit hooks
can syntax-check them directly without additional wrapping.

To regenerate all golden files after changing output::

    uv run pytest tests/integration/ --regen-all
"""

import dataclasses
import enum
import functools
import os
from collections.abc import Callable, Iterable
from pathlib import Path

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture
from ruamel.yaml import YAML

import literalizer
from literalizer._language import StubReturn
from literalizer.exceptions import (
    HeterogeneousCollectionError,
    IncompatibleFormatsError,
    NullInCollectionError,
    UnrepresentableIntegerError,
)
from literalizer.languages import (
    ALL_LANGUAGES,
    C,
    Crystal,
    CSharp,
    Dart,
    Elm,
    Fortran,
    FSharp,
    Gleam,
    Go,
    Haskell,
    Kotlin,
    Mojo,
    OCaml,
    Odin,
    PureScript,
    Python,
    Rust,
    Swift,
    VisualBasic,
)

# ---------------------------------------------------------------------------
# Test-only data keyed by language class.
#
# Keeping the language-specific test values here — keyed by the language
# class itself, not by ``__name__`` — lets the parameterized tests below
# iterate uniformly over ``ALL_LANGUAGES`` without any
# ``if lang_cls.__name__ == "..."`` branches.  Genuine language facts
# live on the language class; only arbitrary test fixtures (alternative
# type names, fictional constructor prefixes, chosen field names, etc.)
# belong in this block.
# ---------------------------------------------------------------------------

# Alternative type names passed to the various ``default_*_type`` kwargs.
# Each value must differ from the language's own default *and* be a valid
# type name for that language's linter / compiler.  ``"String"`` is used
# as the fallback for any supported language not listed explicitly.
_DEFAULT_TYPE_OVERRIDE_FALLBACK = "String"

_DEFAULT_SET_ELEMENT_TYPE_OVERRIDES: dict[literalizer.LanguageCls, str] = {
    Crystal: "Int32",
    Go: "string",
    CSharp: "string",
    Mojo: "Int",
    Odin: "int",
    Python: "int",
    Rust: "i32",
}

_DEFAULT_SEQUENCE_ELEMENT_TYPE_OVERRIDES: dict[
    literalizer.LanguageCls, str
] = {
    Go: "interface{}",
    CSharp: "string",
    Mojo: "Int",
    Python: "int",
}

_DEFAULT_DICT_VALUE_TYPE_OVERRIDES: dict[literalizer.LanguageCls, str] = {
    Crystal: "Int32",
    Go: "interface{}",
    CSharp: "object?",
    Dart: "Object?",
    Kotlin: "Comparable<*>?",
    Mojo: "Int",
    Python: "int",
    Rust: "i32",
}

_DEFAULT_DICT_KEY_TYPE_OVERRIDES: dict[literalizer.LanguageCls, str] = {
    Crystal: "Int32",
    Go: "any",
    CSharp: "object",
    Dart: "Object",
    Kotlin: "Any",
    Python: "int",
    Rust: "&str",
    Swift: "AnyHashable",
    VisualBasic: "Object",
}

_DEFAULT_ORDERED_MAP_VALUE_TYPE_OVERRIDES: dict[
    literalizer.LanguageCls, str
] = {Go: "interface{}"}

# Languages that expose ``type_name`` / ``constructor_prefix`` kwargs for
# the ADT they emit; the value is the test override to apply.
_TYPE_NAME_OVERRIDES: dict[literalizer.LanguageCls, str] = {
    Elm: "JsonVal",
    FSharp: "JsonVal",
    Gleam: "JsonVal",
    Haskell: "JsonVal",
    OCaml: "json_t",
    PureScript: "JsonVal",
}

_CONSTRUCTOR_PREFIX_OVERRIDES: dict[literalizer.LanguageCls, str] = {
    Elm: "J",
    FSharp: "J",
    Gleam: "J",
    Haskell: "J",
    OCaml: "J",
    PureScript: "J",
}

# Languages that accept constructor-name kwargs (Fortran) or field-name
# kwargs (C); the inner dict is the kwargs to pass to the constructor.
_CONSTRUCTOR_NAME_OVERRIDES: dict[literalizer.LanguageCls, dict[str, str]] = {
    Fortran: {
        "null_name": "jnull",
        "bool_name": "jbool",
        "int_name": "jint",
        "real_name": "jreal",
        "str_name": "jstr",
        "list_name": "jlist",
        "map_name": "jmap",
        "set_name": "jset",
        "entry_name": "jentry",
    },
}

_FIELD_NAME_OVERRIDES: dict[literalizer.LanguageCls, dict[str, str]] = {
    C: {
        "bool_field": "bl",
        "int_field": "integer",
        "float_field": "fp",
        "string_field": "str",
        "array_field": "arr",
        "map_field": "dict",
        "key_field": "key",
        "value_field": "val",
    },
}

# Declaration-style → alternative-sequence-format overrides, by enum name.
# Rust CONST and STATIC raise ``IncompatibleFormatsError`` with the default
# ``Vec`` sequence format, so the test falls back to ``Array``.
_DECLARATION_STYLE_SEQUENCE_FORMAT_OVERRIDES: dict[
    literalizer.LanguageCls, dict[str, str]
] = {Rust: {"CONST": "ARRAY", "STATIC": "ARRAY"}}


@pytest.fixture(name="cases_dir")
def fixture_cases_dir(request: pytest.FixtureRequest) -> Path:
    """Return the absolute path to the integration test cases
    directory.
    """
    return request.config.rootpath / "tests" / "integration" / "cases"


@beartype
def _check_golden(
    *,
    file_regression: FileRegressionFixture,
    contents: str,
    golden_path: Path,
    extension: str,
    newline: str | None,
) -> None:
    """Compare ``contents`` against ``golden_path`` in memory.

    ``file_regression.check`` writes an ``.obtained`` file, reads both
    files back from disk, and runs ``difflib`` even on the pass path,
    which dominates this module's runtime (~13k calls per run).  For
    the pass path we can compare the already-in-memory ``contents``
    against the golden file directly; only on miss or regen do we
    delegate to the fixture for its ``.obtained`` + HTML-diff output.
    """
    config = file_regression.request.config
    regen = file_regression.force_regen or bool(
        config.getoption(name="regen_all")
        or config.getoption(name="force_regen"),
    )
    if (
        not regen
        and golden_path.is_file()
        and contents.splitlines() == golden_path.read_text().splitlines()
    ):
        return
    file_regression.check(
        contents=contents,
        extension=extension,
        newline=newline,
        fullpath=golden_path,
    )


def test_check_golden_mismatch_delegates(
    tmp_path: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """``_check_golden`` delegates to ``file_regression.check`` on miss.

    Every golden file matches in CI, so nothing else reaches the
    fallback branch.
    """
    golden = tmp_path / "golden.txt"
    golden.write_text(data="expected\n")
    with pytest.raises(
        expected_exception=AssertionError,
        match="FILES DIFFER",
    ):
        _check_golden(
            file_regression=file_regression,
            contents="different\n",
            golden_path=golden,
            extension=".txt",
            newline="",
        )


@beartype
def _find_redefinition_styles(
    spec: literalizer.Language,
) -> list[enum.Enum]:
    """Return all declaration styles that support redefinition."""
    return [
        style
        for style in spec.declaration_styles
        if style.value.supports_redefinition
    ]


@beartype
def _prepend_preamble(
    wrapped: str,
    preamble: tuple[str, ...],
) -> str:
    """Prepend *preamble* lines before *wrapped*."""
    if not preamble:
        return wrapped
    return "\n".join(preamble) + "\n" + wrapped


@dataclasses.dataclass
class _Variant:
    """A formatting variant for a language (date, sequence, set, etc.)."""

    name: str
    spec: literalizer.Language
    lang_cls: literalizer.LanguageCls


def _wrap_variable_name(lang_cls: literalizer.LanguageCls) -> str | None:
    """Return the wrap variable name for a language class."""
    return "my_data" if lang_cls.supports_variable_names else None


def _wrap_variable_form(
    lang_cls: literalizer.LanguageCls,
) -> literalizer.NewVariable | None:
    """Return a :class:`NewVariable` form for a language class, or
    None.
    """
    name = _wrap_variable_name(lang_cls=lang_cls)
    if name is None:
        return None
    return literalizer.NewVariable(name=name)


def _lang_cls_name(cls: literalizer.LanguageCls) -> str:
    """Return the class name for sorting."""
    return cls.__name__


@functools.cache
def _sorted_languages() -> list[literalizer.LanguageCls]:
    """Return all languages sorted by class name."""
    return sorted(ALL_LANGUAGES, key=_lang_cls_name)


@functools.cache
def _cached_spec(
    *,
    lang_cls: literalizer.LanguageCls,
    kwargs_items: frozenset[tuple[str, object]],
) -> literalizer.Language:
    """Return a cached instance of *lang_cls* built from *kwargs_items*.

    Each ``lang_cls()`` call rebuilds ``@beartype``-wrapped closures
    inside the formatter factories; sharing one instance per
    ``(class, kwargs)`` combination cuts thousands of redundant builds
    across collection and test execution.
    """
    return lang_cls(**dict(kwargs_items))


def _spec(
    *,
    lang_cls: literalizer.LanguageCls,
    **kwargs: object,
) -> literalizer.Language:
    """Return a cached instance of *lang_cls* for the given kwargs."""
    return _cached_spec(
        lang_cls=lang_cls,
        kwargs_items=frozenset(kwargs.items()),
    )


@dataclasses.dataclass
class _VariantCase:
    """A format-variant golden-file test case."""

    variant_name: str
    variant: _Variant
    case_dir_name: str
    variable_form: literalizer.NewVariable | None


@beartype
def _build_non_default_variants(
    *,
    category: str,
    get_default: Callable[[literalizer.Language], object],
    get_formats: Callable[[literalizer.Language], type[enum.Enum]],
    make_spec: Callable[
        [literalizer.LanguageCls, enum.Enum],
        literalizer.Language,
    ],
) -> list[_Variant]:
    """Build variants for every non-default value of a format enum.

    This is the generic version of the many per-format builder functions
    that all follow the same pattern: iterate all languages, find the
    non-default members of a format enum, and create a ``_Variant`` for
    each one.
    """
    variants: list[_Variant] = []
    for lang_cls in _sorted_languages():
        lang_name = lang_cls.__name__
        spec = _spec(lang_cls=lang_cls)
        default_format = get_default(spec)
        for fmt in get_formats(spec):
            if fmt is default_format:
                continue
            variants.append(
                _Variant(
                    name=f"{lang_name}_{category}_{fmt.name.lower()}",
                    spec=make_spec(lang_cls, fmt),
                    lang_cls=lang_cls,
                )
            )
    return variants


@beartype
def _build_default_set_element_type_variants() -> Iterable[_Variant]:
    """Build default-set-type variants for languages that support it."""
    variants: list[_Variant] = []
    for lang_cls in _sorted_languages():
        if not lang_cls.supports_default_set_element_type:
            continue
        type_name = _DEFAULT_SET_ELEMENT_TYPE_OVERRIDES.get(
            lang_cls,
            _DEFAULT_TYPE_OVERRIDE_FALLBACK,
        )
        variants.append(
            _Variant(
                name=f"{lang_cls.__name__}_default_set_element_type_string",
                spec=lang_cls(default_set_element_type=type_name),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def _build_default_sequence_element_type_variants() -> Iterable[_Variant]:
    """Build default-sequence-type variants for languages that support
    it.
    """
    variants: list[_Variant] = []
    for lang_cls in _sorted_languages():
        if not lang_cls.supports_default_sequence_element_type:
            continue
        type_name = _DEFAULT_SEQUENCE_ELEMENT_TYPE_OVERRIDES.get(
            lang_cls,
            _DEFAULT_TYPE_OVERRIDE_FALLBACK,
        )
        variants.append(
            _Variant(
                name=(
                    f"{lang_cls.__name__}_default_sequence_element_type_string"
                ),
                spec=lang_cls(default_sequence_element_type=type_name),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def _build_default_dict_value_type_variants() -> Iterable[_Variant]:
    """Build default-dict-value-type variants for languages that support
    it.
    """
    variants: list[_Variant] = []
    for lang_cls in _sorted_languages():
        if not lang_cls.supports_default_dict_value_type:
            continue
        type_name = _DEFAULT_DICT_VALUE_TYPE_OVERRIDES.get(
            lang_cls,
            _DEFAULT_TYPE_OVERRIDE_FALLBACK,
        )
        variants.append(
            _Variant(
                name=f"{lang_cls.__name__}_default_dict_value_type_string",
                spec=lang_cls(default_dict_value_type=type_name),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def _build_default_dict_key_type_variants() -> Iterable[_Variant]:
    """Build default-dict-key-type variants for languages that support
    it.
    """
    variants: list[_Variant] = []
    for lang_cls in _sorted_languages():
        if not lang_cls.supports_default_dict_key_type:
            continue
        type_name = _DEFAULT_DICT_KEY_TYPE_OVERRIDES.get(
            lang_cls,
            _DEFAULT_TYPE_OVERRIDE_FALLBACK,
        )
        variants.append(
            _Variant(
                name=f"{lang_cls.__name__}_default_dict_key_type",
                spec=lang_cls(default_dict_key_type=type_name),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def _build_default_ordered_map_value_type_variants() -> Iterable[_Variant]:
    """Build default-ordered-map-value-type variants for every language
    that supports the option.
    """
    variants: list[_Variant] = []
    for lang_cls in _sorted_languages():
        if not lang_cls.supports_default_ordered_map_value_type:
            continue
        type_name = _DEFAULT_ORDERED_MAP_VALUE_TYPE_OVERRIDES.get(
            lang_cls,
            _DEFAULT_TYPE_OVERRIDE_FALLBACK,
        )
        variants.append(
            _Variant(
                name=f"{lang_cls.__name__}_default_ordered_map_value_type",
                spec=lang_cls(default_ordered_map_value_type=type_name),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def _build_line_ending_decl_variants() -> Iterable[_Variant]:
    """Build line-ending + declaration-style cross-option variants.

    For each language with multiple line endings *and* multiple
    declaration styles, create a variant for every non-default
    line ending paired with every non-default declaration style.
    """
    variants: list[_Variant] = []
    for lang_cls in _sorted_languages():
        lang_name = lang_cls.__name__
        spec = _spec(lang_cls=lang_cls)
        default_line_ending = spec.line_ending
        default_declaration_style = spec.declaration_style
        non_default_line_endings = [
            line_ending
            for line_ending in spec.line_endings
            if line_ending is not default_line_ending
        ]
        non_default_declaration_styles = [
            declaration_style
            for declaration_style in spec.declaration_styles
            if declaration_style is not default_declaration_style
        ]
        variants.extend(
            _Variant(
                name=(
                    f"{lang_name}_line_ending_{line_ending.name.lower()}"
                    f"_decl_{declaration_style.name.lower()}"
                ),
                spec=lang_cls(
                    line_ending=line_ending,
                    declaration_style=declaration_style,
                ),
                lang_cls=lang_cls,
            )
            for line_ending in non_default_line_endings
            for declaration_style in non_default_declaration_styles
        )
    return variants


@beartype
def _build_sequence_decl_variants() -> Iterable[_Variant]:
    """Build sequence format + declaration style cross-option variants.

    For each language with multiple sequence formats *and* multiple
    declaration styles, create a variant for every non-default
    sequence format paired with every non-default declaration style.
    """
    variants: list[_Variant] = []
    for lang_cls in _sorted_languages():
        lang_name = lang_cls.__name__
        spec = _spec(lang_cls=lang_cls)
        default_sequence_format = spec.sequence_format
        default_declaration_style = spec.declaration_style
        non_default_sequence_formats = [
            sequence_format
            for sequence_format in spec.sequence_formats
            if sequence_format is not default_sequence_format
        ]
        non_default_declaration_styles = [
            declaration_style
            for declaration_style in spec.declaration_styles
            if declaration_style is not default_declaration_style
        ]
        variants.extend(
            _Variant(
                name=(
                    f"{lang_name}_sequence_{sequence_format.name.lower()}"
                    f"_decl_{declaration_style.name.lower()}"
                ),
                spec=lang_cls(
                    sequence_format=sequence_format,
                    declaration_style=declaration_style,
                ),
                lang_cls=lang_cls,
            )
            for sequence_format in non_default_sequence_formats
            for declaration_style in non_default_declaration_styles
        )
    return variants


def _has_non_printable_ascii_dict_keys(data: object) -> bool:
    """Return ``True`` if *data* contains a dict key that is empty or
    has characters outside printable ASCII.
    """
    if isinstance(data, dict):
        for key in data:  # pyright: ignore[reportUnknownVariableType]
            if isinstance(key, str) and (
                not key or not key.isprintable() or not key.isascii()
            ):
                return True
        return any(
            _has_non_printable_ascii_dict_keys(data=v)  # pyright: ignore[reportUnknownArgumentType]
            for v in data.values()  # pyright: ignore[reportUnknownVariableType]
        )
    if isinstance(data, list):
        return any(
            _has_non_printable_ascii_dict_keys(data=item)  # pyright: ignore[reportUnknownArgumentType]
            for item in data  # pyright: ignore[reportUnknownVariableType]
        )
    return False


@functools.cache
@beartype
def _cases_with_non_trivial_dict_keys(
    cases_dir: Path,
) -> frozenset[str]:
    """Return case directory names whose input YAML has dict keys that
    some languages cannot represent (empty or non-printable-ASCII).
    """
    yaml = YAML()
    result: set[str] = set()
    for case_dir in cases_dir.iterdir():
        loaded: object = yaml.load(  # pyright: ignore[reportUnknownMemberType]
            stream=(case_dir / "input.yaml").read_text(),
        )
        if _has_non_printable_ascii_dict_keys(data=loaded):
            result.add(case_dir.name)
    return frozenset(result)


@dataclasses.dataclass
class _CallCaseConfig:
    """Configuration for a ``literalize_call`` golden-file test case."""

    case_dir_name: str
    target_function: str
    parameter_names: list[str]
    call_transform: Callable[[str], str] | None
    transform_stub_names: list[str]
    per_element: bool
    call_style_type: type[literalizer.CallStyle] | None = None


_CALL_STYLE_VARIANTS: list[tuple[str, type[literalizer.CallStyle]]] = [
    ("keyword", literalizer.KeywordCallStyle),
    ("positional", literalizer.PositionalCallStyle),
    ("object", literalizer.ObjectCallStyle),
]


_CALL_CASE_CONFIGS: list[_CallCaseConfig] = [
    _CallCaseConfig(
        case_dir_name="call_keyword_args",
        target_function="throttler.check",
        parameter_names=["user_id", "ts"],
        call_transform=lambda c: f"emit({c})",
        transform_stub_names=["emit"],
        per_element=True,
    ),
    _CallCaseConfig(
        case_dir_name="call_scalar_args",
        target_function="process",
        parameter_names=["value"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
    ),
    _CallCaseConfig(
        case_dir_name="call_dotted_method",
        target_function="app.client.fetch",
        parameter_names=["payload"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
    ),
    _CallCaseConfig(
        case_dir_name="call_deep_dotted_method",
        target_function="obj.api.client.post",
        parameter_names=["data"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
    ),
    _CallCaseConfig(
        case_dir_name="call_deep_dotted_transformed",
        target_function="app.client.fetch",
        parameter_names=["payload"],
        call_transform=lambda c: f"emit({c})",
        transform_stub_names=["emit"],
        per_element=True,
    ),
    _CallCaseConfig(
        case_dir_name="call_transform_no_wrapper",
        target_function="process",
        parameter_names=["value"],
        call_transform=lambda c: c,
        transform_stub_names=[],
        per_element=True,
    ),
    *[
        _CallCaseConfig(
            case_dir_name=f"call_{name}",
            target_function="throttler.check",
            parameter_names=["user_id", "ts"],
            call_transform=lambda c: f"emit({c})",
            transform_stub_names=["emit"],
            per_element=True,
            call_style_type=cls,
        )
        for name, cls in _CALL_STYLE_VARIANTS
    ],
]


@functools.cache
@beartype
def _discover_cases() -> list[tuple[str, literalizer.LanguageCls]]:
    """Return ``(case_name, lang_cls)`` tuples."""
    cases_dir = Path(__file__).parent / "cases"
    call_case_dirs = frozenset(cfg.case_dir_name for cfg in _CALL_CASE_CONFIGS)
    non_trivial_key_cases = _cases_with_non_trivial_dict_keys(
        cases_dir=cases_dir,
    )
    cases: list[tuple[str, literalizer.LanguageCls]] = []
    for case_dir in sorted(cases_dir.iterdir()):
        if case_dir.name in call_case_dirs:
            continue
        non_trivial = case_dir.name in non_trivial_key_cases
        for lang_cls in _sorted_languages():
            if (
                non_trivial
                and not lang_cls.supports_non_printable_ascii_dict_keys
            ):
                continue
            cases.append((case_dir.name, lang_cls))
    return cases


@functools.cache
def _group_cases_by_language() -> dict[
    literalizer.LanguageCls,
    list[str],
]:
    """Return case names grouped by language class.

    The test takes the language as its only pytest axis and iterates
    that language's case names inside the test body with ``subtests``.
    Folding thousands of cases into ~30 cuts collection and per-test
    overhead on slower CI runners (notably Windows).
    """
    groups: dict[literalizer.LanguageCls, list[str]] = {}
    for case_name, lang_cls in _discover_cases():
        groups.setdefault(lang_cls, []).append(case_name)
    return groups


@functools.cache
def _golden_file_languages() -> list[literalizer.LanguageCls]:
    """Return languages that have at least one golden-file case."""
    groups = _group_cases_by_language()
    return [cls for cls in _sorted_languages() if cls in groups]


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=_golden_file_languages(),
    ids=_lang_cls_name,
)
def test_golden_file(
    lang_cls: literalizer.LanguageCls,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Test that literalize_yaml output matches expected golden file."""
    lang_name = lang_cls.__name__
    for case_name in _group_cases_by_language()[lang_cls]:
        with subtests.test(case_name=case_name):
            input_path = cases_dir / case_name / "input.yaml"
            yaml_string = input_path.read_text()
            golden_path = input_path.parent / (lang_name + lang_cls.extension)
            try:
                result = literalizer.literalize(
                    source=yaml_string,
                    input_format=literalizer.InputFormat.YAML,
                    language=_spec(lang_cls=lang_cls),
                    pre_indent_level=0,
                    include_delimiters=True,
                    variable_form=_wrap_variable_form(lang_cls=lang_cls),
                    wrap_in_file=True,
                )
            except UnrepresentableIntegerError:
                golden_path.unlink(missing_ok=True)
                pytest.skip(
                    f"{lang_name} cannot represent integer in this input",
                )
            except HeterogeneousCollectionError:
                golden_path.unlink(missing_ok=True)
                pytest.skip(
                    f"{lang_name} cannot represent this heterogeneous input",
                )
            # newline="" prevents Python text-mode from converting \r\n to
            # \n on Windows, which would corrupt golden files containing
            # literal CR bytes (e.g. CommonLisp string_control_chars).
            _check_golden(
                file_regression=file_regression,
                contents=result.code + "\n",
                extension=lang_cls.extension,
                newline="",
                golden_path=golden_path,
            )


@dataclasses.dataclass
class _CombinedCase:
    """A combined-variable-forms test case for a specific redefinition
    style.
    """

    case_name: str
    lang_name: str
    lang_cls: literalizer.LanguageCls
    declaration_style: enum.Enum
    golden_file_name: str


@functools.cache
@beartype
def _discover_combined_cases() -> list[_CombinedCase]:
    """Return combined test cases for all redefinition-supporting
    styles.
    """
    cases_dir = Path(__file__).parent / "cases"
    call_case_dirs = frozenset(cfg.case_dir_name for cfg in _CALL_CASE_CONFIGS)
    non_trivial_key_cases = _cases_with_non_trivial_dict_keys(
        cases_dir=cases_dir,
    )
    cases: list[_CombinedCase] = []
    for case_dir in sorted(cases_dir.iterdir()):
        if case_dir.name in call_case_dirs:
            continue
        non_trivial = case_dir.name in non_trivial_key_cases
        for lang_cls in _sorted_languages():
            lang_name = lang_cls.__name__
            if (
                non_trivial
                and not lang_cls.supports_non_printable_ascii_dict_keys
            ):
                continue
            spec = _spec(lang_cls=lang_cls)
            redef_styles = _find_redefinition_styles(spec=spec)
            for style in redef_styles:
                if style is redef_styles[0]:
                    golden_name = f"{lang_name}_combined"
                else:
                    style_suffix = style.name.lower()
                    golden_name = (
                        f"{lang_name}_combined"
                        f"_declaration_style_{style_suffix}"
                    )
                cases.append(
                    _CombinedCase(
                        case_name=case_dir.name,
                        lang_name=lang_name,
                        lang_cls=lang_cls,
                        declaration_style=style,
                        golden_file_name=golden_name,
                    )
                )
    return cases


@functools.cache
def _group_combined_cases_by_language() -> dict[
    literalizer.LanguageCls,
    list[_CombinedCase],
]:
    """Return combined cases grouped by language class.

    The test takes the language as its only pytest axis and iterates
    that language's combined cases inside the test body with
    ``subtests``.  Folding thousands of cases into ~30 cuts collection
    and per-test overhead on slower CI runners (notably Windows).
    """
    groups: dict[literalizer.LanguageCls, list[_CombinedCase]] = {}
    for case in _discover_combined_cases():
        groups.setdefault(case.lang_cls, []).append(case)
    return groups


@functools.cache
def _combined_languages() -> list[literalizer.LanguageCls]:
    """Return languages that have at least one combined-form case."""
    groups = _group_combined_cases_by_language()
    return [cls for cls in _sorted_languages() if cls in groups]


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=_combined_languages(),
    ids=_lang_cls_name,
)
def test_golden_file_combined_variable_forms(
    lang_cls: literalizer.LanguageCls,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Test that literalize with BothVariableForms produces expected
    golden output combining declaration and assignment in one file.
    """
    for combined_case in _group_combined_cases_by_language()[lang_cls]:
        with subtests.test(
            case_name=combined_case.case_name,
            golden_file_name=combined_case.golden_file_name,
        ):
            input_path = cases_dir / combined_case.case_name / "input.yaml"
            spec = _spec(
                lang_cls=lang_cls,
                declaration_style=combined_case.declaration_style,
            )
            yaml_string = input_path.read_text()
            golden_path = input_path.parent / (
                combined_case.golden_file_name + lang_cls.extension
            )
            try:
                result = literalizer.literalize(
                    source=yaml_string,
                    input_format=literalizer.InputFormat.YAML,
                    language=spec,
                    pre_indent_level=0,
                    include_delimiters=True,
                    variable_form=literalizer.BothVariableForms(
                        name="my_data",
                    ),
                    wrap_in_file=True,
                )
            except UnrepresentableIntegerError:
                golden_path.unlink(missing_ok=True)
                pytest.skip(
                    f"{lang_cls.__name__} cannot represent integer in "
                    "this input"
                )
            except HeterogeneousCollectionError:
                golden_path.unlink(missing_ok=True)
                pytest.skip(
                    f"{lang_cls.__name__} cannot represent this "
                    "heterogeneous input"
                )
            _check_golden(
                file_regression=file_regression,
                contents=result.code + "\n",
                extension=lang_cls.extension,
                newline="",
                golden_path=golden_path,
            )


@beartype
def _build_constructor_name_variants() -> Iterable[_Variant]:
    """Build constructor-name variants for languages listed in
    :data:`_CONSTRUCTOR_NAME_OVERRIDES` (e.g. Fortran).
    """
    variants: list[_Variant] = []
    for lang_cls in _sorted_languages():
        kwargs = _CONSTRUCTOR_NAME_OVERRIDES.get(lang_cls)
        if kwargs is None:
            continue
        variants.append(
            _Variant(
                name=f"{lang_cls.__name__}_constructor_names_j",
                spec=lang_cls(**kwargs),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def _build_type_name_variants() -> Iterable[_Variant]:
    """Build type-name variants for languages that generate a named type.

    These languages emit a custom algebraic data type in their body
    preamble (e.g. ``data Val = …`` in Haskell).  The ``type_name``
    constructor parameter lets users customize that name.
    """
    variants: list[_Variant] = []
    for lang_cls in _sorted_languages():
        custom_name = _TYPE_NAME_OVERRIDES.get(lang_cls)
        if custom_name is None:
            continue
        variants.append(
            _Variant(
                name=f"{lang_cls.__name__}_type_name_{custom_name}",
                spec=lang_cls(type_name=custom_name),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def _build_constructor_prefix_variants() -> Iterable[_Variant]:
    """Build constructor-prefix variants for languages with custom
    ADTs.
    """
    variants: list[_Variant] = []
    for lang_cls in _sorted_languages():
        custom_prefix = _CONSTRUCTOR_PREFIX_OVERRIDES.get(lang_cls)
        if custom_prefix is None:
            continue
        variants.append(
            _Variant(
                name=f"{lang_cls.__name__}_prefix_{custom_prefix}",
                spec=lang_cls(constructor_prefix=custom_prefix),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def _build_c_field_name_variants() -> Iterable[_Variant]:
    """Build field-name variants for languages listed in
    :data:`_FIELD_NAME_OVERRIDES` (e.g. C).
    """
    variants: list[_Variant] = []
    for lang_cls in _sorted_languages():
        kwargs = _FIELD_NAME_OVERRIDES.get(lang_cls)
        if kwargs is None:
            continue
        variants.append(
            _Variant(
                name=f"{lang_cls.__name__}_field_names_custom",
                spec=lang_cls(**kwargs),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def _build_string_format_cross_variants(
    *,
    other_kwarg: str,
    other_tag: str,
    get_other_default: Callable[[literalizer.Language], object],
    get_other_formats: Callable[[literalizer.Language], type[enum.Enum]],
) -> list[_Variant]:
    """Build cross-product variants of ``string_format`` and another axis.

    For every language, pair every non-default ``string_format`` with
    every non-default value of the other axis.  Covers code paths where
    the chosen ``string_format`` interacts with another formatter axis
    (e.g. the plain-ISO date/datetime fallback that only fires when both
    ``string_format`` and the date/datetime format are non-default).
    """
    variants: list[_Variant] = []
    for lang_cls in _sorted_languages():
        spec = _spec(lang_cls=lang_cls)
        default_string = spec.string_format
        default_other = get_other_default(spec)
        lang_name = lang_cls.__name__
        for sf in spec.string_formats:
            if sf is default_string:
                continue
            for of in get_other_formats(spec):
                if of is default_other:
                    continue
                variants.append(
                    _Variant(
                        name=(
                            f"{lang_name}"
                            f"_string_{sf.name.lower()}"
                            f"_{other_tag}_{of.name.lower()}"
                        ),
                        spec=lang_cls(
                            string_format=sf,
                            **{other_kwarg: of},
                        ),
                        lang_cls=lang_cls,
                    )
                )
    return variants


@beartype
def _build_type_hints_cross_variants() -> list[_Variant]:
    """Build cross-product variants: each non-default type-hint format
    combined with each non-default value of another format axis.

    These cover code paths where the type annotation depends on the
    chosen sequence / date / datetime / dict / set format.
    """
    axes: list[
        tuple[
            str,
            Callable[[literalizer.Language], object],
            Callable[[literalizer.Language], type[enum.Enum]],
            str,
        ]
    ] = [
        (
            "seq",
            lambda s: s.sequence_format,
            lambda s: s.sequence_formats,
            "sequence_format",
        ),
        (
            "date",
            lambda s: s.format_date,
            lambda s: s.date_formats,
            "date_format",
        ),
        (
            "dt",
            lambda s: s.format_datetime,
            lambda s: s.datetime_formats,
            "datetime_format",
        ),
        (
            "dict",
            lambda s: s.dict_format,
            lambda s: s.dict_formats,
            "dict_format",
        ),
        (
            "set",
            lambda s: s.set_format,
            lambda s: s.set_formats,
            "set_format",
        ),
        (
            "nls",
            lambda s: s.numeric_literal_suffix,
            lambda s: s.numeric_literal_suffixes,
            "numeric_literal_suffix",
        ),
    ]
    variants: list[_Variant] = []
    for lang_cls in _sorted_languages():
        spec = _spec(lang_cls=lang_cls)
        default_th = spec.variable_type_hints
        lang_name = lang_cls.__name__
        for th_fmt in spec.variable_type_hints_formats:
            if th_fmt is default_th:
                continue
            th_tag = th_fmt.name.lower()
            for axis_name, get_default, get_formats, kwarg in axes:
                default = get_default(spec)
                for fmt in get_formats(spec):
                    if fmt is default:
                        continue
                    variants.append(
                        _Variant(
                            name=(
                                f"{lang_name}"
                                f"_type_hints_{th_tag}"
                                f"_{axis_name}"
                                f"_{fmt.name.lower()}"
                            ),
                            spec=lang_cls(
                                variable_type_hints=th_fmt,
                                **{kwarg: fmt},
                            ),
                            lang_cls=lang_cls,
                        ),
                    )
    return variants


@beartype
def _build_modifier_variant_cases() -> list[_VariantCase]:
    """Build variants exercising per-language modifier rendering.

    For every language with a non-empty ``modifiers`` enum, emit one
    singleton-modifier variant per member plus one variant per entry
    in ``lang_cls.modifier_combinations``.  Each variant runs against
    inputs covering scalar / dict / set / date / datetime values so
    each branch of typed-declaration inference is exercised;
    combinations the language rejects at literalize time are skipped
    by the test itself.
    """
    cases: list[_VariantCase] = []
    case_dirs = (
        "scalar_int",
        "simple_dict",
        "set",
        "empty_set",
        "scalar_date",
        "scalar_datetime",
    )
    for lang_cls in _sorted_languages():
        spec = _spec(lang_cls=lang_cls)
        if len(spec.modifiers) == 0:
            continue
        entries: list[tuple[str, frozenset[enum.Enum]]] = [
            (member.name.lower(), frozenset({member}))
            for member in spec.modifiers
        ]
        entries.extend(
            (combo.name, combo.modifiers)
            for combo in lang_cls.modifier_combinations
        )
        for mod_name, modifiers in entries:
            variant = _Variant(
                name=f"{lang_cls.__name__}_modifiers_{mod_name}",
                spec=_spec(lang_cls=lang_cls),
                lang_cls=lang_cls,
            )
            cases.extend(
                _VariantCase(
                    variant_name=variant.name,
                    variant=variant,
                    case_dir_name=case_dir_name,
                    variable_form=literalizer.NewVariable(
                        name="my_data",
                        modifiers=modifiers,
                    ),
                )
                for case_dir_name in case_dirs
            )

    # C#'s default sequence format is a tuple, but a typed declaration
    # forces an array type — mixing the two yields invalid C#.  Force
    # ARRAY for sequence cases so the inferred ``object[]`` matches the
    # generated initializer.
    csharp_readonly_mixed = _Variant(
        name="CSharp_modifiers_readonly_mixed_numbers",
        spec=_spec(
            lang_cls=CSharp,
            sequence_format=CSharp.sequence_formats.ARRAY,
        ),
        lang_cls=CSharp,
    )
    cases.append(
        _VariantCase(
            variant_name=csharp_readonly_mixed.name,
            variant=csharp_readonly_mixed,
            case_dir_name="mixed_number_list",
            variable_form=literalizer.NewVariable(
                name="my_data",
                modifiers=frozenset({CSharp.modifiers.READONLY}),
            ),
        )
    )
    csharp_readonly_array = _Variant(
        name="CSharp_modifiers_readonly_array",
        spec=_spec(
            lang_cls=CSharp,
            sequence_format=CSharp.sequence_formats.ARRAY,
        ),
        lang_cls=CSharp,
    )
    cases.append(
        _VariantCase(
            variant_name=csharp_readonly_array.name,
            variant=csharp_readonly_array,
            case_dir_name="simple_sequence",
            variable_form=literalizer.NewVariable(
                name="my_data",
                modifiers=frozenset({CSharp.modifiers.READONLY}),
            ),
        )
    )
    return cases


@functools.cache
def _build_variant_cases() -> list[_VariantCase]:
    """Collect all format-variant golden-file test cases."""
    nv = _build_non_default_variants
    date = nv(
        category="date",
        get_default=lambda s: s.format_date,
        get_formats=lambda s: s.date_formats,
        make_spec=lambda cls, fmt: cls(date_format=fmt),
    )
    datetime_ = nv(
        category="datetime",
        get_default=lambda s: s.format_datetime,
        get_formats=lambda s: s.datetime_formats,
        make_spec=lambda cls, fmt: cls(datetime_format=fmt),
    )
    sequence = nv(
        category="sequence",
        get_default=lambda s: s.sequence_format,
        get_formats=lambda s: s.sequence_formats,
        make_spec=lambda cls, fmt: cls(sequence_format=fmt),
    )
    set_ = nv(
        category="set",
        get_default=lambda s: s.set_format,
        get_formats=lambda s: s.set_formats,
        make_spec=lambda cls, fmt: cls(set_format=fmt),
    )
    comment = nv(
        category="comment",
        get_default=lambda s: s.comment_format,
        get_formats=lambda s: s.comment_formats,
        make_spec=lambda cls, fmt: cls(comment_format=fmt),
    )
    type_hints = nv(
        category="type_hints",
        get_default=lambda s: s.variable_type_hints,
        get_formats=lambda s: s.variable_type_hints_formats,
        make_spec=lambda cls, fmt: cls(variable_type_hints=fmt),
    )

    def _declaration_style_make_spec(
        cls: literalizer.LanguageCls,
        fmt: enum.Enum,
    ) -> literalizer.Language:
        """Build a spec for *fmt*, applying any per-language sequence-
        format
        override listed in
        :data:`_DECLARATION_STYLE_SEQUENCE_FORMAT_OVERRIDES`.

        Some declaration styles are incompatible with the default sequence
        format (e.g. Rust CONST/STATIC raise ``IncompatibleFormatsError``
        when combined with ``VEC``).
        """
        overrides = _DECLARATION_STYLE_SEQUENCE_FORMAT_OVERRIDES.get(cls, {})
        seq_format_name = overrides.get(fmt.name)
        if seq_format_name is None:
            return cls(declaration_style=fmt)
        spec = cls()
        seq_fmt = next(
            f for f in spec.sequence_formats if f.name == seq_format_name
        )
        return cls(declaration_style=fmt, sequence_format=seq_fmt)

    declaration_style = nv(
        category="declaration_style",
        get_default=lambda s: s.declaration_style,
        get_formats=lambda s: s.declaration_styles,
        make_spec=_declaration_style_make_spec,
    )
    dict_format = nv(
        category="dict_format",
        get_default=lambda s: s.dict_format,
        get_formats=lambda s: s.dict_formats,
        make_spec=lambda cls, fmt: cls(dict_format=fmt),
    )
    dict_entry_style = nv(
        category="dict_entry_style",
        get_default=lambda s: s.dict_entry_style,
        get_formats=lambda s: s.dict_entry_styles,
        make_spec=lambda cls, fmt: cls(dict_entry_style=fmt),
    )
    integer_format = nv(
        category="integer_format",
        get_default=lambda s: s.integer_format,
        get_formats=lambda s: s.integer_formats,
        make_spec=lambda cls, fmt: cls(integer_format=fmt),
    )
    numeric_literal_suffix = nv(
        category="numeric_literal_suffix",
        get_default=lambda s: s.numeric_literal_suffix,
        get_formats=lambda s: s.numeric_literal_suffixes,
        make_spec=lambda cls, fmt: cls(numeric_literal_suffix=fmt),
    )
    numeric_separator = nv(
        category="numeric_separator",
        get_default=lambda s: s.numeric_separator,
        get_formats=lambda s: s.numeric_separators,
        make_spec=lambda cls, fmt: cls(numeric_separator=fmt),
    )
    float_format = nv(
        category="float_format",
        get_default=lambda s: s.float_format,
        get_formats=lambda s: s.float_formats,
        make_spec=lambda cls, fmt: cls(float_format=fmt),
    )
    numeric_style = nv(
        category="numeric_style",
        get_default=lambda s: s.numeric_style,
        get_formats=lambda s: s.numeric_styles,
        make_spec=lambda cls, fmt: cls(numeric_style=fmt),
    )
    string_format = nv(
        category="string_format",
        get_default=lambda s: s.string_format,
        get_formats=lambda s: s.string_formats,
        make_spec=lambda cls, fmt: cls(string_format=fmt),
    )
    bytes_format = nv(
        category="bytes_format",
        get_default=lambda s: s.format_bytes,
        get_formats=lambda s: s.bytes_formats,
        make_spec=lambda cls, fmt: cls(bytes_format=fmt),
    )
    trailing_comma = nv(
        category="trailing_comma",
        get_default=lambda s: s.trailing_comma,
        get_formats=lambda s: s.trailing_commas,
        make_spec=lambda cls, fmt: cls(trailing_comma=fmt),
    )
    line_ending = nv(
        category="line_ending",
        get_default=lambda s: s.line_ending,
        get_formats=lambda s: s.line_endings,
        make_spec=lambda cls, fmt: cls(line_ending=fmt),
    )

    type_hints_cross = _build_type_hints_cross_variants()
    string_format_date_cross = _build_string_format_cross_variants(
        other_kwarg="date_format",
        other_tag="date",
        get_other_default=lambda s: s.date_format,
        get_other_formats=lambda s: s.date_formats,
    )
    string_format_datetime_cross = _build_string_format_cross_variants(
        other_kwarg="datetime_format",
        other_tag="dt",
        get_other_default=lambda s: s.datetime_format,
        get_other_formats=lambda s: s.datetime_formats,
    )

    cases: list[_VariantCase] = []
    variant_sources: list[tuple[Iterable[_Variant], str, str]] = [
        (date, "scalar_date", ""),
        (date, "date_list", ""),
        (date, "date_set", ""),
        (datetime_, "scalar_datetime", ""),
        (datetime_, "scalar_datetime_naive", "_naive"),
        (datetime_, "scalar_datetime_non_utc", "_non_utc"),
        (sequence, "simple_sequence", ""),
        (sequence, "pair_sequence", "_pair"),
        (sequence, "triple_sequence", "_triple"),
        (sequence, "simple_sequence", "_varname"),
        (set_, "set", ""),
        (_build_default_set_element_type_variants(), "empty_set", ""),
        (_build_default_set_element_type_variants(), "set", ""),
        (
            _build_default_sequence_element_type_variants(),
            "empty_sequence",
            "",
        ),
        (
            _build_default_sequence_element_type_variants(),
            "simple_sequence",
            "",
        ),
        (_build_default_dict_value_type_variants(), "empty_dict", ""),
        (_build_default_dict_value_type_variants(), "simple_dict", ""),
        (_build_default_dict_key_type_variants(), "empty_dict", ""),
        (_build_default_dict_key_type_variants(), "simple_dict", ""),
        (
            _build_default_ordered_map_value_type_variants(),
            "ordered_map",
            "",
        ),
        (comment, "comments", ""),
        (type_hints, "type_hints", ""),
        (type_hints, "scalar_date", ""),
        (type_hints, "scalar_datetime", ""),
        (type_hints, "binary", ""),
        (type_hints, "mixed_type_dicts_in_sequence", ""),
        (type_hints, "empty_dicts_in_sequence", ""),
        (type_hints, "float_list", ""),
        (type_hints, "int_list", ""),
        (type_hints, "empty_list", ""),
        (type_hints, "int_set", ""),
        (type_hints, "empty_set", ""),
        (type_hints, "mixed_number_list", ""),
        (type_hints, "nested_sequence", ""),
        (type_hints, "dict_with_list_value", ""),
        (type_hints, "ordered_map_in_sequence", ""),
        (type_hints_cross, "int_list", ""),
        (type_hints_cross, "int_list_large", ""),
        (type_hints_cross, "pair_sequence", ""),
        (type_hints_cross, "empty_list", ""),
        (type_hints_cross, "scalar_date", ""),
        (type_hints_cross, "scalar_datetime", ""),
        (type_hints_cross, "simple_dict", ""),
        (type_hints_cross, "int_set", ""),
        (declaration_style, "simple_sequence", ""),
        (declaration_style, "simple_dict", ""),
        (declaration_style, "empty_list", ""),
        (declaration_style, "scalar_int", ""),
        (declaration_style, "scalar_int_large", ""),
        (declaration_style, "scalar_float", ""),
        (declaration_style, "scalar_bool", ""),
        (declaration_style, "scalar_string", ""),
        (declaration_style, "scalar_null", ""),
        (declaration_style, "scalar_date", ""),
        (declaration_style, "scalar_datetime", ""),
        (declaration_style, "binary", ""),
        (dict_format, "simple_dict", ""),
        (dict_format, "dict_with_list_value", "_list_val"),
        (dict_entry_style, "simple_dict", ""),
        (
            dict_entry_style,
            "dict_with_list_value",
            "_list_val",
        ),
        (sequence, "float_list", "_float"),
        (float_format, "float_list", ""),
        (float_format, "float_scientific_notation", "_s"),
        (float_format, "float_special_values", "_v"),
        (float_format, "nested_float_list", "_n"),
        (integer_format, "int_list", ""),
        (integer_format, "int_list_large", "_large"),
        (integer_format, "int_list_with_zero", "_zero"),
        (numeric_literal_suffix, "int_list", ""),
        (numeric_literal_suffix, "int_list_large", "_large"),
        (
            numeric_literal_suffix,
            "int_list_with_zero",
            "_zero",
        ),
        (numeric_separator, "int_list", ""),
        (numeric_separator, "int_list_large", "_large"),
        (numeric_separator, "int_list_with_zero", "_zero"),
        (string_format, "string_list", ""),
        (string_format, "string_with_backslash", ""),
        (string_format, "simple_dict", "_dict"),
        (string_format, "binary", "_binary"),
        (string_format_date_cross, "scalar_date", ""),
        (string_format_datetime_cross, "scalar_datetime", "_dt"),
        (bytes_format, "binary", ""),
        (trailing_comma, "simple_sequence", ""),
        (line_ending, "simple_sequence", ""),
        (line_ending, "simple_dict", "_dict"),
        (_build_line_ending_decl_variants(), "simple_sequence", ""),
        (_build_sequence_decl_variants(), "int_list", ""),
        (_build_type_name_variants(), "simple_dict", ""),
        (_build_constructor_prefix_variants(), "simple_dict", ""),
        (_build_constructor_prefix_variants(), "float_special_values", "_v"),
        (_build_constructor_prefix_variants(), "float_list", "_float"),
        (_build_constructor_prefix_variants(), "binary", "_binary"),
        (_build_constructor_prefix_variants(), "scalar_date", "_date"),
        (_build_constructor_prefix_variants(), "scalar_datetime", "_datetime"),
        (numeric_style, "int_list", ""),
        (numeric_style, "int_list_with_zero", "_zero"),
        (numeric_style, "float_list", ""),
        (numeric_style, "float_special_values", ""),
        (numeric_style, "mixed_number_list", ""),
        (numeric_style, "scalars", ""),
        (_build_c_field_name_variants(), "simple_dict", ""),
        (_build_c_field_name_variants(), "simple_sequence", ""),
        (_build_constructor_name_variants(), "simple_dict", ""),
        (type_hints_cross, "bool_list", ""),
        (type_hints_cross, "float_list", ""),
    ]
    for variants, case_dir_name, suffix in variant_sources:
        cases.extend(
            _VariantCase(
                variant_name=f"{variant.name}{suffix}",
                variant=variant,
                case_dir_name=case_dir_name,
                variable_form=_wrap_variable_form(lang_cls=variant.lang_cls),
            )
            for variant in variants
        )
    cases.extend(_build_modifier_variant_cases())
    return cases


@functools.cache
def _group_variant_cases_by_language() -> dict[
    literalizer.LanguageCls,
    list[_VariantCase],
]:
    """Return variant cases grouped by language class.

    The test takes the language as its only pytest axis and iterates
    that language's cases inside the test body with ``subtests``.
    Folding ~2000 cases into ~30 cuts collection and per-test overhead
    on slower CI runners (notably Windows).
    """
    groups: dict[literalizer.LanguageCls, list[_VariantCase]] = {}
    for case in _build_variant_cases():
        groups.setdefault(case.variant.lang_cls, []).append(case)
    return groups


@functools.cache
def _variant_languages() -> list[literalizer.LanguageCls]:
    """Return languages that have at least one format-variant case."""
    groups = _group_variant_cases_by_language()
    return [cls for cls in _sorted_languages() if cls in groups]


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=_variant_languages(),
    ids=_lang_cls_name,
)
def test_format_variant_golden_file(
    lang_cls: literalizer.LanguageCls,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Test format-variant options (dates, sequences, sets, type hints)
    against golden files.
    """
    for variant_case in _group_variant_cases_by_language()[lang_cls]:
        with subtests.test(
            variant_name=variant_case.variant_name,
            case_dir_name=variant_case.case_dir_name,
        ):
            case_dir = cases_dir / variant_case.case_dir_name
            variant = variant_case.variant
            yaml_string = (case_dir / "input.yaml").read_text()
            golden_path = case_dir / (
                variant_case.variant_name + variant.spec.extension
            )
            try:
                result = literalizer.literalize(
                    source=yaml_string,
                    input_format=literalizer.InputFormat.YAML,
                    language=variant.spec,
                    pre_indent_level=0,
                    include_delimiters=True,
                    variable_form=variant_case.variable_form,
                    wrap_in_file=True,
                )
            except NullInCollectionError:
                pytest.skip("Format rejects null elements in this input")
            except HeterogeneousCollectionError:
                golden_path.unlink(missing_ok=True)
                pytest.skip("Format cannot represent this heterogeneous input")
            except IncompatibleFormatsError:
                golden_path.unlink(missing_ok=True)
                pytest.skip("Format combination cannot represent this input")
            _check_golden(
                file_regression=file_regression,
                contents=result.code + "\n",
                extension=variant.spec.extension,
                newline=None,
                golden_path=golden_path,
            )


@dataclasses.dataclass
class _LineEndingCombinedCase:
    """A combined-variable-forms test case with a non-default line
    ending.
    """

    name: str
    lang_cls: literalizer.LanguageCls
    line_ending: enum.Enum
    case_dir_name: str


@functools.cache
@beartype
def _build_line_ending_combined_cases() -> list[_LineEndingCombinedCase]:
    """Collect combined (declaration + assignment) test cases for
    non-default line endings.
    """
    cases: list[_LineEndingCombinedCase] = []
    for lang_cls in _sorted_languages():
        lang_name = lang_cls.__name__
        spec = _spec(lang_cls=lang_cls)
        if not _find_redefinition_styles(spec=spec):
            continue
        default_line_ending = spec.line_ending
        for line_ending in spec.line_endings:
            if line_ending is default_line_ending:
                continue
            for case_dir_name in ("simple_sequence", "simple_dict"):
                name = (
                    f"{lang_name}_line_ending"
                    f"_{line_ending.name.lower()}_{case_dir_name}"
                )
                cases.append(
                    _LineEndingCombinedCase(
                        name=name,
                        lang_cls=lang_cls,
                        line_ending=line_ending,
                        case_dir_name=case_dir_name,
                    )
                )
    return cases


@pytest.mark.parametrize(
    argnames="case",
    argvalues=_build_line_ending_combined_cases(),
    ids=[c.name for c in _build_line_ending_combined_cases()],
)
def test_line_ending_combined_variable_forms(
    case: _LineEndingCombinedCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that combined (declaration + assignment) output with a
    non-default line ending matches the golden file.
    """
    input_path = cases_dir / case.case_dir_name / "input.yaml"
    yaml_string = input_path.read_text()
    base_spec = _spec(lang_cls=case.lang_cls)
    redef_styles = _find_redefinition_styles(spec=base_spec)
    assert redef_styles
    spec = _spec(
        lang_cls=case.lang_cls,
        line_ending=case.line_ending,
        declaration_style=redef_styles[0],
    )
    result = literalizer.literalize(
        source=yaml_string,
        input_format=literalizer.InputFormat.YAML,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=literalizer.BothVariableForms(name="my_data"),
        wrap_in_file=True,
    )
    _check_golden(
        file_regression=file_regression,
        contents=result.code + "\n",
        extension=spec.extension,
        newline=None,
        golden_path=input_path.parent / (case.name + spec.extension),
    )


def test_no_dead_golden_files(request: pytest.FixtureRequest) -> None:
    """Every file under ``cases/`` must be referenced by a parameterized
    test.  Orphaned golden files silently rot and waste repository space.
    """
    cases_dir = request.config.rootpath / "tests" / "integration" / "cases"
    expected: set[Path] = set()

    for case_dir in sorted(cases_dir.iterdir()):
        expected.add(case_dir / "input.yaml")

    for case_name, lang_cls in _discover_cases():
        ext = lang_cls.extension
        expected.add(cases_dir / case_name / (lang_cls.__name__ + ext))

    for combined_case in _discover_combined_cases():
        ext = combined_case.lang_cls.extension
        expected.add(
            cases_dir
            / combined_case.case_name
            / (combined_case.golden_file_name + ext)
        )

    for variant_case in _build_variant_cases():
        ext = variant_case.variant.spec.extension
        expected.add(
            cases_dir
            / variant_case.case_dir_name
            / (variant_case.variant_name + ext)
        )

    for line_ending_case in _build_line_ending_combined_cases():
        line_ending_spec = _spec(
            lang_cls=line_ending_case.lang_cls,
            line_ending=line_ending_case.line_ending,
        )
        expected.add(
            cases_dir
            / line_ending_case.case_dir_name
            / (line_ending_case.name + line_ending_spec.extension)
        )

    for call_case in _discover_call_cases():
        ext = call_case.lang_cls.extension
        golden_name = f"{call_case.lang_cls.__name__}_call"
        expected.add(
            cases_dir / call_case.config.case_dir_name / (golden_name + ext)
        )

    actual = {path for path in cases_dir.rglob(pattern="*") if path.is_file()}
    dead_files = sorted(
        os.path.relpath(path=path, start=cases_dir)
        for path in actual - expected
    )
    assert not dead_files


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_sorted_languages(),
    ids=[c.__name__ for c in _sorted_languages()],
)
def test_format_enumeration_properties(
    language_cls: literalizer.LanguageCls,
) -> None:
    """Every language exposes iterable format-enumeration properties."""
    spec = language_cls()
    assert issubclass(spec.bytes_formats, enum.Enum)
    assert len(spec.bytes_formats) >= 1
    assert issubclass(spec.sequence_formats, enum.Enum)
    assert len(spec.sequence_formats) >= 1
    assert issubclass(spec.set_formats, enum.Enum)
    assert len(spec.set_formats) >= 1
    assert issubclass(spec.date_formats, enum.Enum)
    assert len(spec.date_formats) >= 1
    assert issubclass(spec.datetime_formats, enum.Enum)
    assert len(spec.datetime_formats) >= 1
    assert issubclass(spec.comment_formats, enum.Enum)
    assert len(spec.comment_formats) >= 1
    assert issubclass(spec.declaration_styles, enum.Enum)
    assert len(spec.declaration_styles) >= 1
    assert issubclass(spec.dict_formats, enum.Enum)
    assert len(spec.dict_formats) >= 1
    assert issubclass(spec.float_formats, enum.Enum)
    assert len(spec.float_formats) >= 1
    assert issubclass(spec.integer_formats, enum.Enum)
    assert len(spec.integer_formats) >= 1
    assert issubclass(spec.numeric_separators, enum.Enum)
    assert len(spec.numeric_separators) >= 1
    assert issubclass(spec.numeric_styles, enum.Enum)
    assert len(spec.numeric_styles) >= 1
    assert issubclass(spec.string_formats, enum.Enum)
    assert len(spec.string_formats) >= 1
    assert issubclass(spec.trailing_commas, enum.Enum)
    assert len(spec.trailing_commas) >= 1
    assert issubclass(spec.line_endings, enum.Enum)
    assert len(spec.line_endings) >= 1
    assert issubclass(spec.call_styles, enum.Enum)


# --- literalize_call golden-file tests ---


@dataclasses.dataclass
class _CallCase:
    """A parameterized call-style golden-file test case."""

    config: _CallCaseConfig
    lang_cls: literalizer.LanguageCls


@functools.cache
@beartype
def _discover_call_cases() -> list[_CallCase]:
    """Return call test cases for all languages."""
    cases: list[_CallCase] = []
    for config in _CALL_CASE_CONFIGS:
        for lang_cls in _sorted_languages():
            if len(lang_cls.CallStyles) == 0:
                continue
            has_dotted_target = "." in config.target_function
            if has_dotted_target and not lang_cls.supports_dotted_calls:
                continue
            if config.call_style_type is not None:
                # Only include languages that have this as a
                # non-default style.
                styles = list(lang_cls.CallStyles)
                matching = [
                    s
                    for s in styles
                    if isinstance(s.value, config.call_style_type)
                ]
                if not matching:
                    continue
                default_style = styles[0]
                if isinstance(default_style.value, config.call_style_type):
                    continue
            cases.append(_CallCase(config=config, lang_cls=lang_cls))
    return cases


@pytest.mark.parametrize(
    argnames="call_case",
    argvalues=_discover_call_cases(),
    ids=[
        f"{c.config.case_dir_name}/{c.lang_cls.__name__}"
        for c in _discover_call_cases()
    ],
)
def test_call_golden_file(
    call_case: _CallCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_call output matches expected golden file."""
    config = call_case.config
    lang_cls = call_case.lang_cls
    kwargs: dict[str, object] = {}
    if config.call_style_type is not None:
        style = next(
            s
            for s in lang_cls.CallStyles
            if isinstance(s.value, config.call_style_type)
        )
        kwargs["call_style"] = style
    spec = _spec(lang_cls=lang_cls, **kwargs)
    input_path = cases_dir / config.case_dir_name / "input.yaml"
    yaml_string = input_path.read_text()
    result = literalizer.literalize_call(
        source=yaml_string,
        input_format=literalizer.InputFormat.YAML,
        language=spec,
        target_function=config.target_function,
        parameter_names=config.parameter_names,
        call_transform=config.call_transform,
        per_element=config.per_element,
    )
    # Build stub declarations for undefined names.
    body_stubs: list[str] = []
    preamble_stubs: list[str] = []
    stub_return = (
        StubReturn.VALUE
        if config.call_transform is not None
        else StubReturn.VOID
    )
    # Stubs for the call function (with full parameter names).
    body_stubs.extend(
        spec.format_call_stub(
            config.target_function,
            config.parameter_names,
            stub_return,
        ),
    )
    preamble_stubs.extend(
        spec.format_call_preamble_stub(
            config.target_function,
            config.parameter_names,
            stub_return,
        ),
    )
    # Stubs for transform function names (single argument).
    for wrapper_name in config.transform_stub_names:
        body_stubs.extend(
            spec.format_call_stub(
                wrapper_name,
                ["_arg"],
                StubReturn.VOID,
            ),
        )
        preamble_stubs.extend(
            spec.format_call_preamble_stub(
                wrapper_name,
                ["_arg"],
                StubReturn.VOID,
            ),
        )
    call_body_preamble = result.body_preamble + tuple(body_stubs)

    wrapped = spec.wrap_in_file(
        content=result.bare_code,
        variable_name="",
        body_preamble=call_body_preamble,
    )
    all_preamble = result.preamble + tuple(preamble_stubs)
    wrapped = _prepend_preamble(wrapped=wrapped, preamble=all_preamble)
    lang_name = lang_cls.__name__
    golden_name = f"{lang_name}_call"
    _check_golden(
        file_regression=file_regression,
        contents=wrapped + "\n",
        extension=lang_cls.extension,
        newline="",
        golden_path=input_path.parent / (golden_name + lang_cls.extension),
    )
