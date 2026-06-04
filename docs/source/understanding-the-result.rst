Understanding the result
========================

Every call to :func:`~literalizer.literalize` and :func:`~literalizer.literalize_call` returns a single :class:`~literalizer.LiteralizeResult`.
The examples elsewhere reach for whichever field they need, but the object is worth understanding as a whole: for several languages the headline :attr:`~literalizer.LiteralizeResult.code` does **not** compile on its own, and assembling output correctly means knowing which other fields to place around it.

The fields
----------

The members below are rendered directly from the :class:`~literalizer.LiteralizeResult` source, the authoritative description of each field.
:attr:`~literalizer.LiteralizeResult.code` is the field most callers read; the rest of this page explains when you need the others.

.. autoclass:: literalizer.LiteralizeResult
   :members:
   :noindex:

When ``code`` is not enough on its own
---------------------------------------

For many languages and the default settings, :attr:`~literalizer.LiteralizeResult.code` is a complete, drop-in literal and :attr:`~literalizer.LiteralizeResult.preamble` is empty.
That changes the moment a strategy or ``json_type`` synthesizes a declaration.
Rendering a heterogeneous list for :class:`~literalizer.Rust` with the ``TAGGED_ENUM`` strategy puts the generated ``enum`` in :attr:`~literalizer.LiteralizeResult.preamble`; the literal in :attr:`~literalizer.LiteralizeResult.code` references that ``enum`` and will not compile without it:

.. code-block:: python

   """The Rust TAGGED_ENUM literal needs its preamble to compile."""

   from literalizer import InputFormat, literalize
   from literalizer.languages import Rust

   result = literalize(
       source='[1, "two", 3.0]',
       input_format=InputFormat.JSON,
       language=Rust(
           heterogeneous_strategy=Rust.heterogeneous_strategies.TAGGED_ENUM,
       ),
   )

   # The literal references a type that is defined in the preamble:
   assert "Value::I32(1)" in result.code
   assert result.preamble == (
       "enum Value {",
       "    I32(i32),",
       "    Str(&'static str),",
       "    F64(f64),",
       "}",
   )

To turn this into source that compiles by hand, join :attr:`~literalizer.LiteralizeResult.preamble` ahead of :attr:`~literalizer.LiteralizeResult.code`:

.. code-block:: python

   """Assemble preamble + code into a fragment that compiles by hand."""

   from literalizer import InputFormat, literalize
   from literalizer.languages import Rust

   result = literalize(
       source='[1, "two", 3.0]',
       input_format=InputFormat.JSON,
       language=Rust(
           heterogeneous_strategy=Rust.heterogeneous_strategies.TAGGED_ENUM,
       ),
   )

   source = "\n".join((*result.preamble, result.code))
   assert source.startswith("enum Value {")
   assert source.endswith("]")

Letting ``wrap_in_file`` do the assembly
-----------------------------------------

Stitching the fields together yourself is error-prone, because the correct placement of :attr:`~literalizer.LiteralizeResult.preamble` and :attr:`~literalizer.LiteralizeResult.body_preamble` differs by language.
Pass ``wrap_in_file=True`` and |project| assembles a complete, valid file for you: the preamble is placed at the top, the literal is bound to your variable inside whatever scope the language requires, and the regions are ordered correctly.

.. code-block:: python

   """wrap_in_file=True assembles the preamble and literal into a file."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import Rust

   result = literalize(
       source='[1, "two", 3.0]',
       input_format=InputFormat.JSON,
       language=Rust(
           heterogeneous_strategy=Rust.heterogeneous_strategies.TAGGED_ENUM,
       ),
       variable_form=NewVariable(name="values"),
       wrap_in_file=True,
   )

   # The enum, a main function, and the bound literal are all present,
   # in the order required to compile:
   assert result.code == (
       "enum Value {\n"
       "    I32(i32),\n"
       "    Str(&'static str),\n"
       "    F64(f64),\n"
       "}\n"
       "fn main() {\n"
       "    let values = vec![\n"
       "        Value::I32(1),\n"
       '        Value::Str("two"),\n'
       "        Value::F64(3.0),\n"
       "    ];\n"
       "    let _ = values;\n"
       "}"
   )

Prefer ``wrap_in_file=True`` whenever you need output that compiles or runs as-is.
Read :attr:`~literalizer.LiteralizeResult.code` and :attr:`~literalizer.LiteralizeResult.preamble` separately only when you are embedding the literal into a larger template of your own and want to control where the preamble lands.

``body_preamble`` and ``bare_code``
-----------------------------------

Some languages express a heterogeneous value as a literal of a type they must also define, where that type definition belongs immediately ahead of the literal rather than at file scope.
F# is one such language: its ``type Val =`` discriminated union appears in :attr:`~literalizer.LiteralizeResult.body_preamble`, already folded into :attr:`~literalizer.LiteralizeResult.code`.
Use :attr:`~literalizer.LiteralizeResult.bare_code` when you want the literal on its own and intend to place the type definition yourself:

.. code-block:: python

   """code folds in the body_preamble; bare_code omits it."""

   from literalizer import InputFormat, literalize
   from literalizer.languages import FSharp

   result = literalize(
       source='[1, "two", 3.0]',
       input_format=InputFormat.JSON,
       language=FSharp(),
   )

   assert result.body_preamble == (
       "type Val =",
       "    | FInt of int64",
       "    | FFloat of float",
       "    | FStr of string",
       "    | FList of Val list",
   )
   # code includes the type definition; bare_code starts at the literal:
   assert result.code.startswith("type Val =")
   assert result.bare_code.startswith("FList [")

Multi-section output
--------------------

A few languages cannot express a value as one drop-in fragment: their output spans more than one region of a source file that a wrapping template must place separately.
For these, :attr:`~literalizer.LiteralizeResult.sections` holds the rendered :class:`~literalizer.FileSection` regions and :attr:`~literalizer.LiteralizeResult.code` holds an opaque marker payload rather than usable source.
This is empty for almost every language; see :attr:`~literalizer.LiteralizeResult.sections` for details and the one current example.
