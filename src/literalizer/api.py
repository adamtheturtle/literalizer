"""Public entry points for converting data to language literals.

The rendering machinery lives in :mod:`literalizer._literalize`; this
module holds the two supported entry points, re-exported from the
package root as :func:`literalizer.literalize` and
:func:`literalizer.literalize_call`.
"""

import dataclasses
from collections.abc import Callable, Mapping, Sequence

from beartype import beartype

from literalizer._language import (
    CollectionLayout,
    IdentifierCase,
    Language,
    LanguageCls,
    is_reserved_identifier,
)
from literalizer._literalize import (
    BothVariableForms,
    CallContext,
    ExistingVariable,
    LiteralizeResult,
    NewVariable,
    VariableForm,
    disabled_ref_key,
    literalize_apply_form,
    literalize_both_forms,
    literalize_bound_refs,
    literalize_call_parsed,
    literalize_pre_form,
    materialize_value_input,
)
from literalizer._parsing import (
    InputFormat,
    parse_input,
)
from literalizer._types import Value, ValueInput
from literalizer.exceptions import (
    BoundRefOutputCollisionError,
    DelimiterlessVariableError,
    DelimiterlessWrappedFileError,
    ImmutableVariableModifierError,
    InvalidPreIndentLevelError,
    InvalidSequenceArgumentError,
    InvalidVariableModifierError,
    ModuleNameVariableCollisionError,
    PreIndentedWrappedFileError,
    UnsupportedCallShapeError,
    UnsupportedIdentifierCaseError,
    VariableNameNotSupportedError,
    WrapInFileWithoutVariableNotSupportedError,
)


def _fresh_language(language: Language) -> Language:
    """Return a spec with fresh per-render cached formatter state."""
    return dataclasses.replace(language)


def _validate_bound_ref_output_name(
    *,
    language: Language,
    variable_form: VariableForm | None,
    bound_ref_names: Mapping[str, object],
    ref_case: IdentifierCase | None,
    wrap_in_file: bool,
) -> None:
    """Reject a bound ref that would re-declare the output binding.

    The comparison is on the identifiers the two sides are emitted
    with, not on the names the caller spelled: a bound ref is declared
    under its ``ref_case`` conversion, so names that differ before the
    conversion can converge after it (issue #3906).

    Only a declaration can collide with another, and ``bound_refs``
    emits declarations under ``wrap_in_file`` alone; without it the
    refs stay free identifiers, exactly as ``ref_values`` leaves them,
    and the documented degrade allows the same name (issue #4463).
    """
    if not wrap_in_file:
        return
    if not isinstance(variable_form, NewVariable | BothVariableForms):
        return
    declared = {
        ref_case.convert(name=name) if ref_case is not None else name
        for name in bound_ref_names
    }
    if is_reserved_identifier(
        case_sensitive=language.reserved_variable_identifiers_case_sensitive,
        name=variable_form.name,
        reserved_identifiers=frozenset(declared),
    ):
        raise BoundRefOutputCollisionError(name=variable_form.name)


def _validate_variable_modifiers(
    *,
    language: Language,
    variable_form: VariableForm | None,
) -> None:
    """Reject declaration modifiers owned by another language."""
    if not isinstance(variable_form, NewVariable | BothVariableForms):
        return
    for modifier in variable_form.modifiers:
        if not isinstance(modifier, language.modifiers):
            raise InvalidVariableModifierError(
                language_name=type(language).__name__,
                modifier=modifier,
            )


@beartype
def _validate_module_name_variable_collision(
    *,
    language: Language,
    variable_form: VariableForm | None,
    wrap_in_file: bool,
) -> None:
    """Reject a wrapper named after the variable it would declare.

    Only a language whose wrapper shares a scope with the value it
    binds is affected; nearly every other wrapper opens one of its own
    (issue #4530).
    """
    language_cls = type(language)
    if not isinstance(language_cls, LanguageCls):  # pragma: no cover
        msg = "Module-name validation requires a LanguageCls language"
        raise TypeError(msg)
    # ``BothVariableForms`` is exempt: its wrapper puts the binding in
    # a subroutine named after the module rather than in the module's
    # own scope, so the two names coexist (issue #4530).
    if (
        not wrap_in_file
        or not isinstance(variable_form, NewVariable | ExistingVariable)
        or not language_cls.supports_module_name
        or not language_cls.module_name_shares_variable_scope
    ):
        return
    module_name = vars(language)["module_name"]
    if is_reserved_identifier(
        case_sensitive=language.reserved_variable_identifiers_case_sensitive,
        name=variable_form.name,
        reserved_identifiers=frozenset({module_name}),
    ):
        raise ModuleNameVariableCollisionError(
            language_name=language_cls.__name__,
            name=module_name,
        )


@beartype
def _validate_immutable_both_forms(
    *,
    language: Language,
    variable_form: VariableForm | None,
) -> None:
    """Reject a once-bound declaration the assignment would rebind.

    ``BothVariableForms`` writes a declaration and then an assignment to
    the same name, which a modifier such as ``const`` or ``final``
    forbids (issue #4565).
    """
    if not isinstance(variable_form, BothVariableForms):
        return
    language_cls = type(language)
    if not isinstance(language_cls, LanguageCls):  # pragma: no cover
        msg = "Modifier validation requires a LanguageCls language"
        raise TypeError(msg)
    immutable = sorted(
        variable_form.modifiers & language_cls.immutable_variable_modifiers,
        key=lambda modifier: modifier.name,
    )
    for modifier in immutable:
        raise ImmutableVariableModifierError(
            language_name=language_cls.__name__,
            modifier=modifier,
        )


@beartype
def _validate_pre_indented_wrap(
    *,
    language: Language,
    pre_indent_level: int,
    wrap_in_file: bool,
) -> None:
    """Reject an indented whole file the target could not parse.

    The indent applies to the value declaration and not to the wrapper
    around it, so the file carries two margins.  Only a language that
    reads indentation as structure minds (issue #4535).
    """
    language_cls = type(language)
    if not isinstance(language_cls, LanguageCls):  # pragma: no cover
        msg = "Pre-indent validation requires a LanguageCls language"
        raise TypeError(msg)
    if (
        pre_indent_level
        and wrap_in_file
        and not language_cls.wrap_in_file_tolerates_pre_indent
    ):
        raise PreIndentedWrappedFileError(
            language_name=language_cls.__name__,
        )


@beartype
def _validate_render_arguments(
    *,
    language: Language,
    pre_indent_level: int,
    include_delimiters: bool,
    variable_form: VariableForm | None,
    wrap_in_file: bool,
    ref_case: IdentifierCase | None,
) -> None:
    """Reject rendering arguments that cannot be combined."""
    _validate_variable_modifiers(
        language=language,
        variable_form=variable_form,
    )
    if pre_indent_level < 0:
        raise InvalidPreIndentLevelError
    if not include_delimiters and variable_form is not None:
        raise DelimiterlessVariableError
    # A delimiter-less fragment is the inside of a collection, which no
    # language can stand up as a whole file (issue #4529).
    if not include_delimiters and wrap_in_file:
        raise DelimiterlessWrappedFileError
    _validate_immutable_both_forms(
        language=language,
        variable_form=variable_form,
    )
    _validate_pre_indented_wrap(
        language=language,
        pre_indent_level=pre_indent_level,
        wrap_in_file=wrap_in_file,
    )
    if ref_case is not None and ref_case not in language.supported_ref_cases:
        raise UnsupportedIdentifierCaseError(
            language_name=type(language).__name__,
            case_name=ref_case.name,
        )
    _validate_module_name_variable_collision(
        language=language,
        variable_form=variable_form,
        wrap_in_file=wrap_in_file,
    )


