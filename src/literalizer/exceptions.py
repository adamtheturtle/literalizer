"""Exceptions raised by literalizer."""

import enum

type InputPath = tuple[str | int, ...]


class LiteralizerError(Exception):
    """Base class for every public error raised by Literalizer.

    ``path`` identifies the value associated with an error, using mapping
    keys and zero-based sequence indexes. It is ``None`` when an error is
    not associated with one particular input value.
    """

    def __init__(
        self,
        message: str = "",
        /,
        *,
        path: InputPath | None = None,
    ) -> None:
        """Create a Literalizer error with optional input location
        data.
        """
        super().__init__(message)
        self.path = path


class UnsupportedOptionError(LiteralizerError):
    """Raised when a language does not accept a known constructor option.

    Capability flags remain the preferred pre-construction check. This error
    is the backstop when an option supported by another Literalizer language
    is passed to a language that does not offer it.
    """

    def __init__(self, *, language_name: str, option: str) -> None:
        """Create an ``UnsupportedOptionError``."""
        super().__init__(f"{language_name} does not support option {option!r}")
        self.language_name = language_name
        self.option = option


class ParseError(LiteralizerError):
    """Raised when input cannot be parsed into a data structure.

    Base class for every input-parsing failure; catch it to handle any
    malformed input uniformly.  To resolve, validate the source against
    its declared ``input_format``. ``line`` and ``column`` are one-based
    parser positions when the underlying parser supplies them.
    """

    def __init__(
        self,
        message: str,
        /,
        *,
        line: int | None = None,
        column: int | None = None,
    ) -> None:
        """Create a parse error with optional source coordinates."""
        super().__init__(message)
        self.line = line
        self.column = column


class JSONParseError(ParseError):
    """Raised when a JSON string cannot be parsed.

    To resolve, fix the JSON syntax, or pass the correct ``input_format``
    if the data is really JSON5, YAML, or TOML.
    """


class YAMLParseError(ParseError):
    """Raised when a YAML string cannot be parsed.

    To resolve, fix the YAML syntax, or choose the matching
    ``input_format``.
    """


class TOMLParseError(ParseError):
    """Raised when a TOML string cannot be parsed.

    To resolve, fix the TOML syntax, or choose the matching
    ``input_format``.
    """


class JSON5ParseError(ParseError):
    """Raised when a JSON5 string cannot be parsed.

    To resolve, fix the JSON5 syntax, or choose the matching
    ``input_format``.
    """


class InvalidDictKeyError(LiteralizerError):
    """Raised when a dict key cannot be represented in the target language.

    This includes empty-string keys and keys containing characters that
    the language's label syntax does not support (e.g. control characters
    in Dhall backtick-quoted labels).  To resolve, remove or rename the
    offending key.
    """


class UnrepresentableInputError(LiteralizerError):
    """Raised when an input value cannot be represented in the target
    language.

    Used as the centralized error for shape-level rejections at the
    formatting boundary, e.g. when a dict carries a non-string key for
    a language whose surface syntax only admits string-typed keys.  To
    resolve, adjust the data to a representable shape, or pick a language
    that supports it.
    """


class TargetScalarCollisionError(UnrepresentableInputError):
    """Raised when distinct collection scalars render identically.

    Set members and mapping keys must retain distinct target identities.
    """

    def __init__(
        self,
        *,
        language_name: str,
        first: object,
        second: object,
        rendered: str,
    ) -> None:
        """Create a ``TargetScalarCollisionError``."""
        super().__init__(
            f"{language_name} renders distinct collection scalars "
            f"{first!r} and {second!r} identically as {rendered!r}"
        )
        self.first = first
        self.second = second
        self.rendered = rendered


class UnrepresentableStringError(UnrepresentableInputError):
    """Raised when a string contains a character the target language
    cannot represent in a string literal.

    Used when the language or selected string format has no safe escape
    or embedding for a given code point (for example an embedded null
    byte in R or COBOL).  To resolve, remove the offending character, or
    target a
    language whose string literals can represent it.
    """

    def __init__(self, *, language_name: str, character_name: str) -> None:
        """Create an ``UnrepresentableStringError``."""
        super().__init__(
            f"{language_name} string literals cannot represent "
            f"{character_name}"
        )
        self.language_name = language_name
        self.character_name = character_name


class UnrepresentableNullError(UnrepresentableInputError):
    """Raised when null collapses onto another target-language value."""

    def __init__(self, *, language_name: str, conflated_value: str) -> None:
        """Create an ``UnrepresentableNullError``."""
        super().__init__(
            f"{language_name} cannot represent null distinctly from "
            f"{conflated_value}"
        )
        self.language_name = language_name
        self.conflated_value = conflated_value


class HeterogeneousCollectionError(LiteralizerError):
    """Base class for errors raised when data is incompatible with the
    target language's collection-shape constraints.

    To resolve, pick a non-default ``heterogeneous_strategy`` (see
    :ref:`heterogeneous-strategies`) or render the value through a
    ``json_type`` (see :ref:`json-value-types`); catch this base class to
    skip any heterogeneous input a strict-typed language cannot hold.
    """


class HeterogeneousScalarCollectionError(HeterogeneousCollectionError):
    """Raised when a collection contains scalars of multiple types and
    the target language requires homogeneous scalar collections.

    For example, ``[1, "two", 3.0]`` for a language that needs a single
    element type.  To resolve, set ``heterogeneous_strategy`` to
    ``TAGGED_ENUM`` (or the language's equivalent) to wrap each scalar,
    or to ``TUPLE`` for a fixed-length array.
    """


class HeterogeneousSiblingListsError(HeterogeneousCollectionError):
    """Raised when sibling sub-lists contain scalars that, combined,
    span multiple types and the target language requires homogeneous
    scalar collections.

    To resolve, use a ``TAGGED_ENUM`` strategy, or render the value
    through a ``json_type``.
    """


class MixedDictValuesError(HeterogeneousCollectionError):
    """Raised when a dict has values spanning multiple type families
    and the target language requires homogeneous dict values.

    To resolve, use the ``RECORD`` strategy if the dict is conceptually
    a record, or a ``json_type`` for arbitrary mappings.
    """


class HeterogeneousSiblingMapsError(HeterogeneousCollectionError):
    """Raised when a container holds sibling maps whose value types force
    a widened dict slot the target language cannot represent.

    Languages whose dict opener builds a content-specific value type
    (variant/union typing, e.g. C++'s ``std::variant``) have no single
    "accepts anything" value type that every sibling map converts to, so
    a narrower inner map does not fit the widened slot the enclosing
    container declares.  Unlike Go or Kotlin, whose ``map[string]any`` /
    ``Any?`` fallback lets ``literalize`` widen the inner maps, these
    languages can only emit non-compiling code, so ``literalize`` raises
    instead.

    To resolve, use the ``RECORD`` strategy so each map renders as its
    own struct, or render the value through a ``json_type``.
    """


class MixedDictKeysError(HeterogeneousCollectionError):
    """Raised when a dict has keys spanning multiple type families
    and the target language requires homogeneous dict keys.

    To resolve, use a single key type, or render through a ``json_type``.
    """


class MixedListValuesError(HeterogeneousCollectionError):
    """Raised when a list has elements spanning multiple type families
    and the target language requires homogeneous list elements.

    To resolve, use a richer ``heterogeneous_strategy`` or a
    ``json_type``.
    """


class MixedDictShapesError(HeterogeneousCollectionError):
    """Raised when a list contains dicts with different key sets and
    the target language requires uniform record shapes (e.g. Dhall).

    To resolve, make every dict share the same keys, or use a
    ``json_type``.
    """


class HeterogeneousSetError(HeterogeneousCollectionError):
    """Raised when a set contains scalars of multiple types and the
    target language requires homogeneous set elements.

    To resolve, use one scalar type, or a richer
    ``heterogeneous_strategy``.
    """


class TupleArityNotRepresentableError(HeterogeneousCollectionError):
    """Raised when the ``TUPLE`` heterogeneous strategy meets a
    tuple-eligible heterogeneous scalar array whose length the target
    language has no native fixed-size tuple for.

    Kotlin only has ``Pair`` (two elements) and ``Triple`` (three
    elements); an array of any other length cannot be represented as a
    typed tuple without losing the per-position types, so
    ``literalize`` raises rather than falling back to a homogeneous
    list (which would re-trip the heterogeneity checks the strategy
    exists to satisfy).  Subclasses
    :class:`HeterogeneousCollectionError` so the same callers that
    already skip a heterogeneous input the language cannot represent
    also skip this one.

    To resolve, shorten the array to a length the language supports,
    choose a language without the tuple-length cap (Rust, Scala), or
    switch to a ``TAGGED_ENUM`` strategy.
    """

    def __init__(self, *, arity: int) -> None:
        """Create a ``TupleArityNotRepresentableError``.

        The keyword argument is the element count of the rejected
        array.
        """
        super().__init__(
            f"a heterogeneous scalar array of {arity} elements has no "
            f"native fixed-size tuple in the target language"
        )
        self.arity = arity


class NullInCollectionError(LiteralizerError):
    """Raised when a collection contains null elements and the chosen
    format does not support them (e.g. Java's ``List.of()``).

    To resolve, remove the nulls, or select a collection format that
    admits them.
    """


class PerElementNotListError(LiteralizerError):
    """Raised when ``per_element=True`` but the parsed data is not a
    list.

    To resolve, pass a list, or drop ``per_element``.
    """


class ParameterCountMismatchError(LiteralizerError):
    """Raised when the number of ``parameter_names`` does not match the
    number of argument values in a function-call row.

    To resolve, make ``parameter_names`` the same length as each row of
    values.
    """

    def __init__(self, *, expected: int, got: int) -> None:
        """Create a ``ParameterCountMismatchError``."""
        super().__init__(
            f"Expected {expected} parameters but got {got} values"
        )
        self.expected = expected
        self.got = got


class CallsNotSupportedByLanguageError(LiteralizerError):
    """Raised when the target language itself has no function call
    syntax (e.g. pure data/markup formats like YAML, TOML, JSON5, Norg).

    To resolve, use :func:`~literalizer.literalize` instead, or target a
    programming language.
    """

    def __init__(self, *, language_name: str) -> None:
        """Create a ``CallsNotSupportedByLanguageError``."""
        super().__init__(f"{language_name} has no function call syntax")
        self.language_name = language_name


class CallsNotSupportedByToolError(LiteralizerError):
    """Raised when literalizer has not yet implemented function call
    rendering for the target language, even though the language itself
    has function call syntax.

    To resolve, target a language whose call rendering is implemented.
    """

    def __init__(self, *, language_name: str) -> None:
        """Create a ``CallsNotSupportedByToolError``."""
        super().__init__(
            f"literalizer does not support function call rendering "
            f"for {language_name}"
        )
        self.language_name = language_name


class CallArgNotSupportedError(LiteralizerError):
    """Raised when a call argument value cannot be expressed as a
    positional argument in the target language's call syntax.

    Used by languages whose call syntax does not accept compound
    literals as arguments, e.g. Bash, where ``cmd (1 2 3)`` parses
    as a nested ``(...)`` child-process invocation rather than an
    inline array value.

    To resolve, bind the value to a name first, or target a language
    that accepts the argument inline.
    """

    def __init__(self, *, language_name: str, reason: str) -> None:
        """Create a ``CallArgNotSupportedError``."""
        super().__init__(
            f"{language_name} cannot accept this value as a call "
            f"argument: {reason}"
        )
        self.language_name = language_name
        self.reason = reason


