Rendering function calls
========================

If your documentation or test suite needs to show function calls with
literal arguments across multiple languages, :func:`literalizer.literalize_call`
generates those calls from a single YAML, JSON, JSON5, or TOML source.

Each row of a top-level list becomes a separate function call, with
arguments formatted according to the target language's calling
convention.

Example
-------

Suppose you want to generate calls to ``throttler.check`` with two
parameters (``user_id`` and ``ts``) and wrap each call in ``print()``:

.. code-block:: python

   """Generate per-language function call examples."""

   import textwrap

   from literalizer import InputFormat, literalize_call
   from literalizer.languages import Python

   yaml_source = """\
   ---
   - - user_1
     - 1000.0
   - - user_2
     - 2000.5
   """

   result = literalize_call(
       source=yaml_source,
       input_format=InputFormat.YAML,
       language=Python(
           date_format=Python.date_formats.PYTHON,
           datetime_format=Python.datetime_formats.PYTHON,
           bytes_format=Python.bytes_formats.HEX,
           sequence_format=Python.sequence_formats.TUPLE,
           set_format=Python.set_formats.SET,
           variable_type_hints=Python.variable_type_hints_formats.NEVER,
       ),
       target_function="throttler.check",
       parameter_names=["user_id", "ts"],
       call_transform=lambda ctx: f"print({ctx.call})",
   )

   assert result.code == textwrap.dedent(
       text="""\
       print(throttler.check(user_id="user_1", ts=1000.0))
       print(throttler.check(user_id="user_2", ts=2000.5))""",
   )

Calling conventions
-------------------

Each language has a calling convention that determines how arguments are
formatted.  There are three styles:

**Keyword** (e.g. Python, Swift, Ruby):
arguments are passed as ``name=value`` pairs.

.. code-block:: python

   """Illustrate the keyword-call style."""


   class Throttler:
       """Stub throttler for the example."""

       def check(self, *, user_id: str, ts: float) -> str:
           """Return a confirmation string."""
           return f"{type(self).__name__} checked {user_id} at {ts}"


   throttler = Throttler()
   print(throttler.check(user_id="user_1", ts=1000.0))

**Object** (e.g. JavaScript, TypeScript):
arguments are wrapped in an object literal.

.. code-block:: javascript

   print(throttler.check({ user_id: "user_1", ts: 1000.0 }));

**Positional** (e.g. Rust, Java, C++):
arguments are passed by position only — parameter names are not included
in the output.

.. code-block:: rust

   print(throttler.check("user_1", 1000.0));

You do not need to choose a style — it is determined automatically by
the language you pass to :func:`~literalizer.literalize_call`.

Variable references as arguments
--------------------------------

An argument can be a **reference to a named variable** instead of an
inline literal value.  Use a ``{"$ref": "name"}`` marker at the
argument position and :func:`~literalizer.literalize_call` emits the
identifier verbatim at that slot.  Other arguments are still rendered
as literals as usual, so refs and literals can be mixed freely.

For example, passing the JSON source ``[[{"$ref": "my_var"}, 42]]`` to
:func:`~literalizer.literalize_call` with ``parameter_names=["data",
"count"]`` and ``language=Python()`` yields
``process(data=my_var, count=42)``.

This composes with
:class:`~literalizer.NewVariable`: declare the data once with
:func:`~literalizer.literalize` and then refer to it from a call rendered
by :func:`~literalizer.literalize_call`, without repeating the literal
value at the call site.

When the referenced value contains types that affect generated
declarations or imports, pass those source values via ``ref_values``.
The call still renders only the identifier, but the referenced value
participates in preamble inference:

.. code-block:: python

   """Render a call whose ref contributes to preamble inference."""

   from literalizer import InputFormat, NewVariable, literalize, literalize_call
   from literalizer.languages import Haskell

   language = Haskell()
   declaration = literalize(
       source="[1, 2, 3]",
       input_format=InputFormat.JSON,
       language=language,
       variable_form=NewVariable(name="myList"),
   )
   call = literalize_call(
       source='[[{"$ref": "myList"}, 42]]',
       input_format=InputFormat.JSON,
       language=language,
       target_function="process",
       parameter_names=["data", "count"],
       ref_values={"myList": declaration.source_data},
   )
   assert call.declaration_code == "process(myList, 42)"

If a ref name is omitted from ``ref_values``, its marker is ignored for
preamble inference as before.  ``ref_values`` keys are the names from
the input data before any ``ref_case`` conversion.

By default the identifier is emitted verbatim.  Pass ``ref_case`` to
:func:`~literalizer.literalize_call` to convert the name to the target
language's idiomatic case.

Case conversion
~~~~~~~~~~~~~~~

The ``ref_case`` parameter accepts a :class:`~literalizer.IdentifierCase`
value (``SNAKE``, ``CAMEL``, ``PASCAL``, ``UPPER_SNAKE``, or ``KEBAB``).
Each :class:`Language` exposes two related but independent attributes:

* :attr:`~literalizer.Language.supported_ref_cases` -- the cases that
  produce a syntactically legal identifier in the target language.
  Passing a case outside this set raises
  :class:`~literalizer.exceptions.UnsupportedIdentifierCaseError`.
  Most C-family languages set this to
  :data:`~literalizer.NON_KEBAB_REF_CASES`, since ``my-var`` is not a
  legal identifier; Lisp-family languages and other kebab-friendly
  grammars use :data:`~literalizer.ALL_REF_CASES`.
* :attr:`~literalizer.Language.identifier_cases` -- the cases that are
  *idiomatic* for the language, ordered by stylistic preference (the
  first element is the default).  This list is documentation of style
  only; it is not used to reject explicit ``ref_case`` choices.  A
  language may prefer only ``SNAKE`` while still syntactically
  supporting ``CAMEL``, ``PASCAL``, and ``UPPER_SNAKE``.

The same YAML source can drive idiomatic identifiers across multiple
languages.  For example, the JSON source ``[[{"$ref": "user_obj"}, 42]]``
with ``parameter_names=["data", "count"]`` produces:

* ``ref_case=IdentifierCase.SNAKE`` with ``language=Python()`` →
  ``process(data=user_obj, count=42)``.
* ``ref_case=IdentifierCase.CAMEL`` with ``language=JavaScript()`` →
  ``process({ data: userObj, count: 42 });``.
* ``ref_case=IdentifierCase.PASCAL`` with ``language=Go()`` →
  ``process(UserObj, 42)``.

Composing declarations and calls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pairing a :func:`~literalizer.literalize` call (which declares a
variable) with a :func:`~literalizer.literalize_call` call (which
references that variable via ``{"$ref": "name"}``) is the natural way
to render a complete, self-contained source file: declaration first,
call second.

Each call independently computes its own
:attr:`~literalizer.LiteralizeResult.preamble` and
:attr:`~literalizer.LiteralizeResult.body_preamble` from the data it
sees.  When the two halves see overlapping data — for example, both
contain integers in a language where integers require a wrapper type
declaration — concatenating their outputs as-is produces duplicates.
Strict compilers reject the result (Haskell rejects duplicate ``data``
declarations; D rejects duplicate ``import`` lines) and a linter flags
it (``ruff`` and ``pylint`` warn about repeated ``from typing import
Any`` lines).

Pass the ref values through the ``bound_refs`` argument of
:func:`~literalizer.literalize_call` (with ``wrap_in_file=True``) and
it renders the whole file for you: each ref is declared ahead of the
calls, a no-op stub for the target function is injected, and one
reconciled preamble is placed in front.  This is the call-side
counterpart of :func:`~literalizer.literalize`'s own ``bound_refs``
argument; the returned :attr:`~literalizer.LiteralizeResult.code` is
the finished file:

.. code-block:: python

   """Render a call that declares its refs into one Haskell file."""

   from literalizer import InputFormat, literalize_call
   from literalizer.languages import Haskell

   composed = literalize_call(
       source='[[{"$ref": "my_list"}, 42]]',
       input_format=InputFormat.JSON,
       language=Haskell(),
       target_function="process",
       parameter_names=["data", "count"],
       wrap_in_file=True,
       bound_refs={"my_list": [1, 2, 3]},
   )

   assert composed.code.count("data Val = HInt Integer | HList [Val]") == 1

``bound_refs`` entries double as ``ref_values``, so a name need not be
repeated in both mappings, and they are emitted in iteration order
ahead of their first use.

Snake case is the recommended authoring convention for ``$ref`` names:
``pyhumps`` converts ``snake_case`` to every other case without loss.
Inputs in other conventions are normalized to ``snake_case`` first, so
``userObj`` or ``UserObj`` also convert correctly, but at the cost of
losing any preserved acronyms: ``HTTPRequest`` normalizes to
``http_request`` and converts back to Pascal case as ``HttpRequest``.

References inside plain data structures
----------------------------------------

``{"$ref": "name"}`` markers also work inside data passed to
:func:`~literalizer.literalize` -- not just inside call arguments.  This
is useful when you want to emit a data structure where some values are
references to variables declared elsewhere rather than inline literals.

By default, ref identifiers are emitted verbatim.  Pass ``ref_case`` to
:func:`~literalizer.literalize` when the identifier should be converted
before rendering.

For example, suppose you have a configuration dict where ``timeout`` and
``host`` are already declared as named constants and you want to reference
them rather than repeat the values:

.. code-block:: python

   """Emit a config dict with variable references as values."""

   from literalizer import IdentifierCase, InputFormat, literalize
   from literalizer.languages import Python

   config_json = (
       '{"timeout": {"$ref": "timeout_secs"}, "host": {"$ref": "default_host"}}'
   )

   result = literalize(
       source=config_json,
       input_format=InputFormat.JSON,
       language=Python(),
       ref_case=IdentifierCase.SNAKE,
   )
   assert result.bare_code == (
       '{\n    "timeout": timeout_secs,\n    "host": default_host,\n}'
   )

