|project|
=========

|project| converts JSON, JSON5, YAML, and TOML data structures to native language literal syntax.

Supported languages
-------------------

See :ref:`languages` for the full list with per-language options.

Installation
------------

Requires Python |minimum-python-version|\+.

.. code-block:: shell

   pip install literalizer


Usage
-----

Use :func:`literalizer.literalize` to convert data to native language literals.
Pass your data, its format, and a target language:

.. code-block:: python

   """Minimal example of using literalizer."""

   from literalizer import InputFormat, literalize
   from literalizer.languages import Python

   result = literalize(  # returns LiteralizeResult with .code and .preamble
       source='{"x": 1}',
       input_format=InputFormat.JSON,
       language=Python(),
   )
   # result.code:
   # {
   #     "x": 1,
   # }

Configure the language to control how individual data types are rendered.
Comments in the source are preserved using the target language's comment syntax:

.. code-block:: python

   """Layering format options on top of the minimal call."""

   from literalizer import InputFormat, literalize
   from literalizer.languages import Go

   yaml_config = """\
   # Server configuration
   host: localhost  # default host
   port: 8080
   released: 2026-06-02
   """
   result = literalize(
       source=yaml_config,
       input_format=InputFormat.YAML,
       language=Go(date_format=Go.date_formats.ISO),
   )
   # result.code:
   # map[string]any{
   #     // Server configuration
   #     "host": "localhost",  // default host
   #     "port": 8080,
   #     "released": "2026-06-02",
   # }

TOML is read the same way, and its comments are preserved too:

.. code-block:: python

   """Reading TOML, with comments preserved."""

   from literalizer import InputFormat, literalize
   from literalizer.languages import Python

   toml_config = """\
   # Server configuration
   host = "localhost"  # default host
   port = 8080
   """
   result = literalize(
       source=toml_config,
       input_format=InputFormat.TOML,
       language=Python(),
   )
   # result.code:
   # {
   #     # Server configuration
   #     "host": "localhost",  # default host
   #     "port": 8080,
   # }

JSON5 is also accepted. Its relaxed syntax, such as comments, single-quoted
strings, trailing commas, and hexadecimal numbers, is converted to the target
language:

.. code-block:: python

   """Reading JSON5's relaxed syntax."""

   from literalizer import InputFormat, literalize
   from literalizer.languages import Python

   json5_config = """\
   {
     // Relaxed syntax is accepted here.
     name: 'literalizer',
     port: 0x1F90,
   }"""
   result = literalize(
       source=json5_config,
       input_format=InputFormat.JSON5,
       language=Python(),
   )
   # result.code:
   # {
   #     "name": "literalizer",
   #     "port": 8080,
   # }

Use cases
---------

* Generate test fixtures from JSON, JSON5, YAML, or TOML samples.
* Convert API responses to language-native data structures for documentation.
* Generate multi-language function call examples from data — see :doc:`function-call-use-case`.
* Create type-safe literal data from JSON, JSON5, YAML, or TOML config files.

CLI
---

A command-line interface is available at `literalizer-cli <https://github.com/adamtheturtle/literalizer-cli>`__.

Reference
---------

.. toctree::
   :maxdepth: 3

   json-api-use-case
   function-call-use-case
   api-reference
   languages
   heterogeneous-strategies
   common-errors
   release-process
   unreleased
   changelog
   contributing
