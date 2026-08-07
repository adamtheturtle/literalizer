"""Golden-file tests that drive :func:`literalizer.literalize`.

Every scenario declared in :mod:`golden_scenarios` -- single
declaration form, combined declaration + assignment, format-variant
kwargs, statement-terminator option, heterogeneous-scalar strategy,
``pre_indent_level`` -- shares the one runner below: render a case
input to a language and compare against a checked-in golden file.

Each rendering covers every member of its language's
``VersionFormats``, bar a spec that pins its own version, so adding a
second member to a language's enum automatically produces a parallel
set of golden files.
"""

import enum
from pathlib import Path
from typing import NoReturn

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer.exceptions import VariableNameNotSupportedError

from .case_inputs import CaseInput
from .case_manifests import case_input
from .golden_scenarios import (
    GoldenGroup,
    GoldenRendering,
    SkipReasons,
    golden_groups,
)
from .language_specs import make_golden_path, with_per_fixture_module_name

_GROUPS = golden_groups()


@beartype
def _skip_unrepresentable(
    *,
    exc: Exception,
    reasons: SkipReasons,
    golden_path: Path,
    prefix: str,
    suffix: str,
) -> NoReturn:
    """Skip the current test with a message keyed off the caught error.

    The message reads ``"{prefix} {reason}{suffix}"``, so a rendering
    whose skip turns on more than the error type -- the strategy it was
    rendered under, say -- says so in *suffix* rather than restating the
    reason.  The ``except`` clause is built from the same table, so the
    lookup below is total by construction; ``StopIteration`` propagating
    out of this helper would indicate a divergence between the two.
    """
    entry = next(entry for entry in reasons if isinstance(exc, entry.error))
    if entry.unlink:
        golden_path.unlink(missing_ok=True)
    pytest.skip(f"{prefix} {entry.reason}{suffix}")


@beartype
def _literalize(
    *,
    rendering: GoldenRendering,
    spec: literalizer.Language,
    input_info: CaseInput,
    source_text: str,
    variable_form: literalizer.VariableForm | None,
) -> literalizer.LiteralizeResult:
    """Render one case input under *spec*.

    *variable_form* is passed rather than read off *rendering* so the
    caller can retry without one, which is the only way a language that
    cannot name a variable reaches its golden.
    """
    render = rendering.render
    return literalizer.literalize(
        source=source_text,
        input_format=input_info.input_format,
        language=spec,
        pre_indent_level=render.pre_indent_level,
        include_delimiters=True,
        variable_form=variable_form,
        wrap_in_file=True,
        collection_layout=render.collection_layout,
        record_null_substitutions=render.record_null_substitutions,
    )


@beartype
def _check_rendering(
    *,
    rendering: GoldenRendering,
    spec: literalizer.Language,
    version: enum.Enum,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Render one golden file and compare it against its fixture."""
    input_info = case_input(case_dir=cases_dir / rendering.case_dir_name)
    source_text = input_info.path.read_text(encoding="utf-8")
    golden_path = make_golden_path(
        parent=input_info.path.parent,
        name=rendering.golden_name,
        extension=spec.extension,
        lang_cls=rendering.lang_cls,
        version=version,
    )
    spec = with_per_fixture_module_name(spec=spec, golden_path=golden_path)
    try:
        try:
            result = _literalize(
                rendering=rendering,
                spec=spec,
                input_info=input_info,
                source_text=source_text,
                variable_form=rendering.render.variable_form,
            )
        except VariableNameNotSupportedError:
            result = _literalize(
                rendering=rendering,
                spec=spec,
                input_info=input_info,
                source_text=source_text,
                variable_form=None,
            )
    except rendering.skip_errors as exc:
        _skip_unrepresentable(
            exc=exc,
            reasons=rendering.skip.reasons,
            golden_path=golden_path,
            prefix=rendering.lang_cls.__name__,
            suffix=rendering.skip.suffix,
        )
    # newline="" prevents Python text-mode from converting \r\n to \n on
    # Windows, which would corrupt golden files containing literal CR
    # bytes (e.g. CommonLisp string_control_chars).
    file_regression.check(
        contents=rendering.fixture_prefix + result.code + "\n",
        encoding="utf-8",
        extension=spec.extension,
        newline="",
        fullpath=golden_path,
    )


@pytest.mark.parametrize(
    argnames="group",
    argvalues=_GROUPS,
    ids=[group.test_id for group in _GROUPS],
)
def test_golden_file(
    group: GoldenGroup,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Every declared rendering matches its checked-in golden file."""
    for rendering in group.renderings:
        for version in rendering.versions:
            spec = rendering.spec_for(version=version)
            # A spec keyword may pin a required version (Java ``RECORD``
            # needs ``JDK_16``); skip the iterations it overrides so
            # only the pinned version's golden is generated and
            # lint-checked.
            if spec.language_version is not version:
                continue
            with subtests.test(
                golden_name=rendering.golden_name,
                case_dir_name=rendering.case_dir_name,
                version=version.name,
            ):
                _check_rendering(
                    rendering=rendering,
                    spec=spec,
                    version=version,
                    cases_dir=cases_dir,
                    file_regression=file_regression,
                )
