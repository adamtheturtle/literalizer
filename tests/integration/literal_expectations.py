"""Documented literal rejections resolved before rendering."""

import dataclasses
import datetime as dt
import enum
import functools
import math
from collections.abc import Iterable, Iterator, Mapping
from pathlib import Path

from beartype import beartype

import literalizer
from literalizer._checks import (
    has_heterogeneous,
    has_heterogeneous_sibling_lists,
    has_mixed_dict_list_depths,
    has_unwrappable_value_mix,
)
from literalizer._formatters.format_integers import I64_MAX, I64_MIN
from literalizer._language import is_reserved_identifier, redefinition_config
from literalizer._literalize import (
    materialize_value_mapping,
    substitute_record_nulls,
)
from literalizer._parsing import parse_input
from literalizer._types import OrderedMap, Value
from literalizer.exceptions import (
    ExcessiveNestingError,
    ExistingVariableNotSelfContainedError,
    InvalidNewVariableNameError,
    NullInCollectionError,
    ReservedVariableNameError,
    UnrepresentableEmptyDictError,
    UnrepresentableInputError,
    UnrepresentableNullError,
    UnrepresentableSpecialFloatError,
)
from literalizer.languages import (
    Bash,
    Erlang,
    Java,
    Mojo,
    OCaml,
    Scala,
    SystemVerilog,
    Tcl,
    Toml,
    V,
)
from tests.language_options import HasJsonType

from .case_inputs import CaseInput
from .case_manifests import load_case_manifest
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


@dataclasses.dataclass(frozen=True, kw_only=True)
class _LiteralSource:
    """The effective source text and input metadata for a literal case."""

    input_info: CaseInput
    source_text: str


@functools.cache
def literal_source(*, case_dir: Path) -> _LiteralSource:
    """Resolve the source and input format used by the literal runner."""
    manifest = load_case_manifest(case_dir=case_dir)
    input_info = manifest.input
    source_text = input_info.path.read_text(encoding="utf-8")
    roundtrip = manifest.input_roundtrip
    if roundtrip is not None:
        with expected_yaml_warnings(
            expectation=input_info.expected_reused_anchor_warning,
        ):
            source_text = literalizer.literalize(
                source=source_text,
                input_format=input_info.input_format,
                language=roundtrip.language(),
            ).code
        input_info = dataclasses.replace(
            input_info,
            input_format=roundtrip.input_format,
            expected_reused_anchor_warning=None,
        )
    return _LiteralSource(input_info=input_info, source_text=source_text)


@functools.cache
def _parsed_case(*, case_dir: Path) -> Value:
    """Parse the source passed to the target API."""
    source = literal_source(case_dir=case_dir)
    with expected_yaml_warnings(
        expectation=source.input_info.expected_reused_anchor_warning,
    ):
        return parse_input(
            source=source.source_text,
            input_format=source.input_info.input_format,
        ).data


def _effective_case(
    *,
    case_dir: Path,
    substitutions: Mapping[str, literalizer.ValueInput] | None,
) -> Value:
    """Read the authored value after the rendering's null
    substitutions.
    """
    data = _parsed_case(case_dir=case_dir)
    if substitutions is None:
        return data
    return substitute_record_nulls(
        data=data,
        substitutions=materialize_value_mapping(
            values=substitutions,
            argument_name="record_null_substitutions",
        ),
    )


def _has_only_nulls(*, items: Iterable[Value]) -> bool:
    """Check whether a nonempty container has no type-bearing value."""
    values = tuple(items)
    return len(values) > 0 and all(value is None for value in values)


def _has_record_element(*, items: list[Value]) -> bool:
    """Find ordinary mappings that select Scala's record array opener."""
    return any(
        (isinstance(item, dict) and not isinstance(item, OrderedMap))
        or (isinstance(item, list) and _has_record_element(items=item))
        for item in items
    )


def _null_rejection(
    *,
    spec: literalizer.Language,
    case_dir: Path,
    substitutions: Mapping[str, literalizer.ValueInput] | None,
) -> Rejection | None:
    """Resolve null collection limits for the selected native carrier."""
    if not isinstance(spec, Java | Mojo | Scala | V):
        return None
    data = _effective_case(case_dir=case_dir, substitutions=substitutions)
    message = _null_rejection_message(spec=spec, data=data)
    if message is None:
        return None
    return Rejection(error=NullInCollectionError, match=message)


def _mojo_rejects_null_list(
    *, spec: Mojo, data: Value, null_lists: list[list[Value]]
) -> bool:
    """Account for checks before Mojo constructs a list."""
    # Scalar wrapping cannot reconcile a container with a scalar in
    # the same slot, even under the VARIANT strategy.
    if any(
        has_unwrappable_value_mix(
            data=data,
            container_type=container,
            excluded_container_ids=frozenset(),
        )
        for container in (dict, list)
    ):
        return False
    if spec.heterogeneous_strategy is Mojo.HeterogeneousStrategies["VARIANT"]:
        return True
    # Default inference checks the collection's shape and its sibling
    # element types before it asks the list factory for delimiters.
    return any(_has_only_nulls(items=items) for items in null_lists) and not (
        has_heterogeneous(
            data=data, record_dict_ids=frozenset(), tuple_list_ids=frozenset()
        )
        or has_heterogeneous_sibling_lists(
            data=data, record_dict_ids=frozenset(), tuple_list_ids=frozenset()
        )
        or has_mixed_dict_list_depths(data=data, record_dict_ids=frozenset())
    )


