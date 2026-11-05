"""Structured, explicitly typed native invocation expressions.

Called functions and classes belong to the caller: native output never
invents stub receivers or infers signatures from input values.
"""

from __future__ import annotations

import dataclasses
import enum
import re
from collections.abc import Callable
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


@runtime_checkable
class _NativeEmitterLanguage(Language, _NativeInvocationLanguage, Protocol):
    """A language with the original native emission callbacks."""


@runtime_checkable
class _PositionedNativeInvocationLanguage(Protocol):
    """An emitter accepting caller-owned columns without parsing
    source.
    """

    @staticmethod
    def render_native_invocation_at_column(
        language: Language,
        invocation: NativeInvocation,
        /,
        *,
        initial_column: int,
        scope_indent: int,
    ) -> str:
        """Render directly at a known insertion point."""
        ...


@runtime_checkable
class _ObjectiveCNativeOptions(Protocol):
    """Independent options supplied by the Objective-C backend."""

    native_argument_layout: enum.Enum
    native_align_selectors: bool
    native_continuation_indent: int
    native_column_limit: int
    native_collection_layout: CollectionLayout


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
    initial_column: int = 0,
) -> LiteralizeResult:
    """Render a typed native invocation using caller-owned declarations.

    The returned fragment is executable code, suitable for composition
    inside a caller's function scope. It never synthesizes callee stubs.
    Existing string-target ``literalize_call`` behavior is unchanged.
    ``initial_column`` counts caller-owned text before the fragment after
    its scope indentation; binding prefixes are accounted for automatically.
    """
    language = dataclasses.replace(language)
    if (
        not isinstance(language, _NativeEmitterLanguage)
        or not language.supports_native_invocations
    ):
        msg = f"{type(language).__name__} does not support native invocations"
        raise NativeCallError(msg)
    if pre_indent_level < 0:
        msg = "pre_indent_level must be non-negative"
        raise NativeCallError(msg)
    if initial_column < 0:
        msg = "initial_column must be non-negative"
        raise NativeCallError(msg)
    if initial_column != 0 and not isinstance(
        language, _PositionedNativeInvocationLanguage
    ):
        msg = "Native backend does not support initial_column"
        raise NativeCallError(msg)
    binding = ""
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
            binding = f"{spelling}{separator}{variable_form.name} = "
        else:
            binding = f"{variable_form.name} = "
    prefix = language.indent * pre_indent_level
    code = _bound_native_expression(
        language,
        invocation,
        binding,
        initial_column=initial_column,
        scope_indent=len(prefix),
    )
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
def _render_native_expression(
    language: _NativeEmitterLanguage,
    invocation: NativeInvocation,
    /,
    *,
    initial_column: int,
    scope_indent: int,
) -> str:
    """Use an optional positioned emitter while retaining legacy
    backends.
    """
    if isinstance(language, _PositionedNativeInvocationLanguage):
        return language.render_native_invocation_at_column(
            language,
            invocation,
            initial_column=initial_column,
            scope_indent=scope_indent,
        )
    return language.render_native_invocation(language, invocation)


@beartype
def _bound_native_expression(
    language: _NativeEmitterLanguage,
    invocation: NativeInvocation,
    binding: str,
    /,
    *,
    initial_column: int,
    scope_indent: int,
) -> str:
    """Choose a binding break before emitting its expression again."""
    column = initial_column + len(binding)
    expression = _render_native_expression(
        language, invocation, initial_column=column, scope_indent=scope_indent
    )
    if (
        binding
        and isinstance(language, _ObjectiveCNativeOptions)
        and language.native_argument_layout.name != "INLINE"
        and scope_indent + column + len(expression.split(sep="\n")[0])
        > language.native_column_limit
    ):
        continuation = language.indent * language.native_continuation_indent
        binding = binding.rstrip() + "\n" + continuation
        expression = _render_native_expression(
            language,
            invocation,
            initial_column=len(continuation),
            scope_indent=scope_indent,
        )
    return binding + expression


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
        collection_layout=language.native_collection_layout
        if isinstance(language, _ObjectiveCNativeOptions)
        else CollectionLayout.COMPACT,
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
def _indent_operand(code: str, column: int, /) -> str:
    """Place continuation lines of a freshly emitted literal operand."""
    first, *rest = code.split(sep="\n")
    return "\n".join(
        [first, *(" " * column + line if line else line for line in rest)]
    )


