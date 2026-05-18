Added two metadata properties to the :class:`~literalizer.Language`
protocol: ``supports_multi_param_call_wrapper_stub`` (whether the
language can declare and positionally invoke a wrapper stub that
receives the call's result alongside other positional arguments) and
``supports_dict_literal_as_free_expression`` (whether a map literal
can appear as a free-standing expression rather than only on the
right-hand side of a typed assignment).  Both are test-harness
metadata, like the existing ``has_free_function_calls`` and
``supports_dotted_call_stub`` properties;
:func:`~literalizer.literalize_call` does not inspect them.