The same ``ref_case`` rules apply as for :func:`~literalizer.literalize_call`:
the identifier is case-converted to the requested convention and any
language-specific sigil is applied (e.g. ``$timeout_secs`` in PHP).
Refs can appear at any depth -- nested inside dicts, inside lists, or as
the top-level value -- and can be mixed freely with ordinary literals in
the same structure.

Pairing each call with a value
------------------------------

``call_transform`` receives a :class:`~literalizer.CallContext`, not just
the call string.  Alongside ``ctx.call`` (the rendered call expression)
it carries the call's zero-based ``ctx.index``, its input ``ctx.row``,
and -- when ``zip_source`` is supplied -- ``ctx.zipped``: the matching
top-level element of a second, equal-length companion source, parsed
with the same parser as ``source`` and rendered as a language-native
literal.  This lets you print an expected value beside each call's
actual return value:

.. code-block:: python

   """Pair each generated call with a value from a parallel sequence."""

   from literalizer import InputFormat, literalize_call
   from literalizer.languages import Python

   books_yaml = """\
   ---
   - [Dune, 1965]
   - [Solaris, 1961]
   """

   in_print_yaml = """\
   ---
   - true
   - false
   """

   result = literalize_call(
       source=books_yaml,
       input_format=InputFormat.YAML,
       language=Python(),
       target_function="catalog.lookup",
       parameter_names=["title", "year"],
       zip_source=in_print_yaml,
       zip_input_format=InputFormat.YAML,
       call_transform=lambda ctx: (
           f'print("in_print?", {ctx.zipped}, "->", {ctx.call})'
       ),
   )

   assert result.code == (
       'print("in_print?", True, "->", '
       'catalog.lookup(title="Dune", year=1965))\n'
       'print("in_print?", False, "->", '
       'catalog.lookup(title="Solaris", year=1961))'
   )

``zip_source`` is parsed with the same parser as ``source``; when
``per_element`` is ``True`` it must parse to a list whose top-level
elements pair one-for-one with the generated calls.  It requires
``zip_input_format`` and a ``call_transform``.  ``call_transform`` is
only supported for
languages whose call form is an expression that can be wrapped
(positional, keyword, or object call style); prefix-, postfix-, and
command-style languages reject it with
:class:`~literalizer.exceptions.UnsupportedCallShapeError`.

Annotating each call with a trailing comment
--------------------------------------------

A ``call_transform`` only sees the *call expression*, before the
language's statement terminator is applied, so it cannot append a
trailing line comment: in C-family languages the terminator would land
*inside* the comment (``catalog.lookup("Dune", 1965)  // first
edition;``) and the statement would no longer compile.  ``comment_source``
solves this by handing the core a sequence of comments -- one per
generated call, paired positionally -- which it emits **after** the
statement terminator using the target language's comment syntax:

.. code-block:: python

   """Attach a per-row trailing comment to each generated call."""

   from literalizer import InputFormat, literalize_call
   from literalizer.languages import Java

   books_yaml = """\
   ---
   - [Dune, 1965]
   - [Solaris, 1961]
   """

   result = literalize_call(
       source=books_yaml,
       input_format=InputFormat.YAML,
       language=Java(),
       target_function="catalog.lookup",
       parameter_names=["title", "year"],
       comment_source=["first edition", "translated from Polish"],
   )

   assert result.code == (
       'catalog.lookup("Dune", 1965);  // first edition\n'
       'catalog.lookup("Solaris", 1961);  // translated from Polish'
   )

``comment_source`` is a plain sequence, not a parsed source, so it needs
neither a ``call_transform`` nor an input format.  Its length must equal
the number of generated calls (one per top-level element when
``per_element`` is ``True``, otherwise one) or
:class:`~literalizer.exceptions.CommentSourceLengthMismatchError` is
raised; an empty entry emits no comment, and an entry containing a
newline raises
:class:`~literalizer.exceptions.CommentSourceMultilineError`.  Languages
with no line comment fall back to that language's block-comment form
(``catalog.lookup("Dune", 1965)  (* first edition *)`` in OCaml), which
is valid on a single line.

A trailing comment is only safe where each generated call is a
self-contained line.  Languages that assemble the call sequence into a
single clause, list or expression -- so a separator, terminator or
closer would follow the call on the same line and the line comment
would swallow it (Erlang's clause-terminating ``.``, a Jsonnet list
``,``, a Roc ``dbg ( ... )`` wrapper) -- reject a non-empty
``comment_source``
with :class:`~literalizer.exceptions.UnsupportedCallShapeError`.  The
supported set is exactly the languages whose
:attr:`~literalizer.Language.supports_standalone_comments_in_wrapped_calls`
is ``True``.
