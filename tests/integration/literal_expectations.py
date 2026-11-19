"""Documented literal rejections resolved before rendering."""

import datetime as dt
import enum
import functools
import math
from collections.abc import Iterable, Iterator
from pathlib import Path

from beartype import beartype

import literalizer
from literalizer._formatters.format_integers import I64_MAX, I64_MIN
from literalizer._language import is_reserved_identifier, redefinition_config
from literalizer._parsing import parse_input
from literalizer._types import Value
from literalizer.exceptions import (
    ExcessiveNestingError,
    ExistingVariableNotSelfContainedError,
    InvalidNewVariableNameError,
    NullInCollectionError,
    ReservedVariableNameError,
    UnrepresentableEmptyDictError,
    UnrepresentableInputError,
    UnrepresentableSpecialFloatError,
)
from literalizer.languages import Scala
from tests.language_options import HasJsonType

from .case_manifests import case_input, load_case_manifest
from .golden_outcomes import Rejection
from .rejection_contracts import rejected_examples
from .yaml_warnings import expected_yaml_warnings


@functools.cache
def _nesting_contract() -> dict[literalizer.LanguageCls, int]:
    """Read each bounded target's first rejected depth from its
    example.
    """
    depths: dict[literalizer.LanguageCls, int] = {}
    for case in rejected_examples(
        contract="excessive_nesting", error=ExcessiveNestingError
    ):
        assert case.source is not None  # noqa: S101 - literalize example
        depths[case.lang_cls] = _collection_depth(
            data=parse_input(
                source=case.source, input_format=literalizer.InputFormat.JSON
            ).data,
        )
    return depths


@functools.cache
def _empty_mapping_contract() -> frozenset[literalizer.LanguageCls]:
    """Read which native modes conflate empty maps with sequences."""
    return frozenset(
        case.lang_cls
        for case in rejected_examples(
            contract="empty_dict_indistinct_from_sequence",
            error=UnrepresentableEmptyDictError,
        )
        # COBOL checks for loss of information in source order.
        # The presence of an empty mapping alone does not predict its error.
        if case.lang_cls.language_id != "cobol"
    )


@functools.cache
def _special_float_contract() -> frozenset[enum.Enum | None]:
    """Read which selected JSON representations require finite floats."""
    return frozenset(
        case.option_member
        for case in rejected_examples(
            contract="json_type_special_floats",
            error=UnrepresentableSpecialFloatError,
        )
    )


def _collection_depth(*, data: Value) -> int:
    """Measure the number of enclosing source containers."""
    children: Iterable[Value]
    match data:
        case dict():
            children = data.values()
        case list() | set():
            children = data
        case _:
            return 0
    return 1 + max(
        (_collection_depth(data=item) for item in children), default=0
    )


def _values(*, data: Value) -> Iterator[Value]:
    """Walk values at every depth, preserving maps as values."""
    yield data
    match data:
        case dict():
            for value in data.values():
                yield from _values(data=value)
        case list() | set():
            for value in data:
                yield from _values(data=value)
        case _:
            return


@functools.cache
def _parsed_case(*, case_dir: Path) -> Value:
    """Parse authored values without running any output formatter."""
    input_info = case_input(case_dir=case_dir)
    with expected_yaml_warnings(
        expectation=input_info.expected_reused_anchor_warning,
    ):
        return parse_input(
            source=input_info.path.read_text(encoding="utf-8"),
            input_format=input_info.input_format,
        ).data


def _representation_rejection(
    *,
    spec: literalizer.Language,
    lang_cls: literalizer.LanguageCls,
    case_dir: Path,
    substitutes_nulls: bool,
) -> Rejection | None:
    """Resolve documented representation limits against authored
    values.
    """
    json_type = spec.json_type if isinstance(spec, HasJsonType) else None
    finite_json = (
        json_type is not None and json_type in _special_float_contract()
    )
    rejected_depth = _nesting_contract().get(lang_cls)
    rejects_empty_maps = (
        json_type is None and lang_cls in _empty_mapping_contract()
    )
    if (
        substitutes_nulls
        or load_case_manifest(case_dir=case_dir).input_roundtrip is not None
    ):
        return None
    data = _parsed_case(case_dir=case_dir)
    if rejected_depth is not None and (
        _collection_depth(data=data) >= rejected_depth
    ):
        return Rejection(error=ExcessiveNestingError, match=None)
    if rejects_empty_maps and any(
        isinstance(item, dict) and len(item) == 0
        for item in _values(data=data)
    ):
        return Rejection(error=UnrepresentableEmptyDictError, match=None)
    if finite_json and any(
        isinstance(item, float) and not math.isfinite(item)
        for item in _values(data=data)
    ):
        return Rejection(error=UnrepresentableSpecialFloatError, match=None)
    return _scalar_collection_rejection(
        spec=spec, data=data, native=json_type is None
    )


def _scalar_collection_rejection(
    *, spec: literalizer.Language, data: Value, native: bool
) -> Rejection | None:
    """Check container capabilities for simple collections of scalars."""
    if (
        isinstance(data, set)
        and all(isinstance(item, (int, str)) for item in data)
        and not spec.set_format_config.preserves_set_semantics
    ):
        return Rejection(
            error=UnrepresentableInputError,
            match="cannot preserve native set semantics",
        )
    if (
        not native
        or not isinstance(data, dict)
        or spec.supports_non_string_dict_keys
        or spec.dict_format.name in {"RECORD", "ANONYMOUS_RECORD"}
    ):
        return None
    if (
        all(isinstance(item, (int, str)) for item in data.values())
        and len({type(key) for key in data}) == 1
        and all(
            isinstance(key, (dt.date, dt.time))
            or (isinstance(key, int) and I64_MIN <= key <= I64_MAX)
            for key in data
        )
    ):
        return Rejection(
            error=UnrepresentableInputError,
            match="cannot represent dict key of type",
        )
    return None


@beartype
def _assignment_requires_prior_declaration(
    *, spec: literalizer.Language, case_dir: Path
) -> bool:
    """Use the target's assignment semantics for the existing binding case."""
    return not spec.assignment_declares_binding(
        _parsed_case(case_dir=case_dir)
    )


@beartype
def literal_rejection(
    *,
    spec: literalizer.Language,
    lang_cls: literalizer.LanguageCls,
    variable_form: literalizer.VariableForm | None,
    case_dir: Path,
    substitutes_nulls: bool,
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
        return _representation_rejection(
            spec=spec,
            lang_cls=lang_cls,
            case_dir=case_dir,
            substitutes_nulls=substitutes_nulls,
        )
    return Rejection(error=expected_error, match=expected_message)