class IncompatibleFormatsError(LiteralizerError):
    """Raised when a combination of format options produces invalid code.

    For example, Rust ``CONST`` and ``STATIC`` declaration styles
    require constant-expression initializers, but the ``VEC`` sequence
    format produces ``vec![…]`` which is not a constant expression.

    To resolve, change one of the conflicting options so they agree.
    """


class InvalidRecordNameError(LiteralizerError):
    """Raised when ``record_struct_name_prefix`` or a value in
    ``record_shape_names`` is not a valid PascalCase identifier, collides
    with a reserved keyword of the target language, collides with
    ``heterogeneous_value_enum_name``, or duplicates another mapped
    struct name.

    To resolve, use distinct, valid PascalCase names that avoid reserved
    keywords.
    """


class InvalidCppRawStringDelimiterError(LiteralizerError, ValueError):
    """Raised when C++'s multiline raw-string delimiter base is invalid.

    C++ raw-string delimiters are limited to 16 characters from the basic
    source character set and exclude whitespace, parentheses, and
    backslashes.  Literalizer also requires a non-empty configured base so
    the empty delimiter can remain its first automatically selected
    candidate.
    """

    def __init__(self, *, delimiter: str, reason: str) -> None:
        """Create an ``InvalidCppRawStringDelimiterError``."""
        super().__init__(
            "Cpp multiline_raw_string_delimiter_base "
            f"{delimiter!r} is invalid: {reason}"
        )
        self.delimiter = delimiter
        self.reason = reason


class ReservedVariableNameError(LiteralizerError):
    """Raised when a variable or reference name is reserved by the target
    language.

    To resolve, use a non-reserved identifier for the target language.
    """

    def __init__(
        self,
        *,
        language_name: str,
        name_source: str = "NewVariable",
        variable_name: str,
    ) -> None:
        """Create a ``ReservedVariableNameError``."""
        super().__init__(
            f"{language_name} cannot use {name_source} name "
            f"{variable_name!r}: it is a reserved identifier"
        )
        self.language_name = language_name
        self.name_source = name_source
        self.variable_name = variable_name


class InvalidNewVariableNameError(LiteralizerError):
    """Raised when a variable or reference name is not a syntactically
    valid identifier for the target language.

    Literalizer does not repair or escape variable names.  To resolve, use
    a name whose spelling is valid for the target language.
    """

    def __init__(
        self,
        *,
        language_name: str,
        name_source: str = "NewVariable",
        variable_name: str,
    ) -> None:
        """Create an ``InvalidNewVariableNameError``."""
        super().__init__(
            f"{language_name} cannot use {name_source} name "
            f"{variable_name!r}: it is not a valid identifier"
        )
        self.language_name = language_name
        self.name_source = name_source
        self.variable_name = variable_name


class InvalidModuleNameError(LiteralizerError):
    """Raised when a module name is not a safe source identifier."""

    def __init__(self, *, language_name: str, module_name: str) -> None:
        """Create an ``InvalidModuleNameError``."""
        super().__init__(
            f"{language_name} cannot use module_name {module_name!r}: "
            "it is not a valid identifier"
        )
        self.language_name = language_name
        self.module_name = module_name


class InvalidCallParameterNameError(LiteralizerError):
    """Raised when a call parameter is not a target-language
    identifier.
    """

    def __init__(
        self,
        *,
        language_name: str,
        parameter_name: str,
        reason: str,
    ) -> None:
        """Create an ``InvalidCallParameterNameError``."""
        super().__init__(
            f"{language_name} cannot use call parameter "
            f"{parameter_name!r}: {reason}"
        )
        self.language_name = language_name
        self.parameter_name = parameter_name
        self.reason = reason


class InvalidCallTargetError(LiteralizerError):
    """Raised when a call target is not a valid target-language name."""

    def __init__(
        self, *, language_name: str, target_function: str, reason: str
    ) -> None:
        """Create an ``InvalidCallTargetError``."""
        super().__init__(
            f"{language_name} cannot use call target "
            f"{target_function!r}: {reason}"
        )
        self.language_name = language_name
        self.target_function = target_function
        self.reason = reason