@beartype
def _objc_argument(
    language: Language,
    argument: NativeLiteral | NativeReference | NativeInvocation,
    expected: NativeType,
    /,
    *,
    initial_column: int,
    scope_indent: int,
    line_indent: int,
) -> str:
    """Render one typed operand directly at its argument position."""
    _ = objective_c_type(expected)
    if expected is ScalarType.VOID:
        msg = "A parameter cannot have void type"
        raise NativeCallError(msg)
    if isinstance(argument, NativeLiteral):
        code = _objc_literal(language, argument, expected)
        return (
            _indent_operand(code, line_indent)
            if _positioned_operands(language)
            else code
        )
    actual = (
        argument.type
        if isinstance(argument, NativeReference)
        else argument.target.return_type
    )
    _ = objective_c_type(actual)
    box = (
        isinstance(expected, ObjectType)
        and expected.name in {"id", "NSNumber", "NSObject"}
        and actual
        in {
            ScalarType.BOOL,
            ScalarType.INTEGER,
            ScalarType.UNSIGNED,
            ScalarType.FLOAT,
        }
    )
    if not box and not _compatible(actual, expected):
        msg = (
            f"Native operand type {actual!r} is incompatible with {expected!r}"
        )
        raise NativeCallError(msg)
    prefix = (
        "@("
        if box
        else "(double)"
        if expected is ScalarType.FLOAT
        and actual in {ScalarType.INTEGER, ScalarType.UNSIGNED}
        else ""
    )
    code = (
        _identifier(argument.name)
        if isinstance(argument, NativeReference)
        else objective_c_invocation(
            language,
            argument,
            initial_column=initial_column + len(prefix),
            scope_indent=scope_indent,
            line_indent=line_indent,
        )
    )
    return prefix + code + (")" if box else "")


@beartype
def _native_width(code: str, column: int, scope: int, /) -> int:
    """Measure emitted lines without interpreting their source
    contents.
    """
    first, *rest = code.split(sep="\n")
    return (
        scope + max(column + len(first), *(len(line) for line in rest))
        if rest
        else scope + column + len(first)
    )


@beartype
def _positioned_operands(language: Language, /) -> bool:
    """Keep legacy operands unchanged unless layout is explicitly selected."""
    return isinstance(language, _ObjectiveCNativeOptions) and (
        language.native_argument_layout.name != "INLINE"
        or language.native_collection_layout is not CollectionLayout.COMPACT
    )


@beartype
def _objective_c_receiver(
    language: Language,
    target: MessageTarget,
    /,
    *,
    initial_column: int,
    scope_indent: int,
    line_indent: int,
) -> str:
    """Emit a receiver from its declared native structure."""
    receiver = target.receiver
    if isinstance(receiver, NativeLiteral):
        code = _objc_literal(language, receiver, ObjectType(name="id"))
        return (
            _indent_operand(code, line_indent)
            if _positioned_operands(language)
            else code
        )
    if isinstance(receiver, NativeClass):
        return _identifier(receiver.name)
    if isinstance(receiver, NativeReference):
        if not isinstance(receiver.type, ObjectType):
            msg = "A message receiver must be an object"
            raise NativeCallError(msg)
        _ = objective_c_type(receiver.type)
        return _identifier(receiver.name)
    if not isinstance(receiver.target.return_type, ObjectType):
        msg = "A message receiver must return an object"
        raise NativeCallError(msg)
    return objective_c_invocation(
        language,
        receiver,
        initial_column=initial_column + 1,
        scope_indent=scope_indent,
        line_indent=line_indent,
    )


@beartype
def _objective_c_head(
    language: Language,
    invocation: NativeInvocation,
    /,
    *,
    initial_column: int,
    scope_indent: int,
    line_indent: int,
) -> tuple[str, str, tuple[str, ...]]:
    """Emit a target prefix, closing delimiter, and selector labels."""
    target = invocation.target
    if isinstance(target, FunctionTarget):
        return _identifier(target.name) + "(", ")", ()
    labels = _selector(target.selector, len(invocation.arguments))
    if isinstance(target, ConstructorTarget):
        class_name = _identifier(target.class_name)
        if (
            re.fullmatch(pattern=r"init(?:[^a-z].*)?", string=labels[0])
            is None
        ):
            msg = "A constructor selector must be an initializer"
            raise NativeCallError(msg)
        receiver = f"[{class_name} alloc]"
    else:
        receiver = _objective_c_receiver(
            language,
            target,
            initial_column=initial_column,
            scope_indent=scope_indent,
            line_indent=line_indent,
        )
    return f"[{receiver} ", "]", labels


@beartype
def _selector_arguments(
    language: Language,
    head: str,
    labels: tuple[str, ...],
    argument: Callable[[int, int, int], str],
    options: _ObjectiveCNativeOptions,
    /,
    *,
    initial_column: int,
    line_indent: int,
) -> str:
    """Emit selector lines at the selected colon or indent anchor."""
    continuation = (
        initial_column
        + len(language.indent) * options.native_continuation_indent
    )
    first_start = (
        initial_column + len(head)
        if "\n" not in head
        else len(head.rsplit(sep="\n", maxsplit=1)[-1])
    )
    colon = first_start + len(labels[0])
    receiver_break = options.native_align_selectors and any(
        len(label) > colon - initial_column for label in labels
    )
    if receiver_break:
        head = head.rstrip() + "\n"
        colon = continuation + max(len(label) for label in labels)
    rendered: list[str] = []
    for i, label in enumerate(iterable=labels):
        start = (
            colon - len(label)
            if options.native_align_selectors
            else continuation
        )
        if i == 0 and not receiver_break:
            start = first_start
            lead = ""
        else:
            lead = " " * start
        rendered.append(
            lead
            + label
            + ":"
            + argument(
                i,
                start + len(label) + 1,
                line_indent if i == 0 and not receiver_break else start,
            )
        )
    return head + "\n".join(rendered) + "]"


