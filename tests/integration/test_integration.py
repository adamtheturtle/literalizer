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
from collections.abc import Callable, Iterable
from pathlib import Path

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture
from ruamel.yaml import YAML

import literalizer
from literalizer._language import StubReturn
from literalizer.exceptions import NullInCollectionError
from literalizer.languages import (
    ALL_LANGUAGES,
    C,
    Elm,
    Fortran,
    FSharp,
    Gleam,
    Haskell,
    OCaml,
    PureScript,
)


@pytest.fixture(name="cases_dir")
def fixture_cases_dir(request: pytest.FixtureRequest) -> Path:
    """Return the absolute path to the integration test cases
    directory.
    """
    return request.config.rootpath / "tests" / "integration" / "cases"


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


_SORTED_LANGUAGES: list[literalizer.LanguageCls] = sorted(
    ALL_LANGUAGES,
    key=_lang_cls_name,
)


_LAX_COERCE_KWARGS_BY_LANG: dict[str, dict[str, bool]] = {
    "Rust": {
        "coerce_heterogeneous_scalars": True,
        "coerce_heterogeneous_sibling_lists": True,
        "coerce_mixed_dict_values": True,
        "coerce_mixed_list_values": True,
    },
    "Cpp": {
        "coerce_heterogeneous_scalars": True,
        "coerce_heterogeneous_sibling_lists": True,
        "coerce_mixed_dict_values": True,
        "coerce_mixed_list_values": True,
    },
    "Nim": {
        "coerce_heterogeneous_scalars": True,
        "coerce_heterogeneous_sibling_lists": True,
        "coerce_mixed_dict_values": True,
        "coerce_mixed_list_values": True,
    },
    "Mojo": {
        "coerce_heterogeneous_scalars": True,
        "coerce_heterogeneous_sibling_lists": True,
        "coerce_mixed_dict_values": True,
        "coerce_mixed_list_values": True,
    },
    "Dhall": {
        "coerce_heterogeneous_scalars": True,
        "coerce_heterogeneous_sibling_lists": True,
        "coerce_mixed_dict_values": True,
        "coerce_mixed_list_values": True,
        "coerce_nonuniform_record_shapes": True,
    },
}
"""Per-language opt-in coerce flags used to recover the pre-strict
silent-coercion behavior in golden-file tests, which exercise
formatting (not coercion semantics).
"""


def _lax_kwargs(*, lang_cls: literalizer.LanguageCls) -> dict[str, bool]:
    """Return ``coerce_*`` kwargs that allow every coercion for
    *lang_cls*, or an empty dict for languages whose formats always
    support heterogeneity.
    """
    return _LAX_COERCE_KWARGS_BY_LANG.get(lang_cls.__name__, {})


@functools.cache
def _default_spec(
    *,
    lang_cls: literalizer.LanguageCls,
) -> literalizer.Language:
    """Return a cached lax-constructed instance of *lang_cls*.

    Each ``lang_cls()`` call rebuilds ``@beartype``-wrapped closures
    inside the formatter factories; sharing one lax-constructed
    instance per class cuts thousands of redundant builds during test
    collection.

    Languages that gate coercions per-flag are constructed with every
    ``coerce_*`` flag enabled so that golden-file tests, which test
    formatting rather than coercion semantics, can pass heterogeneous
    data through silently.
    """
    return lang_cls(**_lax_kwargs(lang_cls=lang_cls))


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
        [literalizer.LanguageCls, enum.Enum, dict[str, bool]],
        literalizer.Language,
    ],
) -> list[_Variant]:
    """Build variants for every non-default value of a format enum.

    This is the generic version of the many per-format builder functions
    that all follow the same pattern: iterate all languages, find the
    non-default members of a format enum, and create a ``_Variant`` for
    each one.

    *make_spec* is called with the per-language ``coerce_*`` opt-in
    kwargs that recover pre-strict silent-coercion behavior, since these
    variant tests exercise formatting rather than coercion semantics.
    """
    variants: list[_Variant] = []
    for lang_cls in _SORTED_LANGUAGES:
        lang_name = lang_cls.__name__
        spec = _default_spec(lang_cls=lang_cls)
        default_format = get_default(spec)
        lax = _lax_kwargs(lang_cls=lang_cls)
        for fmt in get_formats(spec):
            if fmt is default_format:
                continue
            variants.append(
                _Variant(
                    name=f"{lang_name}_{category}_{fmt.name.lower()}",
                    spec=make_spec(lang_cls, fmt, lax),
                    lang_cls=lang_cls,
                )
            )
    return variants


