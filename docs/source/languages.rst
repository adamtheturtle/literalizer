.. _languages:

Languages
=========

Every target language is a class in :mod:`literalizer.languages`.
You import the class, optionally configure it, and pass an instance to :func:`~literalizer.literalize`.

Selecting a language
--------------------

Each language class lives in :mod:`literalizer.languages` and is listed in :data:`~literalizer.languages.ALL_LANGUAGES`.
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

Language classes define nested :class:`~enum.Enum` classes that control how each data type is rendered.
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

Access a language's enum members through the class itself, e.g. ``Go.sequence_formats.SLICE`` for Go slices or ``Go.date_formats.GO`` for the ``time.Date(...)`` constructor.

Each ``__init__`` parameter has a sensible default, so you only need to specify the options you want to change.

Float emission scope
--------------------

|project| emits a syntactically valid source literal for any finite IEEE 754 ``double`` the target language accepts.
Scientific-notation output always uses a dotted mantissa (``1.0e+16`` rather than ``1e+16``) so the result parses as a float in languages whose grammars reject a bare integer mantissa (Ada, Cobol, Elixir, Erlang, Gleam, Nix, YAML).
Gleam additionally strips the ``+`` from positive exponents because its parser rejects the explicit sign; other languages keep the ``+`` because YAML's resolver regex requires it to recognize the literal as a float.

Whether a round-trip through a *target ecosystem's* JSON encoder preserves edge values such as ``DBL_MAX`` is governed by that ecosystem's encoder (precision, integer-vs-float rendering, ``Inf`` coercion) and is out of scope for the formatter.
Special floats (``inf`` / ``nan``) follow each language's ``supports_special_floats`` policy; targets that have no expression for them (e.g. Gleam's Erlang target) raise :class:`~literalizer.exceptions.UnrepresentableSpecialFloatError`.

Heterogeneous values
--------------------

When the input data mixes value types that the target language's natural collection type cannot hold, a ``heterogeneous_strategy`` constructor argument controls the outcome.
Every language defaults to ``ERROR``; some expose richer strategies such as ``TAGGED_ENUM`` or ``RECORD``.
See :ref:`heterogeneous-strategies` for the strategies, worked examples, and the per-language support matrix.

.. _json-value-types:

JSON value types
----------------

Some languages also have a single runtime JSON value type that is a better fit than native narrow collection types.
These languages support this through the ``json_type`` constructor argument, accessed as ``<Language>.json_types.<VALUE>``.

.. seealso::

   :ref:`heterogeneous-strategies` for the statically typed alternative, and its "Which should I use?" note comparing the two approaches.

Rust is the worked example:

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

This emits ``serde_json::json!(...)`` expressions, relaxes Rust's homogeneous ``Vec<T>`` / ``HashMap<K, V>`` checks, and requires dict keys to be strings so they remain valid JSON object keys.

Every mode requires dict keys to be strings for the same reason.
The remaining languages differ only in the emitted form and a few extra constraints:

.. list-table::
   :header-rows: 1
   :widths: 12 22 30 36

   * - Language
     - ``json_type`` value
     - Emitted form
     - Notable constraints
   * - Crystal
     - ``JSON_ANY``
     - ``JSON.parse(%(...))`` yielding ``JSON::Any``
     - Rejects characters that break the ``%(...)`` literal (``\``, ``"``, ``(``, ``)``, ``#{``); rejects integers overflowing signed 64-bit.
   * - Java
     - ``JACKSON_JSON_NODE``
     - ``new ObjectMapper().readTree("...")`` yielding ``JsonNode``
     - ``RECORD`` ``heterogeneous_strategy`` rejected.
   * - Kotlin
     - ``KOTLINX_JSON_ELEMENT``
     - ``Json.parseToJsonElement("...")`` yielding ``JsonElement``
     - ``RECORD`` and ``TUPLE`` ``heterogeneous_strategy`` options rejected.
   * - Scala
     - ``CIRCE``
     - ``Json.obj(...)`` / ``Json.arr(...)`` with ``Json.fromXxx(...)`` scalars yielding ``io.circe.Json``
     - None beyond string keys.
   * - C#
     - ``SYSTEM_TEXT_JSON_NODE``
     - ``new JsonObject { ... }`` / ``new JsonArray { ... }`` backed by ``System.Text.Json.Nodes``
     - Dates / datetimes / times become ISO 8601 strings; the ``const`` modifier is rejected (the constructors are runtime expressions).
   * - F#
     - ``SYSTEM_TEXT_JSON_NODE``
     - ``JsonObject(dict [ ... ])`` / ``JsonArray([| ... |])`` with ``JsonValue.Create(...)`` scalars
     - Dates / datetimes / times become ISO 8601 strings unless ``datetime_format`` is ``EPOCH``.
   * - Nim
     - ``JSON_NODE``
     - ``%*(...)`` backed by the standard-library ``json`` module
     - Dates / datetimes become ISO 8601 strings; ``CONST`` is rejected (``%*`` is a runtime macro).
   * - Haskell
     - ``AESON_VALUE``
     - ``[aesonQQ| ... |]`` quasi-quote yielding ``Data.Aeson.Value``
     - None beyond string keys.
   * - Zig
     - ``STD_JSON_VALUE``
     - ``std.json.parseFromSlice(std.json.Value, allocator, "...", .{}) catch unreachable`` with an injected ``std.heap.ArenaAllocator`` preamble
     - Dates / datetimes / times / bytes fold into strings; ``RECORD`` is rejected.
   * - C++
     - ``NLOHMANN_JSON``
     - ``nlohmann::json::parse(R"json(...)json")`` plus an ``#include <nlohmann/json.hpp>`` preamble line
     - Input must not encode the raw-string terminator ``)json"``.
   * - Gleam
     - ``GLEAM_JSON_JSON``
     - ``json.int`` / ``json.string`` / ``json.preprocessed_array`` / ``json.object`` builders yielding ``gleam/json.Json``
     - Adds an ``import gleam/json`` line and drops the ``GVal`` ADT; non-finite floats rejected (the Erlang target cannot express them).
   * - Elm
     - ``JSON_ENCODE_VALUE``
     - ``Json.Encode.int`` / ``string`` / ``list identity`` / ``object`` calls yielding ``Json.Encode.Value``
     - Adds an ``import Json.Encode`` line in place of the per-fixture ``Val`` ADT.
   * - PureScript
     - ``ARGONAUT_JSON``
     - ``fromRight jsonNull (jsonParser "...")`` yielding ``Data.Argonaut.Core.Json``
     - Special floats (``NaN``, ``+Infinity``, ``-Infinity``) rejected.
   * - Scheme
     - ``GUILE_JSON``
     - Association lists ``(list (cons "k" v) ...)``, vectors ``(vector v ...)``, and the symbol ``'null``, ready for ``scm->json``
     - Resolves the default mode's object/array ambiguity; special floats (``NaN``, ``+inf.0``, ``-inf.0``) rejected.
   * - Erlang
     - ``OTP_JSON``
     - UTF-8 binary literals (``<<"..."/utf8>>``) for the built-in ``json`` module; null as the atom ``null``; sets as JSON arrays
     - Requires the ``OTP_27`` built-in ``json:encode/1``.
   * - Odin
     - ``JSON_VALUE``
     - JSON text parsed at runtime by a package-scope ``_json_parse`` helper (over ``core:encoding/json.parse_string``) yielding ``json.Value``
     - Dates / datetimes / times / bytes fold into strings; ``RECORD`` is rejected.
   * - C
     - ``CJSON``
     - A ``cJSON_Create*(...)`` node tree composed with ``cJSON_AddItemToObject`` / ``cJSON_AddItemToArray`` plus an ``#include <cjson/cJSON.h>`` preamble, yielding ``cJSON *``
     - Integers render through ``cJSON_CreateNumber((double)...)`` (``cJSON`` has no integer node); ``RECORD`` is rejected.
   * - Cobol
     - ``CJSON``
     - The same ``cJSON_Create*`` tree built through GnuCOBOL's C ``CALL`` interface across the ``WORKING-STORAGE`` and ``PROCEDURE`` divisions, yielding ``cJSON *``
     - Integers are stored in a ``COMP-2`` (C ``double``) item; values beyond COBOL's widest integer are rejected.

