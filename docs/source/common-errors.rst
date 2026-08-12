.. _common-errors:

Common errors and how to resolve them
=====================================

|project| raises a specific, typed exception whenever it cannot turn your data into valid code for the target language, rather than emitting source the compiler would reject.
Every exception lives in :mod:`literalizer.exceptions`; this page groups them by the stage at which they are raised and renders each one's meaning and the recommended fix directly from :mod:`literalizer.exceptions`, so the guidance here cannot drift from the API reference.

All exceptions are importable from :mod:`literalizer.exceptions`, so a name such as ``HeterogeneousScalarCollectionError`` below refers to :class:`literalizer.exceptions.HeterogeneousScalarCollectionError`.

Catch any Literalizer error
---------------------------

Every public exception inherits from :class:`literalizer.LiteralizerError`.
Applications that report any invalid input or configuration uniformly can
catch that shared base::

   from literalizer import LiteralizerError, literalize

   try:
       result = literalize(...)
   except LiteralizerError as error:
       report(error)

Parsing the input
------------------

Raised while reading ``source`` in the declared ``input_format``, before any language-specific rendering.

.. autoexception:: literalizer.exceptions.ParseError
   :no-index:

.. autoexception:: literalizer.exceptions.JSONParseError
   :no-index:

.. autoexception:: literalizer.exceptions.JSON5ParseError
   :no-index:

.. autoexception:: literalizer.exceptions.YAMLParseError
   :no-index:

.. autoexception:: literalizer.exceptions.TOMLParseError
   :no-index:

Mixed-type collections
----------------------

Raised when the data mixes types within one collection but the target language requires that collection to be homogeneous.
Each of these subclasses :class:`~literalizer.exceptions.HeterogeneousCollectionError`, so you can catch the base class to skip any input a strict-typed language cannot hold.
The usual fix is to pick a non-default ``heterogeneous_strategy``; see :ref:`heterogeneous-strategies` for the full discussion and :ref:`json-value-types` for the runtime JSON value alternative.

.. autoexception:: literalizer.exceptions.HeterogeneousCollectionError
   :no-index:

.. autoexception:: literalizer.exceptions.HeterogeneousScalarCollectionError
   :no-index:

.. autoexception:: literalizer.exceptions.HeterogeneousSiblingListsError
   :no-index:

.. autoexception:: literalizer.exceptions.MixedListValuesError
   :no-index:

.. autoexception:: literalizer.exceptions.MixedDictValuesError
   :no-index:

.. autoexception:: literalizer.exceptions.HeterogeneousSiblingMapsError
   :no-index:

.. autoexception:: literalizer.exceptions.MixedDictKeysError
   :no-index:

.. autoexception:: literalizer.exceptions.MixedDictShapesError
   :no-index:

.. autoexception:: literalizer.exceptions.HeterogeneousSetError
   :no-index:

.. autoexception:: literalizer.exceptions.TupleArityNotRepresentableError
   :no-index:

Values the target language cannot represent
-------------------------------------------

Raised at the formatting boundary when an individual value has no faithful representation in the target language.

.. autoexception:: literalizer.exceptions.UnrepresentableInputError
   :no-index:

.. autoexception:: literalizer.exceptions.UnrepresentableStringError
   :no-index:

.. autoexception:: literalizer.exceptions.InvalidDictKeyError
   :no-index:

.. autoexception:: literalizer.exceptions.NullInCollectionError
   :no-index:

.. autoexception:: literalizer.exceptions.UnrepresentableIntegerError
   :no-index:

.. autoexception:: literalizer.exceptions.UnrepresentableEmptyDictError
   :no-index:

.. autoexception:: literalizer.exceptions.UnrepresentableSpecialFloatError
   :no-index:

Identifiers and variable wrapping
---------------------------------

Raised when ``variable_form`` or ``ref_case`` asks for output the target language cannot produce.

Capability flags such as ``supports_empty_dict_key`` let callers check an
option before constructing a language. If a known option is nevertheless
passed to a language that does not support it, construction raises:

.. autoexception:: literalizer.exceptions.UnsupportedOptionError
   :no-index:

.. autoexception:: literalizer.exceptions.UnsupportedIdentifierCaseError
   :no-index:

.. autoexception:: literalizer.exceptions.VariableNameNotSupportedError
   :no-index:

.. autoexception:: literalizer.exceptions.InvalidNewVariableNameError
   :no-index:

.. autoexception:: literalizer.exceptions.ReservedVariableNameError
   :no-index:

.. autoexception:: literalizer.exceptions.WrapInFileWithoutVariableNotSupportedError
   :no-index:

.. autoexception:: literalizer.exceptions.InvalidRecordNameError
   :no-index:

Function calls
--------------

Raised by :func:`~literalizer.literalize_call` and its arguments (``parameter_names``, ``call_transform``, ``zip_source``, ``comment_source``, ``target_function``).
See :doc:`function-call-use-case`.

.. autoexception:: literalizer.exceptions.CallsNotSupportedByLanguageError
   :no-index:

.. autoexception:: literalizer.exceptions.CallsNotSupportedByToolError
   :no-index:

.. autoexception:: literalizer.exceptions.PerElementNotListError
   :no-index:

.. autoexception:: literalizer.exceptions.ParameterCountMismatchError
   :no-index:

.. autoexception:: literalizer.exceptions.CallArgNotSupportedError
   :no-index:

.. autoexception:: literalizer.exceptions.UnsupportedCallShapeError
   :no-index:

.. autoexception:: literalizer.exceptions.DottedCallTargetNotSupportedError
   :no-index:

.. autoexception:: literalizer.exceptions.ZipSourceWithoutInputFormatError
   :no-index:

.. autoexception:: literalizer.exceptions.ZipValuesWithoutCallTransformError
   :no-index:

.. autoexception:: literalizer.exceptions.ZipValuesLengthMismatchError
   :no-index:

.. autoexception:: literalizer.exceptions.CommentSourceLengthMismatchError
   :no-index:

.. autoexception:: literalizer.exceptions.CommentSourceMultilineError
   :no-index:

Format option combinations
--------------------------

Raised when otherwise valid options combine into something the language cannot emit.

.. autoexception:: literalizer.exceptions.IncompatibleFormatsError
   :no-index:

.. autoexception:: literalizer.exceptions.WrapCombinedInFileNotSupportedError
   :no-index:

.. seealso::

   :ref:`heterogeneous-strategies` for resolving mixed-type-collection errors.

   :ref:`json-value-types` for the runtime JSON value alternative.

   :doc:`api-reference` for the generated :mod:`literalizer.exceptions` reference.
