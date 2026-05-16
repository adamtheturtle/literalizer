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
   from literalizer._language import LanguageCls, SequenceFormatConfig


   class MyLanguage(metaclass=LanguageCls):
       """Sketch only; a complete language defines many more nested enums."""

       extension = ".my"
       pygments_name = None

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

Look at any built-in language module under ``literalizer/languages/`` for a
complete working example.
The :class:`~literalizer.Language` protocol documents every required
attribute.

Built-in languages
------------------

.. automodule:: literalizer.languages
   :members:
   :undoc-members:
