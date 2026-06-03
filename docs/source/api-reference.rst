API Reference
=============

.. currentmodule:: literalizer

Everything documented here is importable directly from the top-level
``literalizer`` package (exceptions live in :mod:`literalizer.exceptions`).

Core functions
--------------

.. autofunction:: literalize

.. autofunction:: literalize_call

Result type
-----------

.. autoclass:: LiteralizeResult
   :members:

.. autoclass:: FileSection
   :members:

Variable forms
--------------

The ``bound_refs`` argument to :func:`literalize` and :func:`literalize_call`
describes each referenced name as one of these forms.

.. autoclass:: NewVariable
   :members:
   :undoc-members:

.. autoclass:: ExistingVariable
   :members:
   :undoc-members:

.. autoclass:: BothVariableForms
   :members:
   :undoc-members:

.. autodata:: VariableForm

.. autoclass:: ModifierCombination
   :members:
   :undoc-members:

Identifier cases
----------------

.. autoclass:: IdentifierCase
   :members:
   :undoc-members:

.. autodata:: ALL_REF_CASES

.. autodata:: NON_KEBAB_REF_CASES

Function calls
--------------

.. autoclass:: CallContext
   :members:
   :undoc-members:

A language renders a call using one of these call styles.

.. autodata:: CallStyle

.. autoclass:: PositionalCallStyle
   :members:
   :undoc-members:

.. autoclass:: KeywordCallStyle
   :members:
   :undoc-members:

.. autoclass:: ObjectCallStyle
   :members:
   :undoc-members:

.. autoclass:: PrefixCallStyle
   :members:
   :undoc-members:

.. autoclass:: PostfixCallStyle
   :members:
   :undoc-members:

.. autoclass:: CommandCallStyle
   :members:
   :undoc-members:

.. autoclass:: StubReturn
   :members:
   :undoc-members:

Input formats
-------------

.. autoclass:: InputFormat
   :members:
   :undoc-members:

Formatting configuration
------------------------

Building blocks used when defining how a language renders collections,
comments and scalars.

.. autoclass:: CollectionLayout
   :members:
   :undoc-members:

.. autoclass:: TrailingCommaConfig
   :members:
   :undoc-members:

.. autoclass:: CommentConfig
   :members:
   :undoc-members:

.. autoclass:: SequenceFormatConfig
   :members:
   :undoc-members:

.. autoclass:: SetFormatConfig
   :members:
   :undoc-members:

.. autoclass:: DictFormatConfig
   :members:
   :undoc-members:

.. autoclass:: OrderedMapFormatConfig
   :members:
   :undoc-members:

.. autoclass:: DateFormatConfig
   :members:
   :undoc-members:

.. autoclass:: DatetimeFormatConfig
   :members:
   :undoc-members:

.. autofunction:: fixed_open

Defining a language
-------------------

The :class:`Language` protocol describes how a language formats literals.
Concrete, built-in languages are listed in :doc:`languages`; the members
below are the contract each one implements.

.. autoclass:: Language
   :members:

.. autoclass:: LanguageCls
   :members:

Exceptions
----------

.. automodule:: literalizer.exceptions
   :members:
