|project|
=========

|project| converts JSON data structures to native language literal syntax.

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

.. code-block:: python

   """Example of using literalizer."""

   from literalizer import literalize_yaml
   from literalizer.languages import Go

   # YAML comments are preserved using the target language's comment syntax
   yaml_config = """\
   # Server configuration
   host: localhost  # default host
   port: 8080
   # Enable debug mode for development
   debug: true
   """
   result = literalize_yaml(  # returns LiteralizeResult with .code and .preamble
       yaml_string=yaml_config,
       error_on_coercion=False,
       language=Go(
           date_format=Go.date_formats.GO,
           datetime_format=Go.datetime_formats.GO,
           bytes_format=Go.bytes_formats.HEX,
           sequence_format=Go.sequence_formats.SLICE,
       ),
       line_prefix="",
       include_delimiters=True,
       variable_name=None,
       new_variable=True,
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

* Generate test fixtures from JSON samples.
* Convert API responses to language-native data structures for documentation.
* Create type-safe literal data from JSON config files.

CLI
---

A command-line interface is available at `literalizer-cli <https://github.com/adamtheturtle/literalizer-cli>`__.

Reference
---------

.. toctree::
   :maxdepth: 3

   json-api-use-case
   api-reference
   languages
   release-process
   changelog
   contributing