@beartype
def _build_default_set_element_type_variants(
    *,
    should_coerce_mixed: bool = False,
) -> Iterable[_Variant]:
    """Build default-set-type variants for languages that support it.

    For each language that advertises ``supports_default_set_element_type``,
    create a variant with a non-default value.

    When *should_coerce_mixed* is ``True``, only include languages whose
    set format has ``coerce_mixed_to_str`` enabled, since overriding
    ``default_set_element_type`` to a typed key produces invalid code
    for mixed sets when elements are not coerced.
    """
    # The test value must differ from the language's own default *and* be
    # a valid type name for that language's linter / compiler.
    type_overrides: dict[str, str] = {
        "Crystal": "Int32",
        "Go": "string",
        "CSharp": "string",
        "Mojo": "Int",
        "Odin": "int",
        "Python": "int",
        "Rust": "i32",
    }
    variants: list[_Variant] = []
    for lang_cls in _SORTED_LANGUAGES:
        lang_name = lang_cls.__name__
        if not lang_cls.supports_default_set_element_type:
            continue
        string_type = type_overrides.get(lang_name, "String")
        spec = lang_cls(
            default_set_element_type=string_type,
            **_lax_kwargs(lang_cls=lang_cls),
        )
        if (
            should_coerce_mixed
            and not spec.set_format_config.coerce_mixed_to_str
        ):
            continue
        variants.append(
            _Variant(
                name=f"{lang_name}_default_set_element_type_string",
                spec=spec,
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def _build_default_sequence_element_type_variants() -> Iterable[_Variant]:
    """Build default-sequence-type variants for languages that support it.

    For each language that advertises
    ``supports_default_sequence_element_type``, create a variant with a
    non-default value.
    """
    type_overrides: dict[str, str] = {
        "Go": "interface{}",
        "CSharp": "string",
        "Mojo": "Int",
        "Python": "int",
    }
    variants: list[_Variant] = []
    for lang_cls in _SORTED_LANGUAGES:
        lang_name = lang_cls.__name__
        if not lang_cls.supports_default_sequence_element_type:
            continue
        string_type = type_overrides.get(lang_name, "String")
        variants.append(
            _Variant(
                name=f"{lang_name}_default_sequence_element_type_string",
                spec=lang_cls(
                    default_sequence_element_type=string_type,
                    **_lax_kwargs(lang_cls=lang_cls),
                ),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def _build_default_dict_value_type_variants() -> Iterable[_Variant]:
    """Build default-dict-type variants for languages that support it.

    For each language that advertises ``supports_default_dict_value_type``,
    create a variant with a non-default value.
    """
    type_overrides: dict[str, str] = {
        "Crystal": "Int32",
        "Go": "interface{}",
        "CSharp": "object?",
        "Dart": "Object?",
        "Kotlin": "Comparable<*>?",
        "Mojo": "Int",
        "Python": "int",
        "Rust": "i32",
    }
    variants: list[_Variant] = []
    for lang_cls in _SORTED_LANGUAGES:
        lang_name = lang_cls.__name__
        if not lang_cls.supports_default_dict_value_type:
            continue
        string_type = type_overrides.get(lang_name, "String")
        variants.append(
            _Variant(
                name=f"{lang_name}_default_dict_value_type_string",
                spec=lang_cls(
                    default_dict_value_type=string_type,
                    **_lax_kwargs(lang_cls=lang_cls),
                ),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def _build_default_dict_key_type_variants() -> Iterable[_Variant]:
    """Build default-dict-key-type variants for languages that support it.

    For each language that advertises ``supports_default_dict_key_type``,
    create a variant with a non-default key type.
    """
    type_overrides: dict[str, str] = {
        "Crystal": "Int32",
        "Go": "any",
        "CSharp": "object",
        "Dart": "Object",
        "Kotlin": "Any",
        "Python": "int",
        "Rust": "&str",
        "Swift": "AnyHashable",
        "VisualBasic": "Object",
    }
    variants: list[_Variant] = []
    for lang_cls in _SORTED_LANGUAGES:
        lang_name = lang_cls.__name__
        if not lang_cls.supports_default_dict_key_type:
            continue
        key_type = type_overrides.get(lang_name, "String")
        variants.append(
            _Variant(
                name=f"{lang_name}_default_dict_key_type",
                spec=lang_cls(
                    default_dict_key_type=key_type,
                    **_lax_kwargs(lang_cls=lang_cls),
                ),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def _build_default_ordered_map_value_type_variants() -> Iterable[_Variant]:
    """Build default-ordered-map-value-type variants for languages that
    support it.

    For each language that advertises
    ``supports_default_ordered_map_value_type``, create a variant with a
    non-default value type.
    """
    type_overrides: dict[str, str] = {
        "Go": "interface{}",
    }
    variants: list[_Variant] = []
    for lang_cls in _SORTED_LANGUAGES:
        lang_name = lang_cls.__name__
        if not lang_cls.supports_default_ordered_map_value_type:
            continue
        value_type = type_overrides.get(lang_name, "String")
        variants.append(
            _Variant(
                name=f"{lang_name}_default_ordered_map_value_type",
                spec=lang_cls(
                    default_ordered_map_value_type=value_type,
                    **_lax_kwargs(lang_cls=lang_cls),
                ),
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
    for lang_cls in _SORTED_LANGUAGES:
        lang_name = lang_cls.__name__
        spec = _default_spec(lang_cls=lang_cls)
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
                    **_lax_kwargs(lang_cls=lang_cls),
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
    for lang_cls in _SORTED_LANGUAGES:
        lang_name = lang_cls.__name__
        spec = _default_spec(lang_cls=lang_cls)
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
                    **_lax_kwargs(lang_cls=lang_cls),
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
    call_style_kind: literalizer.CallStyleKind | None = None
    language_overrides: dict[str, object] = dataclasses.field(
        default_factory=dict[str, object],
    )
    language_filter: Callable[[literalizer.LanguageCls], bool] | None = None


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
        case_dir_name="call_dotted_method_record_selectors",
        target_function="app.client.fetch",
        parameter_names=["payload"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        language_overrides={
            "dot_access_style": (Haskell.DotAccessStyles.RECORD_SELECTORS),
        },
        language_filter=lambda cls: hasattr(cls, "DotAccessStyles"),
    ),
    _CallCaseConfig(
        case_dir_name="call_deep_dotted_record_selectors",
        target_function="obj.api.client.post",
        parameter_names=["data"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        language_overrides={
            "dot_access_style": (Haskell.DotAccessStyles.RECORD_SELECTORS),
        },
        language_filter=lambda cls: hasattr(cls, "DotAccessStyles"),
    ),
    _CallCaseConfig(
        case_dir_name="call_scalar_record_selectors",
        target_function="process",
        parameter_names=["value"],
        call_transform=None,
        transform_stub_names=[],
        per_element=True,
        language_overrides={
            "dot_access_style": (Haskell.DotAccessStyles.RECORD_SELECTORS),
        },
        language_filter=lambda cls: hasattr(cls, "DotAccessStyles"),
    ),
    *[
        _CallCaseConfig(
            case_dir_name=f"call_{kind.value}",
            target_function="throttler.check",
            parameter_names=["user_id", "ts"],
            call_transform=lambda c: f"emit({c})",
            transform_stub_names=["emit"],
            per_element=True,
            call_style_kind=kind,
        )
        for kind in literalizer.CallStyleKind
    ],
]

_CALL_CASE_DIRS = frozenset(cfg.case_dir_name for cfg in _CALL_CASE_CONFIGS)


_CASES_DIR = Path(__file__).parent / "cases"
_NON_TRIVIAL_KEY_CASES = _cases_with_non_trivial_dict_keys(
    cases_dir=_CASES_DIR,
)


@beartype
def _discover_cases() -> list[tuple[str, literalizer.LanguageCls]]:
    """Return ``(case_name, lang_cls)`` tuples."""
    cases: list[tuple[str, literalizer.LanguageCls]] = []
    for case_dir in sorted(_CASES_DIR.iterdir()):
        if case_dir.name in _CALL_CASE_DIRS:
            continue
        non_trivial = case_dir.name in _NON_TRIVIAL_KEY_CASES
        for lang_cls in _SORTED_LANGUAGES:
            if (
                non_trivial
                and not lang_cls.supports_non_printable_ascii_dict_keys
            ):
                continue
            cases.append((case_dir.name, lang_cls))
    return cases


_CASES = _discover_cases()


@pytest.mark.parametrize(
    argnames=("_case_name", "lang_cls"),
    argvalues=_CASES,
    ids=[f"{c[0]}/{c[1].__name__}" for c in _CASES],
)
def test_golden_file(
    _case_name: str,
    lang_cls: literalizer.LanguageCls,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_yaml output matches expected golden file."""
    input_path = cases_dir / _case_name / "input.yaml"
    lang_name = lang_cls.__name__
    yaml_string = input_path.read_text()
    result = literalizer.literalize(
        source=yaml_string,
        input_format=literalizer.InputFormat.YAML,
        language=lang_cls(**_lax_kwargs(lang_cls=lang_cls)),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=_wrap_variable_form(lang_cls=lang_cls),
        wrap_in_file=True,
    )
    # newline="" prevents Python text-mode from converting \r\n to \n
    # on Windows, which would corrupt golden files containing literal
    # CR bytes (e.g. CommonLisp string_control_chars).
    file_regression.check(
        contents=result.code + "\n",
        extension=lang_cls.extension,
        newline="",
        fullpath=input_path.parent / (lang_name + lang_cls.extension),
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


@beartype
def _discover_combined_cases() -> list[_CombinedCase]:
    """Return combined test cases for all redefinition-supporting
    styles.
    """
    cases: list[_CombinedCase] = []
    for case_dir in sorted(_CASES_DIR.iterdir()):
        if case_dir.name in _CALL_CASE_DIRS:
            continue
        non_trivial = case_dir.name in _NON_TRIVIAL_KEY_CASES
        for lang_cls in _SORTED_LANGUAGES:
            lang_name = lang_cls.__name__
            if (
                non_trivial
                and not lang_cls.supports_non_printable_ascii_dict_keys
            ):
                continue
            spec = _default_spec(lang_cls=lang_cls)
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


_COMBINED_CASES = _discover_combined_cases()


@pytest.mark.parametrize(
    argnames="combined_case",
    argvalues=_COMBINED_CASES,
    ids=[f"{c.case_name}/{c.golden_file_name}" for c in _COMBINED_CASES],
)
def test_golden_file_combined_variable_forms(
    combined_case: _CombinedCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize with BothVariableForms produces expected
    golden output combining declaration and assignment in one file.
    """
    input_path = cases_dir / combined_case.case_name / "input.yaml"
    lang_cls = combined_case.lang_cls
    spec = lang_cls(
        declaration_style=combined_case.declaration_style,
        **_lax_kwargs(lang_cls=lang_cls),
    )
    yaml_string = input_path.read_text()
    result = literalizer.literalize(
        source=yaml_string,
        input_format=literalizer.InputFormat.YAML,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=literalizer.BothVariableForms(name="my_data"),
        wrap_in_file=True,
    )
    file_regression.check(
        contents=result.code + "\n",
        extension=lang_cls.extension,
        newline="",
        fullpath=input_path.parent
        / (combined_case.golden_file_name + lang_cls.extension),
    )


@beartype
def _build_constructor_name_variants() -> Iterable[_Variant]:
    """Build constructor-name variants for Fortran.

    Fortran emits constructor function calls (e.g. ``fnull``) in its
    output.  The constructor name parameters let users customize those
    names.
    """
    lang_cls = Fortran
    return [
        _Variant(
            name="Fortran_constructor_names_j",
            spec=lang_cls(
                null_name="jnull",
                bool_name="jbool",
                int_name="jint",
                real_name="jreal",
                str_name="jstr",
                list_name="jlist",
                map_name="jmap",
                set_name="jset",
                entry_name="jentry",
            ),
            lang_cls=lang_cls,
        ),
    ]


@beartype
def _build_type_name_variants() -> Iterable[_Variant]:
    """Build type-name variants for languages that generate a named type.

    These languages emit a custom algebraic data type in their body
    preamble (e.g. ``data Val = …`` in Haskell).  The ``type_name``
    constructor parameter lets users customize that name.
    """
    custom_names: dict[literalizer.LanguageCls, str] = {
        Elm: "JsonVal",
        FSharp: "JsonVal",
        Gleam: "JsonVal",
        Haskell: "JsonVal",
        OCaml: "json_t",
        PureScript: "JsonVal",
    }
    variants: list[_Variant] = []
    for lang_cls, custom_name in custom_names.items():
        lang_name = lang_cls.__name__
        variants.append(
            _Variant(
                name=f"{lang_name}_type_name_{custom_name}",
                spec=lang_cls(type_name=custom_name),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def _build_constructor_prefix_variants() -> Iterable[_Variant]:
    """Build constructor-prefix variants for languages with custom ADTs.

    These languages use a single-letter prefix for constructors
    (e.g. ``ENull``, ``HBool``).  The ``constructor_prefix`` parameter
    lets users customize that prefix.
    """
    custom_prefixes: dict[literalizer.LanguageCls, str] = {
        Elm: "J",
        FSharp: "J",
        Gleam: "J",
        Haskell: "J",
        OCaml: "J",
        PureScript: "J",
    }
    variants: list[_Variant] = []
    for lang_cls, custom_prefix in custom_prefixes.items():
        lang_name = lang_cls.__name__
        variants.append(
            _Variant(
                name=f"{lang_name}_prefix_{custom_prefix}",
                spec=lang_cls(
                    constructor_prefix=custom_prefix,
                ),
                lang_cls=lang_cls,
            )
        )
    return variants


@beartype
def _build_c_field_name_variants() -> Iterable[_Variant]:
    """Build field-name variants for the C language.

    The C generator uses single-letter union field names by default.
    The field name parameters let users customize those names.
    """
    lang_cls = C
    return [
        _Variant(
            name="C_field_names_custom",
            spec=lang_cls(
                bool_field="bl",
                int_field="integer",
                float_field="fp",
                string_field="str",
                array_field="arr",
                map_field="dict",
                key_field="key",
                value_field="val",
            ),
            lang_cls=lang_cls,
        ),
    ]


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
    for lang_cls in _SORTED_LANGUAGES:
        spec = _default_spec(lang_cls=lang_cls)
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
                                **_lax_kwargs(lang_cls=lang_cls),
                            ),
                            lang_cls=lang_cls,
                        ),
                    )
    return variants


def _build_variant_cases() -> list[_VariantCase]:
    """Collect all format-variant golden-file test cases."""
    nv = _build_non_default_variants
    date = nv(
        category="date",
        get_default=lambda s: s.format_date,
        get_formats=lambda s: s.date_formats,
        make_spec=lambda cls, fmt, lax: cls(date_format=fmt, **lax),
    )
    datetime_ = nv(
        category="datetime",
        get_default=lambda s: s.format_datetime,
        get_formats=lambda s: s.datetime_formats,
        make_spec=lambda cls, fmt, lax: cls(datetime_format=fmt, **lax),
    )
    sequence = nv(
        category="sequence",
        get_default=lambda s: s.sequence_format,
        get_formats=lambda s: s.sequence_formats,
        make_spec=lambda cls, fmt, lax: cls(sequence_format=fmt, **lax),
    )
    set_ = nv(
        category="set",
        get_default=lambda s: s.set_format,
        get_formats=lambda s: s.set_formats,
        make_spec=lambda cls, fmt, lax: cls(set_format=fmt, **lax),
    )
    comment = nv(
        category="comment",
        get_default=lambda s: s.comment_format,
        get_formats=lambda s: s.comment_formats,
        make_spec=lambda cls, fmt, lax: cls(comment_format=fmt, **lax),
    )
    type_hints = nv(
        category="type_hints",
        get_default=lambda s: s.variable_type_hints,
        get_formats=lambda s: s.variable_type_hints_formats,
        make_spec=lambda cls, fmt, lax: cls(variable_type_hints=fmt, **lax),
    )

    def _declaration_style_make_spec(
        cls: literalizer.LanguageCls,
        fmt: enum.Enum,
        lax: dict[str, bool],
    ) -> literalizer.Language:
        """Build spec, using ARRAY for Rust const/static styles.

        Rust CONST and STATIC raise ``IncompatibleFormatsError``
        with the default sequence format.  Use ARRAY so the golden
        files produce valid Rust that the compiler accepts.
        """
        result: literalizer.Language
        if cls.__name__ == "Rust" and fmt.name in {
            "CONST",
            "STATIC",
        }:
            spec = cls(**lax)
            array_fmt = next(
                f for f in spec.sequence_formats if f.name == "ARRAY"
            )
            result = cls(
                declaration_style=fmt,
                sequence_format=array_fmt,
                **lax,
            )
        else:
            result = cls(declaration_style=fmt, **lax)
        return result

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
        make_spec=lambda cls, fmt, lax: cls(dict_format=fmt, **lax),
    )
    dict_entry_style = nv(
        category="dict_entry_style",
        get_default=lambda s: s.dict_entry_style,
        get_formats=lambda s: s.dict_entry_styles,
        make_spec=lambda cls, fmt, lax: cls(dict_entry_style=fmt, **lax),
    )
    integer_format = nv(
        category="integer_format",
        get_default=lambda s: s.integer_format,
        get_formats=lambda s: s.integer_formats,
        make_spec=lambda cls, fmt, lax: cls(integer_format=fmt, **lax),
    )
    numeric_literal_suffix = nv(
        category="numeric_literal_suffix",
        get_default=lambda s: s.numeric_literal_suffix,
        get_formats=lambda s: s.numeric_literal_suffixes,
        make_spec=lambda cls, fmt, lax: cls(numeric_literal_suffix=fmt, **lax),
    )
    numeric_separator = nv(
        category="numeric_separator",
        get_default=lambda s: s.numeric_separator,
        get_formats=lambda s: s.numeric_separators,
        make_spec=lambda cls, fmt, lax: cls(numeric_separator=fmt, **lax),
    )
    float_format = nv(
        category="float_format",
        get_default=lambda s: s.float_format,
        get_formats=lambda s: s.float_formats,
        make_spec=lambda cls, fmt, lax: cls(float_format=fmt, **lax),
    )
    numeric_style = nv(
        category="numeric_style",
        get_default=lambda s: s.numeric_style,
        get_formats=lambda s: s.numeric_styles,
        make_spec=lambda cls, fmt, lax: cls(numeric_style=fmt, **lax),
    )
    string_format = nv(
        category="string_format",
        get_default=lambda s: s.string_format,
        get_formats=lambda s: s.string_formats,
        make_spec=lambda cls, fmt, lax: cls(string_format=fmt, **lax),
    )
    bytes_format = nv(
        category="bytes_format",
        get_default=lambda s: s.format_bytes,
        get_formats=lambda s: s.bytes_formats,
        make_spec=lambda cls, fmt, lax: cls(bytes_format=fmt, **lax),
    )
    trailing_comma = nv(
        category="trailing_comma",
        get_default=lambda s: s.trailing_comma,
        get_formats=lambda s: s.trailing_commas,
        make_spec=lambda cls, fmt, lax: cls(trailing_comma=fmt, **lax),
    )
    line_ending = nv(
        category="line_ending",
        get_default=lambda s: s.line_ending,
        get_formats=lambda s: s.line_endings,
        make_spec=lambda cls, fmt, lax: cls(line_ending=fmt, **lax),
    )

    type_hints_cross = _build_type_hints_cross_variants()

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
            _build_default_set_element_type_variants(
                should_coerce_mixed=True,
            ),
            "mixed_set",
            "",
        ),
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
        (declaration_style, "scalar_float", ""),
        (declaration_style, "scalar_bool", ""),
        (declaration_style, "scalar_string", ""),
        (declaration_style, "scalar_null", ""),
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
        (numeric_style, "int_list", ""),
        (numeric_style, "int_list_with_zero", "_zero"),
        (numeric_style, "float_list", ""),
        (numeric_style, "float_special_values", ""),
        (numeric_style, "mixed_number_list", ""),
        (numeric_style, "scalars", ""),
        (_build_c_field_name_variants(), "simple_dict", ""),
        (_build_c_field_name_variants(), "simple_sequence", ""),
        (_build_constructor_name_variants(), "simple_dict", ""),
        (type_hints_cross, "int_list", ""),
        (type_hints_cross, "int_list_large", ""),
        (type_hints_cross, "pair_sequence", ""),
        (type_hints_cross, "empty_list", ""),
        (type_hints_cross, "scalar_date", ""),
        (type_hints_cross, "scalar_datetime", ""),
        (type_hints_cross, "simple_dict", ""),
        (type_hints_cross, "int_set", ""),
        (type_hints_cross, "bool_list", ""),
        (type_hints_cross, "float_list", ""),
    ]
    # Rust CONST/STATIC with dict cases produce HashMap::from([…])
    # which is not a constant expression, so skip those.
    _const_static_suffixes = ("_const", "_static")

    for variants, case_dir_name, suffix in variant_sources:
        cases.extend(
            _VariantCase(
                variant_name=f"{variant.name}{suffix}",
                variant=variant,
                case_dir_name=case_dir_name,
                variable_form=_wrap_variable_form(lang_cls=variant.lang_cls),
            )
            for variant in variants
            if not (
                variant.lang_cls.__name__ == "Rust"
                and variant.name.endswith(_const_static_suffixes)
                and "dict" in case_dir_name
            )
        )
    return cases


_FORMAT_VARIANT_CASES = _build_variant_cases()


@pytest.mark.parametrize(
    argnames="variant_case",
    argvalues=_FORMAT_VARIANT_CASES,
    ids=[c.variant_name for c in _FORMAT_VARIANT_CASES],
)
def test_format_variant_golden_file(
    variant_case: _VariantCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test format-variant options (dates, sequences, sets, type hints)
    against golden files.
    """
    case_dir = cases_dir / variant_case.case_dir_name
    variant = variant_case.variant
    yaml_string = (case_dir / "input.yaml").read_text()
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
    file_regression.check(
        contents=result.code + "\n",
        extension=variant.spec.extension,
        fullpath=case_dir
        / (variant_case.variant_name + variant.spec.extension),
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


@beartype
def _build_line_ending_combined_cases() -> list[_LineEndingCombinedCase]:
    """Collect combined (declaration + assignment) test cases for
    non-default line endings.
    """
    cases: list[_LineEndingCombinedCase] = []
    for lang_cls in _SORTED_LANGUAGES:
        lang_name = lang_cls.__name__
        spec = _default_spec(lang_cls=lang_cls)
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


_LINE_ENDING_COMBINED_CASES = _build_line_ending_combined_cases()


@pytest.mark.parametrize(
    argnames="case",
    argvalues=_LINE_ENDING_COMBINED_CASES,
    ids=[c.name for c in _LINE_ENDING_COMBINED_CASES],
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
    lax_kwargs = _lax_kwargs(lang_cls=case.lang_cls)
    base_spec = case.lang_cls(**lax_kwargs)
    redef_styles = _find_redefinition_styles(spec=base_spec)
    assert redef_styles
    spec = case.lang_cls(
        line_ending=case.line_ending,
        declaration_style=redef_styles[0],
        **lax_kwargs,
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
    file_regression.check(
        contents=result.code + "\n",
        extension=spec.extension,
        fullpath=input_path.parent / (case.name + spec.extension),
    )


def test_no_dead_golden_files(request: pytest.FixtureRequest) -> None:
    """Every file under ``cases/`` must be referenced by a parameterized
    test.  Orphaned golden files silently rot and waste repository space.
    """
    cases_dir = request.config.rootpath / "tests" / "integration" / "cases"
    expected: set[Path] = set()

    for case_dir in sorted(cases_dir.iterdir()):
        expected.add(case_dir / "input.yaml")

    for case_name, lang_cls in _CASES:
        ext = lang_cls.extension
        expected.add(cases_dir / case_name / (lang_cls.__name__ + ext))

    for combined_case in _COMBINED_CASES:
        ext = combined_case.lang_cls.extension
        expected.add(
            cases_dir
            / combined_case.case_name
            / (combined_case.golden_file_name + ext)
        )

    for variant_case in _FORMAT_VARIANT_CASES:
        ext = variant_case.variant.spec.extension
        expected.add(
            cases_dir
            / variant_case.case_dir_name
            / (variant_case.variant_name + ext)
        )

    for line_ending_case in _LINE_ENDING_COMBINED_CASES:
        line_ending_spec = line_ending_case.lang_cls(
            line_ending=line_ending_case.line_ending,
        )
        expected.add(
            cases_dir
            / line_ending_case.case_dir_name
            / (line_ending_case.name + line_ending_spec.extension)
        )

    for call_case in _CALL_CASES:
        ext = call_case.lang_cls.extension
        golden_name = f"{call_case.lang_cls.__name__}_call"
        expected.add(
            cases_dir / call_case.config.case_dir_name / (golden_name + ext)
        )

    actual = {path for path in cases_dir.rglob(pattern="*") if path.is_file()}
    dead_files = sorted(
        path.relative_to(cases_dir) for path in actual - expected
    )
    assert not dead_files


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=_SORTED_LANGUAGES,
    ids=[c.__name__ for c in _SORTED_LANGUAGES],
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


@beartype
def _discover_call_cases() -> list[_CallCase]:
    """Return call test cases for all languages."""
    cases: list[_CallCase] = []
    for config in _CALL_CASE_CONFIGS:
        for lang_cls in _SORTED_LANGUAGES:
            if len(lang_cls.CallStyles) == 0:
                continue
            has_dotted_target = "." in config.target_function
            if has_dotted_target and not lang_cls.supports_dotted_calls:
                continue
            if (
                config.language_filter is not None
                and not config.language_filter(lang_cls)
            ):
                continue
            if config.call_style_kind is not None:
                # Only include languages that have this as a
                # non-default style.
                styles = list(lang_cls.CallStyles)
                matching = [
                    s for s in styles if s.value.kind == config.call_style_kind
                ]
                if not matching:
                    continue
                default_style = styles[0]
                if default_style.value.kind == config.call_style_kind:
                    continue
            cases.append(_CallCase(config=config, lang_cls=lang_cls))
    return cases


_CALL_CASES = _discover_call_cases()


@pytest.mark.parametrize(
    argnames="call_case",
    argvalues=_CALL_CASES,
    ids=[
        f"{c.config.case_dir_name}/{c.lang_cls.__name__}" for c in _CALL_CASES
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
    kwargs: dict[str, object] = dict(config.language_overrides)
    if config.call_style_kind is not None:
        style = next(
            s
            for s in lang_cls.CallStyles
            if s.value.kind == config.call_style_kind
        )
        kwargs["call_style"] = style
    kwargs.update(_lax_kwargs(lang_cls=lang_cls))
    spec = lang_cls(**kwargs)
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
    file_regression.check(
        contents=wrapped + "\n",
        extension=lang_cls.extension,
        newline="",
        fullpath=input_path.parent / (golden_name + lang_cls.extension),
    )
