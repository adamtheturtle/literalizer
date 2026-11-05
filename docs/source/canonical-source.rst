Canonical Objective-C source
============================

Objective-C can produce canonical source directly in Python.
Select :class:`literalizer.SourceFormat` when constructing the language:

.. code-block:: python

   """Produce a complete Objective-C program without a formatter."""

   from literalizer import InputFormat, NewVariable, SourceFormat, literalize
   from literalizer.languages import ObjectiveC

   language = ObjectiveC(source_format=SourceFormat.CANONICAL, indent="  ")
   result = literalize(
       source='{"name":"Ada","scores":[10,20]}',
       input_format=InputFormat.JSON,
       language=language,
       variable_form=NewVariable(name="data", modifiers=frozenset()),
       wrap_in_file=True,
   )
   program = result.code

The runtime package needs no formatter executable or LLVM library.
``SourceFormat.PRESERVE`` remains the default and retains existing output.
The canonical policy uses vertical nonempty collections with trailing commas, regardless of ``collection_layout`` or ``trailing_comma``.
Value-level options, boxing, types, comments, and reference bindings remain intact.
Indentation must consist of spaces; unsupported indentation raises :class:`literalizer.exceptions.SourceLayoutError`.

Placement belongs to the request
--------------------------------

A fragment's starting column and enclosing indentation determine its layout.
Pass :class:`literalizer.SourceContext` when inserting a fragment after existing text.
The initial column is an absolute source column, including the caller's prefix.
The indentation level counts steps of the language's ``indent``.

.. code-block:: python

   """Insert generated entries into an authored Objective-C program."""

   from literalizer import InputFormat, SourceContext, SourceFormat, literalize
   from literalizer.languages import ObjectiveC

   prefix = "    id rows = "
   fragment = literalize(
       source='[{"name":"Ada"},{"name":"Grace"}]',
       input_format=InputFormat.JSON,
       language=ObjectiveC(source_format=SourceFormat.CANONICAL, indent="  "),
       source_context=SourceContext(
           indent_level=2,
           initial_column=len(prefix),
       ),
   )
   program = (
       "\n".join(fragment.preamble) + "\n"
       "int main(void) {\n"
       "  @autoreleasepool {\n"
       f"{prefix}{fragment.code};\n"
       "    (void)rows;\n"
       "  }\n"
       "  return 0;\n"
       "}\n"
   )

``continuation_column`` supplies an absolute continuation anchor for an enclosing expression.
``column_limit`` defaults to 80 and describes the whole source line, including caller-owned text.
Use consistent widths throughout one program.
For delimiter-free collection entries, set ``include_delimiters=False`` and make ``indent_level`` describe the entries themselves.

Without an inline prefix, either ``pre_indent_level`` or ``SourceContext`` can place statements inside a function or class.
Combining the two is an error.
An inline context describes one expression or statement; a batch of independent calls requires ordinary enclosing indentation.
Complete files require a zero-column context.

The same placement contract applies to ordinary calls, typed native invocations, result bindings, and composition through ``literalize_call_with_declarations``.
Author surrounding templates and comments in the intended style before combining fragments.
The renderer owns generated syntax, rather than arbitrary caller code.

Independent enforcement
-----------------------

The checked-in ``tests/objective-c.clang-format`` profile uses LLVM defaults with 2-space indentation, an 80-column limit, expanded function bodies, independent trailing comments, and no argument or long collection packing.
The oracle is pinned to clang-format 23.1.3 in development dependencies only.

CI renders the manifest-owned corpus through the public APIs with both the legacy policy and the canonical profile.
Its opt-in ``--check-source-format`` gate compares fresh canonical output against clang-format without modifying it.
The macOS compiler and runtime jobs execute those same canonical artifacts, including caller-owned native classes and placement witnesses.
A separate negative control introduces a whitespace-only defect and requires the oracle to reject it.
The regular supported Python/OS matrix also runs canonical rendering without the formatter dependency, including an execution-unavailable test.

Changing canonical layout requires updating its profile, golden requests, compiler witnesses, and independent oracle together.
A formatter installation at documentation build time is never part of this contract.
