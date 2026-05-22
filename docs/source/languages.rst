.. _languages:

Languages
=========

Every target language is a class in :mod:`literalizer.languages`.
You import the class, optionally configure it, and pass an instance to
:func:`~literalizer.literalize`.

Selecting a language
--------------------

Each language class lives in :mod:`literalizer.languages` and is listed in
:data:`~literalizer.languages.ALL_LANGUAGES`.
Create an instance with its defaults, or override individual format options:

.. code-block:: python

   """Select and configure a language."""

   from literalizer import InputFormat, literalize
   from literalizer.languages import Python

   # Use all defaults
   result = literalize(
       source='{"x": 1}',
       input_format=InputFormat.JSON,
       language=Python(),
   )

   # Override specific formats
   result = literalize(
       source='{"x": 1}',
       input_format=InputFormat.JSON,
       language=Python(
           sequence_format=Python.sequence_formats.LIST,
           string_format=Python.string_formats.SINGLE,
           trailing_comma=Python.trailing_commas.NO,
       ),
   )

Format options
--------------

Language classes define nested :class:`~enum.Enum` classes that control how
each data type is rendered.
The available enums vary by language, but the most common ones are:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Enum
     - Controls
   * - ``DateFormats``
     - How ``datetime.date`` values are rendered (e.g. ISO string, constructor call).
   * - ``DatetimeFormats``
     - How ``datetime.datetime`` values are rendered.
   * - ``BytesFormats``
     - Bytes encoding (hex, base64, or language-native).
   * - ``SequenceFormats``
     - Collection type for lists (e.g. ``TUPLE``, ``LIST``, ``ARRAY``, ``VEC``, ``SLICE``).
   * - ``SetFormats``
     - Collection type for sets (e.g. ``SET``, ``FROZENSET``, ``HASHSET``).
   * - ``DictFormats``
     - Map type (e.g. ``DEFAULT``, ``ORDERED``, ``HASHMAP``).
   * - ``StringFormats``
     - Quote style (``SINGLE``, ``DOUBLE``, ``BACKTICK``, ``RAW``).
   * - ``IntegerFormats``
     - Numeric base (``DECIMAL``, ``HEX``, ``OCTAL``, ``BINARY``).
   * - ``FloatFormats``
     - Float rendering (``REPR``, ``FIXED``, ``SCIENTIFIC``).
   * - ``CommentFormats``
     - Comment syntax (``HASH``, ``DOUBLE_SLASH``, etc.).
   * - ``DeclarationStyles``
     - Variable declaration keyword (``ASSIGN``, ``LET``, ``VAR``, ``CONST``).
   * - ``TrailingCommas``
     - Whether to emit a trailing comma in multi-line collections.
   * - ``StatementTerminatorStyles``
     - Statement terminator (``SEMICOLON``, ``NEWLINE``, ``NONE``).

Access a language's enum members through the class itself, e.g.
``Go.sequence_formats.SLICE`` for Go slices or ``Go.date_formats.GO``
for the ``time.Date(...)`` constructor.

Each ``__init__`` parameter has a sensible default, so you only need to
specify the options you want to change.

Heterogeneous values
--------------------

When the input data mixes value types that the target language's
natural collection type cannot hold, a ``heterogeneous_strategy``
constructor argument controls the outcome.  Every language defaults to
``ERROR``; some expose richer strategies such as ``TAGGED_ENUM`` or
``RECORD``.  See :ref:`heterogeneous-strategies` for the strategies,
worked examples, and the per-language support matrix.

JSON value types
----------------

Some languages also have a single runtime JSON value type that is a better
fit than native narrow collection types.  Rust, Crystal, Java, Scala, C#,
and Nim support this through the ``json_type`` constructor argument:

.. code-block:: python

   """Render Rust data as serde_json::Value."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import Rust

   result = literalize(
       source='{"id": 1, "tags": ["red", 2]}',
       input_format=InputFormat.JSON,
       language=Rust(json_type=Rust.json_types.SERDE_JSON_VALUE),
       variable_form=NewVariable(name="payload"),
   )

This emits ``serde_json::json!(...)`` expressions, relaxes Rust's
homogeneous ``Vec<T>`` / ``HashMap<K, V>`` checks, and requires dict keys
to be strings so they remain valid JSON object keys.

Crystal exposes the same option through its standard-library
``JSON::Any``:

.. code-block:: python

   """Render Crystal data as JSON::Any."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import Crystal

   result = literalize(
       source='{"id": 1, "tags": ["red", 2]}',
       input_format=InputFormat.JSON,
       language=Crystal(json_type=Crystal.json_types.JSON_ANY),
       variable_form=NewVariable(name="payload"),
   )

The rendered literal is a JSON document wrapped in ``JSON.parse(%(...))``,
parsed at runtime into a ``JSON::Any``.  The mode relaxes Crystal's
homogeneous ``Hash(K, V)`` and ``Array(T)`` checks, validates that dict
keys are strings, and rejects characters that would break the
``%(...)`` percent literal (``\\``, ``"``, ``(``, ``)``, and ``#{``)
or overflow JSON's signed 64-bit integer range.

Java exposes the same option through Jackson's ``JsonNode``:

.. code-block:: python

   """Render Java data as a Jackson JsonNode."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import Java

   result = literalize(
       source='{"id": 1, "tags": ["red", 2]}',
       input_format=InputFormat.JSON,
       language=Java(json_type=Java.json_types.JACKSON_JSON_NODE),
       variable_form=NewVariable(name="payload"),
   )

This emits ``new ObjectMapper().readTree("...")`` so the rendered
binding has the static type ``com.fasterxml.jackson.databind.JsonNode``
and can hold the heterogeneous values that Java's narrow ``List`` /
``Map`` types reject.  Dict keys must be strings, and the
``RECORD`` ``heterogeneous_strategy`` is rejected because the two
rendering modes cannot be combined.

Scala exposes the same option for Circe's :class:`io.circe.Json`:

.. code-block:: python

   """Render Scala data as a Circe Json value."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import Scala

   result = literalize(
       source='{"id": 1, "tags": ["red", 2]}',
       input_format=InputFormat.JSON,
       language=Scala(json_type=Scala.json_types.CIRCE),
       variable_form=NewVariable(name="payload"),
   )

This emits ``Json.obj(...)`` / ``Json.arr(...)`` factories with
per-scalar ``Json.fromXxx(...)`` constructors, relaxes Scala's
homogeneous ``List[T]`` / ``Map[String, T]`` checks, and requires dict
keys to be strings so they remain valid JSON object keys.

The same option is available for C# through
``CSharp.json_types.SYSTEM_TEXT_JSON_NODE``:

.. code-block:: python

   """Render C# data as a System.Text.Json.Nodes value tree."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import CSharp

   result = literalize(
       source='{"id": 1, "tags": ["red", 2]}',
       input_format=InputFormat.JSON,
       language=CSharp(json_type=CSharp.json_types.SYSTEM_TEXT_JSON_NODE),
       variable_form=NewVariable(name="payload"),
   )

This emits ``new JsonObject { ... }`` / ``new JsonArray { ... }``
expressions backed by the built-in ``System.Text.Json.Nodes`` library,
relaxes C#'s homogeneous ``Dictionary<K, V>`` / typed-array checks, and
switches date / datetime / time values to ISO 8601 strings so they
remain valid JSON.  The ``const`` modifier is rejected because the JSON
constructors and the implicit ``(JsonNode?)`` cast applied to scalars
are runtime expressions, not C# constant initializers.

Nim exposes the same option through ``Nim.json_types.JSON_NODE``:

.. code-block:: python

   """Render Nim data using the standard library JSON value type."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import Nim

   result = literalize(
       source='{"id": 1, "tags": ["red", 2]}',
       input_format=InputFormat.JSON,
       language=Nim(json_type=Nim.json_types.JSON_NODE),
       variable_form=NewVariable(name="payload"),
   )

This emits ``%*(...)`` expressions backed by Nim's standard-library
``json`` module,
relaxes Nim's homogeneous ``seq`` / ``Table`` checks, and switches date and
datetime values to ISO 8601 strings so they remain valid JSON.  ``CONST``
declarations are rejected because ``%*`` is a runtime macro and not a
constant-expression initializer.

Zig exposes the same option through ``Zig.json_types.STD_JSON_VALUE``:

.. code-block:: python

   """Render Zig data using the standard library JSON value type."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import Zig

   result = literalize(
       source='{"id": 1, "tags": ["red", 2]}',
       input_format=InputFormat.JSON,
       language=Zig(json_type=Zig.json_types.STD_JSON_VALUE),
       variable_form=NewVariable(name="payload"),
   )

This emits ``std.json.parseFromSlice(std.json.Value, allocator, "...",
.{}) catch unreachable`` expressions whose value flows through a
``std.heap.ArenaAllocator`` preamble injected into ``pub fn main()``.
The mode
relaxes Zig's homogeneous ``ZVal`` checks and folds dates, datetimes,
times, and bytes into JSON-friendly strings.  Dict keys must be
strings, and ``heterogeneous_strategy=RECORD`` is rejected because
``parseFromSlice`` rendering cannot be combined with generated
``struct`` declarations.

Custom language implementations
-------------------------------

To support a language that is not built in, create a class that satisfies
the :class:`~literalizer.Language` protocol.
Use ``metaclass=LanguageCls`` and define the required nested enum classes
and attributes:

This sketch is intentionally incomplete; a complete language defines all
of the protocol's nested enum classes and attributes.

.. code-block:: python

   """Sketch of a custom language."""

   import enum

   from literalizer._formatters.collection_openers import fixed_open
   from literalizer._formatters.format_entries import passthrough_sequence_entry
   from literalizer._language import (
       LanguageCls,
       SequenceFormatConfig,
       no_pygments_name,
   )


   class MyLanguage(metaclass=LanguageCls):
       """Sketch only; a complete language defines many more nested enums."""

       extension = ".my"
       pygments_name = no_pygments_name

       class SequenceFormats(enum.Enum):
           """Available sequence wrappers."""

           LIST = SequenceFormatConfig(
               sequence_open=fixed_open(open_str="["),
               close="]",
               supports_heterogeneity=True,
               single_element_trailing_comma=False,
               supports_trailing_comma=True,
               empty_sequence="[]",
               preamble_lines=(),
               format_entry=passthrough_sequence_entry,
               typed_opener_fallback=None,
               uses_typed_literal_for_scalars=False,
               requires_uniform_record_shapes=False,
               declared_type=None,
               narrowed_empty_form=None,
           )

       sequence_formats = SequenceFormats

       # ... define the remaining required enums and attributes ...


   list_member = MyLanguage.sequence_formats.LIST
   assert list_member.name == "LIST"
   assert MyLanguage.extension == ".my"
   assert MyLanguage.pygments_name is None

When an attribute is part of the :class:`~literalizer.Language` protocol but
should resolve to ``None``, expose that value through a descriptor or property
instead of storing literal ``None`` on the class.  CPython treats class-level
``None`` as "attribute is not implemented" during runtime protocol checks,
which can prevent ABC cache warming for large ``@runtime_checkable`` protocols;
see `python/cpython#102433 <https://github.com/python/cpython/issues/102433>`__.
Built-in languages use shared descriptors such as ``no_pygments_name`` and
``no_format_integer_widened`` for this pattern.

Look at any built-in language module under ``literalizer/languages/`` for a
complete working example.
The :class:`~literalizer.Language` protocol documents every required
attribute.

Built-in languages
------------------

.. automodule:: literalizer.languages
   :members:
   :undoc-members:
