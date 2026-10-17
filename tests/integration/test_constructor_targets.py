"""Golden-file coverage for constructor call targets.

Two things are checked here: how each language spells a constructor as
a call target, and what binding that call to a variable looks like.
The bindings vary by call style and by variable modifier, so they are
declared as cases and driven through the one runner below rather than
written out a test body at a time.
"""

import dataclasses
import enum
from pathlib import Path

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer import InputFormat, literalize_call

from .case_manifests import ConstructorCaseSpec
from .constructor_cases import (
    ConstructorBindingCase,
    constructor_binding_cases,
    constructor_golden_path,
)
from .golden_checks import GoldenSkips, check_golden
from .language_specs import (
    make_golden_path,
    make_spec,
    sorted_languages,
    with_per_fixture_module_name,
)

_CONSTRUCTOR_NAME = "Playlist"
_GOLDEN_DIR = Path(__file__).parent / "constructor_targets"


@beartype
def _golden_path(
    *,
    name: str,
    lang_cls: literalizer.LanguageCls,
    version: enum.Enum,
) -> Path:
    """Return the checked-in golden path for a constructor-target case."""
    return make_golden_path(
        parent=_GOLDEN_DIR,
        name=name,
        extension=".txt",
        lang_cls=lang_cls,
        version=version,
    )


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=sorted_languages(),
    ids=lambda lang_cls: lang_cls.__name__,
)
def test_constructor_targets_golden_file(
    *,
    lang_cls: literalizer.LanguageCls,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Every language's constructor target helper is golden-checked."""
    for version_format in lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            spec = make_spec(
                lang_cls=lang_cls,
                language_version=version_format,
            )
            check_golden(
                contents=(
                    spec.format_constructor_target(_CONSTRUCTOR_NAME) + "\n"
                ),
                extension=".txt",
                golden_path=_golden_path(
                    name=f"{lang_cls.__name__}_constructor_target",
                    lang_cls=lang_cls,
                    version=version_format,
                ),
                file_regression=file_regression,
            )


@pytest.mark.parametrize(
    argnames="case",
    argvalues=constructor_binding_cases(),
    ids=lambda case: case.name,
)
def test_constructor_binding_golden_file(
    *,
    case: ConstructorBindingCase,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Every declared constructor binding matches its golden file."""
    for version_format in case.lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            golden_path = constructor_golden_path(
                case=case, version=version_format
            )
            language = make_spec(
                lang_cls=case.lang_cls,
                language_version=version_format,
                **case.spec_overrides,
            )
            manifest = case.manifest
            config = ConstructorCaseSpec()
            source = "[[]]"
            input_format = InputFormat.JSON
            if manifest is not None:
                language = with_per_fixture_module_name(
                    spec=language, golden_path=golden_path
                )
                assert manifest.constructor is not None
                config = manifest.constructor
                source = manifest.input.path.read_text(encoding="utf-8")
                input_format = manifest.input.input_format
            with GoldenSkips(
                policy=case.skip,
                golden_path=golden_path,
                prefix=case.lang_cls.__name__,
                config=file_regression.request.config,
            ):
                result = literalize_call(
                    source=source,
                    input_format=input_format,
                    language=language,
                    target_function=language.format_constructor_target(
                        config.class_name,
                    ),
                    parameter_names=[],
                    wrap_in_file=manifest is not None,
                    variable_form=dataclasses.replace(
                        case.variable_form, name=config.variable_name
                    ),
                )
            check_golden(
                contents=result.code + "\n",
                extension=golden_path.suffix,
                golden_path=golden_path,
                file_regression=file_regression,
            )
