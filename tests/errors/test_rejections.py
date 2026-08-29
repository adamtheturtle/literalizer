"""Golden-file tests for the declared per-language rejections.

Each manifest under ``rejections/`` runs its call against every
language it selects and records what was raised in that manifest's
``expected.toml``: a table per exception type, a line per case.  A
language that joins a manifest's gates -- a new language declaring
``json_type``, say -- shows up as a new line rather than as silence.
"""

from typing import Any, assert_never

import pytest
import tomlkit
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
    substituted,
)

_MANIFESTS = load_rejection_manifests(rejections_dir=REJECTIONS_DIR)


@beartype
def _variable_form(
    *,
    call: CallSpec,
    lang_cls: literalizer.LanguageCls,
    value: str | None,
) -> (
    literalizer.NewVariable
    | literalizer.ExistingVariable
    | literalizer.BothVariableForms
    | None
):
    """Return the variable form a rendering case declares its value in.

    Modifiers are resolved against the language rather than declared as
    values, so a manifest naming ``CONST`` covers every language whose
    declarations take one.  A language with no named variables to bind
    to renders the value on its own, which is the only form it has.
    """
    name = substituted(template=call.variable_name, value=value)
    modifiers = frozenset(
        enum_member_by_name(enum_cls=lang_cls.Modifiers, name=modifier_name)
        for modifier_name in call.modifiers
    )
    match call.variable_form:
        case "new":
            return literalizer.NewVariable(
                name=name,
                modifiers=frozenset(),
            )
        case "existing":
            return literalizer.ExistingVariable(name=name)
        case "both":
            return literalizer.BothVariableForms(
                name=name,
                modifiers=modifiers,
            )
        case None:
            if not lang_cls.supports_variable_names:
                return None
            return literalizer.NewVariable(
                name="my_data",
                modifiers=modifiers,
            )
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _run(*, case: RejectionCase, call: CallSpec) -> None:
    """Make the call one case declares.

    A source, ``input_format`` and ``target_function`` accompany the
    APIs that take them, which the manifest's own validation enforces,
    so the seams below only restate that for the type checker.
    """
    lang_cls = case.lang_cls
    variable_form = _variable_form(
        call=call,
        lang_cls=lang_cls,
        value=case.value,
    )
    ref_case = None
    if call.ref_case is not None:
        resolved_ref_case = enum_member_by_name(
            enum_cls=literalizer.IdentifierCase,
            name=call.ref_case,
        )
        assert isinstance(resolved_ref_case, literalizer.IdentifierCase)
        ref_case = resolved_ref_case
    match call.api:
        case "constructor":
            lang_cls(**case.kwargs)
        case "literalize":
            assert case.source is not None
            assert call.input_format is not None
            literalizer.literalize(
                source=case.source,
                input_format=call.input_format,
                language=lang_cls(**case.kwargs),
                variable_form=variable_form,
                wrap_in_file=call.wrap_in_file,
                pre_indent_level=call.pre_indent_level,
                include_delimiters=call.include_delimiters,
                ref_key=call.ref_key,
                ref_case=ref_case,
                bound_refs=dict(call.bound_refs) or None,
            )
        case "literalize_call":
            assert case.source is not None
            assert call.input_format is not None
            assert call.target_function is not None
            if "parameter_names_bare" in call.model_fields_set:
                parameter_names: Any = call.parameter_names_bare
            else:
                parameter_names = [
                    substituted(template=name, value=case.value)
                    for name in call.parameter_names
                ]
            if "comment_source_bare" in call.model_fields_set:
                comment_source: Any = call.comment_source_bare
            else:
                comment_source = call.comment_source
            literalizer.literalize_call(
                source=case.source,
                input_format=call.input_format,
                language=lang_cls(**case.kwargs),
                target_function=substituted(
                    template=call.target_function,
                    value=case.value,
                ),
                parameter_names=parameter_names,
                per_element=call.per_element,
                wrap_in_file=call.wrap_in_file,
                ref_key=call.ref_key,
                ref_case=ref_case,
                bound_refs=dict(call.bound_refs) or None,
                comment_source=comment_source,
                variable_form=(
                    variable_form if call.variable_form is not None else None
                ),
            )
        case _ as unreachable_call:  # pragma: no cover
            assert_never(unreachable_call)


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
    messages_by_exception: dict[str, dict[str, str]] = {}
    for case in rejection_cases(manifest=manifest):
        with pytest.raises(expected_exception=manifest.exceptions) as caught:
            _run(case=case, call=manifest.call)
        raised = caught.value
        raised_by = messages_by_exception.setdefault(type(raised).__name__, {})
        raised_by[case.case_id] = str(object=raised)
    accepting = len(manifest.accepting_languages)
    document = tomlkit.document()
    document.add(
        key=tomlkit.comment(
            string=(
                f"languages rejecting: "
                f"{len(selected_languages(manifest=manifest)) - accepting}"
                f"; languages accepting: {accepting}"
            ),
        ),
    )
    # One table per exception type, so a language raising a different
    # one from the rest of its family stands out as its own table
    # rather than as a word buried in a line.
    for exception_name in sorted(messages_by_exception):
        table = tomlkit.table()
        for case_id, message in messages_by_exception[exception_name].items():
            table[case_id] = message
        document[exception_name] = table
    check_golden(
        contents=tomlkit.dumps(data=document),
        extension=".toml",
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
