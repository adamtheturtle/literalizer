.. _heterogeneous-strategies:

Heterogeneous strategies
========================

Some target languages can hold a collection whose elements have
different types; others require every element of a list, or every
value of a map, to share one static type.  A *heterogeneous strategy*
controls what :func:`~literalizer.literalize` does when the input data
has mixed-type values but the target language's natural collection type
cannot hold them.

Every built-in language exposes the strategy as a
``heterogeneous_strategy`` constructor argument whose value comes from
the language's ``heterogeneous_strategies`` enum.  The default for every
language is ``ERROR``.

What "heterogeneous" means here
-------------------------------

A value is heterogeneous when a single collection mixes more than one
scalar type, or a map mixes value types that a strict-map language
cannot unify.  Two shapes come up most often:

* A **list** whose elements are not all the same scalar type, e.g.
  ``[1, "two", 3.0]``.  In a dynamically typed language this is an
  ordinary list; in Rust it is not a valid ``Vec<T>``.
* A **record-shaped dict**: a non-empty, string-keyed dict whose values
  mix scalars with at least one container, e.g.
  ``{"id": 100, "blocks": [102, 103]}``.  Conceptually this is a record
  (a struct), not a map, so a strict-map language has no ``HashMap``
  that fits it.

Languages whose native collections are already heterogeneous (most
dynamically typed languages, plus formats such as JSON5, YAML, and
TOML) never reach a strategy: the data is representable as-is, so they
expose only ``ERROR`` and never raise for these inputs.

The strategies
--------------

``ERROR`` (default)
~~~~~~~~~~~~~~~~~~~

Refuse to render data the target language's natural collection type
cannot hold.  :func:`~literalizer.literalize` raises
:class:`~literalizer.exceptions.HeterogeneousScalarCollectionError`
(or :class:`~literalizer.exceptions.HeterogeneousSiblingListsError`,
or :class:`~literalizer.exceptions.MixedDictValuesError`) instead of
emitting code the target compiler would reject.  This is the safe
default and matches the strict-typing convention of statically typed
languages.

.. code-block:: python

   """The default ERROR strategy refuses a mixed-type list."""

   from literalizer import InputFormat, literalize
   from literalizer.exceptions import HeterogeneousScalarCollectionError
   from literalizer.languages import Rust

   raised = False
   try:
       literalize(
           source='[1, "two", 3.0]',
           input_format=InputFormat.JSON,
           language=Rust(),
       )
   except HeterogeneousScalarCollectionError:
       raised = True

   assert raised

``TAGGED_ENUM`` (and its per-language equivalents)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate a sum type in the preamble that contains only the variants
actually present in the data, and wrap each heterogeneous scalar in the
matching variant.  This keeps the collection homogeneous (every element
is now the one wrapper type) while preserving each value's original
type at the variant level.

This family appears under different names because each language's sum
type is different: ``TAGGED_ENUM`` on :class:`~literalizer.Rust` (a
tagged ``enum``), ``UNION_TYPE`` on :class:`~literalizer.Dhall`,
``VARIANT`` on :class:`~literalizer.Mojo`, ``OBJECT_VARIANT`` on
:class:`~literalizer.Nim`, and ``INTERFACE`` on :class:`~literalizer.V`.
The generated type's name is configurable (for example
``Rust.heterogeneous_value_enum_name``, default ``"Value"``).

.. code-block:: python

   """TAGGED_ENUM wraps each mixed scalar in a generated Rust enum."""

   import textwrap

   from literalizer import InputFormat, literalize
   from literalizer.languages import Rust

   result = literalize(
       source='[1, "two", 3.0]',
       input_format=InputFormat.JSON,
       language=Rust(
           heterogeneous_strategy=Rust.heterogeneous_strategies.TAGGED_ENUM,
       ),
   )

   assert result.code == textwrap.dedent(
       text="""\
       vec![
           Value::I32(1),
           Value::Str("two"),
           Value::F64(3.0),
       ]""",
   )
   assert result.preamble == (
       "enum Value {",
       "    I32(i32),",
       "    Str(&'static str),",
       "    F64(f64),",
       "}",
   )

A tagged enum cannot wrap container values, so it does not help a
record-shaped dict whose fields mix scalars with a list or another
dict.  Use ``RECORD`` for that.

``RECORD``
~~~~~~~~~~

Treat each record-shaped dict (non-empty, string-keyed) as a generated
struct/record declared in the preamble plus a matching struct literal,
so its fields may legitimately mix scalars and containers.  Each
distinct ordered key set becomes one declaration; the declaration name
prefix is configurable via ``record_struct_name_prefix`` (default
``"Record"``).

This is the right strategy for data that is conceptually a record, not
a map.  On :class:`~literalizer.Python` (whose ``dict`` is already
heterogeneous) it is purely an idiomatic-output choice; the default
``ERROR`` strategy renders the same data as a plain ``dict``.

.. code-block:: python

   """RECORD renders a record-shaped dict as a frozen dataclass."""

   import textwrap

   from literalizer import InputFormat, literalize
   from literalizer.languages import Python

   source = (
       '{"id": 100, "description": "first task", '
       '"is_done": false, "blocks": [102, 103]}'
   )

   result = literalize(
       source=source,
       input_format=InputFormat.JSON,
       language=Python(
           heterogeneous_strategy=Python.heterogeneous_strategies.RECORD,
       ),
   )

   assert result.code == textwrap.dedent(
       text="""\
       Record0(
           id=100,
           description="first task",
           is_done=False,
           blocks=(
               102,
               103,
           ),
       )""",
   )
   assert result.preamble == (
       "from __future__ import annotations",
       "import dataclasses",
       textwrap.dedent(
           text="""\
           @dataclasses.dataclass(frozen=True)
           class Record0:
               id: int
               description: str
               is_done: bool
               blocks: tuple[int, ...]""",
       ),
   )

   # The default ERROR strategy renders the same data as a plain dict:
   default_result = literalize(
       source=source,
       input_format=InputFormat.JSON,
       language=Python(),
   )
   assert default_result.code.startswith("{")

``TUPLE``
~~~~~~~~~

Render a fixed-length heterogeneous **scalar** array (all elements
scalar, spanning at least two scalar types) as the language's native
fixed-length tuple instead of rejecting it or widening it to a
homogeneous list.  Where the language also has ``RECORD``, ``TUPLE``
composes with it, so a record field whose value is such an array
becomes a tuple-typed field.  Some languages cap the tuple length
(:class:`~literalizer.Kotlin` has only ``Pair`` and ``Triple`` and
raises :class:`~literalizer.exceptions.TupleArityNotRepresentableError`
otherwise); :class:`~literalizer.Rust` and :class:`~literalizer.Scala`
impose no length limit.

Which should I use? Heterogeneous strategies vs. JSON value types
-----------------------------------------------------------------

A heterogeneous strategy is not the only way to render mixed-type data.
Several languages also expose a ``json_type`` constructor argument that
renders the whole value through a single runtime JSON value type (for
example ``Rust.json_types.SERDE_JSON_VALUE`` yielding
``serde_json::Value``).  Both features accept input such as
``[1, "two", 3.0]`` that the language's narrow collection type cannot
hold, so the same data often qualifies for either one.  They differ in
the type of the rendered value:

* A heterogeneous strategy keeps the result **statically typed**.  The
  generated enum, struct, or tuple preserves each value's original type,
  and the rendered collection stays a normal typed collection of that
  wrapper.  Reach for this when the surrounding code is statically typed
  and you want the compiler to keep tracking the element types, or when
  the data is conceptually a record (use ``RECORD``).
* ``json_type`` renders the value as **one runtime JSON value type**
  (``serde_json::Value``, ``JsonNode``, ``JSON::Any``, and so on).  The
  static type is uniform and the element types are recovered at runtime.
  Reach for this when the value is genuinely arbitrary JSON, when you
  already pass it to a JSON library, or when synthesizing a typed wrapper
  per shape would be more structure than the data deserves.

The two are mutually exclusive for a given render, and some languages
reject specific combinations (for instance Java, Kotlin, Zig, and Odin
reject ``RECORD`` while in their ``json_type`` mode).  See
:ref:`json-value-types` for every ``json_type`` value, its emitted form,
and the per-language constraints.

Per-language support matrix
---------------------------

Every built-in language supports ``ERROR`` and defaults to it.  The
table below lists every language that exposes a richer strategy; any
language not listed exposes ``ERROR`` only.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Language
     - Strategies (besides ``ERROR``)
   * - :class:`~literalizer.Rust`
     - ``TAGGED_ENUM``, ``RECORD``, ``TUPLE``
   * - :class:`~literalizer.Kotlin`
     - ``RECORD``, ``TUPLE``
   * - :class:`~literalizer.Scala`
     - ``RECORD``, ``TUPLE``
   * - :class:`~literalizer.Go`
     - ``RECORD``
   * - :class:`~literalizer.Java`
     - ``RECORD``
   * - :class:`~literalizer.Python`
     - ``RECORD``
   * - :class:`~literalizer.Swift`
     - ``RECORD``
   * - :class:`~literalizer.Cpp`
     - ``RECORD``, ``TUPLE``
   * - :class:`~literalizer.TypeScript`
     - ``TUPLE``
   * - :class:`~literalizer.Dhall`
     - ``UNION_TYPE``
   * - :class:`~literalizer.Mojo`
     - ``VARIANT``
   * - :class:`~literalizer.Nim`
     - ``OBJECT_VARIANT``, ``RECORD``
   * - :class:`~literalizer.V`
     - ``INTERFACE``

Naming the generated type
-------------------------

The strategies that synthesize a declaration accept a constructor
argument that controls its name:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Argument
     - Applies to
   * - ``record_struct_name_prefix`` (default ``"Record"``)
     - ``RECORD`` on Rust, Go, Java, Python, Kotlin, Scala, Cpp,
       Swift, Nim
   * - ``heterogeneous_value_enum_name`` (default ``"Value"``)
     - ``TAGGED_ENUM`` on Rust
   * - ``heterogeneous_value_union_name`` (default ``"Value"``)
     - ``UNION_TYPE`` on Dhall
   * - ``heterogeneous_value_variant_name`` (default ``"Value"``)
     - ``VARIANT`` on Mojo, ``OBJECT_VARIANT`` on Nim

Rust, Go, Java, Kotlin, and Scala additionally accept
``record_shape_names`` to map a specific key set to a custom
declaration name; see each language's reference entry.

.. seealso::

   :ref:`json-value-types` for the runtime JSON value type alternative
   to a statically typed strategy.

   :ref:`languages` for every language class and its other format
   options.
