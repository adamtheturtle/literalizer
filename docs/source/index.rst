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

Use :func:`literalizer.literalize` to convert data to native language literals:

.. code-block:: python

   """Example of using literalizer."""

   from literalizer import InputFormat, literalize
   from literalizer.languages import Go

   # YAML comments are preserved using the target language's comment syntax
   yaml_config = """\
   # Server configuration
   host: localhost  # default host
   port: 8080
   # Enable debug mode for development
   debug: true
   """
   result = literalize(  # returns LiteralizeResult with .code and .preamble
       source=yaml_config,
       input_format=InputFormat.YAML,
       language=Go(
           date_format=Go.date_formats.GO,
           datetime_format=Go.datetime_formats.GO,
           bytes_format=Go.bytes_formats.HEX,
           sequence_format=Go.sequence_formats.SLICE,
       ),
       pre_indent_level=0,
       include_delimiters=True,
       variable_form=None,
   )
   # result.code:
   # map[string]any{
   #     // Server configuration
   #     "host": "localhost",  // default host
   #     "port": 8080,
   #     // Enable debug mode for development
   #     "debug": true,
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
   release-process
   changelog
   contributing
