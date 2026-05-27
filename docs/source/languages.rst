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
fit than native narrow collection types.  Rust, Crystal, Java, Kotlin,
Scala, C#, F#, Nim, Haskell, Zig, C++, OCaml, Elm, and D support this through the
``json_type`` constructor argument (D's polarity is reversed; see below):

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

Kotlin exposes the same option through the ``JsonElement`` type from
``kotlinx.serialization.json``:

.. code-block:: python

   """Render Kotlin data as a JsonElement."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import Kotlin

   result = literalize(
       source='{"id": 1, "tags": ["red", 2]}',
       input_format=InputFormat.JSON,
       language=Kotlin(json_type=Kotlin.json_types.KOTLINX_JSON_ELEMENT),
       variable_form=NewVariable(name="payload"),
   )

This emits ``Json.parseToJsonElement("...")`` so the rendered binding
has the static type ``kotlinx.serialization.json.JsonElement`` and can
hold the heterogeneous values that Kotlin's narrow ``List`` / ``Map``
types reject.  Dict keys must be strings, and the ``RECORD`` and
``TUPLE`` ``heterogeneous_strategy`` options are rejected because the
two rendering modes cannot be combined.

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

F# exposes the same option through
``FSharp.json_types.SYSTEM_TEXT_JSON_NODE``:

.. code-block:: python

   """Render F# data as a System.Text.Json.Nodes value tree."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import FSharp

   result = literalize(
       source='{"id": 1, "tags": ["red", 2]}',
       input_format=InputFormat.JSON,
       language=FSharp(json_type=FSharp.json_types.SYSTEM_TEXT_JSON_NODE),
       variable_form=NewVariable(name="payload"),
   )

This emits ``JsonObject(dict [ ... ])`` / ``JsonArray([| ... |])``
expressions wrapping per-scalar ``JsonValue.Create(...)`` constructors,
widened to ``JsonNode`` so heterogeneous children type-infer uniformly.
The mode opens ``System.Text.Json.Nodes`` inside the generated module,
relaxes F#'s homogeneous collection checks, switches dates, datetimes,
and times to ISO 8601 strings (unless ``datetime_format`` is ``EPOCH``),
and requires dict keys to be strings so they remain valid JSON object
keys.

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

Haskell exposes the same option through the ``Data.Aeson.Value``
type from the ``aeson`` package:

.. code-block:: python

   """Render Haskell data as a ``Data.Aeson.Value``."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import Haskell

   result = literalize(
       source='{"id": 1, "tags": ["red", 2]}',
       input_format=InputFormat.JSON,
       language=Haskell(json_type=Haskell.json_types.AESON_VALUE),
       variable_form=NewVariable(name="payload"),
   )

This emits an ``[aesonQQ| ... |]`` quasi-quote bracket from
``Data.Aeson.QQ``, mirroring the ``serde_json::json!`` macro on the
Rust side, so the rendered binding has the static type
``Data.Aeson.Value`` instead of Haskell's narrow custom ``Val``
algebraic type, and can hold the heterogeneous values that ``Val``'s
closed set of constructors rejects.  Dict keys must be strings so they
remain valid JSON object keys.

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

C++ exposes the same option through ``Cpp.json_types.NLOHMANN_JSON``:

.. code-block:: python

   """Render C++ data as nlohmann::json."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import Cpp

   result = literalize(
       source='{"id": 1, "tags": ["red", 2]}',
       input_format=InputFormat.JSON,
       language=Cpp(json_type=Cpp.json_types.NLOHMANN_JSON),
       variable_form=NewVariable(name="payload"),
   )

This emits ``nlohmann::json::parse(R"json(...)json")`` expressions and
adds the ``#include <nlohmann/json.hpp>`` preamble line so the rendered
binding has the static type ``nlohmann::json`` instead of C++'s narrow
``std::vector`` / ``std::map`` / ``std::unordered_map`` collection
types, and can hold the heterogeneous values that ``std::variant``
would otherwise be needed for.  Dict keys must be strings so they
remain valid JSON object keys, and the input must not encode the
raw-string terminator sequence ``)json"`` (e.g. through a dict key
ending in ``)json``).

Gleam exposes the same option through
``Gleam.json_types.GLEAM_JSON_JSON``:

.. code-block:: python

   """Render Gleam data using the gleam_json builder type."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import Gleam

   result = literalize(
       source='{"id": 1, "tags": ["red", 2]}',
       input_format=InputFormat.JSON,
       language=Gleam(json_type=Gleam.json_types.GLEAM_JSON_JSON),
       variable_form=NewVariable(name="payload"),
   )

This emits ``gleam_json`` builder calls such as ``json.int(1)``,
``json.string("red")``, ``json.preprocessed_array([...])``, and
``json.object([#("k", v), ...])`` so each binding has the static type
``gleam/json.Json``, ready to feed straight into ``json.to_string``.
An ``import gleam/json`` line is added at file scope and the generated
``GVal`` ADT is dropped.  Dict keys must be strings so they remain
valid JSON object keys, and non-finite floats are rejected because
the Erlang target has no expression that evaluates to a non-finite
float.

OCaml exposes the same option through ``OCaml.json_types.YOJSON_SAFE_T``:

.. code-block:: python

   """Render OCaml data as a ``Yojson.Safe.t`` polymorphic variant."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import OCaml

   result = literalize(
       source='{"id": 1, "tags": ["red", 2]}',
       input_format=InputFormat.JSON,
       language=OCaml(json_type=OCaml.json_types.YOJSON_SAFE_T),
       variable_form=NewVariable(name="payload"),
   )

This emits ``Yojson.Safe.t`` polymorphic-variant literals directly,
keyed by the standard ``yojson`` tag set (``Bool``, ``Int``,
``Float``, ``String``, ``Null``, ``List``, ``Assoc``, ``Intlit``), so
the rendered binding has the static type ``Yojson.Safe.t`` instead of
OCaml's generated ``val_t`` algebraic type, and the ``type val_t = ...``
preamble drops out entirely:

.. code-block:: ocaml

   let payload : Yojson.Safe.t = `Assoc [
       ("id", `Int 1);
       ("tags", `List [`String "red"; `Int 2])
   ]

Dates, datetimes, times, and bytes fold into JSON-friendly strings;
integers that exceed OCaml's native ``int`` range route through the
``Intlit`` arbitrary-precision escape hatch (a string-tagged JSON
number) instead of raising.  Dict keys must be strings so they remain
valid JSON object keys.

Elm exposes the same option through
``Elm.json_types.JSON_ENCODE_VALUE``:

.. code-block:: python

   """Render Elm data as a Json.Encode.Value."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import Elm

   result = literalize(
       source='{"id": 1, "tags": ["red", 2]}',
       input_format=InputFormat.JSON,
       language=Elm(json_type=Elm.json_types.JSON_ENCODE_VALUE),
       variable_form=NewVariable(name="payload"),
   )

This emits idiomatic ``elm/json`` ``Json.Encode.bool``,
``Json.Encode.int``, ``Json.Encode.string``,
``Json.Encode.list identity [ ... ]``, and
``Json.Encode.object [ ( "k", ... ) ]`` calls and adds an
``import Json.Encode`` line.  The rendered binding has the static type
``Json.Encode.Value`` rather than Elm's narrow per-fixture ``Val`` ADT,
so no walker is needed before ``Json.Encode.encode 0`` and
heterogeneous collections are accepted.  Dict keys must be strings so
they remain valid JSON object keys.

Erlang exposes the same option through
``Erlang.json_types.OTP_JSON``:

.. code-block:: python

   """Render Erlang data for Erlang's built-in json module."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import Erlang

   result = literalize(
       source='{"id": 1, "tags": ["red", 2]}',
       input_format=InputFormat.JSON,
       language=Erlang(json_type=Erlang.json_types.OTP_JSON),
       variable_form=NewVariable(name="payload"),
   )

This emits string values, dict keys, ISO 8601 dates / datetimes /
times, and base64-encoded bytes as UTF-8 binary literals
(``<<"..."/utf8>>``) rather than Erlang's default ``"..."`` string
form (a list of code points), since Erlang's ``json:encode/1``
(available since ``OTP_27``) rejects the list form as a map key and
emits list-form string values as arrays of integers.  Null renders
as the bare atom ``null`` (rather than ``undefined``), and sets
render as JSON arrays.  Dict keys must be strings so they remain
valid JSON object keys.

D's polarity is reversed from the others: its default already renders
every value through ``std.json.JSONValue``, so the ``json_type``
constructor argument selects the inverse mode.  ``D.json_types.STD_JSON_VALUE``
is the default and matches the other languages' opt-in JSON value
rendering; passing ``json_type=None`` instead activates a narrow-typed
mode that mirrors the typed-collection defaults the other languages
provide:

.. code-block:: python

   """Render D data through narrow native collections."""

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import D

   result = literalize(
       source='{"a": 1, "b": 2}',
       input_format=InputFormat.JSON,
       language=D(json_type=None),
       variable_form=NewVariable(name="counts"),
   )

This emits raw D scalars, ``T[]`` array literals, and ``V[K]``
associative-array literals (``auto counts = ["a": 1, "b": 2];``)
without the ``JSONValue`` wrapper.  Inputs that have no narrow form,
a heterogeneous list, a heterogeneous-valued dict, an empty list or
dict (D's ``auto`` cannot infer an element type for an empty literal),
a set, an ordered map, or a non-record dict, are rejected with
:class:`~literalizer.exceptions.UnrepresentableInputError`.  The
``RECORD`` ``heterogeneous_strategy`` is also rejected because it
already renders record-shaped dicts as generated ``struct`` literals,
which conflicts with narrow mode's associative-array form.

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
