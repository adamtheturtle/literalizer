"""Golden-file tests for the declared per-language rejections.

Each manifest under ``rejections/`` runs its call against every
language it selects and records what was raised in that manifest's
``expected.toml``: a table per exception type, a line per case.  A
language that joins a manifest's gates -- a new language declaring
``json_type``, say -- shows up as a new line rather than as silence.

A message may instead declare an inline table with ``default`` and
Python ``major.minor`` overrides. Each runtime checks its exact message;
regeneration preserves entries for every other Python version.
"""

import re
import sys
import tomllib
from collections.abc import Callable
from pathlib import Path
from typing import assert_never

import pytest
import tomlkit
from beartype import beartype
from pydantic import ConfigDict, TypeAdapter
from pytest_regressions.file_regression import FileRegressionFixture
from ruamel.yaml import YAML
from tomlkit.items import InlineTable

import literalizer
from literalizer.exceptions import ParseError
from literalizer.languages import Python
from tests.enum_members import enum_member_by_name
from tests.integration.case_manifests import CallTransform
from tests.integration.golden_checks import check_golden
from tests.yaml_support import as_yaml_parser

from .rejection_cases import (
    RejectionCase,
    accepting_cases,
    rejection_cases,
    selected_languages,
)
from .rejection_manifests import (
    LANGUAGES_BY_NAME,
    REJECTIONS_DIR,
    CallSpec,
    ErrorAttributes,
    RejectionManifest,
    load_rejection_manifests,
    substituted,
)

_MANIFESTS = load_rejection_manifests(rejections_dir=REJECTIONS_DIR)

_BOUND_VALUE = TypeAdapter[literalizer.ValueInput](
    type=literalizer.ValueInput,
    config=ConfigDict(arbitrary_types_allowed=True),
)


type ExpectedMessage = str | dict[str, str]
type ExpectedMessages = dict[str, dict[str, ExpectedMessage]]

_EXPECTED_MESSAGES = TypeAdapter[ExpectedMessages](type=ExpectedMessages)


@beartype
def _load_expected_messages(*, golden_path: Path) -> ExpectedMessages:
    """Read messages and validate each optional Python-version map."""
    if not golden_path.exists():
        return {}
    expected = _EXPECTED_MESSAGES.validate_python(
        tomllib.loads(golden_path.read_text(encoding="utf-8")), strict=True
    )
    for cases in expected.values():
        for message in cases.values():
            if isinstance(message, dict):
                if "default" not in message:
                    msg = "a versioned message requires a default"
                    raise ValueError(msg)
                for version in message:
                    if (
                        version != "default"
                        and re.fullmatch(
                            pattern=r"[0-9]+\.[0-9]+", string=version
                        )
                        is None
                    ):
                        msg = f"invalid Python version key: {version!r}"
                        raise ValueError(msg)
    return expected


@beartype
def _message_golden(
    *, message: str, expected: ExpectedMessage | None, python_version: str
) -> str | InlineTable:
    """Record the active runtime while retaining other exact messages."""
    if not isinstance(expected, dict):
        return message
    active = python_version if python_version in expected else "default"
    variants = tomlkit.inline_table()
    for version, text in expected.items():
        variants[version] = message if version == active else text
    return variants


@beartype
def _rejection_document(
    *,
    messages_by_exception: dict[str, dict[str, str]],
    expected: ExpectedMessages,
    rejecting: int,
    accepting: int,
    python_version: str,
) -> str:
    """Build observed case tables, preserving inactive message
    variants.
    """
    document = tomlkit.document()
    _ = document.add(
        key=tomlkit.comment(
            string=(
                f"languages rejecting: {rejecting}; "
                f"languages accepting: {accepting}"
            ),
        ),
    )
    for exception_name in sorted(messages_by_exception):
        table = tomlkit.table()
        previous_cases = expected.get(exception_name, {})
        for case_id, message in messages_by_exception[exception_name].items():
            table[case_id] = _message_golden(
                message=message,
                expected=previous_cases.get(case_id),
                python_version=python_version,
            )
        document[exception_name] = table
    return tomlkit.dumps(data=document)


@beartype
def _yaml_reference_values(
    *, sources: tuple[tuple[str, str], ...], value: str | None
) -> dict[str, literalizer.ValueInput] | None:
    """Resolve manifest-owned native YAML bindings or inference hints."""
    values: dict[str, literalizer.ValueInput] = {}
    for name, source in sources:
        parser = as_yaml_parser(parser=YAML(typ="safe"))
        values[name] = _BOUND_VALUE.validate_python(
            parser.load(stream=substituted(template=source, value=value)),
            strict=True,
        )
    return values if len(values) > 0 else None


@beartype
def _bound_refs(
    *, call: CallSpec, value: str | None
) -> dict[str, literalizer.ValueInput] | None:
    """Resolve scalar bindings and manifest-owned native YAML values."""
    bindings: dict[str, literalizer.ValueInput] = dict(call.bound_refs)
    bindings.update(call.bound_ref_times)
    yaml_bindings = _yaml_reference_values(
        sources=call.bound_ref_yaml, value=value
    )
    if yaml_bindings is not None:
        bindings.update(yaml_bindings)
    return bindings if len(bindings) > 0 else None


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
    Explicit ``none`` renders a bare value even for languages with names;
    an omitted form preserves the legacy default declaration.
    """
    name = substituted(template=call.variable_name, value=value)
    modifier_cls = (
        lang_cls
        if call.modifier_language is None
        else LANGUAGES_BY_NAME[call.modifier_language]
    )
    modifiers = frozenset(
        enum_member_by_name(
            enum_cls=modifier_cls.Modifiers, name=modifier_name
        )
        for modifier_name in call.modifiers
    )
    match call.variable_form:
        case "none":
            return None
        case "new":
            return literalizer.NewVariable(
                name=name,
                modifiers=modifiers,
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
def _call_transform(
    *, template: str | None
) -> Callable[[literalizer.CallContext], str] | None:
    """Build the callable represented by a manifest template."""
    if template is None:
        return None
    return CallTransform(template=template)


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
    if call.api == "constructor":
        _ = lang_cls(**case.kwargs)
        return
    if call.api == "literalize":
        assert case.source is not None
        assert call.input_format is not None
        _ = literalizer.literalize(
            source=case.source,
            input_format=call.input_format,
            language=lang_cls(**case.kwargs),
            variable_form=variable_form,
            wrap_in_file=call.wrap_in_file,
            pre_indent_level=call.pre_indent_level,
            include_delimiters=call.include_delimiters,
            ref_key=call.ref_key,
            ref_case=ref_case,
            bound_refs=_bound_refs(call=call, value=case.value),
            ref_values=_yaml_reference_values(
                sources=call.ref_value_yaml, value=case.value
            ),
        )
        return
    assert case.source is not None
    assert call.input_format is not None
    assert call.target_function is not None
    parameter_names: str | list[str]
    if "parameter_names_bare" in call.model_fields_set:
        parameter_names = call.parameter_names_bare
    else:
        parameter_names = [
            substituted(template=name, value=case.value)
            for name in call.parameter_names
        ]
    comment_source: str | tuple[str, ...] | None
    if "comment_source_bare" in call.model_fields_set:
        comment_source = call.comment_source_bare
    else:
        comment_source = call.comment_source
    effective_variable_form = None
    if call.variable_form is not None:
        effective_variable_form = variable_form
    _ = literalizer.literalize_call(
        source=case.source,
        input_format=call.input_format,
        input_root_key=call.input_root_key,
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
        bound_refs=_bound_refs(call=call, value=case.value),
        ref_values=_yaml_reference_values(
            sources=call.ref_value_yaml, value=case.value
        ),
        comment_source=comment_source,
        variable_form=(effective_variable_form),
        call_transform=_call_transform(template=call.call_transform),
        zip_source=call.zip_source,
        zip_input_format=call.zip_input_format,
    )


@pytest.mark.parametrize(
    argnames="manifest",
    argvalues=_MANIFESTS,
    ids=lambda manifest: manifest.name,
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
        if manifest.position is not None:
            assert isinstance(raised, ParseError)
            assert (raised.line, raised.column) == manifest.position
        if manifest.attributes is not None:
            actual_attributes = ErrorAttributes.model_validate(
                obj=raised, from_attributes=True, strict=True
            ).model_dump(include=manifest.attributes.model_fields_set)
            assert actual_attributes == manifest.attributes.model_dump(
                exclude_unset=True
            )
        raised_by = messages_by_exception.setdefault(type(raised).__name__, {})
        raised_by[case.case_id] = str(object=raised)
    accepting = len(manifest.accepting_languages)
    check_golden(
        contents=_rejection_document(
            messages_by_exception=messages_by_exception,
            expected=_load_expected_messages(golden_path=manifest.golden_path),
            rejecting=len(selected_languages(manifest=manifest)) - accepting,
            accepting=accepting,
            python_version=f"{sys.version_info.major}.{sys.version_info.minor}",
        ),
        extension=".toml",
        golden_path=manifest.golden_path,
        file_regression=file_regression,
    )


@pytest.mark.parametrize(
    argnames="manifest",
    argvalues=_MANIFESTS,
    ids=lambda manifest: manifest.name,
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


@pytest.mark.parametrize(
    argnames=("declaration", "expected"),
    argvalues=[
        ({}, literalizer.NewVariable(name="my_data", modifiers=frozenset())),
        ({"variable_form": "none"}, None),
    ],
)
def test_explicit_absence_preserves_omitted_default(
    declaration: dict[str, str],
    expected: literalizer.NewVariable | None,
) -> None:
    """An explicit bare value differs from the legacy implicit declaration."""
    call = CallSpec.model_validate(
        obj={
            "api": "literalize",
            "sources": ["1"],
            "input_format": "json",
            **declaration,
        },
    )
    assert _variable_form(call=call, lang_cls=Python, value=None) == expected


@pytest.mark.parametrize(
    argnames=("source", "error", "message"),
    argvalues=[
        (
            '[Error]\ncase = { "3.12" = "old" }',
            ValueError,
            "requires a default",
        ),
        (
            '[Error]\ncase = { default = "new", py312 = "old" }',
            ValueError,
            "invalid Python version key",
        ),
        (
            '[Error]\ncase = { default = "new", "3.12.1" = "old" }',
            ValueError,
            "invalid Python version key",
        ),
        ("[Error]\ncase = { default = 1 }", ValueError, "valid string"),
        ("[Error]\ncase = 1", ValueError, "valid string"),
    ],
)
def test_invalid_versioned_message_is_rejected(
    source: str, error: type[Exception], message: str, tmp_path: Path
) -> None:
    """Malformed message variants cannot silently bypass comparison."""
    golden_path = tmp_path / "expected.toml"
    _ = golden_path.write_text(data=source, encoding="utf-8")
    with pytest.raises(expected_exception=error, match=message):
        _ = _load_expected_messages(golden_path=golden_path)


def test_missing_message_golden_can_be_generated(tmp_path: Path) -> None:
    """A new family starts with plain messages until variants are declared."""
    assert (
        _load_expected_messages(golden_path=tmp_path / "expected.toml") == {}
    )


@pytest.mark.parametrize(
    argnames=("version", "active"),
    argvalues=[("3.12", "3.12"), ("3.13", "default"), ("3.99", "default")],
)
def test_versioned_messages_preserve_inactive_variants(
    version: str, active: str, tmp_path: Path
) -> None:
    """Regeneration changes only the active exact message and drops stale
    cases.
    """
    golden_path = tmp_path / "expected.toml"
    _ = golden_path.write_text(
        data=(
            '[Error]\nvariant = { default = "modern", "3.12" = "older" }\n'
            'plain = "old"\nstale = "deleted case"\n'
            '[StaleError]\ncase = "deleted exception"\n'
        ),
        encoding="utf-8",
    )
    expected = _load_expected_messages(golden_path=golden_path)
    document = _rejection_document(
        messages_by_exception={
            "Error": {"variant": "actual", "plain": "actual", "new": "actual"}
        },
        expected=expected,
        rejecting=1,
        accepting=0,
        python_version=version,
    )
    variants = {"default": "modern", "3.12": "older"}
    variants[active] = "actual"
    assert tomllib.loads(document) == {
        "Error": {"variant": variants, "plain": "actual", "new": "actual"}
    }
    assert expected["Error"]["variant"] == {
        "default": "modern",
        "3.12": "older",
    }