class InvalidRenderArgumentError(LiteralizerError, ValueError):
    """Base class for invalid rendering-option combinations."""


class InvalidValueInputError(InvalidRenderArgumentError):
    """Raised when a supplemental Python value is cyclic or too deep."""

    def __init__(self, *, argument_name: str) -> None:
        """Create an ``InvalidValueInputError``."""
        super().__init__(
            f"{argument_name} must contain an acyclic value within the "
            "supported nesting depth"
        )
        self.argument_name = argument_name


class BoundRefOutputCollisionError(InvalidRenderArgumentError):
    """Raised when a bound ref would re-declare the output binding."""

    def __init__(self, *, name: str) -> None:
        """Create a ``BoundRefOutputCollisionError``."""
        super().__init__(
            f"bound_refs name {name!r} collides with the output variable"
        )
        self.name = name


class InvalidPreIndentLevelError(InvalidRenderArgumentError):
    """Raised when ``pre_indent_level`` is negative."""

    def __init__(self) -> None:
        """Create an ``InvalidPreIndentLevelError``."""
        super().__init__(
            "pre_indent_level must be greater than or equal to zero"
        )


class InvalidSequenceArgumentError(InvalidRenderArgumentError):
    """Raised when a sequence argument is passed as a bare string."""

    def __init__(self, *, argument_name: str) -> None:
        """Create an ``InvalidSequenceArgumentError``."""
        super().__init__(
            f"{argument_name} must be a sequence of strings, not a string"
        )
        self.argument_name = argument_name


class ModuleNameVariableCollisionError(InvalidRenderArgumentError):
    """Raised when the wrapper name is the bound variable's own name."""

    def __init__(self, *, language_name: str, name: str) -> None:
        """Create a ``ModuleNameVariableCollisionError``."""
        super().__init__(
            f"{language_name} cannot use module_name {name!r}: the "
            "wrapper and the variable it binds share one scope"
        )
        self.language_name = language_name
        self.name = name


class RefOutputCollisionError(InvalidRenderArgumentError):
    """Raised when a ref identifier is the output binding's own name."""

    def __init__(self, *, name: str) -> None:
        """Create a ``RefOutputCollisionError``."""
        super().__init__(
            f"ref name {name!r} collides with the output variable"
        )
        self.name = name


class DelimiterlessVariableError(InvalidRenderArgumentError):
    """Raised when a delimiter-less collection is bound as one value."""

    def __init__(self) -> None:
        """Create a ``DelimiterlessVariableError``."""
        super().__init__(
            "include_delimiters=False cannot be combined with variable_form"
        )


class DelimiterlessWrappedFileError(InvalidRenderArgumentError):
    """Raised when a delimiter-less fragment would become a whole file."""

    def __init__(self) -> None:
        """Create a ``DelimiterlessWrappedFileError``."""
        super().__init__(
            "include_delimiters=False cannot be combined with wrap_in_file"
        )


class ExistingVariableNotSelfContainedError(InvalidRenderArgumentError):
    """Raised when a complete file would assign an undeclared name."""

    def __init__(self, *, language_name: str) -> None:
        """Create an ``ExistingVariableNotSelfContainedError``."""
        super().__init__(
            f"{language_name} cannot combine ExistingVariable with "
            "wrap_in_file=True because the assignment has no prior declaration"
        )
        self.language_name = language_name


class InvalidVariableModifierError(LiteralizerError):
    """Raised when a declaration modifier belongs to another language."""

    def __init__(
        self,
        *,
        language_name: str,
        modifier: enum.Enum,
    ) -> None:
        """Create an ``InvalidVariableModifierError``."""
        modifier_name = f"{type(modifier).__qualname__}.{modifier.name}"
        super().__init__(
            f"{language_name} cannot apply variable modifier "
            f"{modifier_name}: it is not a member of the target "
            "language's Modifiers enum"
        )
        self.language_name = language_name
        self.modifier = modifier


