"""Golden-file tests for the declared per-language rejections.

Each manifest under ``rejections/`` runs its call against every
language it selects and records what was raised, one line per case, in
that manifest's ``expected.txt``.  A language that joins a manifest's
gates -- a new language declaring ``json_type``, say -- shows up as a
new line rather than as silence.
"""

from typing import assert_never

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from tests.enum_members import enum_member_by_name
from tests.integration.golden_checks import check_golden

from .rejection_cases import (
    RejectionCase,
    accepting_cases,
    rejection_cases,
    selected_languages,
)
from .rejection_manifests import (
    REJECTIONS_DIR,
    CallSpec,
    RejectionManifest,
    load_rejection_manifests,
)

_MANIFESTS = load_rejection_manifests(rejections_dir=REJECTIONS_DIR)


@beartype
def _variable_form(
    *,
    call: CallSpec,
    lang_cls: literalizer.LanguageCls,
) -> literalizer.NewVariable:
    """Return the variable form a rendering case declares its value in.

    Modifiers are resolved against the language rather than declared as
    values, so a manifest naming ``CONST`` covers every language whose
    declarations take one.
    """
    modifiers = frozenset(
        enum_member_by_name(enum_cls=lang_cls.Modifiers, name=name)
        for name in call.modifiers
    )
    return literalizer.NewVariable(name="my_data", modifiers=modifiers)


@beartype
def _run(*, case: RejectionCase, call: CallSpec) -> None:
    """Make the call one case declares.

    ``source``, ``input_format`` and ``target_function`` accompany the
    APIs that take them, which the manifest's own validation enforces,
    so the seams below only restate that for the type checker.
    """
    lang_cls = case.lang_cls
    match call.api:
        case "constructor":
            lang_cls(**case.kwargs)
        case "literalize":
            assert call.source is not None
            assert call.input_format is not None
            literalizer.literalize(
                source=call.source,
                input_format=call.input_format,
                language=lang_cls(**case.kwargs),
                variable_form=_variable_form(call=call, lang_cls=lang_cls),
            )
        case "literalize_call":
            assert call.source is not None
            assert call.input_format is not None
            assert call.target_function is not None
            literalizer.literalize_call(
                source=call.source,
                input_format=call.input_format,
                language=lang_cls(**case.kwargs),
                target_function=call.target_function,
                parameter_names=list(call.parameter_names),
            )
        case _ as unreachable:
            assert_never(unreachable)


@pytest.mark.parametrize(
    argnames="manifest",
    argvalues=_MANIFESTS,
    ids=[manifest.name for manifest in _MANIFESTS],
)
def test_rejection_messages(
    manifest: RejectionManifest,
    file_regression: FileRegressionFixture,
) -> None:
    """Every selected language raises, with the golden file's message."""
    accepting = len(manifest.accepting_languages)
    header = (
        f"# languages rejecting: "
        f"{len(selected_languages(manifest=manifest)) - accepting}"
        f"; languages accepting: {accepting}"
    )
    lines: list[str] = [header, ""]
    for case in rejection_cases(manifest=manifest):
        with pytest.raises(expected_exception=manifest.exceptions) as caught:
            _run(case=case, call=manifest.call)
        raised = caught.value
        lines.append(f"{case.case_id} -> {type(raised).__name__}: {raised}")
    check_golden(
        contents="".join(f"{line}\n" for line in lines),
        extension=".txt",
        golden_path=manifest.golden_path,
        file_regression=file_regression,
    )


@pytest.mark.parametrize(
    argnames="manifest",
    argvalues=_MANIFESTS,
    ids=[manifest.name for manifest in _MANIFESTS],
)
def test_accepting_languages_still_accept(
    manifest: RejectionManifest,
) -> None:
    """Every language a manifest records as accepting still accepts.

    An ``accepts`` entry is the manifest's record of a language its
    gates admit that represents the input rather than refusing it.
    Running the same call for those languages is what keeps the record
    honest: a language that starts rejecting fails here rather than
    sitting in the file as a stale reason.
    """
    for case in accepting_cases(manifest=manifest):
        _run(case=case, call=manifest.call)