@beartype
def literalize(
    *,
    source: str,
    input_format: InputFormat,
    language: Language,
    pre_indent_level: int = 0,
    include_delimiters: bool = True,
    variable_form: VariableForm | None = None,
    wrap_in_file: bool = False,
    ref_case: IdentifierCase | None = None,
    ref_values: Mapping[str, ValueInput] | None = None,
    bound_refs: Mapping[str, ValueInput] | None = None,
    ref_key: str | None = None,
    record_null_substitutions: Mapping[str, ValueInput] | None = None,
    collection_layout: CollectionLayout = CollectionLayout.COMPACT,
) -> LiteralizeResult:
    r"""Convert a JSON, JSON5, YAML, or TOML string to a native
    language literal.

    YAML and TOML comments are preserved in the output using the target
    language's comment syntax. JSON5 comments are not preserved; JSON5 input
    is parsed as plain data.

    Args:
        source: The input string to convert.
        input_format: The serialization format of *source*.
        language: A :class:`Language` instance describing how to format
            literals.  Use one of the built-in constants
            (e.g. :data:`PYTHON`, :data:`GO`) or provide your own.
            Languages whose ``wrap_in_file`` introduces a named scope
            (the wrapping class in Java, the ``program`` in Fortran,
            the ``-module`` in Erlang) carry that name as a constructor
            argument (``Java(module_name="Foo")``); languages whose
            wrappers do not introduce a named scope take no such
            argument.
        pre_indent_level: Number of ``indent`` steps to prepend to
            every output line.  For example, ``2`` with a 4-space
            indent produces an 8-space margin.  Defaults to ``0``.
        include_delimiters: If True, include the collection delimiters
            (``[`` … ``]`` for arrays, ``{`` … ``}`` for dicts).
        variable_form: Controls how the output is wrapped in a variable.
            Pass :class:`NewVariable` to use
            ``format_variable_declaration`` (e.g. ``const x =`` in
            JavaScript), :class:`ExistingVariable` to use
            ``format_variable_assignment`` (e.g. ``x =``),
            or :class:`BothVariableForms` to produce both a declaration
            and an assignment combined in one output (requires
            *wrap_in_file*).  ``None`` (default) means no variable
            wrapping.
        wrap_in_file: If ``True``, assemble :attr:`code` as a
            complete, valid source file using the language's
            ``wrap_in_file`` method and prepend :attr:`preamble`.
            Some back ends require companion support files; in particular,
            Ada output imports the ``A_Stub`` package shipped in
            ``scripts/a_stub.ads`` and ``scripts/a_stub.adb``.
            When set, :attr:`preamble` and :attr:`body_preamble`
            on the result are empty tuples (their content has been
            folded into :attr:`code`).
        ref_case: Optional :class:`IdentifierCase` controlling how ref
            identifiers are cased in the rendered output.
            ``{ref_key: "name"}`` markers anywhere in the data are
            rendered as bare identifiers using the
            language's
            :attr:`~literalizer._language.Language.format_call_ref_identifier`
            hook.  When ``None`` (default), ref names are emitted
            verbatim.  When set, the identifier name is converted to
            *ref_case* first.
        ref_values: Optional mapping from ref identifier to the value
            declared elsewhere for that ref.  Some languages render a
            ref differently depending on the type behind it (V emits
            ``name`` for primitive scalars but ``name.clone()`` for
            arrays and maps); supplying *ref_values* lets those
            languages pick the right form.  When omitted, a ref's type
            is unknown and languages fall back to their type-agnostic
            default.  Keys should match the identifiers used in *source*
            before any *ref_case* conversion.
        bound_refs: Optional mapping from ref identifier to the value
            that ref should be bound to.  Unlike *ref_values* (which
            only feeds type knowledge to the ref site, leaving the ref
            as a free external identifier), each name in *bound_refs*
            additionally has a binding emitted for it, in *bound_refs*
            iteration order, so a single ``literalize`` call with
            ``wrap_in_file=True`` produces a complete, valid file with
            per-language declaration sequencing (Nix nested ``let``,
            Fortran two-phase declarations, and so on).  Supply
            *bound_refs* ordered by each ref's first use in *source*
            (and limited to refs that appear there) so every binding
            precedes its first use and no unused binding is emitted.
            Binding
            emission only happens when *wrap_in_file* is ``True`` and
            *variable_form* is a :class:`NewVariable` or
            :class:`ExistingVariable` (a binding the refs can precede);
            otherwise *bound_refs* degrades to type information only,
            exactly like *ref_values*, and the refs stay free
            identifiers.  Entries also act as *ref_values* for their
            names, so a name need not be repeated in both mappings.
            Keys should match the identifiers used in *source* before
            any *ref_case* conversion.  Defaults to ``None`` (no
            bindings emitted; behavior is byte-identical to omitting
            this argument).
        ref_key: Optional dict key used to identify variable-reference
            markers in the input data.  A single-key dict whose key
            equals *ref_key* and whose value is a string is treated as a
            ref marker.  Detection is disabled by default so JSON Schema and
            OpenAPI ``$ref`` objects remain data; pass ``"$ref"`` explicitly
            to enable the historical marker syntax.
        record_null_substitutions: Optional replacements for null-valued
            record fields, keyed by original field name. Replacements are
            applied before validation and type inference, so their normal
            target-language literals and inferred types are used. A field
            remains unchanged when it is non-null or has no mapping.
        collection_layout: Controls layout for collections nested
            inside other collections.  ``CollectionLayout.COMPACT``
            preserves the existing one-line nested rendering, while
            ``CollectionLayout.MULTILINE`` expands non-empty nested
            collections with one element per line.

    Raises:
        JSONParseError: If *input_format* is ``JSON`` and *source* is
            not valid JSON.
        JSON5ParseError: If *input_format* is ``JSON5`` and *source*
            is not valid JSON5.
        YAMLParseError: If *input_format* is ``YAML`` and *source* is
            not valid YAML.
        TOMLParseError: If *input_format* is ``TOML`` and *source* is
            not valid TOML.
        HeterogeneousCollectionError: If the data contains collections
            whose shape cannot be represented in the target language
            (e.g. heterogeneous scalar types in a language that requires
            homogeneous collections).
        ValueError: If *variable_form* is :class:`BothVariableForms`
            and *wrap_in_file* is ``False``, or if the language's
            ``declaration_style`` does not support redefinition.
        UnsupportedIdentifierCaseError: If *ref_case* is not in
            :attr:`~literalizer._language.Language.supported_ref_cases`
            for the target language.
        VariableNameNotSupportedError: If *variable_form* is supplied
            but the target language sets
            :attr:`~literalizer._language.Language.supports_variable_names`
            to ``False``.
        WrapInFileWithoutVariableNotSupportedError: If *wrap_in_file*
            is ``True`` and *variable_form* is ``None`` but the target
            language sets
            :attr:`~literalizer._language.Language.supports_no_variable_wrap_in_file`
            to ``False`` (i.e. it cannot represent a bare value at
            file-statement scope).
    """
    language = _fresh_language(language=language)
    effective_ref_key = disabled_ref_key() if ref_key is None else ref_key
    _validate_render_arguments(
        language=language,
        pre_indent_level=pre_indent_level,
        include_delimiters=include_delimiters,
        variable_form=variable_form,
        wrap_in_file=wrap_in_file,
        ref_case=ref_case,
    )
    explicit_ref_values: dict[str, Value] = (
        {
            name: materialize_value_input(
                value=value,
                argument_name="ref_values",
            )
            for name, value in ref_values.items()
        }
        if ref_values is not None
        else {}
    )
    materialized_bound_refs: dict[str, Value] = (
        {
            name: materialize_value_input(
                value=value,
                argument_name="bound_refs",
            )
            for name, value in bound_refs.items()
        }
        if bound_refs is not None
        else {}
    )
    materialized_record_null_substitutions: Mapping[str, Value] | None = (
        {
            name: materialize_value_input(
                value=value,
                argument_name="record_null_substitutions",
            )
            for name, value in record_null_substitutions.items()
        }
        if record_null_substitutions is not None
        else None
    )
    # ``bound_refs`` entries double as ``ref_values`` so a name need not
    # be repeated in both mappings; an explicit ``ref_values`` entry for
    # the same name wins (it is the caller's stated type intent).
    combined_ref_values = {**materialized_bound_refs, **explicit_ref_values}
    materialized_ref_values: Mapping[str, Value] | None = (
        combined_ref_values or None
    )
    _validate_bound_ref_output_name(
        language=language,
        variable_form=variable_form,
        bound_ref_names=materialized_bound_refs,
        ref_case=ref_case,
        wrap_in_file=wrap_in_file,
    )
    if variable_form is not None and not language.supports_variable_names:
        raise VariableNameNotSupportedError(
            language_name=type(language).__name__,
            variable_name=variable_form.name,
        )
    if (
        wrap_in_file
        and variable_form is None
        and not language.supports_no_variable_wrap_in_file
    ):
        raise WrapInFileWithoutVariableNotSupportedError(
            language_name=type(language).__name__,
        )
    if isinstance(variable_form, BothVariableForms):
        if not wrap_in_file:
            msg = "BothVariableForms requires wrap_in_file=True"
            raise ValueError(msg)
        if not language.declaration_style.value.supports_redefinition:
            msg = (
                "BothVariableForms requires a declaration_style that "
                "supports redefinition; "
                f"{language.declaration_style.name!r} does not."
            )
            raise ValueError(msg)
        return literalize_both_forms(
            source=source,
            input_format=input_format,
            language=language,
            pre_indent_level=pre_indent_level,
            include_delimiters=include_delimiters,
            variable_form=variable_form,
            ref_case=ref_case,
            ref_values=materialized_ref_values,
            explicit_ref_values=explicit_ref_values or None,
            bound_refs=materialized_bound_refs,
            ref_key=effective_ref_key,
            record_null_substitutions=materialized_record_null_substitutions,
            collection_layout=collection_layout,
        )

    if (
        materialized_bound_refs
        and wrap_in_file
        and isinstance(variable_form, NewVariable | ExistingVariable)
    ):
        return literalize_bound_refs(
            source=source,
            input_format=input_format,
            language=language,
            pre_indent_level=pre_indent_level,
            include_delimiters=include_delimiters,
            variable_form=variable_form,
            ref_case=ref_case,
            explicit_ref_values=explicit_ref_values or None,
            bound_refs=materialized_bound_refs,
            ref_key=effective_ref_key,
            record_null_substitutions=materialized_record_null_substitutions,
            collection_layout=collection_layout,
        )

    pre_form = literalize_pre_form(
        source=source,
        input_format=input_format,
        language=language,
        pre_indent_level=pre_indent_level,
        include_delimiters=include_delimiters,
        ref_case=ref_case,
        ref_values=materialized_ref_values,
        ref_key=effective_ref_key,
        record_null_substitutions=materialized_record_null_substitutions,
        collection_layout=collection_layout,
    )
    return literalize_apply_form(
        pre_form=pre_form,
        language=language,
        variable_form=variable_form,
        wrap_in_file=wrap_in_file,
    )


