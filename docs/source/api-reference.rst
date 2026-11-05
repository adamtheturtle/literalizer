API Reference
=============

.. currentmodule:: literalizer

Everything documented here is importable directly from the top-level ``literalizer`` package (exceptions live in :mod:`literalizer.exceptions`).

Core functions
--------------

.. autofunction:: literalize

.. autofunction:: literalize_call

.. autofunction:: literalize_call_with_declarations

.. autofunction:: literalize_invocations

.. autofunction:: describe_callable

Native invocations
------------------

.. autofunction:: literalize_native_call

.. autofunction:: literalize_native_calls

.. autofunction:: native_invocation_from_data

.. autoclass:: ScalarType
   :members:

.. autoclass:: ObjectType
   :members:

.. autoclass:: NativeLiteral
   :members:

.. autoclass:: NativeReference
   :members:

.. autoclass:: NativeClass
   :members:

.. autoclass:: FunctionTarget
   :members:

.. autoclass:: MessageTarget
   :members:

.. autoclass:: ConstructorTarget
   :members:

.. autoclass:: NativeInvocation
   :members:

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

.. py:data:: ValueInput

   The recursive input-value type accepted by the public rendering functions.

Exceptions
----------

.. automodule:: literalizer.exceptions
   :members:

Callable description recipes
----------------------------

``describe_callable`` renders a short reference for prose, not a function declaration.
It does not generate argument values, receivers, or stubs.
For example:

.. code-block:: python

    """Describe one callable in two languages."""

    from literalizer import describe_callable
    from literalizer.languages import ObjectiveC, Python

    description = {
        "default": {
            "name": "accept",
            "parameter-names": ["value"],
        },
        "languages": {"objective-c": {"selector": "accept:"}},
    }
    assert (
        describe_callable(language=Python(), description=description)
        == "accept(value)"
    )
    assert (
        describe_callable(language=ObjectiveC(), description=description)
        == "accept:"
    )

Generic language overrides amend the default.
Use explicit display spellings for ``name``, ``parameter-names``, and optional ``return-annotation``.
Optional boolean ``space-before-paren`` and ``space-after-paren`` settings preserve the presentation of existing prose.
A ``selector`` requires a native-message backend and exactly one label per parameter.
Unknown fields and language keys, malformed names, and multiline descriptions are rejected.
