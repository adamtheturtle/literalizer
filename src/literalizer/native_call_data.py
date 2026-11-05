"""Decode native invocation recipes without source interpolation."""

import dataclasses
import datetime as dt
from collections.abc import Mapping, Sequence

from beartype import beartype
from typing_extensions import TypeIs

from literalizer._language import Language
from literalizer._literalize import (
    ExistingVariable,
    LiteralizeResult,
    NewVariable,
)
from literalizer._parsing import InputFormat, parse_input
from literalizer._types import Scalar, Value, ValueInput
from literalizer.exceptions import NativeCallError
from literalizer.native_calls import (
    ConstructorTarget,
    FunctionTarget,
    MessageTarget,
    NativeClass,
    NativeInvocation,
    NativeLiteral,
    NativeReference,
    NativeTarget,
    NativeType,
    ObjectType,
    ScalarType,
    literalize_native_call,
)

_MISSING = object()


def _is_mapping(value: object, /) -> TypeIs[dict[object, object]]:
    """Narrow unknown schema mappings before inspecting keys."""
    return isinstance(value, dict)


def _is_list(value: object, /) -> TypeIs[list[object]]:
    """Narrow unknown sequences before iterating values."""
    return isinstance(value, list)


def _is_scalar(value: object, /) -> TypeIs[Scalar]:
    """Recognize the scalar leaves accepted by the data renderer."""
    return value is None or isinstance(
        value, str | int | float | bool | bytes | dt.date | dt.time
    )


@beartype
def _mapping(value: object, /) -> dict[str, object]:
    """Require a string-keyed schema object."""
    if not _is_mapping(value) or not all(
        isinstance(key, str) for key in value
    ):
        msg = "Native invocation schema requires a string-keyed object"
        raise NativeCallError(msg)
    return {_text(key): item for key, item in value.items()}


@beartype
def _keys(
    value: Mapping[str, object], allowed: set[str], required: set[str], /
) -> None:
    """Reject misspelled fields instead of ignoring author intent."""
    if len(set(value) - allowed) > 0 or len(required - set(value)) > 0:
        msg = (
            f"Invalid native fields: unknown={sorted(set(value) - allowed)}, "
            f"missing={sorted(required - set(value))}"
        )
        raise NativeCallError(msg)


@beartype
def _text(value: object, /) -> str:
    """Require a string without implicit coercion."""
    if not isinstance(value, str):
        msg = "Expected a native name or type string"
        raise NativeCallError(msg)
    return value


@beartype
def _list(value: object, /) -> list[object]:
    """Require an explicit sequence in the declarative schema."""
    if not _is_list(value):
        msg = "Expected a native argument/type list"
        raise NativeCallError(msg)
    return value


@beartype
def _native_type(value: object, /) -> NativeType:
    """Resolve portable scalar roles or explicit object type names."""
    if isinstance(value, str):
        for role in ScalarType:
            if value == role.value:
                return role
        return ObjectType(name=value)
    spec = _mapping(value)
    _keys(spec, {"object", "arguments"}, {"object", "arguments"})
    return ObjectType(
        name=_text(spec["object"]),
        arguments=tuple(_native_type(arg) for arg in _list(spec["arguments"])),
    )


@beartype
def _reference(spec: Mapping[str, object], /) -> NativeReference:
    """Decode a typed caller-owned reference."""
    _keys(spec, {"reference", "type"}, {"reference", "type"})
    return NativeReference(
        name=_text(spec["reference"]), type=_native_type(spec["type"])
    )


@beartype
def _value(value: object, /) -> ValueInput:
    """Validate data operands without coercing unsupported objects."""
    if _is_scalar(value):
        return value
    if _is_list(value):
        return [_value(item) for item in value]
    if _is_mapping(value):
        result: dict[Scalar, ValueInput] = {}
        for key, item in value.items():
            if not _is_scalar(key):
                msg = "Native literal mappings require scalar keys"
                raise NativeCallError(msg)
            result[key] = _value(item)
        return result
    msg = "Native literal operands require supported data values"
    raise NativeCallError(msg)


@beartype
def _operand(
    spec: object, values: Sequence[ValueInput], zipped: object, /
) -> NativeLiteral | NativeReference | NativeInvocation:
    """Bind source data to schema operands without string substitution."""
    fields = _mapping(spec)
    if "input" in fields:
        _keys(fields, {"input"}, {"input"})
        index = fields["input"]
        if (
            not isinstance(index, int)
            or isinstance(index, bool)
            or index < 0
            or index >= len(values)
        ):
            msg = "Native input index is outside the source row"
            raise NativeCallError(msg)
        return NativeLiteral(value=values[index])
    if "zipped" in fields:
        _keys(fields, {"zipped"}, {"zipped"})
        if fields["zipped"] is not True or zipped is _MISSING:
            msg = "Native zipped operand requires a companion value"
            raise NativeCallError(msg)
        # The upstream literal conversion validates these values.
        return NativeLiteral(value=_value(zipped))
    if "literal" in fields:
        _keys(fields, {"literal"}, {"literal"})
        return NativeLiteral(value=_value(fields["literal"]))
    if "reference" in fields:
        return _reference(fields)
    return native_invocation_from_data(
        spec=fields, values=values, zipped=zipped
    )


