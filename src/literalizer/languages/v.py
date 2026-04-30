"""V language specification."""

import dataclasses
import datetime
import enum
import textwrap
from collections.abc import Callable, Sequence
from functools import cached_property, partial
from types import MappingProxyType
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_separator,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    variable_declaration_formatter,
    variable_formatter,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    format_integer_underscore,
    make_overflow_fallback_formatter,
    make_unsigned_overflow_fallback,
)
from literalizer._formatters.format_strings import (
    format_string_backslash_dollar_single,
)
from literalizer._heterogeneous import collect_heterogeneous_container_ids
from literalizer._language import (
    NO_HETEROGENEOUS_BEHAVIOR,
    CallStyle,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    HeterogeneousBehavior,
    IdentifierCase,
    LanguageCls,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    default_wrap_calls_with_declarations,
    identity_call_target,
    no_data_preamble,
    no_type_hint_preamble,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import Value

_V_I32_MIN = -(2**31)  # -2147483648
_V_I32_MAX = 2**31 - 1  # 2147483647

_V_IFACE_NAME = "IVal"
_V_IFACE_DECL = f"interface {_V_IFACE_NAME} {{}}"
_V_NULL_WRAPPED = f"{_V_IFACE_NAME}(unsafe {{ nil }})"


@beartype
def _format_v_u64_positive(value: int) -> str:
    """Format a positive value outside signed 64-bit range as a V
    ``u64`` typed conversion.
    """
    return f"u64({value})"


def _make_v_i64_formatter(
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Return a formatter that wraps *base*-formatted values in
    ``i64(...)``.

    Used for values that overflow V's 32-bit ``int`` but fit in ``i64``.
    The inner representation preserves the requested integer format (hex,
    octal, binary, etc.) rather than forcing decimal.
    """

    def _format(value: int) -> str:
        """Format *value* as ``i64(<base(value)>)``."""
        return f"i64({base(value)})"

    return _format


def _v_collect_ids_needing_wrap(data: Value) -> frozenset[int]:
    """Return container ids that need interface-type wrapping in V.

    Extends :func:`collect_heterogeneous_container_ids` with a
    bottom-up traversal that also catches:

    * Empty containers (V requires explicit typed empty literals).
    * Containers with any ``None`` values (V cannot store ``none`` in
      typed collections).
    * Sets with mixed Python types.
    * Containers whose children have mixed V types because some
      children are in wrap_ids and others are not.
    """
    base_ids = collect_heterogeneous_container_ids(data=data)
    wrap_ids: set[int] = set(base_ids)

    def _visit(item: Value) -> None:
        """Recursively mark *item* and its containers if wrapping
        needed.
        """
        if isinstance(item, dict):
            children: list[Value] = list(item.values())
        elif isinstance(item, (list, set)):
            children = list(item)
        else:
            return
        for child in children:
            _visit(item=child)
        if id(item) in wrap_ids:
            return
        if not children or any(v is None for v in children):
            wrap_ids.add(id(item))
            return
        python_types = {type(v) for v in children if v is not None}
        if len(python_types) > 1:
            wrap_ids.add(id(item))
            return
        container_children = [
            v for v in children if isinstance(v, (list, dict, set))
        ]
        if container_children:
            wrapped = [v for v in container_children if id(v) in wrap_ids]
            if wrapped and len(wrapped) < len(container_children):
                wrap_ids.add(id(item))

    _visit(item=data)
    return frozenset(wrap_ids)


@dataclasses.dataclass(frozen=True)
class _VHeterogeneousStrategyConfig:
    """Configuration for one V heterogeneous-values strategy."""

    build_behavior: Callable[[], HeterogeneousBehavior]
    build_preamble: Callable[[], Callable[[Value], tuple[str, ...]]]


def _build_v_interface_behavior() -> HeterogeneousBehavior:
    """INTERFACE strategy: wrap scalars in ``IVal(...)``."""

    def _compute(data: Value) -> frozenset[int]:
        """Return container ids whose scalar children should be
        wrapped.
        """
        return _v_collect_ids_needing_wrap(data=data)

    def _wrap(raw_value: Value, formatted: str) -> str:
        """Wrap a scalar as ``IVal(formatted)`` or the null sentinel."""
        if raw_value is None:
            return _V_NULL_WRAPPED
        return f"{_V_IFACE_NAME}({formatted})"

    return HeterogeneousBehavior(
        skip_scalar_checks=True,
        compute_wrap_ids=_compute,
        wrap_scalar=_wrap,
    )


def _build_v_interface_preamble() -> Callable[[Value], tuple[str, ...]]:
    """INTERFACE strategy: emit ``interface IVal {}`` when needed."""

    def _preamble(data: Value, /) -> tuple[str, ...]:
        """Emit ``interface IVal {}`` when any container needs
        wrapping.
        """
        wrap_ids = _v_collect_ids_needing_wrap(data=data)
        if not wrap_ids:
            return ()
        return (_V_IFACE_DECL,)

    return _preamble


@beartype
def _v_call_preamble_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    stub_return: StubReturn,
    /,
    *,
    indent: str,
) -> tuple[str, ...]:
    """Return V preamble stub declarations for a call name.

    Includes ``interface ICallArg_ {}`` in every result so that
    duplicate copies can be dropped when multiple stubs are combined.
    For dotted targets like ``app.client.fetch``, one struct per
    prefix level is emitted together with the method declaration.
    """
    iface = "interface ICallArg_ {}"

    if len(parts) == 1:
        if stub_return is StubReturn.VOID:
            return (iface, f"fn {parts[0]}(args ...ICallArg_) {{}}")
        return (
            iface,
            f"fn {parts[0]}(args ...ICallArg_) ICallArg_ {{ return 0 }}",
        )

    def _cap_type(name: str, /) -> str:
        """Return *name* with an upper-case first letter and ``Type_``
        suffix.
        """
        return name[0].upper() + name[1:] + "Type_"

    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    receiver_type = _cap_type(fields[-1]) if fields else _cap_type(root)

    if stub_return is StubReturn.VOID:
        method_line = (
            f"fn (r {receiver_type}) {method}(args ...ICallArg_) {{}}"
        )
    else:
        method_line = (
            f"fn (r {receiver_type}) {method}(args ...ICallArg_)"
            f" ICallArg_ {{ return 0 }}"
        )

    lines: list[str] = [iface, f"struct {receiver_type} {{}}", method_line]

    if fields:
        prev_type = receiver_type
        for i in range(len(fields) - 2, -1, -1):
            curr_type = _cap_type(fields[i])
            field = fields[i + 1]
            lines.append(
                f"struct {curr_type} {{\n{indent}{field} {prev_type}\n}}"
            )
            prev_type = curr_type
        root_type = _cap_type(root)
        lines.append(
            f"struct {root_type} {{\n{indent}{fields[0]} {prev_type}\n}}"
        )

    return tuple(lines)


@beartype
def _v_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    /,
) -> tuple[str, ...]:
    """Return V body-level variable stubs for a call name.

    For dotted targets the root variable is declared inside ``fn main``
    so it is in scope when the call expression is evaluated.  Simple
    one-part targets are declared at file level (preamble) and need no
    body stub.
    """
    if len(parts) == 1:
        return ()
    root = parts[0]
    root_type = root[0].upper() + root[1:] + "Type_"
    return (f"{root} := {root_type}{{}}",)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class V(metaclass=LanguageCls):
    """V language specification.

    Args:
        declaration_style: How to declare variables.

            * ``declaration_styles.ASSIGN`` — immutable short
              declaration, e.g. ``x := value``.
            * ``declaration_styles.MUT`` — mutable short
              declaration, e.g. ``mut x := value``.
    """

    extension = ".v"
    pygments_name = "v"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_special_floats = True
    supports_variable_names = True
    supports_dotted_calls = True

    class DateFormats(enum.Enum):
        """Date format options for V."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for V."""

        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            type_produced=str,
        )

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)
        BASE64 = enum.member(value=format_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for V."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="["),
            close="]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=f"[]{_V_IFACE_NAME}{{}}",
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for V."""

        ARRAY = SetFormatConfig(
            set_open=fixed_open(open_str="["),
            close="]",
            empty_set=f"[]{_V_IFACE_NAME}{{}}",
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_SLASH = CommentConfig(
            prefix="//",
            suffix="",
        )
        BLOCK = CommentConfig(
            prefix="/*",
            suffix=" */",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        ASSIGN = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="{name} := {value}"
            ),
            supports_redefinition=False,
        )
        MUT = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="mut {name} := {value}"
            ),
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = enum.auto()

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="math.inf(1)",
        negative_infinity="math.inf(-1)",
        nan="math.nan()",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = MappingProxyType(
            mapping={
                "NONE": str,
                "UNDERSCORE": format_integer_underscore,
            }
        )
        HEX = MappingProxyType(
            mapping={
                "NONE": format_integer_hex,
                "UNDERSCORE": format_integer_hex,
            }
        )
        OCTAL = MappingProxyType(
            mapping={
                "NONE": format_integer_octal,
                "UNDERSCORE": format_integer_octal,
            }
        )
        BINARY = MappingProxyType(
            mapping={
                "NONE": format_integer_binary,
                "UNDERSCORE": format_integer_binary,
            }
        )

        def get_formatter(
            self,
            numeric_separator: enum.Enum,
        ) -> Callable[[int], str]:
            """Return the integer formatter for the given separator."""
            formatter: Callable[[int], str] = self.value[
                numeric_separator.name
            ]
            return formatter

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = enum.auto()
        UNDERSCORE = enum.auto()

    class NumericStyles(enum.Enum):
        """Numeric literal style options."""

        OVERLOADED = enum.auto()

    class StringFormats(enum.Enum):
        """String format options."""

        SINGLE = "single"

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        YES = TrailingCommaConfig(multiline_trailing_comma=True)
        NO = TrailingCommaConfig(multiline_trailing_comma=False)

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats

    class VariableTypeHints(enum.Enum):
        """Variable type hint options."""

        AUTO = enum.auto()

    variable_type_hints_formats = VariableTypeHints
    declaration_styles = DeclarationStyles
    dict_entry_styles = DictEntryStyles
    dict_formats = DictFormats
    empty_dict_keys = EmptyDictKey
    float_formats = FloatFormats
    integer_formats = IntegerFormats
    numeric_literal_suffixes = NumericLiteralSuffixes
    numeric_separators = NumericSeparators
    numeric_styles = NumericStyles
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class LineEndings(enum.Enum):
        """Line ending options."""

        NEWLINE = "newline"

    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """V call style options."""

        POSITIONAL = PositionalCallStyle()

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Heterogeneous-scalar strategy options for V."""

        ERROR = _VHeterogeneousStrategyConfig(
            build_behavior=lambda: NO_HETEROGENEOUS_BEHAVIOR,
            build_preamble=lambda: no_data_preamble,
        )
        """Raise on heterogeneous scalar collections (default)."""

        INTERFACE = _VHeterogeneousStrategyConfig(
            build_behavior=_build_v_interface_behavior,
            build_preamble=_build_v_interface_preamble,
        )
        """Wrap heterogeneous scalars and null values with ``IVal(...)``
        and emit ``interface IVal {}`` in the file preamble.
        """

    heterogeneous_strategies = HeterogeneousStrategies

    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.PASCAL,
        IdentifierCase.CAMEL,
    )

    validate_spec_for_data = no_validate_spec_for_data
    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a V declaration in ``fn main()``."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        indented = textwrap.indent(text=content, prefix=self.indent)
        use_line = (
            f"\n{self.indent}_ = {variable_name}" if variable_name else ""
        )
        return f"\nfn main() {{\n{indented}{use_line}\n}}"

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap V declaration + assignment in ``fn main()``."""
        return self.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.ARRAY
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.DEFAULT
    float_format: FloatFormats = FloatFormats.REPR
    integer_format: IntegerFormats = IntegerFormats.DECIMAL
    numeric_literal_suffix: NumericLiteralSuffixes = (
        NumericLiteralSuffixes.NONE
    )
    numeric_separator: NumericSeparators = NumericSeparators.NONE
    numeric_style: NumericStyles = NumericStyles.OVERLOADED
    string_format: StringFormats = StringFormats.SINGLE
    trailing_comma: TrailingCommas = TrailingCommas.YES
    line_ending: LineEndings = LineEndings.NEWLINE
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.INTERFACE
    )
    indent: str = "\t"
    call_style: CallStyles = CallStyles.POSITIONAL

    null_literal: ClassVar[str] = "unsafe { nil }"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = True
    statement_terminator: ClassVar[str] = ";"
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ("import math",)

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Return the active call-style configuration."""
        return self.call_style.value

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash_dollar_single

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        return variable_formatter(template="{name} = {value}")

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines."""
        return self.heterogeneous_strategy.value.build_preamble()

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config."""
        return self.heterogeneous_strategy.value.build_behavior()

    @cached_property
    def type_hint_collection_preamble_lines(
        self,
    ) -> Callable[[frozenset[type]], tuple[str, ...]]:
        """Return preamble lines for empty-collection type hints."""
        return no_type_hint_preamble

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return stub declarations for a call expression."""
        return _v_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return file-scope stubs for a call expression."""
        return partial(_v_call_preamble_stub, indent=self.indent)

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into the language's call
        syntax.
        """
        return identity_call_target

    @cached_property
    def format_call_ref_identifier(self) -> Callable[[str], str]:
        """Append ``.clone()`` to copy a V map value.

        V maps are not automatically copyable in direct assignment
        context, so ``.clone()`` is required to produce a valid copy.
        """

        def _format_v_ref_identifier(name: str, /) -> str:
            """Append ``.clone()`` for V map copy semantics."""
            return f"{name}.clone()"

        return _format_v_ref_identifier

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return self.sequence_format.value

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return self.set_format.value

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format.value.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=fixed_open(open_str="{"),
            close="}",
            format_entry=dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=f"map[string]{_V_IFACE_NAME}{{}}",
            preamble_lines=(),
            narrowed_open=None,
            supports_trailing_comma=True,
        )

    @cached_property
    def trailing_comma_config(self) -> TrailingCommaConfig:
        """Configuration for trailing-comma behavior."""
        return self.trailing_comma.value

    @cached_property
    def format_bytes(self) -> Callable[[bytes], str]:
        """Callable that formats a bytes value as a string literal."""
        return self.bytes_format

    @cached_property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a date as a string literal."""
        return self.date_format

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        return self.datetime_format

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal.

        Values in 32-bit signed range are formatted with the chosen
        integer format.  Values outside that range but within 64-bit
        signed range use ``i64(...)``.  Values outside 64-bit signed
        range use ``u64(...)`` (or raise for negative overflow).
        """
        base = self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )
        i64_or_u64_fallback = make_overflow_fallback_formatter(
            base=_make_v_i64_formatter(base=base),
            fallback=make_unsigned_overflow_fallback(
                format_positive=_format_v_u64_positive,
                language_name="V",
            ),
        )
        return make_overflow_fallback_formatter(
            base=base,
            fallback=i64_or_u64_fallback,
            min_value=_V_I32_MIN,
            max_value=_V_I32_MAX,
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="{"),
            close="}",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return dict_entry_with_separator(
            separator=": ",
            format_value=passthrough_sequence_entry,
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return self.declaration_style.value.formatter

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (V needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (V needs none)."""
        return {}

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines from the scalar map."""
        return body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )
