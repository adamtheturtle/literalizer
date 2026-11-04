"""Structured, explicitly typed native invocation expressions.

Called functions and classes belong to the caller: native output never
invents stub receivers or infers signatures from input values.
"""

from __future__ import annotations

import dataclasses
import enum
import re
from typing import Protocol, runtime_checkable

from beartype import beartype

from literalizer._language import (
    CollectionLayout,
    Language,
    is_reserved_identifier,
)
from literalizer._literalize import (
    ExistingVariable,
    LiteralizeResult,
    NewVariable,
    materialize_value_input,
    render_value_literal,
)
from literalizer._types import Value, ValueInput
from literalizer.exceptions import NativeCallError


class ScalarType(enum.Enum):
    """Scalar roles whose spelling is owned by the native renderer."""

    BOOL = "bool"
    INTEGER = "integer"
    UNSIGNED = "unsigned"
    FLOAT = "float"
    VOID = "void"


@dataclasses.dataclass(frozen=True, kw_only=True)
class ObjectType:
    """A caller-owned object type, optionally with generic arguments."""

    name: str
    arguments: tuple[NativeType, ...] = ()


type NativeType = ScalarType | ObjectType


@dataclasses.dataclass(frozen=True, kw_only=True)
class NativeReference:
    """An existing value with its caller-declared native type."""

    name: str
    type: NativeType


@dataclasses.dataclass(frozen=True, kw_only=True)
class NativeClass:
    """A class receiver, distinct from an instance reference."""

    name: str


@dataclasses.dataclass(frozen=True, kw_only=True)
class NativeLiteral:
    """A literal value; its parameter signature controls boxing."""

    value: ValueInput


@dataclasses.dataclass(frozen=True, kw_only=True)
class FunctionTarget:
    """A genuine free-function target with an explicit signature."""

    name: str
    parameter_types: tuple[NativeType, ...]
    return_type: NativeType


@dataclasses.dataclass(frozen=True, kw_only=True)
class MessageTarget:
    """An instance or class message with a complete native selector."""

    receiver: NativeLiteral | NativeReference | NativeClass | NativeInvocation
    selector: str
    parameter_types: tuple[NativeType, ...]
    return_type: NativeType


@dataclasses.dataclass(frozen=True, kw_only=True)
class ConstructorTarget:
    """Allocation followed by the explicitly named initializer."""

    class_name: str
    selector: str = "init"
    parameter_types: tuple[NativeType, ...] = ()

    @property
    def return_type(self) -> ObjectType:
        """The allocated object's declared type."""
        return ObjectType(name=self.class_name)


type NativeTarget = FunctionTarget | MessageTarget | ConstructorTarget


@dataclasses.dataclass(frozen=True, kw_only=True)
class NativeInvocation:
    """A call expression whose arguments may themselves be calls."""

    target: NativeTarget
    arguments: tuple[NativeLiteral | NativeReference | NativeInvocation, ...]


@runtime_checkable
class _NativeInvocationLanguage(Protocol):
    """Optional native syntax renderer, selected through a capability."""

    supports_native_invocations: bool

    @staticmethod
    def render_native_invocation(
        language: Language, invocation: NativeInvocation, /
    ) -> str:
        """Render one validated expression without a terminator."""
        ...

    @staticmethod
    def native_type_name(native_type: NativeType, /) -> str:
        """Spell a declared native type."""
        ...


@beartype
def _identifier(name: str, /) -> str:
    """Reject source fragments where a single identifier is required."""
    if re.fullmatch(pattern=r"[A-Za-z_][A-Za-z0-9_]*", string=name) is None:
        msg = f"Invalid native identifier: {name!r}"
        raise NativeCallError(msg)
    if name in {
        "if",
        "else",
        "while",
        "for",
        "return",
        "switch",
        "case",
        "break",
        "continue",
        "do",
        "goto",
        "struct",
        "enum",
        "typedef",
        "static",
        "const",
        "void",
        "char",
        "int",
        "float",
        "double",
        "long",
        "short",
        "unsigned",
        "signed",
        "sizeof",
        "union",
        "register",
        "auto",
        "volatile",
        "extern",
    }:
        msg = f"Reserved native identifier: {name!r}"
        raise NativeCallError(msg)
    return name