@beartype
def _flat_arguments(
    head: str,
    close: str,
    labels: tuple[str, ...],
    count: int,
    argument: Callable[[int, int, int], str],
    /,
    *,
    initial_column: int,
    line_indent: int,
) -> tuple[str, tuple[bool, ...]]:
    """Emit the inline argument choice before deciding optional
    wrapping.
    """
    cursor = (
        initial_column + len(head)
        if "\n" not in head
        else len(head.rsplit(sep="\n", maxsplit=1)[-1])
    )
    pieces: list[str] = []
    multiline: list[bool] = []
    for i in range(count):
        label = labels[i] + ":" if labels else ""
        value = argument(i, cursor + len(label), line_indent)
        multiline.append("\n" in value)
        if "\n" in value:
            last = value.rsplit(sep="\n", maxsplit=1)[-1]
            line_indent = len(last) - len(last.lstrip())
        piece = label + value
        pieces.append(piece)
        cursor = (
            len(value.rsplit(sep="\n", maxsplit=1)[-1])
            if "\n" in value
            else cursor + len(piece)
        )
        cursor += 1 if labels else 2
    return head + (" " if labels else ", ").join(pieces) + close, tuple(
        multiline
    )


@beartype
def _function_arguments(
    language: Language,
    head: str,
    close: str,
    count: int,
    argument: Callable[[int, int, int], str],
    /,
    *,
    options: _ObjectiveCNativeOptions,
    initial_column: int,
    scope_indent: int,
    line_indent: int,
) -> str:
    """Emit function arguments at the caller's prefix and width."""
    anchor = initial_column + len(head)
    longest = max(
        len(argument(i, anchor, line_indent).split(sep="\n")[0])
        for i in range(count)
    )
    if scope_indent + anchor + longest + 2 > options.native_column_limit:
        anchor = (
            initial_column
            + len(language.indent) * options.native_continuation_indent
        )
        head += "\n" + " " * anchor
        line_indent = anchor
    return (
        head
        + (",\n" + " " * anchor).join(
            argument(i, anchor, line_indent if i == 0 else anchor)
            for i in range(count)
        )
        + close
    )


@beartype
def objective_c_invocation(
    language: Language,
    invocation: NativeInvocation,
    /,
    *,
    initial_column: int = 0,
    scope_indent: int = 0,
    line_indent: int = 0,
) -> str:
    """Emit a typed call using explicit breaks and alignment choices."""
    options = (
        language if isinstance(language, _ObjectiveCNativeOptions) else None
    )
    if options is not None and (
        options.native_continuation_indent < 0
        or options.native_column_limit < 1
    ):
        msg = (
            "Native continuation indentation must be non-negative "
            "and column limit positive"
        )
        raise NativeCallError(msg)
    target = invocation.target
    _ = objective_c_type(target.return_type)
    count = len(invocation.arguments)
    if count != len(target.parameter_types):
        msg = "Native argument count does not match the declared signature"
        raise NativeCallError(msg)
    head, close, labels = _objective_c_head(
        language,
        invocation,
        initial_column=initial_column,
        scope_indent=scope_indent,
        line_indent=line_indent,
    )
    if count == 0:
        return head + (labels[0] if labels else "") + close

    def argument(index: int, column: int, leading: int, /) -> str:
        """Render one operand at the position chosen by its parent."""
        return _objc_argument(
            language,
            invocation.arguments[index],
            target.parameter_types[index],
            initial_column=column,
            scope_indent=scope_indent,
            line_indent=leading,
        )

    flat, multiline = _flat_arguments(
        head,
        close,
        labels,
        count,
        argument,
        initial_column=initial_column,
        line_indent=line_indent,
    )
    if options is None or not _positioned_operands(language):
        return flat
    split = (
        (options.native_argument_layout.name == "MULTILINE" and count > 1)
        or (
            options.native_argument_layout.name == "AUTO"
            and _native_width(flat, initial_column, scope_indent) + 1
            > options.native_column_limit
        )
        or any(
            is_multiline and isinstance(value, NativeInvocation)
            for is_multiline, value in zip(
                multiline, invocation.arguments, strict=True
            )
        )
    )
    if not split:
        return flat
    if not labels:
        return _function_arguments(
            language,
            head,
            close,
            count,
            argument,
            options=options,
            initial_column=initial_column,
            scope_indent=scope_indent,
            line_indent=line_indent,
        )
    return _selector_arguments(
        language,
        head,
        labels,
        argument,
        options,
        initial_column=initial_column,
        line_indent=line_indent,
    )
