.. _common-errors:

Common errors and how to resolve them
=====================================

|project| raises a specific, typed exception whenever it cannot turn your
data into valid code for the target language, rather than emitting source
the compiler would reject.  Every exception lives in
:mod:`literalizer.exceptions`; this page maps each one to its cause and the
recommended fix.

The tables group the exceptions by the stage at which they are raised.  All
exceptions are importable from :mod:`literalizer.exceptions`, so a name such
as ``HeterogeneousScalarCollectionError`` below refers to
:class:`literalizer.exceptions.HeterogeneousScalarCollectionError`.

Parsing the input
------------------

Raised while reading ``source`` in the declared ``input_format``, before any
language-specific rendering.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Exception
     - Cause
     - How to resolve
   * - :class:`~literalizer.exceptions.ParseError`
     - Base class for every input-parsing failure.  Catch this to handle any
       malformed input uniformly.
     - Validate the source against its declared ``input_format``.
   * - :class:`~literalizer.exceptions.JSONParseError`
     - The ``source`` is not well-formed JSON.
     - Fix the JSON syntax, or pass the correct ``input_format`` if the data
       is really JSON5, YAML, or TOML.
   * - :class:`~literalizer.exceptions.JSON5ParseError`
     - The ``source`` is not well-formed JSON5.
     - Fix the JSON5 syntax, or choose the matching ``input_format``.
   * - :class:`~literalizer.exceptions.YAMLParseError`
     - The ``source`` is not well-formed YAML.
     - Fix the YAML syntax, or choose the matching ``input_format``.
   * - :class:`~literalizer.exceptions.TOMLParseError`
     - The ``source`` is not well-formed TOML.
     - Fix the TOML syntax, or choose the matching ``input_format``.

Mixed-type collections
----------------------

Raised when the data mixes types within one collection but the target
language requires that collection to be homogeneous.  Each of these
subclasses :class:`~literalizer.exceptions.HeterogeneousCollectionError`,
so you can catch the base class to skip any input a strict-typed language
cannot hold.  The usual fix is to pick a non-default ``heterogeneous_strategy``;
see :ref:`heterogeneous-strategies` for the full discussion and
:ref:`json-value-types` for the runtime JSON value alternative.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Exception
     - Cause
     - How to resolve
   * - :class:`~literalizer.exceptions.HeterogeneousCollectionError`
     - Base class for every mixed-type-collection rejection.
     - Catch this to skip any heterogeneous input the language cannot hold.
   * - :class:`~literalizer.exceptions.HeterogeneousScalarCollectionError`
     - A list mixes scalars of more than one type (e.g. ``[1, "two", 3.0]``)
       and the language needs a homogeneous element type.
     - Set ``heterogeneous_strategy`` to ``TAGGED_ENUM`` (or the language's
       equivalent) to wrap each scalar, or to ``TUPLE`` for a fixed-length
       array.
   * - :class:`~literalizer.exceptions.HeterogeneousSiblingListsError`
     - Sibling sub-lists hold scalars that, combined, span more than one type.
     - Use a ``TAGGED_ENUM`` strategy, or render the value through a
       ``json_type``.
   * - :class:`~literalizer.exceptions.MixedListValuesError`
     - A list mixes elements from more than one type family.
     - Use a richer ``heterogeneous_strategy`` or a ``json_type``.
   * - :class:`~literalizer.exceptions.MixedDictValuesError`
     - A dict mixes value types that a strict-map language cannot unify.
     - Use the ``RECORD`` strategy if the dict is conceptually a record, or a
       ``json_type`` for arbitrary mappings.
   * - :class:`~literalizer.exceptions.MixedDictKeysError`
     - A dict mixes key types that the language cannot unify.
     - Use a single key type, or render through a ``json_type``.
   * - :class:`~literalizer.exceptions.MixedDictShapesError`
     - A list holds dicts with different key sets, but the language needs a
       uniform record shape (e.g. Dhall).
     - Make every dict share the same keys, or use a ``json_type``.
   * - :class:`~literalizer.exceptions.HeterogeneousSetError`
     - A set mixes scalars of more than one type and the language needs
       homogeneous set elements.
     - Use one scalar type, or a richer ``heterogeneous_strategy``.
   * - :class:`~literalizer.exceptions.TupleArityNotRepresentableError`
     - Under the ``TUPLE`` strategy, a heterogeneous scalar array has a length
       the language has no native fixed-size tuple for (e.g. Kotlin has only
       ``Pair`` and ``Triple``).
     - Shorten the array to a length the language supports, choose a language
       without the tuple-length cap (Rust, Scala), or switch to a
       ``TAGGED_ENUM`` strategy.

