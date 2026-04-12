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
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture
from ruamel.yaml import YAML

import literalizer
from literalizer.exceptions import NullInCollectionError
from literalizer.languages import ALL_LANGUAGES


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
    wrap_variable_name: str | None


@dataclasses.dataclass
class _LanguageConfig:
    """Language configuration for integration tests."""

    lang_cls: literalizer.LanguageCls
    wrap_variable_name: str | None


_LANGUAGES: dict[str, _LanguageConfig] = {
    lang_cls.__name__: _LanguageConfig(
        lang_cls=lang_cls,
        wrap_variable_name=(
            "my_data" if lang_cls.supports_variable_names else None
        ),
    )
    for lang_cls in ALL_LANGUAGES
}

_COVERED_LANGUAGES = frozenset(cfg.lang_cls for cfg in _LANGUAGES.values())
assert _COVERED_LANGUAGES == ALL_LANGUAGES, (
    f"Missing from integration tests: {ALL_LANGUAGES - _COVERED_LANGUAGES}"
)


@dataclasses.dataclass
class _VariantCase:
    """A format-variant golden-file test case."""

    variant_name: str
    variant: _Variant
    case_dir_name: str
    variable_name: str | None


@beartype
def _build_date_variants() -> Iterable[_Variant]:
    """Build date-format variants for scalar dates.

    For each language, create a variant for every non-default date format,
    using ``wrap``.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.format_date
        for fmt in list(spec.date_formats):
            if fmt is default_format:
                continue
            # Date and datetime formats can share enum member names
            # within the same language (e.g. Python has both
            # DateFormats.ISO and DatetimeFormats.ISO), so we include
            # a "_date_" infix to keep keys unique.
            variants.append(
                _Variant(
                    name=f"{lang_name}_date_{fmt.name.lower()}",
                    spec=lang_config.lang_cls(date_format=fmt),
                    lang_cls=lang_config.lang_cls,
                    wrap_variable_name=lang_config.wrap_variable_name,
                )
            )
    return variants


@beartype
def _build_datetime_variants() -> Iterable[_Variant]:
    """Build datetime-format variants for scalar datetimes.

    For each language, create a variant for every non-default datetime format,
    using ``wrap``.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.format_datetime
        for fmt in list(spec.datetime_formats):
            if fmt is default_format:
                continue
            # See _build_date_variants for why "_datetime_" is needed.
            variants.append(
                _Variant(
                    name=f"{lang_name}_datetime_{fmt.name.lower()}",
                    spec=lang_config.lang_cls(datetime_format=fmt),
                    lang_cls=lang_config.lang_cls,
                    wrap_variable_name=lang_config.wrap_variable_name,
                )
            )
    return variants


@beartype
def _build_sequence_variants() -> Iterable[_Variant]:
    """Build sequence-format variants for all languages with multiple
    formats.

    For each language that has more than one sequence format, create a variant
    for every non-default format.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format: Any = spec.sequence_format
        for fmt in list(spec.sequence_formats):
            if fmt is default_format:
                continue
            variants.append(
                _Variant(
                    name=f"{lang_name}_sequence_{fmt.name.lower()}",
                    spec=lang_config.lang_cls(sequence_format=fmt),
                    lang_cls=lang_config.lang_cls,
                    wrap_variable_name=lang_config.wrap_variable_name,
                )
            )
    return variants


@beartype
def _build_sequence_varname_variants() -> Iterable[_Variant]:
    """Build sequence-format variants with variable declarations.

    Like :func:`_build_sequence_variants` but exercises
    ``_format_variable_declaration`` for each non-default sequence format.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format: Any = spec.sequence_format
        for fmt in list(spec.sequence_formats):
            if fmt is default_format:
                continue
            variants.append(
                _Variant(
                    name=f"{lang_name}_sequence_{fmt.name.lower()}",
                    spec=lang_config.lang_cls(sequence_format=fmt),
                    lang_cls=lang_config.lang_cls,
                    wrap_variable_name=lang_config.wrap_variable_name,
                )
            )
    return variants


@beartype
def _build_set_variants() -> Iterable[_Variant]:
    """Build set-format variants for all languages with multiple formats.

    For each language that has more than one set format, create a variant
    for every non-default set format.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.set_format
        for fmt in list(spec.set_formats):
            if fmt is default_format:
                continue
            variants.append(
                _Variant(
                    name=f"{lang_name}_set_{fmt.name.lower()}",
                    spec=lang_config.lang_cls(set_format=fmt),
                    lang_cls=lang_config.lang_cls,
                    wrap_variable_name=lang_config.wrap_variable_name,
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
    for lang_name, lang_config in _LANGUAGES.items():
        if not lang_config.lang_cls.supports_default_set_element_type:
            continue
        string_type = type_overrides.get(lang_name, "String")
        spec = lang_config.lang_cls(
            default_set_element_type=string_type,
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
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
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
    for lang_name, lang_config in _LANGUAGES.items():
        if not lang_config.lang_cls.supports_default_sequence_element_type:
            continue
        string_type = type_overrides.get(lang_name, "String")
        variants.append(
            _Variant(
                name=f"{lang_name}_default_sequence_element_type_string",
                spec=lang_config.lang_cls(
                    default_sequence_element_type=string_type,
                ),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
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
    for lang_name, lang_config in _LANGUAGES.items():
        if not lang_config.lang_cls.supports_default_dict_value_type:
            continue
        string_type = type_overrides.get(lang_name, "String")
        variants.append(
            _Variant(
                name=f"{lang_name}_default_dict_value_type_string",
                spec=lang_config.lang_cls(default_dict_value_type=string_type),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
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
    for lang_name, lang_config in _LANGUAGES.items():
        if not lang_config.lang_cls.supports_default_dict_key_type:
            continue
        key_type = type_overrides.get(lang_name, "String")
        variants.append(
            _Variant(
                name=f"{lang_name}_default_dict_key_type",
                spec=lang_config.lang_cls(default_dict_key_type=key_type),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
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
    for lang_name, lang_config in _LANGUAGES.items():
        if not lang_config.lang_cls.supports_default_ordered_map_value_type:
            continue
        value_type = type_overrides.get(lang_name, "String")
        variants.append(
            _Variant(
                name=f"{lang_name}_default_ordered_map_value_type",
                spec=lang_config.lang_cls(
                    default_ordered_map_value_type=value_type,
                ),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
        )
    return variants


@beartype
def _build_comment_variants() -> Iterable[_Variant]:
    """Build comment-format variants for all languages with multiple
    formats.

    For each language that has more than one comment format, create a variant
    for every non-default format.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.comment_format
        for fmt in list(spec.comment_formats):
            if fmt is default_format:
                continue
            variants.append(
                _Variant(
                    name=f"{lang_name}_comment_{fmt.name.lower()}",
                    spec=lang_config.lang_cls(comment_format=fmt),
                    lang_cls=lang_config.lang_cls,
                    wrap_variable_name=lang_config.wrap_variable_name,
                )
            )
    return variants


@beartype
def _build_type_hint_variants() -> Iterable[_Variant]:
    """Build variable-type-hint variants for all languages with multiple
    formats.

    For each language that has more than one variable type-hint format,
    create a variant for every non-default type-hint style.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.variable_type_hints
        for fmt in list(spec.variable_type_hints_formats):
            if fmt is default_format:
                continue
            variants.append(
                _Variant(
                    name=f"{lang_name}_type_hints_{fmt.name.lower()}",
                    spec=lang_config.lang_cls(variable_type_hints=fmt),
                    lang_cls=lang_config.lang_cls,
                    wrap_variable_name="my_data",
                )
            )
    return variants


@beartype
def _build_declaration_style_variants() -> Iterable[_Variant]:
    """Build declaration-style variants for all languages with multiple
    styles.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.declaration_style
        non_defaults = [
            fmt for fmt in spec.declaration_styles if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_declaration_style_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    declaration_style=fmt,
                ),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_dict_format_variants() -> Iterable[_Variant]:
    """Build dict/map-format variants for all languages with multiple
    formats.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.dict_format
        non_defaults = [
            fmt for fmt in spec.dict_formats if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_dict_format_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    dict_format=fmt,
                ),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_dict_entry_style_variants() -> Iterable[_Variant]:
    """Build dict-entry-style variants for all languages with multiple
    styles.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_style = spec.dict_entry_style
        non_defaults = [
            fmt for fmt in spec.dict_entry_styles if fmt is not default_style
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_dict_entry_style_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    dict_entry_style=fmt,
                ),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_integer_format_variants() -> Iterable[_Variant]:
    """Build integer-format variants for all languages with multiple
    formats.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.integer_format
        non_defaults = [
            fmt for fmt in spec.integer_formats if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_integer_format_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    integer_format=fmt,
                ),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_numeric_literal_suffix_variants() -> Iterable[_Variant]:
    """Build numeric-literal-suffix variants for all languages with
    multiple options.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.numeric_literal_suffix
        non_defaults = [
            fmt
            for fmt in spec.numeric_literal_suffixes
            if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_numeric_literal_suffix_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    numeric_literal_suffix=fmt,
                ),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_numeric_separator_variants() -> Iterable[_Variant]:
    """Build numeric-separator variants for all languages with multiple
    options.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.numeric_separator
        non_defaults = [
            fmt for fmt in spec.numeric_separators if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_numeric_separator_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    numeric_separator=fmt,
                ),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_float_format_variants() -> Iterable[_Variant]:
    """Build float-format variants for all languages with multiple
    formats.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.float_format
        non_defaults = [
            fmt for fmt in spec.float_formats if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_float_format_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    float_format=fmt,
                ),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_string_format_variants() -> Iterable[_Variant]:
    """Build string-format variants for all languages with multiple
    formats.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.string_format
        non_defaults = [
            fmt for fmt in spec.string_formats if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_string_format_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    string_format=fmt,
                ),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_bytes_format_variants() -> Iterable[_Variant]:
    """Build bytes-format variants for all languages with multiple
    formats.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.format_bytes
        non_defaults = [
            fmt for fmt in spec.bytes_formats if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_bytes_format_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    bytes_format=fmt,
                ),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_trailing_comma_variants() -> Iterable[_Variant]:
    """Build trailing-comma variants for all languages with multiple
    options.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.trailing_comma
        non_defaults = [
            fmt for fmt in spec.trailing_commas if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_trailing_comma_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    trailing_comma=fmt,
                ),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
        )
    return variants


@beartype
def _build_line_ending_variants() -> Iterable[_Variant]:
    """Build line-ending variants for all languages with multiple
    options.
    """
    variants: list[_Variant] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
        default_format = spec.line_ending
        non_defaults = [
            fmt for fmt in spec.line_endings if fmt is not default_format
        ]
        variants.extend(
            _Variant(
                name=f"{lang_name}_line_ending_{fmt.name.lower()}",
                spec=lang_config.lang_cls(
                    line_ending=fmt,
                ),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for fmt in non_defaults
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
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
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
                spec=lang_config.lang_cls(
                    line_ending=line_ending,
                    declaration_style=declaration_style,
                ),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
            for line_ending in non_default_line_endings
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


_CASES_DIR = Path(__file__).parent / "cases"
_NON_TRIVIAL_KEY_CASES = _cases_with_non_trivial_dict_keys(
    cases_dir=_CASES_DIR,
)


@beartype
def _discover_cases() -> list[tuple[str, str]]:
    """Return ``(case_name, language)`` tuples."""
    cases: list[tuple[str, str]] = []
    for case_dir in sorted(_CASES_DIR.iterdir()):
        non_trivial = case_dir.name in _NON_TRIVIAL_KEY_CASES
        for lang_name, lang_config in _LANGUAGES.items():
            cls = lang_config.lang_cls
            if non_trivial and not cls.supports_non_printable_ascii_dict_keys:
                continue
            cases.append((case_dir.name, lang_name))
    return cases


_CASES = _discover_cases()


@pytest.mark.parametrize(
    argnames=("_case_name", "language"),
    argvalues=_CASES,
    ids=[f"{c[0]}/{c[1]}" for c in _CASES],
)
def test_golden_file(
    _case_name: str,
    language: str,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_yaml output matches expected golden file."""
    input_path = cases_dir / _case_name / "input.yaml"
    lang_config = _LANGUAGES[language]
    yaml_string = input_path.read_text()
    result = literalizer.literalize(
        source=yaml_string,
        input_format=literalizer.InputFormat.YAML,
        language=lang_config.lang_cls(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_name=lang_config.wrap_variable_name,
        new_variable=True,
        error_on_coercion=False,
    )
    variable_name = lang_config.wrap_variable_name or ""
    wrapped = lang_config.lang_cls.wrap_in_file(
        content=result.bare_code,
        variable_name=variable_name,
        body_preamble=result.body_preamble,
    )

    wrapped = _prepend_preamble(wrapped=wrapped, preamble=result.preamble)
    # newline="" prevents Python text-mode from converting \r\n to \n
    # on Windows, which would corrupt golden files containing literal
    # CR bytes (e.g. CommonLisp string_control_chars).
    file_regression.check(
        contents=wrapped + "\n",
        extension=lang_config.lang_cls.extension,
        newline="",
        fullpath=input_path.parent
        / (language + lang_config.lang_cls.extension),
    )


@dataclasses.dataclass
class _CombinedCase:
    """A combined-variable-forms test case for a specific redefinition
    style.
    """

    case_name: str
    lang_name: str
    lang_config: _LanguageConfig
    declaration_style: enum.Enum
    golden_file_name: str


@beartype
def _discover_combined_cases() -> list[_CombinedCase]:
    """Return combined test cases for all redefinition-supporting
    styles.
    """
    cases: list[_CombinedCase] = []
    for case_dir in sorted(_CASES_DIR.iterdir()):
        non_trivial = case_dir.name in _NON_TRIVIAL_KEY_CASES
        for lang_name, lang_config in _LANGUAGES.items():
            cls = lang_config.lang_cls
            if non_trivial and not cls.supports_non_printable_ascii_dict_keys:
                continue
            spec = cls()
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
                        lang_config=lang_config,
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
    """Test that literalize_yaml with new_variable=True (declaration) and
    new_variable=False (assignment to existing variable) produce expected
    golden output, combined in one file to show the difference in syntax.
    """
    input_path = cases_dir / combined_case.case_name / "input.yaml"
    lang_config = combined_case.lang_config
    spec = lang_config.lang_cls(
        declaration_style=combined_case.declaration_style,
    )
    yaml_string = input_path.read_text()
    declaration = literalizer.literalize(
        source=yaml_string,
        input_format=literalizer.InputFormat.YAML,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_data",
        new_variable=True,
        error_on_coercion=False,
    )
    assignment = literalizer.literalize(
        source=yaml_string,
        input_format=literalizer.InputFormat.YAML,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_data",
        new_variable=False,
        error_on_coercion=False,
    )
    variable_name = lang_config.wrap_variable_name or ""
    decl_preamble = (
        *declaration.body_preamble,
        *declaration.pre_declaration_comments,
    )
    combined = lang_config.lang_cls.wrap_combined_in_file(
        declaration=declaration.declaration_code,
        assignment=assignment.bare_code,
        variable_name=variable_name,
        body_preamble=decl_preamble,
    )
    combined = _prepend_preamble(
        wrapped=combined, preamble=declaration.preamble
    )
    file_regression.check(
        contents=combined + "\n",
        extension=lang_config.lang_cls.extension,
        newline="",
        fullpath=input_path.parent
        / (combined_case.golden_file_name + lang_config.lang_cls.extension),
    )


@beartype
def _build_constructor_name_variants() -> Iterable[_Variant]:
    """Build constructor-name variants for Fortran.

    Fortran emits constructor function calls (e.g. ``fnull``) in its
    output.  The constructor name parameters let users customize those
    names.
    """
    lang_config = _LANGUAGES["Fortran"]
    return [
        _Variant(
            name="Fortran_constructor_names_j",
            spec=lang_config.lang_cls(
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
            lang_cls=lang_config.lang_cls,
            wrap_variable_name=lang_config.wrap_variable_name,
        ),
    ]


@beartype
@beartype
def _build_type_name_variants() -> Iterable[_Variant]:
    """Build type-name variants for languages that generate a named type.

    These languages emit a custom algebraic data type in their body
    preamble (e.g. ``data Val = …`` in Haskell).  The ``type_name``
    constructor parameter lets users customize that name.
    """
    custom_names: dict[str, str] = {
        "Elm": "JsonVal",
        "FSharp": "JsonVal",
        "Gleam": "JsonVal",
        "Haskell": "JsonVal",
        "OCaml": "json_t",
        "PureScript": "JsonVal",
    }
    variants: list[_Variant] = []
    for lang_name, custom_name in custom_names.items():
        lang_config = _LANGUAGES[lang_name]
        variants.append(
            _Variant(
                name=f"{lang_name}_type_name_{custom_name}",
                spec=lang_config.lang_cls(type_name=custom_name),
                lang_cls=lang_config.lang_cls,
                wrap_variable_name=lang_config.wrap_variable_name,
            )
        )
    return variants


@beartype
def _build_c_field_name_variants() -> Iterable[_Variant]:
    """Build field-name variants for the C language.

    The C generator uses single-letter union field names by default.
    The field name parameters let users customize those names.
    """
    lang_config = _LANGUAGES["C"]
    return [
        _Variant(
            name="C_field_names_custom",
            spec=lang_config.lang_cls(
                bool_field="bl",
                int_field="integer",
                float_field="fp",
                string_field="str",
                array_field="arr",
                map_field="dict",
                key_field="key",
                value_field="val",
            ),
            lang_cls=lang_config.lang_cls,
            wrap_variable_name=lang_config.wrap_variable_name,
        ),
    ]


def _build_variant_cases() -> list[_VariantCase]:
    """Collect all format-variant golden-file test cases."""
    cases: list[_VariantCase] = []
    variant_sources: list[tuple[Iterable[_Variant], str, str]] = [
        (_build_date_variants(), "scalar_date", ""),
        (_build_date_variants(), "date_list", ""),
        (_build_date_variants(), "date_set", ""),
        (_build_datetime_variants(), "scalar_datetime", ""),
        (_build_datetime_variants(), "scalar_datetime_naive", "_naive"),
        (_build_datetime_variants(), "scalar_datetime_non_utc", "_non_utc"),
        (_build_sequence_variants(), "simple_sequence", ""),
        (_build_sequence_variants(), "pair_sequence", "_pair"),
        (_build_sequence_variants(), "triple_sequence", "_triple"),
        (_build_sequence_varname_variants(), "simple_sequence", "_varname"),
        (_build_set_variants(), "set", ""),
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
        (_build_comment_variants(), "comments", ""),
        (_build_type_hint_variants(), "type_hints", ""),
        (_build_type_hint_variants(), "scalar_date", ""),
        (_build_type_hint_variants(), "scalar_datetime", ""),
        (_build_type_hint_variants(), "binary", ""),
        (_build_type_hint_variants(), "mixed_type_dicts_in_sequence", ""),
        (_build_type_hint_variants(), "empty_dicts_in_sequence", ""),
        (_build_declaration_style_variants(), "simple_sequence", ""),
        (_build_declaration_style_variants(), "simple_dict", ""),
        (_build_declaration_style_variants(), "empty_list", ""),
        (_build_dict_format_variants(), "simple_dict", ""),
        (_build_dict_format_variants(), "dict_with_list_value", "_list_val"),
        (_build_dict_entry_style_variants(), "simple_dict", ""),
        (
            _build_dict_entry_style_variants(),
            "dict_with_list_value",
            "_list_val",
        ),
        (_build_sequence_variants(), "float_list", "_float"),
        (_build_float_format_variants(), "float_list", ""),
        (_build_float_format_variants(), "float_scientific_notation", "_s"),
        (_build_float_format_variants(), "float_special_values", "_v"),
        (_build_float_format_variants(), "nested_float_list", "_n"),
        (_build_integer_format_variants(), "int_list", ""),
        (_build_integer_format_variants(), "int_list_large", "_large"),
        (_build_integer_format_variants(), "int_list_with_zero", "_zero"),
        (_build_numeric_literal_suffix_variants(), "int_list", ""),
        (_build_numeric_literal_suffix_variants(), "int_list_large", "_large"),
        (
            _build_numeric_literal_suffix_variants(),
            "int_list_with_zero",
            "_zero",
        ),
        (_build_numeric_separator_variants(), "int_list", ""),
        (_build_numeric_separator_variants(), "int_list_large", "_large"),
        (_build_numeric_separator_variants(), "int_list_with_zero", "_zero"),
        (_build_string_format_variants(), "string_list", ""),
        (_build_string_format_variants(), "string_with_backslash", ""),
        (_build_bytes_format_variants(), "binary", ""),
        (_build_trailing_comma_variants(), "simple_sequence", ""),
        (_build_line_ending_variants(), "simple_sequence", ""),
        (_build_line_ending_variants(), "simple_dict", "_dict"),
        (_build_line_ending_decl_variants(), "simple_sequence", ""),
        (_build_type_name_variants(), "simple_dict", ""),
        (_build_c_field_name_variants(), "simple_dict", ""),
        (_build_c_field_name_variants(), "simple_sequence", ""),
        (_build_constructor_name_variants(), "simple_dict", ""),
    ]
    for variants, case_dir_name, suffix in variant_sources:
        cases.extend(
            _VariantCase(
                variant_name=f"{variant.name}{suffix}",
                variant=variant,
                case_dir_name=case_dir_name,
                variable_name=variant.wrap_variable_name,
            )
            for variant in variants
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
            variable_name=variant_case.variable_name,
            new_variable=True,
            error_on_coercion=False,
        )
    except NullInCollectionError:
        pytest.skip("Format rejects null elements in this input")
    variable_name = variant.wrap_variable_name or ""
    wrapped = variant.lang_cls.wrap_in_file(
        content=result.bare_code,
        variable_name=variable_name,
        body_preamble=result.body_preamble,
    )
    wrapped = _prepend_preamble(wrapped=wrapped, preamble=result.preamble)
    file_regression.check(
        contents=wrapped + "\n",
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
    lang_config: _LanguageConfig
    line_ending: enum.Enum
    case_dir_name: str


@beartype
def _build_line_ending_combined_cases() -> list[_LineEndingCombinedCase]:
    """Collect combined (declaration + assignment) test cases for
    non-default line endings.
    """
    cases: list[_LineEndingCombinedCase] = []
    for lang_name, lang_config in _LANGUAGES.items():
        spec = lang_config.lang_cls()
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
                        lang_config=lang_config,
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
    base_spec = case.lang_config.lang_cls()
    redef_styles = _find_redefinition_styles(spec=base_spec)
    assert redef_styles
    spec = case.lang_config.lang_cls(
        line_ending=case.line_ending,
        declaration_style=redef_styles[0],
    )
    declaration = literalizer.literalize(
        source=yaml_string,
        input_format=literalizer.InputFormat.YAML,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_data",
        new_variable=True,
        error_on_coercion=False,
    )
    assignment = literalizer.literalize(
        source=yaml_string,
        input_format=literalizer.InputFormat.YAML,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_name="my_data",
        new_variable=False,
        error_on_coercion=False,
    )
    decl_preamble = (
        *declaration.body_preamble,
        *declaration.pre_declaration_comments,
    )
    combined = case.lang_config.lang_cls.wrap_combined_in_file(
        declaration=declaration.declaration_code,
        assignment=assignment.bare_code,
        variable_name=case.lang_config.wrap_variable_name or "",
        body_preamble=decl_preamble,
    )
    combined = _prepend_preamble(
        wrapped=combined, preamble=declaration.preamble
    )
    file_regression.check(
        contents=combined + "\n",
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

    for case_name, lang_name in _CASES:
        lang_config = _LANGUAGES[lang_name]
        ext = lang_config.lang_cls.extension
        expected.add(cases_dir / case_name / (lang_name + ext))

    for combined_case in _COMBINED_CASES:
        ext = combined_case.lang_config.lang_cls.extension
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
        line_ending_spec = line_ending_case.lang_config.lang_cls(
            line_ending=line_ending_case.line_ending,
        )
        expected.add(
            cases_dir
            / line_ending_case.case_dir_name
            / (line_ending_case.name + line_ending_spec.extension)
        )

    actual = {path for path in cases_dir.rglob(pattern="*") if path.is_file()}
    dead_files = sorted(
        path.relative_to(cases_dir) for path in actual - expected
    )
    assert not dead_files


def _lang_cls_name(cls: literalizer.LanguageCls) -> str:
    """Return the class name for sorting."""
    return cls.__name__


_SORTED_LANGUAGES: list[literalizer.LanguageCls] = sorted(
    ALL_LANGUAGES,
    key=_lang_cls_name,
)


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
    assert issubclass(spec.string_formats, enum.Enum)
    assert len(spec.string_formats) >= 1
    assert issubclass(spec.trailing_commas, enum.Enum)
    assert len(spec.trailing_commas) >= 1
    assert issubclass(spec.line_endings, enum.Enum)
    assert len(spec.line_endings) >= 1