@beartype
def native_invocation_from_data(
    *,
    spec: Mapping[str, object],
    values: Sequence[ValueInput],
    zipped: object = _MISSING,
) -> NativeInvocation:
    """Build a native expression from a validated declarative recipe.

    Operands explicitly select ``input`` indexes, ``zipped`` companion
    values, ``literal`` values, typed references, or nested invocations.
    No field is interpreted as executable source text.
    """
    target: NativeTarget
    receiver: NativeLiteral | NativeClass | NativeReference | NativeInvocation
    parameter_types = tuple(
        _native_type(value) for value in _list(spec.get("parameter-types", []))
    )
    arguments = tuple(
        _operand(value, values, zipped)
        for value in _list(spec.get("arguments", []))
    )
    if "constructor" in spec:
        _keys(
            spec,
            {"constructor", "initializer", "parameter-types", "arguments"},
            {"constructor"},
        )
        target = ConstructorTarget(
            class_name=_text(spec["constructor"]),
            selector=_text(spec.get("initializer", "init")),
            parameter_types=parameter_types,
        )
    else:
        required = {"parameter-types", "arguments", "return-type"}
        return_type = _native_type(spec.get("return-type"))
        if "function" in spec:
            _keys(spec, required | {"function"}, required | {"function"})
            target = FunctionTarget(
                name=_text(spec["function"]),
                parameter_types=parameter_types,
                return_type=return_type,
            )
        else:
            _keys(
                spec,
                required | {"receiver", "selector"},
                required | {"receiver", "selector"},
            )
            receiver_data = _mapping(spec["receiver"])
            if "class" in receiver_data:
                _keys(receiver_data, {"class"}, {"class"})
                receiver = NativeClass(name=_text(receiver_data["class"]))
            elif "literal" in receiver_data:
                _keys(receiver_data, {"literal"}, {"literal"})
                receiver = NativeLiteral(
                    value=_value(receiver_data["literal"])
                )
            elif "reference" in receiver_data:
                receiver = _reference(receiver_data)
            else:
                receiver = native_invocation_from_data(
                    spec=receiver_data, values=values, zipped=zipped
                )
            target = MessageTarget(
                receiver=receiver,
                selector=_text(spec["selector"]),
                parameter_types=parameter_types,
                return_type=return_type,
            )
    return NativeInvocation(target=target, arguments=arguments)


@beartype
def _source_rows(
    *,
    source: str,
    input_format: InputFormat,
    per_element: bool,
    zip_source: str | None,
    zip_input_format: InputFormat | None,
) -> tuple[Sequence[Value], Sequence[object]]:
    """Parse and pair source rows before rendering expressions."""
    if (zip_source is None) != (zip_input_format is None):
        msg = "zip_source and zip_input_format must be supplied together"
        raise NativeCallError(msg)
    data = parse_input(source=source, input_format=input_format).data
    if per_element:
        if not isinstance(data, list):
            msg = "Per-element native calls require a list of rows"
            raise NativeCallError(msg)
        rows = data
    else:
        rows = [data]
    zipped_values: list[object] = [_MISSING] * len(rows)
    if zip_source is not None and zip_input_format is not None:
        companion = parse_input(
            source=zip_source, input_format=zip_input_format
        ).data
        paired = companion if per_element else [companion]
        if not isinstance(paired, list) or len(paired) != len(rows):
            msg = "Native zipped values must match the source row count"
            raise NativeCallError(msg)
        zipped_values = list(paired)
    return rows, zipped_values


@beartype
def literalize_native_calls(
    *,
    source: str,
    input_format: InputFormat,
    language: Language,
    invocation: Mapping[str, object],
    per_element: bool = True,
    zip_source: str | None = None,
    zip_input_format: InputFormat | None = None,
    variable_form: NewVariable | ExistingVariable | None = None,
    pre_indent_level: int = 0,
    initial_column: int = 0,
) -> LiteralizeResult:
    """Render source rows through an explicit native invocation recipe.

    Every row supplies positional data to ``input`` operands. Zipped
    data is optional, length-checked, and may contain null values.
    """
    rows, zipped_values = _source_rows(
        source=source,
        input_format=input_format,
        per_element=per_element,
        zip_source=zip_source,
        zip_input_format=zip_input_format,
    )
    if variable_form is not None and len(rows) != 1:
        msg = "A native result binding requires exactly one call"
        raise NativeCallError(msg)
    results: list[LiteralizeResult] = []
    for index, row in enumerate(iterable=rows):
        if not isinstance(row, list):
            msg = f"Native call row {index} must be a list"
            raise NativeCallError(msg)
        try:
            native = native_invocation_from_data(
                spec=invocation, values=row, zipped=zipped_values[index]
            )
            results.append(
                literalize_native_call(
                    language=language,
                    invocation=native,
                    variable_form=variable_form,
                    pre_indent_level=pre_indent_level,
                    initial_column=initial_column,
                )
            )
        except NativeCallError as exc:
            msg = f"Native call row {index}: {exc}"
            raise NativeCallError(msg, path=(index,)) from exc
    if len(results) == 0:
        # Validate the recipe/capability even when no row will be rendered.
        msg = "Native source must contain at least one call row"
        raise NativeCallError(msg)
    return dataclasses.replace(
        results[0],
        declaration_code="\n".join(result.code for result in results),
        source_data=[result.source_data for result in results],
        types_present=frozenset().union(
            *(result.types_present for result in results)
        ),
    )