Two cases are unusual enough to keep as prose.

OCaml's ``YOJSON_SAFE_T`` mode emits ``Yojson.Safe.t`` polymorphic-variant literals directly, keyed by the standard ``yojson`` tag set (``Bool``, ``Int``, ``Float``, ``String``, ``Null``, ``List``, ``Assoc``, ``Intlit``), so the rendered binding has the static type ``Yojson.Safe.t`` instead of OCaml's generated ``val_t`` algebraic type, and the ``type val_t = ...`` preamble drops out entirely:

.. code-block:: ocaml

   let payload : Yojson.Safe.t = `Assoc [
       ("id", `Int 1);
       ("tags", `List [`String "red"; `Int 2])
   ]

Dates, datetimes, times, and bytes fold into JSON-friendly strings; integers that exceed OCaml's native ``int`` range route through the ``Intlit`` arbitrary-precision escape hatch (a string-tagged JSON number) instead of raising.

D's polarity is reversed from the others: its default already renders every value through ``std.json.JSONValue``, so the ``json_type`` constructor argument selects the inverse mode.
``D.json_types.STD_JSON_VALUE`` is the default and matches the other languages' opt-in JSON value rendering; passing ``json_type=None`` instead activates a narrow-typed mode that mirrors the typed-collection defaults the other languages provide:

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

This emits raw D scalars, ``T[]`` array literals, and ``V[K]`` associative-array literals (``auto counts = ["a": 1, "b": 2];``) without the ``JSONValue`` wrapper.
Inputs that have no narrow form, a heterogeneous list, a heterogeneous-valued dict, an empty list or dict (D's ``auto`` cannot infer an element type for an empty literal), a set, an ordered map, or a non-record dict, are rejected with :class:`~literalizer.exceptions.UnrepresentableInputError`.
The ``RECORD`` ``heterogeneous_strategy`` is also rejected because it already renders record-shaped dicts as generated ``struct`` literals, which conflicts with narrow mode's associative-array form.

Empty mappings on Ada, Lua, PHP, and R
--------------------------------------

Ada, Lua, PHP, and R all have a runtime representation that cannot distinguish an empty mapping from an empty sequence.
Lua's table, PHP's array, and R's ``list()`` each serialize an empty mapping the same way their JSON encoders serialize an empty sequence (typically ``[]``).
The Ada literalizer's unified ``A_Val`` aggregate likewise collapses an empty ``AMap'[]`` and an empty ``AList'[]`` to the same runtime value, so the mapping/sequence distinction is lost on round-trip.
``literalize`` refuses to emit a literal that cannot round-trip and raises :class:`~literalizer.exceptions.UnrepresentableEmptyDictError` on those four languages whenever an empty mapping appears at any depth in the input.
Empty sequences are unambiguous and are still accepted.

.. code-block:: python

   """Ada, Lua, PHP, and R reject empty mappings."""

   import contextlib
   import json

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.exceptions import UnrepresentableEmptyDictError
   from literalizer.languages import Lua

   # Strip or replace the empty mapping before retrying on a real input.
   with contextlib.suppress(UnrepresentableEmptyDictError):
       literalize(
           source=json.dumps(obj={"outer": {}}),
           input_format=InputFormat.JSON,
           language=Lua(),
           variable_form=NewVariable(name="my_data"),
       )

Forth visitor stream
--------------------

Forth has no native mapping or sequence type, so the Forth language does not emit a data literal.
Instead it emits a colon definition that executes a sequence of small constructor words, one per structural event in the document:

============  ===========================  =================================
Word          Stack effect                 Meaning
============  ===========================  =================================
``+obj``      ``( -- )``                   start of an object
``-obj``      ``( -- )``                   end of an object
``+arr``      ``( -- )``                   start of an array
``-arr``      ``( -- )``                   end of an array
``+key``      ``( c-addr u -- )``          a member name
``+int``      ``( n -- )``                 an integer value
``+float``    ``( F: r -- )``              a floating-point value
``+str``      ``( c-addr u -- )``          a string value
``+bool``     ``( flag -- )``              a boolean value
``+null``     ``( -- )``                   a null value
============  ===========================  =================================

For example, ``{"name": "Alice", "tags": [1, 2]}`` is literalized to:

.. code-block:: forth

   : my_data
   +obj
       s\" name" +key s\" Alice" +str
       s\" tags" +key +arr 1 +int 2 +int -arr
    -obj
   ;

The constructor words are the protocol; the caller supplies their bindings.
The Forth language ships a default binding in ``src/literalizer/languages/forth_prelude.fs`` that writes JSON to a shared output stream through the Forth Foundation Library ``jos`` module, so loading the prelude and then running ``my_data`` prints the document as JSON out of the box:

.. code-block:: forth

   include forth_prelude.fs
   \ ... the literalized : my_data ... ; definition ...
   my_data json-out str-get type

To consume the same definition another way -- to build a Forth-side data structure, walk into custom storage, compute over the values, or emit a different format -- redefine any of the constructor words before running the definition.
Nothing in the definition is tied to JSON beyond the bindings the caller chooses to load.

Custom language implementations
-------------------------------

To support a language that is not built in, create a class that satisfies the :class:`~literalizer.Language` protocol, using ``metaclass=LanguageCls`` and defining the required nested enum classes and attributes.

When an attribute is part of the :class:`~literalizer.Language` protocol but should resolve to ``None``, expose that value through a descriptor or property instead of storing literal ``None`` on the class.
CPython treats class-level ``None`` as "attribute is not implemented" during runtime protocol checks, which can prevent ABC cache warming for large ``@runtime_checkable`` protocols; see `python/cpython#102433 <https://github.com/python/cpython/issues/102433>`__.
Built-in languages use shared descriptors such as ``no_pygments_name`` and ``no_format_integer_widened`` for this pattern.

Look at any built-in language module under ``literalizer/languages/`` for a complete working example.
The :class:`~literalizer.Language` protocol documents every required attribute.

Language-definition API
-----------------------

.. currentmodule:: literalizer

These symbols are only needed when defining a language that is not built in.
Everything here is importable directly from the top-level ``literalizer`` package.

Formatting configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

Building blocks used when defining how a language renders collections, comments and scalars.

.. autoclass:: CollectionLayout
   :members:
   :undoc-members:

.. autoclass:: TrailingCommaConfig
   :members:
   :undoc-members:

.. autoclass:: CommentConfig
   :members:
   :undoc-members:

.. autoclass:: SequenceFormatConfig
   :members:
   :undoc-members:

.. autoclass:: SetFormatConfig
   :members:
   :undoc-members:

.. autoclass:: DictFormatConfig
   :members:
   :undoc-members:

.. autoclass:: OrderedMapFormatConfig
   :members:
   :undoc-members:

.. autoclass:: DateFormatConfig
   :members:
   :undoc-members:

.. autoclass:: DatetimeFormatConfig
   :members:
   :undoc-members:

.. autofunction:: fixed_open

Defining a language
~~~~~~~~~~~~~~~~~~~~

The :class:`Language` protocol describes how a language formats literals.
The members below are the contract each built-in language implements.

.. autoclass:: Language
   :members:

.. autoclass:: LanguageCls
   :members:

Built-in languages
------------------

.. automodule:: literalizer.languages
   :members:
   :undoc-members:
