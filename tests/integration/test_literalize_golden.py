"""Golden-file tests that drive :func:`literalizer.literalize`.

Each test exercises a different axis of the public API — single
declaration form, combined declaration + assignment, format-variant
kwargs, statement-terminator option, heterogeneous-scalar strategy,
``pre_indent_level`` — but all share the same shape: render YAML to a
language and compare against a checked-in golden file.

Every golden test loops over ``lang_cls.VersionFormats`` so adding a
second member to a language's ``VersionFormats`` enum automatically
produces a parallel set of golden files; today the enum has a single
member so the loop runs once per language and case.
"""

from pathlib import Path
from typing import Final, NoReturn

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer.exceptions import (
    HeterogeneousCollectionError,
    IncompatibleFormatsError,
    NullInCollectionError,
    UnrepresentableEmptyDictError,
    UnrepresentableInputError,
    UnrepresentableIntegerError,
    UnrepresentableSpecialFloatError,
    VariableNameNotSupportedError,
)
from literalizer.languages.rust import Rust

from .case_discovery import (
    KEBAB_NEW_VARIABLE_CASE_DIR,
    PRIMED_NEW_VARIABLE_CASE_DIR,
    HeterogeneousStrategyCombinedCase,
    IndentCase,
    NoVariableFormCase,
    PreIndentCase,
    StatementTerminatorCombinedCase,
    build_heterogeneous_strategy_combined_cases,
    build_indent_cases,
    build_no_variable_form_cases,
    build_pre_indent_cases,
    build_statement_terminator_combined_cases,
    case_input,
    group_cases_by_language,
    group_combined_cases_by_language,
    kebab_new_variable_languages,
    primed_new_variable_languages,
)
from .language_specs import (
    find_redefinition_styles,
    lang_cls_name,
    make_golden_path,
    make_spec,
    sorted_languages,
    with_per_fixture_module_name,
)
from .variant_cases import (
    group_variant_cases_by_language,
    variant_languages,
    wrap_variable_form,
)

_SkipReasons = tuple[tuple[type[Exception], str, bool], ...]

_LANG_SKIP_REASONS: _SkipReasons = (
    (
        UnrepresentableIntegerError,
        "cannot represent integer in this input",
        True,
    ),
    (UnrepresentableEmptyDictError, "cannot represent an empty dict", True),
    (
        HeterogeneousCollectionError,
        "cannot represent this heterogeneous input",
        True,
    ),
    (NullInCollectionError, "cannot represent null in a collection", True),
    (UnrepresentableInputError, "cannot represent this input", True),
)

_VARIANT_SKIP_REASONS: _SkipReasons = (
    (
        UnrepresentableIntegerError,
        "cannot represent integer in this input",
        True,
    ),
    (UnrepresentableEmptyDictError, "cannot represent an empty dict", True),
    (NullInCollectionError, "rejects null elements in this input", False),
    (
        HeterogeneousCollectionError,
        "cannot represent this heterogeneous input",
        True,
    ),
    (
        IncompatibleFormatsError,
        "combination cannot represent this input",
        True,
    ),
    (
        UnrepresentableSpecialFloatError,
        "cannot represent special floats in this input",
        True,
    ),
    (UnrepresentableInputError, "cannot represent this input", True),
)

_RECORD_NULL_SUBSTITUTIONS_CASE: Final = "record_null_substitutions"
_RECORD_NULL_SUBSTITUTIONS: Final = {"replacement": -1}


def _merge_fixture_prefix(*, fixture_prefix: str, generated_code: str) -> str:
    """Place a fixture declaration after one de-duplicated include
    block.
    """
    if not fixture_prefix:
        return generated_code

    prefix_lines = fixture_prefix.rstrip("\n").splitlines()
    generated_lines = generated_code.splitlines()
    prefix_include_count = next(
        (
            index
            for index, line in enumerate(iterable=prefix_lines)
            if not line.startswith("#include ")
        ),
        len(prefix_lines),
    )
    generated_include_count = next(
        (
            index
            for index, line in enumerate(iterable=generated_lines)
            if not line.startswith("#include ")
        ),
        len(generated_lines),
    )
    includes = dict.fromkeys(
        (
            *generated_lines[:generated_include_count],
            *prefix_lines[:prefix_include_count],
        )
    )
    return "\n".join(
        (
            *includes,
            *prefix_lines[prefix_include_count:],
            *generated_lines[generated_include_count:],
        )
    )


def _skip_unrepresentable(
    *,
    exc: Exception,
    reasons: _SkipReasons,
    golden_path: Path,
    prefix: str,
) -> NoReturn:
    """Skip the current test with a message keyed off the caught error.

    Callers pair their ``except`` tuple with the same reasons table,
    so the lookup below is total by construction; ``StopIteration``
    propagating out of this helper would indicate a divergence between
    the two.  For matching entries whose third tuple field is ``True``
    the golden file is removed first so a stale fixture cannot pose
    as a real failure on the next run.
    """
    _, reason, unlink = next(
        entry for entry in reasons if isinstance(exc, entry[0])
    )
    if unlink:
        golden_path.unlink(missing_ok=True)
    pytest.skip(f"{prefix} {reason}")


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=sorted_languages(),
    ids=lang_cls_name,
)
def test_golden_file(
    lang_cls: literalizer.LanguageCls,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Test that literalize_yaml output matches expected golden file."""
    lang_name = lang_cls.__name__
    grouped = group_cases_by_language(cases_dir=cases_dir)
    for case_name in grouped.get(lang_cls, []):
        for version_format in lang_cls.VersionFormats:
            with subtests.test(
                case_name=case_name,
                version=version_format.name,
            ):
                input_info = case_input(case_dir=cases_dir / case_name)
                source_text = input_info.path.read_text(encoding="utf-8")
                golden_path = make_golden_path(
                    parent=input_info.path.parent,
                    name=lang_name,
                    extension=lang_cls.extension,
                    lang_cls=lang_cls,
                    version=version_format,
                )
                spec = with_per_fixture_module_name(
                    spec=make_spec(
                        lang_cls=lang_cls,
                        language_version=version_format,
                    ),
                    golden_path=golden_path,
                )
                try:
                    try:
                        result = literalizer.literalize(
                            source=source_text,
                            input_format=input_info.input_format,
                            language=spec,
                            pre_indent_level=0,
                            include_delimiters=True,
                            variable_form=wrap_variable_form(),
                            wrap_in_file=True,
                            record_null_substitutions=(
                                _RECORD_NULL_SUBSTITUTIONS
                                if case_name == _RECORD_NULL_SUBSTITUTIONS_CASE
                                else None
                            ),
                        )
                    except VariableNameNotSupportedError:
                        result = literalizer.literalize(
                            source=source_text,
                            input_format=input_info.input_format,
                            language=spec,
                            pre_indent_level=0,
                            include_delimiters=True,
                            variable_form=None,
                            wrap_in_file=True,
                            record_null_substitutions=(
                                _RECORD_NULL_SUBSTITUTIONS
                                if case_name == _RECORD_NULL_SUBSTITUTIONS_CASE
                                else None
                            ),
                        )
                except (
                    UnrepresentableIntegerError,
                    UnrepresentableEmptyDictError,
                    HeterogeneousCollectionError,
                    NullInCollectionError,
                    UnrepresentableInputError,
                ) as exc:
                    _skip_unrepresentable(
                        exc=exc,
                        reasons=_LANG_SKIP_REASONS,
                        golden_path=golden_path,
                        prefix=lang_name,
                    )
                # newline="" prevents Python text-mode from converting
                # \r\n to \n on Windows, which would corrupt golden
                # files containing literal CR bytes (e.g. CommonLisp
                # string_control_chars).
                file_regression.check(
                    contents=result.code + "\n",
                    encoding="utf-8",
                    extension=lang_cls.extension,
                    newline="",
                    fullpath=golden_path,
                )


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=kebab_new_variable_languages(),
    ids=lang_cls_name,
)
def test_kebab_new_variable_golden_file(
    lang_cls: literalizer.LanguageCls,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Hyphen-friendly languages preserve a hyphenated declaration
    name.
    """
    input_info = case_input(case_dir=cases_dir / KEBAB_NEW_VARIABLE_CASE_DIR)
    source_text = input_info.path.read_text(encoding="utf-8")
    for version_format in lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            golden_path = make_golden_path(
                parent=input_info.path.parent,
                name=lang_cls.__name__,
                extension=lang_cls.extension,
                lang_cls=lang_cls,
                version=version_format,
            )
            spec = with_per_fixture_module_name(
                spec=make_spec(
                    lang_cls=lang_cls,
                    language_version=version_format,
                ),
                golden_path=golden_path,
            )
            result = literalizer.literalize(
                source=source_text,
                input_format=input_info.input_format,
                language=spec,
                pre_indent_level=0,
                include_delimiters=True,
                variable_form=literalizer.NewVariable(
                    name="a-b",
                    modifiers=frozenset(),
                ),
                wrap_in_file=True,
            )
            file_regression.check(
                contents=result.code + "\n",
                encoding="utf-8",
                extension=lang_cls.extension,
                newline=None,
                fullpath=golden_path,
            )


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=primed_new_variable_languages(),
    ids=lang_cls_name,
)
def test_primed_new_variable_golden_file(
    lang_cls: literalizer.LanguageCls,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Prime-friendly languages preserve a primed declaration name."""
    input_info = case_input(case_dir=cases_dir / PRIMED_NEW_VARIABLE_CASE_DIR)
    source_text = input_info.path.read_text(encoding="utf-8")
    for version_format in lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            golden_path = make_golden_path(
                parent=input_info.path.parent,
                name=lang_cls.__name__,
                extension=lang_cls.extension,
                lang_cls=lang_cls,
                version=version_format,
            )
            spec = with_per_fixture_module_name(
                spec=make_spec(
                    lang_cls=lang_cls,
                    language_version=version_format,
                ),
                golden_path=golden_path,
            )
            result = literalizer.literalize(
                source=source_text,
                input_format=input_info.input_format,
                language=spec,
                pre_indent_level=0,
                include_delimiters=True,
                variable_form=literalizer.NewVariable(
                    name="a'",
                    modifiers=frozenset(),
                ),
                wrap_in_file=True,
            )
            file_regression.check(
                contents=result.code + "\n",
                encoding="utf-8",
                extension=lang_cls.extension,
                newline=None,
                fullpath=golden_path,
            )


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=sorted_languages(),
    ids=lang_cls_name,
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
    grouped = group_combined_cases_by_language(cases_dir=cases_dir)
    for combined_case in grouped.get(lang_cls, []):
        for version_format in lang_cls.VersionFormats:
            with subtests.test(
                case_name=combined_case.case_name,
                golden_file_name=combined_case.golden_file_name,
                version=version_format.name,
            ):
                input_info = case_input(
                    case_dir=cases_dir / combined_case.case_name,
                )
                golden_path = make_golden_path(
                    parent=input_info.path.parent,
                    name=combined_case.golden_file_name,
                    extension=lang_cls.extension,
                    lang_cls=lang_cls,
                    version=version_format,
                )
                spec = with_per_fixture_module_name(
                    spec=make_spec(
                        lang_cls=lang_cls,
                        declaration_style=combined_case.declaration_style,
                        language_version=version_format,
                    ),
                    golden_path=golden_path,
                )
                source_text = input_info.path.read_text(encoding="utf-8")
                try:
                    result = literalizer.literalize(
                        source=source_text,
                        input_format=input_info.input_format,
                        language=spec,
                        pre_indent_level=0,
                        include_delimiters=True,
                        variable_form=literalizer.BothVariableForms(
                            name="my_data",
                            modifiers=frozenset(),
                        ),
                        wrap_in_file=True,
                    )
                except UnrepresentableIntegerError:
                    golden_path.unlink(missing_ok=True)
                    pytest.skip(
                        f"{lang_cls.__name__} cannot represent integer in "
                        "this input"
                    )
                except UnrepresentableEmptyDictError:
                    golden_path.unlink(missing_ok=True)
                    pytest.skip(
                        f"{lang_cls.__name__} cannot represent an empty dict"
                    )
                except HeterogeneousCollectionError:
                    golden_path.unlink(missing_ok=True)
                    pytest.skip(
                        f"{lang_cls.__name__} cannot represent this "
                        "heterogeneous input"
                    )
                except NullInCollectionError:
                    golden_path.unlink(missing_ok=True)
                    pytest.skip(
                        f"{lang_cls.__name__} cannot represent null in a "
                        "collection"
                    )
                except UnrepresentableInputError:
                    golden_path.unlink(missing_ok=True)
                    pytest.skip(
                        f"{lang_cls.__name__} cannot represent this input"
                    )
                file_regression.check(
                    contents=result.code + "\n",
                    encoding="utf-8",
                    extension=lang_cls.extension,
                    newline="",
                    fullpath=golden_path,
                )


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=variant_languages(),
    ids=lang_cls_name,
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
    for variant_case in group_variant_cases_by_language()[lang_cls]:
        variant = variant_case.variant
        # Each variant pins a specific ``language_version`` (e.g. PY38
        # version variants), so render only that one version.
        # ``lang_cls.VersionFormats`` is iterated by other tests where
        # the spec is rebuilt per version.
        version_format = variant.spec.language_version
        with subtests.test(
            variant_name=variant_case.variant_name,
            case_dir_name=variant_case.case_dir_name,
            version=version_format.name,
        ):
            case_dir = cases_dir / variant_case.case_dir_name
            input_info = case_input(case_dir=case_dir)
            source_text = input_info.path.read_text(encoding="utf-8")
            golden_path = make_golden_path(
                parent=case_dir,
                name=variant_case.variant_name,
                extension=variant.spec.extension,
                lang_cls=lang_cls,
                version=version_format,
            )
            spec = with_per_fixture_module_name(
                spec=variant.spec,
                golden_path=golden_path,
            )
            try:
                try:
                    result = literalizer.literalize(
                        source=source_text,
                        input_format=input_info.input_format,
                        language=spec,
                        pre_indent_level=0,
                        include_delimiters=True,
                        variable_form=variant_case.variable_form,
                        wrap_in_file=True,
                        collection_layout=variant.collection_layout,
                        record_null_substitutions=(
                            variant.record_null_substitutions
                        ),
                    )
                except VariableNameNotSupportedError:
                    result = literalizer.literalize(
                        source=source_text,
                        input_format=input_info.input_format,
                        language=spec,
                        pre_indent_level=0,
                        include_delimiters=True,
                        variable_form=None,
                        wrap_in_file=True,
                        collection_layout=variant.collection_layout,
                        record_null_substitutions=(
                            variant.record_null_substitutions
                        ),
                    )
            except (
                UnrepresentableIntegerError,
                UnrepresentableSpecialFloatError,
                UnrepresentableEmptyDictError,
                NullInCollectionError,
                HeterogeneousCollectionError,
                IncompatibleFormatsError,
                UnrepresentableInputError,
            ) as exc:
                _skip_unrepresentable(
                    exc=exc,
                    reasons=_VARIANT_SKIP_REASONS,
                    golden_path=golden_path,
                    prefix="Format",
                )
            file_regression.check(
                contents=(
                    _merge_fixture_prefix(
                        fixture_prefix=variant.fixture_prefix,
                        generated_code=result.code,
                    )
                    + "\n"
                ),
                encoding="utf-8",
                extension=variant.spec.extension,
                newline=None,
                fullpath=golden_path,
            )


@pytest.mark.parametrize(
    argnames="case",
    argvalues=build_statement_terminator_combined_cases(),
    ids=[c.name for c in build_statement_terminator_combined_cases()],
)
def test_statement_terminator_style_combined_variable_forms(
    case: StatementTerminatorCombinedCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Test that combined (declaration + assignment) output with a
    non-default statement terminator matches the golden file.
    """
    input_info = case_input(case_dir=cases_dir / case.case_dir_name)
    source_text = input_info.path.read_text(encoding="utf-8")
    base_spec = make_spec(lang_cls=case.lang_cls)
    redef_styles = find_redefinition_styles(spec=base_spec)
    assert redef_styles
    for version_format in case.lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            spec = make_spec(
                lang_cls=case.lang_cls,
                statement_terminator_style=case.statement_terminator_style,
                declaration_style=redef_styles[0],
                language_version=version_format,
            )
            result = literalizer.literalize(
                source=source_text,
                input_format=input_info.input_format,
                language=spec,
                pre_indent_level=0,
                include_delimiters=True,
                variable_form=literalizer.BothVariableForms(
                    name="my_data", modifiers=frozenset()
                ),
                wrap_in_file=True,
            )
            file_regression.check(
                contents=result.code + "\n",
                encoding="utf-8",
                extension=spec.extension,
                newline=None,
                fullpath=make_golden_path(
                    parent=input_info.path.parent,
                    name=case.name,
                    extension=spec.extension,
                    lang_cls=case.lang_cls,
                    version=version_format,
                ),
            )


@pytest.mark.parametrize(
    argnames="case",
    argvalues=build_heterogeneous_strategy_combined_cases(),
    ids=[c.name for c in build_heterogeneous_strategy_combined_cases()],
)
def test_heterogeneous_strategy_combined_variable_forms(
    case: HeterogeneousStrategyCombinedCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Test that combined (declaration + assignment) output with a
    non-default heterogeneous-scalar strategy matches the golden file.
    """
    input_info = case_input(case_dir=cases_dir / case.case_dir_name)
    source_text = input_info.path.read_text(encoding="utf-8")
    base_spec = make_spec(lang_cls=case.lang_cls)
    redef_styles = find_redefinition_styles(spec=base_spec)
    assert redef_styles
    for version_format in case.lang_cls.VersionFormats:
        spec = make_spec(
            lang_cls=case.lang_cls,
            heterogeneous_strategy=case.heterogeneous_strategy,
            declaration_style=redef_styles[0],
            language_version=version_format,
        )
        # A strategy may pin a required version (e.g. Java ``RECORD``
        # needs ``JDK_16``); skip the iterations it overrides so only
        # the pinned version's golden is generated and lint-checked.
        if spec.language_version is not version_format:
            continue
        with subtests.test(version=version_format.name):
            golden_path = make_golden_path(
                parent=input_info.path.parent,
                name=case.name,
                extension=case.lang_cls.extension,
                lang_cls=case.lang_cls,
                version=version_format,
            )
            spec = with_per_fixture_module_name(
                spec=spec,
                golden_path=golden_path,
            )
            try:
                result = literalizer.literalize(
                    source=source_text,
                    input_format=input_info.input_format,
                    language=spec,
                    pre_indent_level=0,
                    include_delimiters=True,
                    variable_form=literalizer.BothVariableForms(
                        name="my_data",
                        modifiers=frozenset(),
                    ),
                    wrap_in_file=True,
                )
            except HeterogeneousCollectionError:
                # A strategy may not be able to represent the paired
                # fixture for every language (e.g. Kotlin ``TUPLE`` has
                # no native tuple for the four-element
                # ``tuple_record_field`` array), exactly as the base
                # variant golden test skips such an input.  Drop any
                # stale golden and skip.
                golden_path.unlink(missing_ok=True)
                pytest.skip(
                    f"{case.lang_cls.__name__} cannot represent this "
                    "heterogeneous input under "
                    f"{case.heterogeneous_strategy.name}",
                )
            file_regression.check(
                contents=result.code + "\n",
                encoding="utf-8",
                extension=spec.extension,
                newline=None,
                fullpath=golden_path,
            )


@pytest.mark.parametrize(
    argnames="case",
    argvalues=build_pre_indent_cases(),
    ids=[c.name for c in build_pre_indent_cases()],
)
def test_pre_indent_level_with_new_variable_golden_file(
    case: PreIndentCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """``pre_indent_level > 0`` with ``NewVariable`` produces uniformly
    indented output.

    Regression test for the bug where the first line of a multi-line
    value was inserted after ``=`` with the indent baked in, producing
    extra spaces between ``=`` and the value and shifting continuation
    lines by an extra indent.
    """
    input_info = case_input(case_dir=cases_dir / case.case_dir_name)
    source_text = input_info.path.read_text(encoding="utf-8")
    for version_format in case.lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            spec = make_spec(
                lang_cls=case.lang_cls,
                language_version=version_format,
            )
            result = literalizer.literalize(
                source=source_text,
                input_format=input_info.input_format,
                language=spec,
                pre_indent_level=case.pre_indent_level,
                include_delimiters=True,
                variable_form=literalizer.NewVariable(
                    name="my_data",
                    modifiers=case.modifiers,
                ),
                wrap_in_file=True,
            )
            file_regression.check(
                contents=result.code + "\n",
                encoding="utf-8",
                extension=spec.extension,
                newline=None,
                fullpath=make_golden_path(
                    parent=input_info.path.parent,
                    name=case.name,
                    extension=spec.extension,
                    lang_cls=case.lang_cls,
                    version=version_format,
                ),
            )


@pytest.mark.parametrize(
    argnames="case",
    argvalues=build_no_variable_form_cases(),
    ids=[c.name for c in build_no_variable_form_cases()],
)
def test_no_variable_form_golden_file(
    case: NoVariableFormCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """``literalize(wrap_in_file=True, variable_form=None)`` renders to a
    stable per-language golden for every opt-in language.

    Locks in issue #2138: languages whose
    :attr:`~literalizer._language.Language.supports_no_variable_wrap_in_file`
    is ``True`` must produce valid file-scope output for a bare value;
    opt-out languages are rejected upstream with
    :class:`~literalizer.exceptions.WrapInFileWithoutVariableNotSupportedError`.
    """
    input_info = case_input(case_dir=cases_dir / case.case_dir_name)
    source_text = input_info.path.read_text(encoding="utf-8")
    for version_format in case.lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            golden_path = make_golden_path(
                parent=input_info.path.parent,
                name=case.name,
                extension=case.lang_cls.extension,
                lang_cls=case.lang_cls,
                version=version_format,
            )
            spec = with_per_fixture_module_name(
                spec=make_spec(
                    lang_cls=case.lang_cls,
                    language_version=version_format,
                ),
                golden_path=golden_path,
            )
            result = literalizer.literalize(
                source=source_text,
                input_format=input_info.input_format,
                language=spec,
                pre_indent_level=0,
                include_delimiters=True,
                variable_form=None,
                wrap_in_file=True,
            )
            file_regression.check(
                contents=result.code + "\n",
                encoding="utf-8",
                extension=case.lang_cls.extension,
                newline=None,
                fullpath=golden_path,
            )


@pytest.mark.parametrize(
    argnames="case",
    argvalues=build_indent_cases(),
    ids=[c.name for c in build_indent_cases()],
)
def test_indent_golden_file(
    case: IndentCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """A non-default ``indent`` renders to a stable per-language golden.

    Locks in issue #2084: every spec carries an ``indent`` field, but
    until #2087 most languages hard-coded their indentation in the
    ``wrap_in_file`` / preamble helpers.  Rendering ``bool_list`` with
    a three-space indent for every language pins down the result so a
    future regression that re-introduces a literal ``"    "`` (or
    two-space, or a tab) cannot pass silently.
    """
    input_info = case_input(case_dir=cases_dir / case.case_dir_name)
    source_text = input_info.path.read_text(encoding="utf-8")
    for version_format in case.lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            golden_path = make_golden_path(
                parent=input_info.path.parent,
                name=case.name,
                extension=case.lang_cls.extension,
                lang_cls=case.lang_cls,
                version=version_format,
            )
            spec = with_per_fixture_module_name(
                spec=make_spec(
                    lang_cls=case.lang_cls,
                    indent=case.indent,
                    language_version=version_format,
                ),
                golden_path=golden_path,
            )
            try:
                result = literalizer.literalize(
                    source=source_text,
                    input_format=input_info.input_format,
                    language=spec,
                    pre_indent_level=0,
                    include_delimiters=True,
                    variable_form=literalizer.NewVariable(
                        name="my_data", modifiers=frozenset()
                    ),
                    wrap_in_file=True,
                )
            except VariableNameNotSupportedError:
                result = literalizer.literalize(
                    source=source_text,
                    input_format=input_info.input_format,
                    language=spec,
                    pre_indent_level=0,
                    include_delimiters=True,
                    variable_form=None,
                    wrap_in_file=True,
                )
            file_regression.check(
                contents=result.code + "\n",
                encoding="utf-8",
                extension=case.lang_cls.extension,
                newline=None,
                fullpath=golden_path,
            )


def test_rust_record_strategy_error_path(cases_dir: Path) -> None:
    """RECORD requested with non-record-eligible data still raises.

    The carve-out only skips record-shaped dicts; a heterogeneous list
    nested inside a record still fails the standard heterogeneous-list
    check because Rust ``vec![]`` cannot represent mixed scalar types.
    """
    del cases_dir
    record_strategy = next(
        strategy
        for strategy in Rust.heterogeneous_strategies
        if strategy.name == "RECORD"
    )
    spec = Rust(heterogeneous_strategy=record_strategy)
    yaml_string = 'items:\n  - 1\n  - "two"\n'
    with pytest.raises(expected_exception=HeterogeneousCollectionError):
        literalizer.literalize(
            source=yaml_string,
            input_format=literalizer.InputFormat.YAML,
            language=spec,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=literalizer.NewVariable(
                name="my_data", modifiers=frozenset()
            ),
            wrap_in_file=True,
        )
