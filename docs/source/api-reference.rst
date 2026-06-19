API Reference
=============

.. currentmodule:: literalizer

Everything documented here is importable directly from the top-level ``literalizer`` package (exceptions live in :mod:`literalizer.exceptions`).

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

The ``bound_refs`` argument to :func:`literalize` and :func:`literalize_call` describes each referenced name as one of these forms.

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

The ``dispatch_field`` / ``call_specs`` arguments to :func:`literalize_call` render an ordered sequence of *different* calls, one per input element, using this table.

.. autoclass:: CallSpec
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

Exceptions
----------

.. automodule:: literalizer.exceptions
   :members:
