"""Scheme language specification."""

import dataclasses
import datetime
import enum
import math
from collections.abc import Callable, Sequence
from functools import cached_property
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
    format_time_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_template,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    variable_declaration_formatter,
    variable_formatter,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_strings import format_string_backslash
from literalizer._language import (
    ALL_REF_CASES,
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    BareIntegerWidthStrategies,
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
    ModifierCombination,
    NestedMapWideningVariant,
    OrderedMapFormatConfig,
    PrefixCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    VariantMetadata,
    body_preamble_from_scalars,
    default_format_call_variable_assignment,
    default_format_call_variable_declaration,
    default_sequence_binding_declarations,
    default_wrap_calls_with_declarations,
    identity_call_arg,
    identity_call_statement,
    identity_call_target,
    identity_constructor_target,
    never_inhibits_consuming_form,
    no_call_binding_body_preamble,
    no_call_binding_file_pragmas,
    no_call_stub,
    no_data_preamble,
    no_format_integer_widened,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    wrap_combined_in_file_noop,
    wrap_in_file_noop,
)
from literalizer._types import OrderedMap, Value
from literalizer.exceptions import (
    CallArgNotSupportedError,
    UnrepresentableInputError,
    UnrepresentableSpecialFloatError,
)

# Format definitions used while ``json_type=GUILE_JSON`` is active.
# Objects are emitted as association lists
# (``(list (cons "k" v) ...)``) because the ``json-valid?`` predicate
# in guile-json accepts only that form, not hash tables (see
# ``json/builder.scm:188`` upstream; matches the round-trip helper's
# existing ``normalize`` walker).  Arrays become vectors
# (``(vector v ...)``) since the ``scm->json`` writer in guile-json
# distinguishes vector arrays from list-of-pairs objects.  Sets
# reuse the array (vector) form because JSON has no set type.
_GUILE_JSON_SEQUENCE_CONFIG = SequenceFormatConfig(
    sequence_open=fixed_open(open_str="(vector "),
    close=")",
    supports_heterogeneity=True,
    single_element_trailing_comma=False,
    supports_trailing_comma=False,
    empty_sequence="(vector)",
    preamble_lines=(),
    format_entry=passthrough_sequence_entry,
    typed_opener_fallback=None,
    uses_typed_literal_for_scalars=False,
    requires_uniform_record_shapes=False,
    declared_type=None,
    narrowed_empty_form=None,
)

_GUILE_JSON_SET_CONFIG = SetFormatConfig(
    set_open=fixed_open(open_str="(vector "),
    close=")",
    empty_set="(vector)",
    preamble_lines=(),
    set_opener_template="",
    supports_heterogeneity=True,
    supports_trailing_comma=False,
)