@beartype
def _invocation_values(invocation: NativeInvocation, /) -> list[Value]:
    """Retain the values supporting a native expression's preamble."""
    values: list[Value] = []
    target = invocation.target
    if isinstance(target, MessageTarget):
        if isinstance(target.receiver, NativeInvocation):
            values.extend(_invocation_values(target.receiver))
        elif isinstance(target.receiver, NativeLiteral):
            values.append(
                materialize_value_input(
                    value=target.receiver.value,
                    argument_name="native receiver",
                )
            )
    for argument in invocation.arguments:
        if isinstance(argument, NativeLiteral):
            values.append(
                materialize_value_input(
                    value=argument.value, argument_name="native literal"
                )
            )
        elif isinstance(argument, NativeInvocation):
            values.extend(_invocation_values(argument))
    return values


@beartype
def _value_types(value: Value, /) -> frozenset[type]:
    """Retain nested literal types without inventing reference values."""
    types = {type(value)}
    if isinstance(value, (list, set)):
        for item in value:
            types.update(_value_types(item))
    elif isinstance(value, dict):
        for key, item in value.items():
            types.update(_value_types(key))
            types.update(_value_types(item))
    return frozenset(types)


@beartype
def literalize_native_call(
    *,
    language: Language,
    invocation: NativeInvocation,
    variable_form: NewVariable | ExistingVariable | None = None,
    pre_indent_level: int = 0,
) -> LiteralizeResult:
    """Render a typed native invocation using caller-owned declarations.

    The returned fragment is executable code, suitable for composition
    inside a caller's function scope. It never synthesizes callee stubs.
    Existing string-target ``literalize_call`` behavior is unchanged.
    """
    language = dataclasses.replace(language)
    if (
        not isinstance(language, _NativeInvocationLanguage)
        or not language.supports_native_invocations
    ):
        msg = f"{type(language).__name__} does not support native invocations"
        raise NativeCallError(msg)
    if pre_indent_level < 0:
        msg = "pre_indent_level must be non-negative"
        raise NativeCallError(msg)
    code = language.render_native_invocation(language, invocation)
    if variable_form is not None:
        _ = _identifier(variable_form.name)
        if is_reserved_identifier(
            case_sensitive=language.reserved_variable_identifiers_case_sensitive,
            name=variable_form.name,
            reserved_identifiers=language.reserved_variable_identifiers,
        ):
            msg = f"Reserved native binding identifier: {variable_form.name!r}"
            raise NativeCallError(msg)
        if invocation.target.return_type is ScalarType.VOID:
            msg = "Cannot bind a void invocation"
            raise NativeCallError(msg)
        if isinstance(variable_form, NewVariable):
            if len(variable_form.modifiers) > 0:
                msg = "Native bindings do not accept modifiers"
                raise NativeCallError(msg)
            spelling = language.native_type_name(invocation.target.return_type)
            separator = "" if spelling.endswith("*") else " "
            code = f"{spelling}{separator}{variable_form.name} = {code}"
        else:
            code = f"{variable_form.name} = {code}"
    prefix = language.indent * pre_indent_level
    code = "\n".join(
        prefix + line if line != "" else line
        for line in (code + ";").splitlines()
    )
    values = _invocation_values(invocation)
    return LiteralizeResult(
        declaration_code=code,
        preamble=tuple(language.static_preamble),
        body_preamble=(),
        pre_declaration_comments=(),
        types_present=_value_types(values),
        contains_standalone_comments=False,
        source_data=values,
        sections=(),
        data_dependent_preamble=(),
        uses_existing_variable=isinstance(variable_form, ExistingVariable),
        # Native object initializers are runtime expressions even when bound.
        is_call_statement=True,
    )


@beartype
def objective_c_type(native_type: NativeType, /) -> str:
    """Spell explicit Objective-C scalar and object types."""
    if isinstance(native_type, ScalarType):
        return {
            ScalarType.BOOL: "BOOL",
            ScalarType.INTEGER: "NSInteger",
            ScalarType.UNSIGNED: "NSUInteger",
            ScalarType.FLOAT: "double",
            ScalarType.VOID: "void",
        }[native_type]
    name = _identifier(native_type.name)
    if len(native_type.arguments) > 0:
        if name in {"id", "Class", "instancetype"}:
            msg = f"{name} cannot have generic arguments"
            raise NativeCallError(msg)
        for argument in native_type.arguments:
            if not isinstance(argument, ObjectType):
                msg = "Objective-C generic arguments must be object types"
                raise NativeCallError(msg)
        name += (
            "<"
            + ", ".join(
                objective_c_type(argument)
                for argument in native_type.arguments
            )
            + ">"
        )
    return (
        name
        if native_type.name in {"id", "Class", "instancetype"}
        else name + " *"
    )


@beartype
def _selector(selector: str, count: int, /) -> tuple[str, ...]:
    """Validate selector spelling and its exact argument count."""
    if count == 0:
        return (_identifier(selector),)
    if not selector.endswith(":") or selector.count(":") != count:
        msg = f"Selector {selector!r} requires {count} argument labels"
        raise NativeCallError(msg)
    return tuple(_identifier(part) for part in selector[:-1].split(sep=":"))


@beartype
def _compatible(actual: NativeType, expected: NativeType, /) -> bool:
    """Allow explicit numeric widening and object-to-id conversion."""
    if actual == expected:
        return True
    if expected is ScalarType.FLOAT and actual in {
        ScalarType.INTEGER,
        ScalarType.UNSIGNED,
    }:
        return True
    return (
        isinstance(actual, ObjectType)
        and isinstance(expected, ObjectType)
        and (expected.name in {"id", "NSObject"} or actual.name == "id")
    )


@beartype
def _object_literal(language: Language, value: Value, /) -> str:
    """Reuse the ordinary literal renderer, including collection
    boxing.
    """
    code = render_value_literal(
        value=value,
        language=language,
        collection_layout=CollectionLayout.COMPACT,
    )
    return language.format_call_arg(value, code)


@beartype
def _validate_generic_literal(
    language: Language, value: Value, expected: ObjectType, /
) -> None:
    """Check collection element contracts before rendering a literal."""
    if len(expected.arguments) > 0:
        if not isinstance(value, (list, dict, set)):
            msg = "Generic literal arguments require a collection value"
            raise NativeCallError(msg)
        arity = 2 if expected.name == "NSDictionary" else 1
        if len(expected.arguments) != arity:
            msg = "Generic object literal type has the wrong arity"
            raise NativeCallError(msg)
        if isinstance(value, (list, set)):
            for item in value:
                _ = _objc_literal(
                    language,
                    NativeLiteral(value=item),
                    expected.arguments[0],
                )
        else:
            for key, item in value.items():
                _ = _objc_literal(
                    language,
                    NativeLiteral(value=key),
                    expected.arguments[0],
                )
                _ = _objc_literal(
                    language,
                    NativeLiteral(value=item),
                    expected.arguments[1],
                )


@beartype
def _objc_literal(
    language: Language, argument: NativeLiteral, expected: NativeType, /
) -> str:
    """Render a literal with explicit scalar versus object intent."""
    value = materialize_value_input(
        value=argument.value, argument_name="native literal"
    )
    if isinstance(expected, ObjectType):
        object_names: dict[type, str] = {
            str: "NSString",
            bool: "NSNumber",
            int: "NSNumber",
            float: "NSNumber",
            list: "NSArray",
            dict: "NSDictionary",
            set: "NSSet",
            bytes: "NSData",
        }
        actual_name = object_names.get(type(value))
        if value is None:
            if expected.name in {"id", "NSNull", "NSObject"}:
                return "[NSNull null]"
            msg = (
                "NSNull is not a typed object reference; "
                "use an explicit native reference for nil"
            )
            raise NativeCallError(msg)
        if expected.name not in {"id", "NSObject", actual_name}:
            msg = f"Literal does not have declared object type {expected.name}"
            raise NativeCallError(msg)
        _validate_generic_literal(language, value, expected)
        return _object_literal(language, value)
    if expected is ScalarType.BOOL and isinstance(value, bool):
        return "YES" if value else "NO"
    if (
        expected in {ScalarType.INTEGER, ScalarType.UNSIGNED}
        and isinstance(value, int)
        and not isinstance(value, bool)
    ):
        minimum = 0 if expected is ScalarType.UNSIGNED else -(1 << 63)
        maximum = (
            (1 << 64) - 1 if expected is ScalarType.UNSIGNED else (1 << 63) - 1
        )
        if value < minimum or value > maximum:
            msg = "Integer literal is outside the declared native scalar range"
            raise NativeCallError(msg)
        return language.format_integer(value)
    if (
        expected is ScalarType.FLOAT
        and isinstance(value, int | float)
        and not isinstance(value, bool)
    ):
        return language.format_float(float(value))
    msg = f"Literal does not have declared scalar type {expected.value}"
    raise NativeCallError(msg)


@beartype
def _objc_argument(
    language: Language,
    argument: NativeLiteral | NativeReference | NativeInvocation,
    expected: NativeType,
    /,
) -> str:
    """Render an operand using the declared parameter type."""
    _ = objective_c_type(expected)
    if expected is ScalarType.VOID:
        msg = "A parameter cannot have void type"
        raise NativeCallError(msg)
    if isinstance(argument, NativeLiteral):
        return _objc_literal(language, argument, expected)
    if isinstance(argument, NativeReference):
        code = _identifier(argument.name)
        actual = argument.type
    else:
        code = objective_c_invocation(language, argument)
        actual = argument.target.return_type
    _ = objective_c_type(actual)
    if (
        isinstance(expected, ObjectType)
        and expected.name in {"id", "NSNumber", "NSObject"}
        and actual
        in {
            ScalarType.BOOL,
            ScalarType.INTEGER,
            ScalarType.UNSIGNED,
            ScalarType.FLOAT,
        }
    ):
        return f"@({code})"
    if not _compatible(actual, expected):
        msg = (
            f"Native operand type {actual!r} is incompatible with {expected!r}"
        )
        raise NativeCallError(msg)
    if expected is ScalarType.FLOAT and actual in {
        ScalarType.INTEGER,
        ScalarType.UNSIGNED,
    }:
        return f"(double){code}"
    return code


@beartype
def objective_c_invocation(
    language: Language, invocation: NativeInvocation, /
) -> str:
    """Lower typed targets to genuine Objective-C expressions."""
    target = invocation.target
    _ = objective_c_type(target.return_type)
    if len(invocation.arguments) != len(target.parameter_types):
        msg = "Native argument count does not match the declared signature"
        raise NativeCallError(msg)
    arguments = tuple(
        _objc_argument(language, argument, expected)
        for argument, expected in zip(
            invocation.arguments, target.parameter_types, strict=True
        )
    )
    if isinstance(target, FunctionTarget):
        return _identifier(target.name) + "(" + ", ".join(arguments) + ")"
    if isinstance(target, ConstructorTarget):
        class_name = _identifier(target.class_name)
        labels = _selector(target.selector, len(arguments))
        if (
            re.fullmatch(pattern=r"init(?:[^a-z].*)?", string=labels[0])
            is None
        ):
            msg = "A constructor selector must be an initializer"
            raise NativeCallError(msg)
        receiver = f"[{class_name} alloc]"
    else:
        labels = _selector(target.selector, len(arguments))
        if isinstance(target.receiver, NativeLiteral):
            receiver = _objc_literal(
                language, target.receiver, ObjectType(name="id")
            )
        elif isinstance(target.receiver, NativeClass):
            receiver = _identifier(target.receiver.name)
        elif isinstance(target.receiver, NativeReference):
            if not isinstance(target.receiver.type, ObjectType):
                msg = "A message receiver must be an object"
                raise NativeCallError(msg)
            _ = objective_c_type(target.receiver.type)
            receiver = _identifier(target.receiver.name)
        else:
            if not isinstance(target.receiver.target.return_type, ObjectType):
                msg = "A message receiver must return an object"
                raise NativeCallError(msg)
            receiver = objective_c_invocation(language, target.receiver)
    message = (
        labels[0]
        if len(arguments) == 0
        else " ".join(
            label + ":" + argument
            for label, argument in zip(labels, arguments, strict=True)
        )
    )
    return f"[{receiver} {message}]"