class UnrepresentableIntegerError(LiteralizerError):
    """Raised when an integer value exceeds the range the target
    language can represent natively.

    Used by languages whose fixed-width integer types cannot hold
    values outside the signed 64-bit range (e.g. Fortran default
    ``integer``, Cobol ``PIC S9(18)``, PureScript ``Int``) when no
    external arbitrary-precision integer library is assumed to be
    available.

    To resolve, keep integers within range, or target a language with
    wider or arbitrary-precision integers.
    """


class ExcessiveIntegerDigitsError(LiteralizerError):
    """Raised when an integer is too wide for the interpreter to write out.

    CPython refuses to convert an integer of more than
    ``sys.get_int_max_str_digits()`` decimal digits to text, and the
    ``ValueError`` it raises names ``sys.set_int_max_str_digits``, which
    describes the interpreter rather than anything about the input or
    the target language.  Both reading such an integer from a document
    and rendering one supplied through the API raise this instead.

    To resolve, use a narrower integer, or raise the interpreter limit
    with ``sys.set_int_max_str_digits`` before calling.
    """

    def __init__(self, *, limit: int) -> None:
        """Create an ``ExcessiveIntegerDigitsError``."""
        super().__init__(
            f"integer has more decimal digits than the {limit} this "
            "interpreter converts to text"
        )
        self.limit = limit


class UnrepresentableEmptyDictError(LiteralizerError):
    """Raised when an empty dict is passed to a target language whose
    runtime cannot distinguish an empty mapping from an empty sequence.

    Lua, PHP, and R encode both empty arrays and empty objects with the
    same surface syntax (``{}``, ``[]``, and ``list()`` respectively),
    so the JSON encoders in their ecosystems serialize an empty mapping
    as ``[]``.  The literalizer refuses to emit a literal that cannot
    round-trip rather than silently lose the mapping/sequence
    distinction.

    To resolve, drop the empty mapping, or target a language that
    distinguishes the two.
    """


class UnrepresentableSpecialFloatError(LiteralizerError):
    """Raised when a non-finite float (``inf``, ``-inf``, or ``nan``)
    is passed to a target language whose runtime cannot produce IEEE
    754 special float values.

    Used by Gleam on the Erlang target, which has no expression that
    evaluates to a non-finite float.

    To resolve, replace the non-finite floats with finite values, or
    pick another language.
    """


class UnsupportedIdentifierCaseError(LiteralizerError):
    """Raised when ``literalize`` or ``literalize_call`` is passed a
    ``ref_case`` that is not in the target language's
    ``supported_ref_cases`` -- i.e. one that would not produce a
    syntactically legal identifier in the target language.

    To resolve, choose a ``ref_case`` from the language's
    ``supported_ref_cases``.
    """

    def __init__(self, *, language_name: str, case_name: str) -> None:
        """Create an ``UnsupportedIdentifierCaseError``."""
        super().__init__(
            f"{language_name} does not support identifier case {case_name!r}"
        )
        self.language_name = language_name
        self.case_name = case_name


class DottedCallTargetNotSupportedError(LiteralizerError):
    """Raised when ``literalize_call`` is given a dotted
    ``target_function``
    but the target language does not support dotted call expressions.

    To resolve, use a target name without dots, or target a language
    with dotted calls.
    """

    def __init__(self, *, language_name: str, target_function: str) -> None:
        """Create a ``DottedCallTargetNotSupportedError``."""
        super().__init__(
            f"{language_name} does not support dotted call targets: "
            f"{target_function!r}"
        )
        self.language_name = language_name
        self.target_function = target_function


class ZipValuesLengthMismatchError(LiteralizerError):
    """Raised when ``literalize_call`` is given a ``zip_source`` whose
    parsed top-level elements differ in number from the generated calls.

    To resolve, make ``zip_source`` hold one element per generated call.
    """

    def __init__(
        self,
        *,
        call_count: int,
        zip_count: int,
    ) -> None:
        """Create a ``ZipValuesLengthMismatchError``."""
        super().__init__(
            f"zip_source parsed to {zip_count} element(s) but "
            f"{call_count} call(s) were generated; the lengths must match"
        )
        self.call_count = call_count
        self.zip_count = zip_count


class ZipValuesWithoutCallTransformError(LiteralizerError):
    """Raised when ``literalize_call`` is given a ``zip_source`` but no
    ``call_transform`` to consume the paired values.

    The paired values are only reachable through
    :attr:`~literalizer.CallContext.zipped`, so supplying them without
    a transform would silently discard them.

    To resolve, supply a ``call_transform`` that reads
    :attr:`~literalizer.CallContext.zipped`, or drop ``zip_source``.
    """

    def __init__(self) -> None:
        """Create a ``ZipValuesWithoutCallTransformError``."""
        super().__init__(
            "zip_source was supplied without a call_transform; the "
            "paired values would be unused"
        )


class ZipSourceWithoutInputFormatError(LiteralizerError):
    """Raised when ``literalize_call`` is given a ``zip_source`` but no
    ``zip_input_format`` describing how to parse it.

    The companion source can only be parsed once its serialization
    format is known, so the two arguments must be supplied together.

    To resolve, pass ``zip_input_format`` alongside ``zip_source``.
    """

    def __init__(self) -> None:
        """Create a ``ZipSourceWithoutInputFormatError``."""
        super().__init__(
            "zip_source was supplied without a zip_input_format; the "
            "companion source cannot be parsed without its format"
        )


class ZipInputFormatWithoutSourceError(LiteralizerError):
    """Raised when ``literalize_call`` is given ``zip_input_format``
    without a companion ``zip_source``.

    To resolve, pass ``zip_source`` alongside ``zip_input_format``, or drop
    ``zip_input_format``.
    """

    def __init__(self) -> None:
        """Create a ``ZipInputFormatWithoutSourceError``."""
        super().__init__(
            "zip_input_format was supplied without a zip_source; there is "
            "no companion source to parse"
        )


class CommentSourceLengthMismatchError(LiteralizerError):
    """Raised when ``literalize_call`` is given a ``comment_source``
    whose entry count differs from the number of generated calls.

    Each comment is paired positionally with one call, so the two
    sequences must be the same length.

    To resolve, provide one comment per generated call.
    """

    def __init__(
        self,
        *,
        call_count: int,
        comment_count: int,
    ) -> None:
        """Create a ``CommentSourceLengthMismatchError``."""
        super().__init__(
            f"comment_source has {comment_count} entry(ies) but "
            f"{call_count} call(s) were generated; the lengths must match"
        )
        self.call_count = call_count
        self.comment_count = comment_count


class CommentSourceMultilineError(LiteralizerError):
    """Raised when a ``comment_source`` entry contains a newline.

    A trailing comment is emitted on the statement's last line; a
    newline would push the remainder onto a line with no comment
    leader and, in languages whose line comment runs to end of line,
    produce invalid source.  Comments must be single-line.

    To resolve, remove the newline, keeping each comment on one line.
    """

    def __init__(self, *, index: int) -> None:
        """Create a ``CommentSourceMultilineError``."""
        super().__init__(
            f"comment_source entry at index {index} contains a newline; "
            "trailing comments must be single-line"
        )
        self.index = index


class CommentSourceNulError(LiteralizerError):
    """Raised when a ``comment_source`` entry contains a null byte.

    Source-code tool chains commonly reject null bytes even inside comments.
    To resolve, remove or replace the null character.
    """

    def __init__(self, *, index: int) -> None:
        """Create a ``CommentSourceNulError``."""
        super().__init__(
            f"comment_source entry at index {index} contains a NUL byte; "
            "source comments cannot contain NUL"
        )
        self.index = index


class VariableNameNotSupportedError(LiteralizerError):
    """Raised when ``literalize`` is given a ``variable_form`` but the
    target language does not support variable-name wrapping.

    To resolve, omit ``variable_form`` for that language, or target one
    that supports it.
    """

    def __init__(self, *, language_name: str, variable_name: str) -> None:
        """Create a ``VariableNameNotSupportedError``."""
        super().__init__(
            f"{language_name} does not support variable names: "
            f"{variable_name!r}"
        )
        self.language_name = language_name
        self.variable_name = variable_name


class WrapInFileWithoutVariableNotSupportedError(LiteralizerError):
    """Raised when ``literalize`` is called with ``wrap_in_file=True``
    and ``variable_form=None`` for a target language that cannot
    represent a bare value at file-statement scope.

    Most strict-typed compiled languages (Rust, C, C++, Haskell, Swift,
    OCaml, Ada, D, Dart, C#, Elm, Mojo, Nim, Objective-C, Odin, SML, V,
    Zig, etc.) require every top-level item to be a declaration; a bare
    expression at file scope is a syntax error.  Such languages opt out
    of the shape by setting
    :attr:`~literalizer._language.Language.supports_no_variable_wrap_in_file`
    to ``False``, and ``literalize`` rejects the combination at the
    boundary instead of silently emitting invalid code.

    To resolve, supply a ``variable_form`` so the value becomes a
    top-level declaration.
    """

    def __init__(self, *, language_name: str) -> None:
        """Create a ``WrapInFileWithoutVariableNotSupportedError``."""
        super().__init__(
            f"{language_name} cannot wrap a bare value (without a "
            f"variable_form) at file scope"
        )
        self.language_name = language_name


class UnsupportedCallShapeError(LiteralizerError):
    """Raised when ``literalize_call`` is given a call shape the target
    language cannot represent.

    Distinct from :class:`CallArgNotSupportedError` (which concerns
    individual argument values): this covers structural properties of
    the call itself, e.g. zero-parameter calls in languages whose
    syntax requires at least one operand.

    To resolve, adjust the call shape, or target a language that
    supports it.
    """

    def __init__(self, *, language_name: str, reason: str) -> None:
        """Create an ``UnsupportedCallShapeError``."""
        super().__init__(
            f"{language_name} cannot represent this call shape: {reason}"
        )
        self.language_name = language_name
        self.reason = reason


class ExcessiveNestingError(LiteralizerError):
    """Raised when a target language's safe collection nesting limit is
    exceeded.
    """

    def __init__(
        self, *, language_name: str, maximum_depth: int, actual_depth: int
    ) -> None:
        """Create an ``ExcessiveNestingError``."""
        super().__init__(
            f"{language_name} supports collection nesting only through depth "
            f"{maximum_depth}; received depth {actual_depth}"
        )
        self.language_name = language_name
        self.maximum_depth = maximum_depth
        self.actual_depth = actual_depth


class WrapCombinedInFileNotSupportedError(LiteralizerError):
    """Raised when a language does not support ``wrap_combined_in_file``.

    Languages that raise this error do not support
    :class:`~literalizer.BothVariableForms`; ``literalize()`` rejects
    that form before reaching ``wrap_combined_in_file``, but each
    language implementation still raises this typed exception as a
    safety net.

    To resolve, use a single variable form, or target a language that
    supports the combined form.
    """


class ConflictingVariableModifiersError(LiteralizerError):
    """Raised when declaration modifiers cannot be combined.

    Some modifier groups are mutually exclusive: a Java or C# field has
    exactly one visibility, and a C# field is ``const`` or ``readonly``
    but not both. Emitting all of them produces source that does not
    compile, so the combination is rejected instead.

    To resolve, pass at most one modifier from the reported group.
    """

    def __init__(
        self,
        *,
        language_name: str,
        group_name: str,
        keywords: tuple[str, ...],
    ) -> None:
        """Create a ``ConflictingVariableModifiersError``."""
        joined = ", ".join(keywords)
        super().__init__(
            f"{language_name} accepts at most one {group_name} modifier; "
            f"received {joined}"
        )
        self.language_name = language_name
        self.group_name = group_name
        self.keywords = keywords