@beartype
def _scheme_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Scheme stub definitions for a call name.

    For dotted names like ``app.client.fetch``, one ``define`` is
    emitted per prefix so that intermediate identifiers are bound.
    Each stub accepts any number of positional arguments via a rest
    parameter.  Stub bodies are ``(if #f #f)`` (the unspecified value)
    for void stubs and ``0`` for value stubs.
    """
    body = "(if #f #f)" if stub_return is StubReturn.VOID else "0"
    return tuple(
        f"(define {'.'.join(parts[: i + 1])} (lambda args {body}))"
        for i in range(len(parts))
    )


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Scheme(metaclass=LanguageCls):
    """Scheme language specification."""

    format_integer_widened = no_format_integer_widened
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    format_call_variable_declaration = default_format_call_variable_declaration
    format_call_variable_assignment = default_format_call_variable_assignment
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".scm"
    pygments_name = "scheme"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = True
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_zero_parameter_calls = True
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_multi_param_call_wrapper_stub = True
    supports_dict_literal_as_free_expression = True
    supports_module_name = False
    supports_empty_dict_key = False
    supports_call_style = True
    supports_default_dict_key_type = False
    supports_default_dict_value_type = False
    supports_default_sequence_element_type = False
    supports_default_set_element_type = False
    supports_default_ordered_map_value_type = False
    non_default_kwargs: ClassVar[dict[str, str]] = {}
    declaration_style_sequence_format_overrides: ClassVar[dict[str, str]] = {}
    json_type_variant_name_suffix: ClassVar[str | None] = None
    supports_non_ascii_string_literals = True
    variant_metadata: ClassVar[VariantMetadata] = VariantMetadata(
        fixture_module_name_template=None,
        fixture_module_name_lowercase=False,
        golden_filename_lowercase=False,
        collection_layout_category="collection_layout",
        record_variants=frozenset(),
        nested_map_widening=NestedMapWideningVariant.NONE,
        modifier_sequence_format_overrides={},
    )
    supports_record_struct_name_prefix = False
    supports_record_shape_names = False
    supports_non_string_dict_keys = True

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

    class DateFormats(enum.Enum):
        """Date format options for Scheme."""

        ISO = DateFormatConfig(
            formatter=format_date_iso, type_produced=str, preamble_lines=()
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Scheme."""

        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            type_produced=str,
            preamble_lines=(),
        )

        EPOCH = DatetimeFormatConfig(
            formatter=format_datetime_epoch,
            type_produced=int,
            preamble_lines=(),
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
        """Sequence type options for Scheme."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="(list "),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=False,
            empty_sequence="(list)",
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Scheme."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="(list "),
            close=")",
            empty_set="(list)",
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        SEMICOLON = CommentConfig(
            prefix=";",
            suffix="",
        )
        BLOCK = CommentConfig(
            prefix="#|",
            suffix=" |#",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        DEFINE = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="(define {name} {value})"
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
        positive_infinity="+inf.0",
        negative_infinity="-inf.0",
        nan="+nan.0",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.auto()

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = enum.auto()

    class NumericStyles(enum.Enum):
        """Numeric literal style options."""

        OVERLOADED = enum.auto()

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.auto()

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        NO = TrailingCommaConfig(multiline_trailing_comma=False)

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats

    class VariableTypeHints(enum.Enum):
        """Variable type hint options."""

        NEVER = enum.auto()
        SAFE = enum.auto()

    variable_type_hints_formats = VariableTypeHints
    declaration_styles = DeclarationStyles
    dict_entry_styles = DictEntryStyles
    dict_formats = DictFormats
    empty_dict_keys = EmptyDictKey
    float_formats = FloatFormats
    integer_formats = IntegerFormats
    integer_width_strategies = BareIntegerWidthStrategies
    numeric_literal_suffixes = NumericLiteralSuffixes
    numeric_separators = NumericSeparators
    numeric_styles = NumericStyles
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class StatementTerminatorStyles(enum.Enum):
        """Statement terminator options."""

        SEMICOLON = enum.auto()

    statement_terminator_styles = StatementTerminatorStyles

    class CallStyles(enum.Enum):
        """Scheme call style options."""

        PREFIX = PrefixCallStyle(
            arg_separator=" ",
            keyword_prefix="",
        )

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Heterogeneous-scalar strategy options — this language only
        supports raising.
        """

        ERROR = NO_HETEROGENEOUS_BEHAVIOR

    heterogeneous_strategies = HeterogeneousStrategies

    class JsonTypes(enum.Enum):
        """JSON value type options for Scheme."""

        GUILE_JSON = "guile-json scm->json value shape"
        """Guile-json's ``scm->json`` value shape: Scheme association
        lists for objects, vectors for arrays, ``'null`` for JSON
        null.  The literalized output can be handed directly to
        ``(scm->json ...)`` without a runtime shape walker.
        """

    json_types = JsonTypes

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for Scheme."""

        R7RS = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.KEBAB,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = ALL_REF_CASES

    @cached_property
    def validate_call_arg(self) -> Callable[[Value], None]:
        """Return call-argument validation for this language."""
        return no_validate_call_arg

    @cached_property
    def format_call_statement(self) -> Callable[[str], str]:
        """Return call-statement formatting for this language."""
        return identity_call_statement

    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap code in a valid file (no-op)."""
        return wrap_in_file_noop(
            content=content,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap declaration and assignment in a valid file (no-op)."""
        return wrap_combined_in_file_noop(
            declaration=declaration,
            assignment=assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.SEMICOLON
    declaration_style: DeclarationStyles = DeclarationStyles.DEFINE
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.DEFAULT
    float_format: FloatFormats = FloatFormats.REPR
    integer_format: IntegerFormats = IntegerFormats.DECIMAL
    integer_width_strategy: BareIntegerWidthStrategies = (
        BareIntegerWidthStrategies.BARE
    )
    numeric_literal_suffix: NumericLiteralSuffixes = (
        NumericLiteralSuffixes.NONE
    )
    numeric_separator: NumericSeparators = NumericSeparators.NONE
    numeric_style: NumericStyles = NumericStyles.OVERLOADED
    string_format: StringFormats = StringFormats.DOUBLE
    trailing_comma: TrailingCommas = TrailingCommas.NO
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.SEMICOLON
    )
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    json_type: JsonTypes | None = None
    call_style: CallStyles = CallStyles.PREFIX
    # The `Install apt packages` step in `.github/workflows/lint.yml`
    # installs the `guile-3.0` apt package, whose Guile 3.x implements
    # the `R7RS` standard, matching this default (`R7RS`). The pin is
    # for reproducible builds, not language selection. Keep the two in
    # sync.
    language_version: VersionFormats = VersionFormats.R7RS
    indent: str = "    "

    true_literal: ClassVar[str] = "#t"
    false_literal: ClassVar[str] = "#f"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = " "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ""
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def _json_type_active(self) -> bool:
        """Return whether ``json_type=GUILE_JSON`` is selected."""
        return self.json_type is not None

    @cached_property
    def null_literal(self) -> str:
        """The literal representing null.

        Under :attr:`json_type` the value must be the null sentinel
        that guile-json recognizes (the symbol ``'null``, matching
        the default of its ``*null*`` parameter); the flat-list mode
        uses the empty list, which is conventional for ``null`` in
        Scheme.
        """
        return "'null" if self._json_type_active else "'()"

    @cached_property
    def static_preamble(self) -> Sequence[str]:
        """File-scope preamble.

        Under :attr:`json_type` the rendered value is a tree of
        Scheme association lists and vectors that
        ``(scm->json ...)`` accepts directly, so the ``(json)``
        module must be imported.
        """
        if self._json_type_active:
            return ("(use-modules (json))",)
        return ()

    def validate_spec_for_data(self, data: Value) -> None:
        """Reject data that ``json_type=GUILE_JSON`` cannot represent.

        Walks *data* under :attr:`json_type` to reject non-string dict
        keys (JSON objects keys must be strings) and the special
        floats ``NaN`` / ``+inf.0`` / ``-inf.0`` (not valid JSON).
        """
        if self._json_type_active:
            self._validate_guile_json_value(data)

    def _validate_guile_json_value(self, data: Value, /) -> None:
        """Recursively validate that *data* is JSON-representable."""
        match data:
            case OrderedMap() | dict():
                for key, value in data.items():
                    if not isinstance(key, str):
                        msg = (
                            "Scheme json_type=GUILE_JSON can only "
                            "represent dict keys as JSON object "
                            f"strings, not {type(key).__name__}"
                        )
                        raise UnrepresentableInputError(msg)
                    self._validate_guile_json_value(value)
            case list() | set():
                for item in data:
                    self._validate_guile_json_value(item)
            case float():
                self._validate_guile_json_float(value=data)
            case _:
                return

    @staticmethod
    def _validate_guile_json_float(*, value: float) -> None:
        """Reject ``NaN`` / ``+inf.0`` / ``-inf.0`` floats."""
        if math.isnan(value) or math.isinf(value):
            msg = (
                "Scheme json_type=GUILE_JSON cannot represent the "
                f"special float {value!r}: JSON has no NaN or "
                "infinity."
            )
            raise UnrepresentableSpecialFloatError(msg)

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Return the active call-style configuration."""
        return self.call_style.value

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Format an int value as a literal."""
        return str

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        return variable_formatter(template="(set! {name} {value})")

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines."""
        return no_data_preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config."""
        return self.heterogeneous_strategy.value

    @cached_property
    def call_data_dependent_preamble(
        self,
    ) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines for call rendering."""
        return self.data_dependent_preamble

    @cached_property
    def type_hint_collection_preamble_lines(
        self,
    ) -> Callable[[frozenset[type]], tuple[str, ...]]:
        """Return preamble lines for empty-collection type hints."""
        return no_type_hint_preamble

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return stub declarations for a call expression."""
        return _scheme_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return file-scope stubs for a call expression."""
        return no_call_stub

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into the language's call
        syntax.
        """
        return identity_call_target

    @cached_property
    def format_call_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Raise for any ``{"$ref": "name"}`` identifier.

        Scheme output is not wrapped in a function body; variable
        references require a surrounding ``define`` that cannot be
        injected via the call framework.
        """

        def _raise_for_scheme_ref(name: str, _value: Value | None, /) -> str:
            """Raise ``CallArgNotSupportedError`` unconditionally."""
            raise CallArgNotSupportedError(
                language_name="Scheme",
                reason=(
                    "Scheme output is not wrapped in a function body; "
                    f"variable references require a surrounding define "
                    f"(got {name!r})"
                ),
            )

        return _raise_for_scheme_ref

    @cached_property
    def format_call_arg_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier in a call-argument
        context.

        Delegates to :attr:`format_call_ref_identifier`.  Override this to
        allow call-argument ``$ref`` values that would otherwise be rejected.
        """
        return self.format_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier_consumable(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Format a ``$ref`` the caller authorized as consumable.

        Delegates to :attr:`format_call_arg_ref_identifier`.  Override
        this to opt into a consuming form (e.g. C++ ``std::move``).
        """
        return self.format_call_arg_ref_identifier

    @cached_property
    def consumable_ref_value_inhibits_consuming_form(
        self,
    ) -> Callable[[Value], bool]:
        """Predicate deciding whether a ref's underlying value type
        inhibits the consume form.

        Delegates to :data:`never_inhibits_consuming_form`.  Languages
        whose consume operator rejects certain value types (notably
        the Mojo ``^`` on register-trivial scalars) override this.
        """
        return never_inhibits_consuming_form

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format.

        Under :attr:`json_type` arrays are emitted as ``(vector ...)``
        so ``scm->json`` round-trips them as JSON arrays unambiguously.
        """
        if self._json_type_active:
            return _GUILE_JSON_SEQUENCE_CONFIG
        return self.sequence_format.value

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format.

        Under :attr:`json_type` sets share the array form
        (``(vector ...)``); JSON has no native set type.
        """
        if self._json_type_active:
            return _GUILE_JSON_SET_CONFIG
        return self.set_format.value

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        if self._json_type_active:
            return _GUILE_JSON_SEQUENCE_CONFIG.sequence_open
        return self.sequence_format.value.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting.

        Each entry is a ``(cons "k" v)`` pair and the dict wraps them
        in ``(list ...)`` to form a Scheme association list -- the
        conventional key/value mapping idiom, what ``assoc`` /
        ``alist->hash-table`` expect, and what ``scm->json``'s
        ``json-valid?`` accepts for JSON objects under
        :attr:`json_type`.  A list of ``pair?`` elements is locally
        distinguishable from a heterogeneous sequence, unlike the
        legacy flat ``(list "k" v "k" v ...)`` form.
        """
        return DictFormatConfig(
            dict_open=fixed_open(open_str="(list "),
            close=")",
            format_entry=dict_entry_with_template(
                template="(cons {key} {value})",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict="(list)",
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
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        return format_time_iso

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting.

        Under :attr:`json_type` an ordered map is rendered as the same
        association-list shape used for plain dicts so ``scm->json``
        round-trips it as a JSON object (key order is preserved by
        the surrounding list's element order).
        """
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="(list "),
            close=")",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry.

        Each entry is a ``(cons "k" v)`` pair matching
        :attr:`dict_format_config`.
        """
        return dict_entry_with_template(
            template="(cons {key} {value})",
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
        """Per-instance scalar preamble (Scheme needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Scheme needs none)."""
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
