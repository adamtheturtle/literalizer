"""Documented literal rejections resolved before rendering."""

from pathlib import Path

from beartype import beartype

import literalizer
from literalizer._language import is_reserved_identifier, redefinition_config
from literalizer._parsing import parse_input
from literalizer.exceptions import (
    ExistingVariableNotSelfContainedError,
    InvalidNewVariableNameError,
    NullInCollectionError,
    ReservedVariableNameError,
)
from literalizer.languages import Scala

from .case_manifests import case_input
from .golden_outcomes import Rejection


@beartype
def _assignment_requires_prior_declaration(
    *, spec: literalizer.Language, case_dir: Path
) -> bool:
    """Use the target's assignment semantics for the existing binding case."""
    input_info = case_input(case_dir=case_dir)
    data = parse_input(
        source=input_info.path.read_text(encoding="utf-8"),
        input_format=input_info.input_format,
    ).data
    return not spec.assignment_declares_binding(data)


@beartype
def literal_rejection(
    *,
    spec: literalizer.Language,
    variable_form: literalizer.VariableForm | None,
    case_dir: Path,
) -> Rejection | None:
    """Resolve documented identifier and fixture compatibility errors."""
    expected_error: type[Exception] | None = None
    expected_message = ""
    if isinstance(variable_form, literalizer.BothVariableForms) and not (
        redefinition_config(spec.declaration_style).supports_redefinition
    ):
        expected_error = ValueError
        expected_message = "BothVariableForms requires a declaration_style"
    elif variable_form is not None and (
        is_reserved_identifier(
            case_sensitive=spec.reserved_variable_identifiers_case_sensitive,
            name=variable_form.name,
            reserved_identifiers=spec.reserved_variable_identifiers,
        )
        or (
            spec.reserved_variable_identifier_pattern is not None
            and spec.reserved_variable_identifier_pattern.fullmatch(
                string=variable_form.name
            )
            is not None
        )
    ):
        expected_error = ReservedVariableNameError
        expected_message = "reserved"
    elif variable_form is not None and not (
        spec.new_variable_name_syntax.accepts(name=variable_form.name)
    ):
        expected_error = InvalidNewVariableNameError
        expected_message = "it is not a valid identifier"
    elif (
        isinstance(spec, Scala)
        and spec.sequence_format is Scala.SequenceFormats["ARRAY"]
        and case_dir.name == "simple_sequence"
    ):
        expected_error = NullInCollectionError
        expected_message = "Array cannot contain null elements"
    elif (
        isinstance(variable_form, literalizer.ExistingVariable)
        and case_dir.name == "existing_variable_self_declaring"
        and _assignment_requires_prior_declaration(
            spec=spec, case_dir=case_dir
        )
    ):
        expected_error = ExistingVariableNotSelfContainedError
        expected_message = "the assignment has no prior declaration"
    if expected_error is None:
        return None
    return Rejection(error=expected_error, match=expected_message)