def _scala_rejects_null_list(
    *, spec: Scala, data: Value, null_lists: list[list[Value]]
) -> bool:
    """Check which lists reach Scala's native typed array opener."""
    if spec.sequence_format is not Scala.SequenceFormats["ARRAY"]:
        return False
    behavior = spec.heterogeneous_behavior
    tuple_ids = behavior.compute_tuple_list_ids
    excluded_ids = frozenset[int]() if tuple_ids is None else tuple_ids(data)
    return any(
        id(items) not in excluded_ids
        and (
            behavior.render_record_literal is None
            or not _has_record_element(items=items)
        )
        for items in null_lists
    )


def _null_rejection_message(
    *, spec: Java | Mojo | Scala | V, data: Value
) -> str | None:
    """Distinguish native list factories and V's all-null inference."""
    if isinstance(spec, V):
        rejects_nulls = (
            spec.heterogeneous_strategy is V.HeterogeneousStrategies["ERROR"]
            and any(
                _has_only_nulls(
                    items=item.values() if isinstance(item, dict) else item
                )
                for item in _values(data=data)
                if isinstance(item, (dict, list, set))
            )
        )
        return "V cannot infer an element type" if rejects_nulls else None

    null_lists = [
        item
        for item in _values(data=data)
        if isinstance(item, list) and any(child is None for child in item)
    ]
    if len(null_lists) == 0:
        return None
    if isinstance(spec, Mojo):
        rejects_nulls = _mojo_rejects_null_list(
            spec=spec, data=data, null_lists=null_lists
        )
        return (
            "Mojo's list literal cannot contain null elements"
            if rejects_nulls
            else None
        )

    if spec.json_type is not None:
        return None
    if isinstance(spec, Java):
        # The native map factory and option compatibility are validated
        # before the list factory runs.
        rejects_nulls = (
            spec.sequence_format is Java.SequenceFormats["LIST"]
            and spec.heterogeneous_strategy
            is Java.HeterogeneousStrategies["ERROR"]
            and all(
                all(child is not None for child in item.values())
                for item in _values(data=data)
                if isinstance(item, dict)
            )
        )
        return (
            r"Java's List\.of\(\) does not accept null elements"
            if rejects_nulls
            else None
        )

    rejects_nulls = _scala_rejects_null_list(
        spec=spec, data=data, null_lists=null_lists
    )
    return (
        "Scala's Array cannot contain null elements" if rejects_nulls else None
    )


def _additional_representation_rejection(
    *,
    spec: literalizer.Language,
    case_dir: Path,
    substitutions: Mapping[str, literalizer.ValueInput] | None,
) -> Rejection | None:
    """Resolve constraints shared by multiple authored fixtures."""
    data = _effective_case(case_dir=case_dir, substitutions=substitutions)
    if isinstance(spec, Bash | Tcl | SystemVerilog | Toml):
        rejection = _null_value_rejection(spec=spec, data=data)
        if rejection is not None:
            return rejection
    if _uses_integer_epoch_seconds(spec=spec) and any(
        isinstance(value, dt.datetime) and _has_fractional_epoch(value=value)
        for value in _values(data=data)
    ):
        return Rejection(
            error=UnrepresentableInputError,
            match=(
                "integer Unix epoch seconds cannot preserve fractional "
                "datetime precision"
            ),
        )
    if any(isinstance(value, set) for value in _values(data=data)) and (
        not spec.set_format_config.preserves_set_semantics
    ):
        return Rejection(
            error=UnrepresentableInputError,
            match="cannot preserve native set semantics",
        )
    return None


def _uses_integer_epoch_seconds(*, spec: literalizer.Language) -> bool:
    """Account for JSON carriers that always encode datetimes as text."""
    return spec.datetime_format.name == "EPOCH" and not (
        isinstance(spec, Erlang | OCaml | Scala) and spec.json_type is not None
    )


def _has_fractional_epoch(*, value: dt.datetime) -> bool:
    """Check the fraction after converting the authored wall time to
    UTC.
    """
    offset = value.utcoffset()
    return value.microsecond != (0 if offset is None else offset.microseconds)


def _null_value_rejection(
    *, spec: Bash | Tcl | SystemVerilog | Toml, data: Value
) -> Rejection | None:
    """Apply the target's null contract to values and mapping keys."""
    values = tuple(_values(data=data))
    has_null_value = None in values
    if isinstance(spec, Bash | Tcl):
        if has_null_value or any(
            isinstance(value, dict) and None in value for value in values
        ):
            return Rejection(
                error=UnrepresentableNullError,
                match="cannot represent null distinctly from the empty string",
            )
    elif has_null_value:
        return Rejection(
            error=UnrepresentableInputError,
            match=(
                "cannot represent null distinctly from an empty string"
                if isinstance(spec, SystemVerilog)
                else "TOML cannot represent null values"
            ),
        )
    return None


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
def literal_rejection(
    *,
    spec: literalizer.Language,
    lang_cls: literalizer.LanguageCls,
    variable_form: literalizer.VariableForm | None,
    case_dir: Path,
    substitutions: Mapping[str, literalizer.ValueInput] | None,
    wrap_in_file: bool,
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
        isinstance(variable_form, literalizer.ExistingVariable)
        and wrap_in_file
        and not spec.assignment_declares_binding(
            _effective_case(case_dir=case_dir, substitutions=substitutions)
        )
    ):
        expected_error = ExistingVariableNotSelfContainedError
        expected_message = "the assignment has no prior declaration"
    if expected_error is not None:
        return Rejection(error=expected_error, match=expected_message)
    rejection = _representation_rejection(
        spec=spec,
        lang_cls=lang_cls,
        case_dir=case_dir,
        substitutes_nulls=substitutions is not None,
    )
    if rejection is not None:
        return rejection
    null_rejection = _null_rejection(
        spec=spec, case_dir=case_dir, substitutions=substitutions
    )
    if null_rejection is not None:
        return null_rejection
    return _additional_representation_rejection(
        spec=spec, case_dir=case_dir, substitutions=substitutions
    )