@beartype
def literalize_call(
    *,
    source: str,
    input_format: InputFormat,
    language: Language,
    target_function: str,
    parameter_names: Sequence[str],
    call_transform: Callable[[CallContext], str] | None = None,
    zip_source: str | None = None,
    zip_input_format: InputFormat | None = None,
    comment_source: Sequence[str] | None = None,
    per_element: bool = True,
    wrap_in_file: bool = False,
    ref_case: IdentifierCase | None = None,
    consumable_refs: frozenset[str] = frozenset(),
    ref_values: Mapping[str, ValueInput] | None = None,
    bound_refs: Mapping[str, ValueInput] | None = None,
    ref_key: str | None = None,
    collection_layout: CollectionLayout = CollectionLayout.COMPACT,
    variable_form: VariableForm | None = None,
) -> LiteralizeResult:
    r"""Convert data to function call expressions in the target language.

    Each top-level list element (when *per_element* is ``True``) becomes
    a separate function call with arguments formatted according to the
    language's :attr:`~Language.call_style_config`.

    Args:
        source: The input string to convert.
        input_format: The serialization format of *source*.
        language: A :class:`Language` instance describing how to format
            literals.
        target_function: The function expression to call
            (e.g. ``"throttler.should_send_notification"``).
        parameter_names: Parameter names, positionally mapped to each
            element in each row.  For :class:`PositionalCallStyle`
            languages these are unused in the output but still
            determine how many values to expect per row.
        call_transform: Optional callable transforming each generated
            call.  Invoked once per call as ``call_transform(context)``
            with a :class:`CallContext` and returns the transformed
            string (e.g. ``lambda ctx: f"print({ctx.call})"``).  The
            context also exposes the call's zero-based ``index``, its
            input ``row``, and the paired ``zipped`` literal, so a
            transform can render data from a parallel sequence beside
            each call.  Only supported for languages whose call form is
            an expression that can be wrapped (positional, keyword, or
            object call style); prefix/postfix/command-style languages
            reject it with
            :class:`~literalizer.exceptions.UnsupportedCallShapeError`.
        zip_source: Optional companion source whose parsed top-level
            elements pair positionally with the generated calls.  It is
            parsed with the *same* parser as *source* (so YAML
            ``!!omap``, datetime/bytes coercion, JSON5, TOML, ...
            behave identically by construction), each paired value is
            rendered to a language-native literal (via the same
            machinery as :func:`literalize`) and exposed on
            :attr:`CallContext.zipped` for the matching call, enabling
            patterns like printing an expected value beside each call's
            actual return value.  When *per_element* is ``True`` it
            must parse to a list whose top-level elements pair
            element-by-element with the calls (a non-list raises
            :class:`~literalizer.exceptions.PerElementNotListError`);
            otherwise the whole parsed value pairs with the single
            call.  A length mismatch raises
            :class:`~literalizer.exceptions.ZipValuesLengthMismatchError`.
            Requires *zip_input_format* (supplying *zip_source* without
            it raises
            :class:`~literalizer.exceptions.ZipSourceWithoutInputFormatError`)
            and *call_transform* (the values are only reachable through
            it; supplying *zip_source* without one raises
            :class:`~literalizer.exceptions.ZipValuesWithoutCallTransformError`).
        zip_input_format: The serialization format of *zip_source*.
            Required whenever *zip_source* is supplied. Supplying it without
            *zip_source* raises
            :class:`~literalizer.exceptions.ZipInputFormatWithoutSourceError`.
        comment_source: Optional sequence of trailing source-code
            comments, one per generated call, paired positionally.
            Each non-empty entry is emitted as a line comment **after**
            the statement terminator on the call's last line, using the
            language's :attr:`~Language.comment_config` leader (``#``,
            ``//``, ``--``, ...); languages with no line comment fall
            back to that language's block-comment form (``/* ... */``),
            which is valid on a single line.  Because the comment is
            applied to the fully terminated statement, a line-comment
            leader never swallows the terminator (a problem a
            *call_transform* cannot avoid, since it only sees the
            pre-terminator call expression).  An empty entry emits no
            comment.  Unlike *zip_source* this is a plain sequence (not
            a parsed source) and needs neither a *call_transform* nor
            an input format.  The entry count must equal the number of
            generated calls -- one per top-level element when
            *per_element* is ``True``, otherwise one for the single
            call -- or
            :class:`~literalizer.exceptions.CommentSourceLengthMismatchError`
            is raised; an entry containing a newline raises
            :class:`~literalizer.exceptions.CommentSourceMultilineError`,
            and an entry containing a null byte raises
            :class:`~literalizer.exceptions.CommentSourceNulError`.
            A trailing comment is only safe where each generated call
            is a self-contained line; languages that assemble the call
            sequence into a single clause/list/expression (so a
            separator, terminator or closer follows the call on the
            same line, which a line comment would swallow) reject a
            non-empty *comment_source* with
            :class:`~literalizer.exceptions.UnsupportedCallShapeError`.
            The supported set is exactly the languages whose
            :attr:`~literalizer.Language.supports_standalone_comments_in_wrapped_calls`
            is ``True``.
        per_element: If ``True`` (default), each top-level list element
            becomes a separate call (an element that is itself an empty
            list yields a zero-argument call).  If ``False``, the whole
            literalized value is passed as a single argument.  A
            *variable_form* binding requires exactly one call, so it is
            valid with ``per_element=False`` (always one call) or with
            ``per_element=True`` over a single-element source; the
            zero-argument constructor ``p2 = Playlist()`` is produced by
            the latter with a ``[[]]`` source.
        wrap_in_file: If ``True``, assemble :attr:`code` as a
            complete source file using the language's
            ``wrap_in_file`` method and prepend :attr:`preamble`.  A
            no-op stub for *target_function* is also injected so the
            generated file does not reference an undefined name; when
            a *call_transform* is supplied the wrapper name it
            introduces is not stubbed — callers that transform calls
            are responsible for providing that definition themselves.
            Some back ends require companion support files; Ada imports the
            ``A_Stub`` package shipped in ``scripts/a_stub.ads`` and
            ``scripts/a_stub.adb``.
            When set, :attr:`preamble` and :attr:`body_preamble`
            on the result are empty tuples (their content has been
            folded into :attr:`code`).
        ref_case: Optional :class:`IdentifierCase` controlling how ref
            identifiers are cased in the rendered output.  When
            ``None`` (default) ref names are emitted verbatim.  When
            set, each ref identifier is normalized to ``snake_case``
            and then converted to the requested case via ``pyhumps``,
            so the same source can drive idiomatic identifiers across
            multiple languages.  When *language*'s ``supported_ref_cases``
            does not expose the requested case,
            :class:`~literalizer.exceptions.UnsupportedIdentifierCaseError`
            is raised.
        consumable_refs: Names of ref identifiers this call owns and
            may move from.  Refs in this set may be rendered with a
            consuming form (e.g. C++ ``std::move``) when they appear in
            exactly one call argument; refs used by more than one call
            -- or omitted from this set -- are emitted as the bare
            identifier so subsequent uses of the variable remain valid.
            Names should match the identifiers used in *source* before
            any *ref_case* conversion.  Defaults to an empty set (no
            refs are consumed).
        ref_values: Optional mapping from ref identifier to the source
            value declared elsewhere.  When supplied, values for refs
            used in *source* are included in data-driven preamble
            inference, so languages with generated body types (for
            example Haskell's ``data Val = ...``) declare constructors
            for types reachable only through refs.  Missing ref names
            keep the historical behavior: their markers are omitted
            from preamble inference.  Keys should match the identifiers
            used in *source* before any *ref_case* conversion.
        bound_refs: Optional mapping from ref identifier to the source
            value that ref should be *declared* with.  The recommended
            way to render a complete, self-contained file that declares
            each ref and then calls the target with it: ``literalize``
            exposes the same argument for the declaration-only case, and
            this is its call-side counterpart.  Each entry is emitted as
            a :class:`NewVariable` declaration (cased via *ref_case*) in
            *bound_refs* iteration order ahead of the calls, the value
            is folded into preamble inference exactly like *ref_values*
            (so a name need not be repeated in both mappings; an
            explicit *ref_values* entry for the same name wins), and the
            declarations, calls, and a no-op stub for *target_function*
            are wrapped into one file via
            :meth:`~literalizer.Language.wrap_calls_with_declarations`
            with a single reconciled preamble.  Declaration emission
            only happens when *wrap_in_file* is ``True``; otherwise
            *bound_refs* degrades to type information only, exactly like
            *ref_values*, and the refs stay free identifiers.  Every
            name should appear as a ``$ref`` marker in *source* (a ref
            that is declared but never referenced is folded into
            neither the call nor its preamble inference and so may
            leave the declaration's data-dependent preamble entries
            uncovered, besides being an unused binding); this mirrors
            ``literalize``'s *bound_refs* contract.  Where declarations
            are emitted, *variable_form* (which binds the call *result*)
            cannot be combined with them and the pair raises
            :class:`~literalizer.exceptions.UnsupportedCallShapeError`,
            because the declaration-composition path cannot apply a
            language's call-result binding file scaffold.  Without
            *wrap_in_file* nothing is composed, so the two coexist and
            *bound_refs* contributes only the type information described
            above.  Keys
            should match the identifiers used in *source* before any
            *ref_case* conversion.  Defaults to ``None`` (no bindings
            emitted; behavior is byte-identical to omitting this
            argument).
        ref_key: Optional dict key used to identify variable-reference
            markers in the input data.  A single-key dict whose key
            equals *ref_key* and whose value is a string is treated as
            a ref marker.  Detection is disabled by default; pass ``"$ref"``
            explicitly to enable ref markers.
        collection_layout: Controls layout for collections nested
            inside call arguments.  ``CollectionLayout.COMPACT``
            preserves the existing one-line nested rendering, while
            ``CollectionLayout.MULTILINE`` expands non-empty nested
            collections with one element per line.
        variable_form: When supplied, wrap the call expression in a
            variable binding using the language's
            ``format_variable_declaration`` /
            ``format_variable_assignment`` hook (the same machinery
            used by :func:`literalize`).  Pass :class:`NewVariable` for
            an idiomatic declaration (``let p2 = Playlist::new();``,
            ``const p2 = new Playlist();``, ``p2 = Playlist()``) or
            :class:`ExistingVariable` for an assignment to an existing
            name.  :class:`BothVariableForms` is rejected with
            :class:`~literalizer.exceptions.UnsupportedCallShapeError`
            because emitting both a declaration and an assignment
            would invoke the target function twice.  Mutability and
            inference are controlled by the per-language
            ``declaration_style`` and ``Modifiers`` enums on the
            supplied ``Language`` instance, not by extra arguments
            here.  A single name can bind only one call result, so the
            input must produce exactly one call: ``per_element=False``
            always does, and ``per_element=True`` does when the source
            has exactly one top-level element (a single-element ``[[]]``
            source is how the zero-argument constructor
            ``p2 = Playlist()`` is reached).  Zero calls (an empty
            ``per_element`` source) or more than one call are rejected
            with
            :class:`~literalizer.exceptions.UnsupportedCallShapeError`,
            as are languages whose call form is not an expression
            (``call_returns_expression=False``).

    .. note::

        When composing the output of this function with
        :func:`literalize` — for example, declaring a variable with
        :func:`literalize` and then referencing it via a ref marker in
        the call — the two halves each
        compute :attr:`~LiteralizeResult.preamble` and
        :attr:`~LiteralizeResult.body_preamble` independently from the
        data they see.  Concatenating the results into a single file
        can produce duplicate import lines or duplicate type
        declarations, which strict compilers (Haskell, D, …) reject
        and a linter (``ruff``, ``pylint``, …) flags.  Pass the ref
        values through *bound_refs* (with ``wrap_in_file=True``) instead
        and this function renders the declarations and the calls into
        one coherent file with a single reconciled preamble.  The
        "Composing declarations and calls" section of
        :doc:`/function-call-use-case` shows a worked example.
    """
    language = _fresh_language(language=language)
    if isinstance(parameter_names, str):
        raise InvalidSequenceArgumentError(argument_name="parameter_names")
    if isinstance(comment_source, str):
        raise InvalidSequenceArgumentError(argument_name="comment_source")
    effective_ref_key = disabled_ref_key() if ref_key is None else ref_key
    _validate_variable_modifiers(
        language=language,
        variable_form=variable_form,
    )
    _validate_bound_ref_output_name(
        language=language,
        variable_form=variable_form,
        bound_ref_names=bound_refs or {},
        ref_case=ref_case,
        wrap_in_file=wrap_in_file,
    )
    _validate_module_name_variable_collision(
        language=language,
        variable_form=variable_form,
        wrap_in_file=wrap_in_file,
    )
    if isinstance(variable_form, BothVariableForms):
        # Rendering both halves would invoke the call twice -- a silent
        # side-effect bug for any non-pure target.  Reject up front so
        # the rest of the function can narrow ``variable_form`` to
        # ``NewVariable | ExistingVariable | None``.
        raise UnsupportedCallShapeError(
            language_name=type(language).__name__,
            reason=(
                "BothVariableForms is not supported for literalize_call: "
                "rendering both a declaration and an assignment would "
                "invoke the target function twice"
            ),
        )
    return literalize_call_parsed(
        parsed=parse_input(source=source, input_format=input_format),
        language=language,
        target_function=target_function,
        parameter_names=parameter_names,
        call_transform=call_transform,
        zip_source=zip_source,
        zip_input_format=zip_input_format,
        comment_source=comment_source,
        per_element=per_element,
        wrap_in_file=wrap_in_file,
        ref_case=ref_case,
        consumable_refs=consumable_refs,
        ref_values=ref_values,
        bound_refs=bound_refs,
        ref_key=effective_ref_key,
        collection_layout=collection_layout,
        variable_form=variable_form,
    )