Values the target language cannot represent
-------------------------------------------

Raised at the formatting boundary when an individual value has no faithful
representation in the target language.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Exception
     - Cause
     - How to resolve
   * - :class:`~literalizer.exceptions.UnrepresentableInputError`
     - The value's shape cannot be represented, e.g. a non-string dict key for
       a language whose surface syntax admits only string keys.
     - Adjust the data to a representable shape, or pick a language that
       supports it.
   * - :class:`~literalizer.exceptions.InvalidDictKeyError`
     - A dict key cannot be expressed as a label, e.g. an empty-string key or a
       key with control characters in Dhall backtick labels.
     - Remove or rename the offending key.
   * - :class:`~literalizer.exceptions.NullInCollectionError`
     - A collection contains ``null`` but the chosen collection format cannot
       hold nulls (e.g. Java's ``List.of()``).
     - Remove the nulls, or select a collection format that admits them.
   * - :class:`~literalizer.exceptions.UnrepresentableIntegerError`
     - An integer falls outside the range the language represents natively
       (e.g. values beyond signed 64-bit on Fortran, Cobol, or PureScript).
     - Keep integers within range, or target a language with wider or
       arbitrary-precision integers.
   * - :class:`~literalizer.exceptions.UnrepresentableEmptyDictError`
     - An empty dict is passed to a language whose runtime cannot tell an empty
       mapping from an empty sequence (Lua, PHP, R).
     - Drop the empty mapping, or target a language that distinguishes the two.
   * - :class:`~literalizer.exceptions.UnrepresentableSpecialFloatError`
     - A non-finite float (``inf``, ``-inf``, ``nan``) is passed to a language
       whose runtime has no such value (e.g. Gleam on the Erlang target).
     - Replace the non-finite floats with finite values, or pick another
       language.

Identifiers and variable wrapping
---------------------------------

Raised when ``variable_form`` or ``ref_case`` asks for output the target
language cannot produce.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Exception
     - Cause
     - How to resolve
   * - :class:`~literalizer.exceptions.UnsupportedIdentifierCaseError`
     - The supplied ``ref_case`` is not in the language's
       ``supported_ref_cases`` and would not form a legal identifier.
     - Choose a ``ref_case`` from the language's ``supported_ref_cases``.
   * - :class:`~literalizer.exceptions.VariableNameNotSupportedError`
     - A ``variable_form`` was given for a language that has no variable-name
       wrapping.
     - Omit ``variable_form`` for that language, or target one that supports it.
   * - :class:`~literalizer.exceptions.WrapInFileWithoutVariableNotSupportedError`
     - ``wrap_in_file=True`` with ``variable_form=None`` for a language that
       cannot place a bare value at file scope (most strict-typed compiled
       languages).
     - Supply a ``variable_form`` so the value becomes a top-level declaration.
   * - :class:`~literalizer.exceptions.InvalidRecordNameError`
     - ``record_struct_name_prefix`` or a ``record_shape_names`` value is not a
       valid name, collides with a keyword or another struct name, or clashes
       with ``heterogeneous_value_enum_name``.
     - Use distinct, valid PascalCase names that avoid reserved keywords.

Function calls
--------------

Raised by :func:`~literalizer.literalize_call` and its arguments
(``parameter_names``, ``call_transform``, ``zip_source``, ``comment_source``,
``target_function``).  See :doc:`function-call-use-case`.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Exception
     - Cause
     - How to resolve
   * - :class:`~literalizer.exceptions.CallsNotSupportedByLanguageError`
     - The target language has no function-call syntax at all (pure data and
       markup formats such as YAML, TOML, JSON5, Norg).
     - Use :func:`~literalizer.literalize` instead, or target a programming
       language.
   * - :class:`~literalizer.exceptions.CallsNotSupportedByToolError`
     - The language has call syntax, but |project| does not yet render calls
       for it.
     - Target a language whose call rendering is implemented.
   * - :class:`~literalizer.exceptions.PerElementNotListError`
     - ``per_element=True`` but the parsed data is not a list.
     - Pass a list, or drop ``per_element``.
   * - :class:`~literalizer.exceptions.ParameterCountMismatchError`
     - The number of ``parameter_names`` does not match the argument values in
       a call row.
     - Make ``parameter_names`` the same length as each row of values.
   * - :class:`~literalizer.exceptions.CallArgNotSupportedError`
     - A call argument value cannot be a positional argument, e.g. an inline
       compound literal in Bash.
     - Bind the value to a name first, or target a language that accepts the
       argument inline.
   * - :class:`~literalizer.exceptions.UnsupportedCallShapeError`
     - The call's structure cannot be represented, e.g. a zero-parameter call
       in a language that needs at least one operand.
     - Adjust the call shape, or target a language that supports it.
   * - :class:`~literalizer.exceptions.DottedCallTargetNotSupportedError`
     - A dotted ``target_function`` was given to a language without dotted call
       expressions.
     - Use a target name without dots, or target a language with dotted calls.
   * - :class:`~literalizer.exceptions.ZipSourceWithoutInputFormatError`
     - ``zip_source`` was supplied without ``zip_input_format``.
     - Pass ``zip_input_format`` alongside ``zip_source``.
   * - :class:`~literalizer.exceptions.ZipValuesWithoutCallTransformError`
     - ``zip_source`` was supplied without a ``call_transform`` to consume the
       paired values.
     - Supply a ``call_transform`` that reads
       :attr:`~literalizer.CallContext.zipped`, or drop ``zip_source``.
   * - :class:`~literalizer.exceptions.ZipValuesLengthMismatchError`
     - ``zip_source`` parsed to a different number of elements than the calls
       generated.
     - Make ``zip_source`` hold one element per generated call.
   * - :class:`~literalizer.exceptions.CommentSourceLengthMismatchError`
     - ``comment_source`` has a different entry count than the calls generated.
     - Provide one comment per generated call.
   * - :class:`~literalizer.exceptions.CommentSourceMultilineError`
     - A ``comment_source`` entry contains a newline; trailing comments must be
       single-line.
     - Remove the newline, keeping each comment on one line.

Format option combinations
--------------------------

Raised when otherwise valid options combine into something the language
cannot emit.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Exception
     - Cause
     - How to resolve
   * - :class:`~literalizer.exceptions.IncompatibleFormatsError`
     - Two format options conflict, e.g. Rust ``CONST``/``STATIC`` needs a
       constant initializer but ``VEC`` produces a non-constant expression.
     - Change one of the conflicting options so they agree.
   * - :class:`~literalizer.exceptions.WrapCombinedInFileNotSupportedError`
     - ``wrap_combined_in_file`` was used with a language that does not support
       :class:`~literalizer.BothVariableForms`.
     - Use a single variable form, or target a language that supports the
       combined form.

.. seealso::

   :ref:`heterogeneous-strategies` for resolving mixed-type-collection errors.

   :ref:`json-value-types` for the runtime JSON value alternative.

   :doc:`api-reference` for the generated :mod:`literalizer.exceptions`
   reference.
