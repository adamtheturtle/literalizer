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
           variable_type_hints=Python.variable_type_hints_formats.AUTO,
       ),
       target_function="throttler.check",
       parameter_names=["user_id", "ts"],
       call_transform=lambda c: f"print({c})",
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

By default the identifier is emitted verbatim.  Pass ``ref_case`` to
:func:`~literalizer.literalize_call` to convert the name to the target
language's idiomatic case.

Case conversion
~~~~~~~~~~~~~~~

The ``ref_case`` parameter accepts a :class:`~literalizer.IdentifierCase`
value (``SNAKE``, ``CAMEL``, ``PASCAL``, ``UPPER_SNAKE``, or ``KEBAB``).
Each :class:`Language` exposes the subset it understands via its nested
``IdentifierCases`` enum; passing a case that the language does not
expose raises
:class:`~literalizer.exceptions.UnsupportedIdentifierCaseError`.

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

Use :func:`~literalizer.compose` to remove duplicate preamble lines in
first-seen order before emitting the file:

.. code-block:: python

   """Compose a declaration and a call into one Python source file."""

   from literalizer import (
       InputFormat,
       NewVariable,
       compose,
       literalize,
       literalize_call,
   )
   from literalizer.languages import Python

   language = Python(date_format=Python.date_formats.PYTHON)

   declaration = literalize(
       source="2026-01-01",
       input_format=InputFormat.YAML,
       language=language,
       variable_form=NewVariable(name="my_date"),
   )
   call = literalize_call(
       source='[[{"$ref": "my_date"}, 2026-01-02]]',
       input_format=InputFormat.YAML,
       language=language,
       target_function="process",
       parameter_names=["first", "second"],
   )

   composed = compose(
       results=(declaration, call),
       language=language,
       wrap_in_file=True,
   )

   assert composed.code.count("import datetime") == 1

Pass ``wrap_in_file=True`` to :func:`~literalizer.compose` when the
language should assemble the merged result as a complete file.  Body
preamble entries are deduplicated by exact string; if separate results
emit different definitions for the same generated type name, resolve
that name collision before composing.

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

Pass ``ref_case`` to :func:`~literalizer.literalize` to activate ref
resolution; without it, ``{"$ref": ...}`` is treated as an ordinary
literal dict, preserving backwards compatibility.

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
