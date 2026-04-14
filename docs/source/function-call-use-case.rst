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
       callee="throttler.check",
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

.. skip doccmd[all]: next

.. code-block:: python

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
