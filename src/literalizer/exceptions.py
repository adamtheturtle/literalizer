"""Exceptions raised by literalizer."""


class ParseError(Exception):
    """Raised when input cannot be parsed into a data structure."""


class JSONParseError(ParseError):
    """Raised when a JSON string cannot be parsed."""


class YAMLParseError(ParseError):
    """Raised when a YAML string cannot be parsed."""


class TOMLParseError(ParseError):
    """Raised when a TOML string cannot be parsed."""


class JSON5ParseError(ParseError):
    """Raised when a JSON5 string cannot be parsed."""


class InvalidDictKeyError(Exception):
    """Raised when a dict key cannot be represented in the target language.

    This includes empty-string keys and keys containing characters that
    the language's label syntax does not support (e.g. control characters
    in Dhall backtick-quoted labels).
    """


class UnrepresentableInputError(Exception):
    """Raised when an input value cannot be represented in the target
    language.

    Used as the centralized error for shape-level rejections at the
    formatting boundary, e.g. when a dict carries a non-string key for
    a language whose surface syntax only admits string-typed keys.
    """


class HeterogeneousCollectionError(Exception):
    """Base class for errors raised when data is incompatible with the
    target language's collection-shape constraints.
    """


class HeterogeneousScalarCollectionError(HeterogeneousCollectionError):
    """Raised when a collection contains scalars of multiple types and
    the target language requires homogeneous scalar collections.
    """


class HeterogeneousSiblingListsError(HeterogeneousCollectionError):
    """Raised when sibling sub-lists contain scalars that, combined,
    span multiple types and the target language requires homogeneous
    scalar collections.
    """


class MixedDictValuesError(HeterogeneousCollectionError):
    """Raised when a dict has values spanning multiple type families
    and the target language requires homogeneous dict values.
    """


class MixedDictKeysError(HeterogeneousCollectionError):
    """Raised when a dict has keys spanning multiple type families
    and the target language requires homogeneous dict keys.
    """


class MixedListValuesError(HeterogeneousCollectionError):
    """Raised when a list has elements spanning multiple type families
    and the target language requires homogeneous list elements.
    """


class MixedDictShapesError(HeterogeneousCollectionError):
    """Raised when a list contains dicts with different key sets and
    the target language requires uniform record shapes (e.g. Dhall).
    """


class HeterogeneousSetError(HeterogeneousCollectionError):
    """Raised when a set contains scalars of multiple types and the
    target language requires homogeneous set elements.
    """


class NullInCollectionError(Exception):
    """Raised when a collection contains null elements and the chosen
    format does not support them (e.g. Java's ``List.of()``).
    """


class PerElementNotListError(Exception):
    """Raised when ``per_element=True`` but the parsed data is not a
    list.
    """


class ParameterCountMismatchError(Exception):
    """Raised when the number of ``parameter_names`` does not match the
    number of argument values in a function-call row.
    """

    def __init__(self, *, expected: int, got: int) -> None:
        """Create a ``ParameterCountMismatchError``."""
        super().__init__(
            f"Expected {expected} parameters but got {got} values"
        )
        self.expected = expected
        self.got = got


class CallsNotSupportedByLanguageError(Exception):
    """Raised when the target language itself has no function call
    syntax (e.g. pure data/markup formats like YAML, TOML, JSON5, Norg).
    """

    def __init__(self, *, language_name: str) -> None:
        """Create a ``CallsNotSupportedByLanguageError``."""
        super().__init__(f"{language_name} has no function call syntax")
        self.language_name = language_name


class CallsNotSupportedByToolError(Exception):
    """Raised when literalizer has not yet implemented function call
    rendering for the target language, even though the language itself
    has function call syntax.
    """

    def __init__(self, *, language_name: str) -> None:
        """Create a ``CallsNotSupportedByToolError``."""
        super().__init__(
            f"literalizer does not support function call rendering "
            f"for {language_name}"
        )
        self.language_name = language_name


class CallArgNotSupportedError(Exception):
    """Raised when a call argument value cannot be expressed as a
    positional argument in the target language's call syntax.

    Used by languages whose call syntax does not accept compound
    literals as arguments — e.g. Bash, where ``cmd (1 2 3)`` parses
    as a nested ``(...)`` child-process invocation rather than an
    inline array value.
    """

    def __init__(self, *, language_name: str, reason: str) -> None:
        """Create a ``CallArgNotSupportedError``."""
        super().__init__(
            f"{language_name} cannot accept this value as a call "
            f"argument: {reason}"
        )
        self.language_name = language_name
        self.reason = reason


class IncompatibleFormatsError(Exception):
    """Raised when a combination of format options produces invalid code.

    For example, Rust ``CONST`` and ``STATIC`` declaration styles
    require constant-expression initializers, but the ``VEC`` sequence
    format produces ``vec![…]`` which is not a constant expression.
    """


class InvalidRecordNameError(Exception):
    """Raised when ``record_struct_name_prefix`` or a value in
    ``record_shape_names`` is not a valid PascalCase identifier, collides
    with a reserved keyword of the target language, collides with
    ``heterogeneous_value_enum_name``, or duplicates another mapped
    struct name.
    """


class UnrepresentableIntegerError(Exception):
    """Raised when an integer value exceeds the range the target
    language can represent natively.

    Used by languages whose fixed-width integer types cannot hold
    values outside the signed 64-bit range (e.g. Fortran default
    ``integer``, Cobol ``PIC S9(18)``, PureScript ``Int``) when no
    external arbitrary-precision integer library is assumed to be
    available.
    """


class UnrepresentableSpecialFloatError(Exception):
    """Raised when a non-finite float (``inf``, ``-inf``, or ``nan``)
    is passed to a target language whose runtime cannot produce IEEE
    754 special float values.

    Used by Gleam on the Erlang target, which has no expression that
    evaluates to a non-finite float.
    """


class UnsupportedIdentifierCaseError(Exception):
    """Raised when ``literalize`` or ``literalize_call`` is passed a
    ``ref_case`` that is not in the target language's
    ``supported_ref_cases`` -- i.e. one that would not produce a
    syntactically legal identifier in the target language.
    """

    def __init__(self, *, language_name: str, case_name: str) -> None:
        """Create an ``UnsupportedIdentifierCaseError``."""
        super().__init__(
            f"{language_name} does not support identifier case {case_name!r}"
        )
        self.language_name = language_name
        self.case_name = case_name


class DottedCallTargetNotSupportedError(Exception):
    """Raised when ``literalize_call`` is given a dotted
    ``target_function``
    but the target language does not support dotted call expressions.
    """

    def __init__(self, *, language_name: str, target_function: str) -> None:
        """Create a ``DottedCallTargetNotSupportedError``."""
        super().__init__(
            f"{language_name} does not support dotted call targets: "
            f"{target_function!r}"
        )
        self.language_name = language_name
        self.target_function = target_function


class DottedCallStubNotSupportedError(Exception):
    """Raised when ``literalize_call`` is given a ``call_transform``
    whose wrapper is dotted (e.g. ``tracer.emit``) but the target
    language does not support dotted call stub names.
    """

    def __init__(
        self,
        *,
        language_name: str,
        transform_stub_name: str,
    ) -> None:
        """Create a ``DottedCallStubNotSupportedError``."""
        super().__init__(
            f"{language_name} does not support dotted call stubs: "
            f"{transform_stub_name!r}"
        )
        self.language_name = language_name
        self.transform_stub_name = transform_stub_name


class FreeFunctionCallNotSupportedError(Exception):
    """Raised when ``literalize_call`` is given a ``call_transform``
    whose wrapper is a bare name with no dot (e.g. ``emit``) but the
    target language has no free function call syntax.
    """

    def __init__(
        self,
        *,
        language_name: str,
        transform_stub_name: str,
    ) -> None:
        """Create a ``FreeFunctionCallNotSupportedError``."""
        super().__init__(
            f"{language_name} has no free function call syntax for "
            f"call stub: {transform_stub_name!r}"
        )
        self.language_name = language_name
        self.transform_stub_name = transform_stub_name


class VariableNameNotSupportedError(Exception):
    """Raised when ``literalize`` is given a ``variable_form`` but the
    target language does not support variable-name wrapping.
    """

    def __init__(self, *, language_name: str, variable_name: str) -> None:
        """Create a ``VariableNameNotSupportedError``."""
        super().__init__(
            f"{language_name} does not support variable names: "
            f"{variable_name!r}"
        )
        self.language_name = language_name
        self.variable_name = variable_name


class WrapInFileWithoutVariableNotSupportedError(Exception):
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
    """

    def __init__(self, *, language_name: str) -> None:
        """Create a ``WrapInFileWithoutVariableNotSupportedError``."""
        super().__init__(
            f"{language_name} cannot wrap a bare value (without a "
            f"variable_form) at file scope"
        )
        self.language_name = language_name


class UnsupportedCallShapeError(Exception):
    """Raised when ``literalize_call`` is given a call shape the target
    language cannot represent.

    Distinct from :class:`CallArgNotSupportedError` (which concerns
    individual argument values): this covers structural properties of
    the call itself, e.g. zero-parameter calls in languages whose
    syntax requires at least one operand.
    """

    def __init__(self, *, language_name: str, reason: str) -> None:
        """Create an ``UnsupportedCallShapeError``."""
        super().__init__(
            f"{language_name} cannot represent this call shape: {reason}"
        )
        self.language_name = language_name
        self.reason = reason


class WrapCombinedInFileNotSupportedError(Exception):
    """Raised when a language does not support ``wrap_combined_in_file``.

    Languages that raise this error do not support
    :class:`~literalizer.BothVariableForms`; ``literalize()`` rejects
    that form before reaching ``wrap_combined_in_file``, but each
    language implementation still raises this typed exception as a
    safety net.
    """
