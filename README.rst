|Build Status| |PyPI|

literalizer
===========

``literalizer`` converts JSON data structures to native language literal syntax (Python, JavaScript, TypeScript, Go, Ruby, C#, C++, Java, Kotlin, Rust, Haskell, Swift, PHP).

.. contents::
   :local:

Installation
------------

Requires Python |minimum-python-version|\+.

.. code-block:: sh

   pip install literalizer


Usage
-----

.. code-block:: python

   """Example of using literalizer."""

   from literalizer import literalize_yaml
   from literalizer.languages import GO

   # YAML comments are preserved using the target language's comment syntax
   yaml_config = """\
   # Server configuration
   host: localhost  # default host
   port: 8080
   # Enable debug mode for development
   debug: true
   """
   result = literalize_yaml(
       yaml_string=yaml_config,
       language=GO,
       prefix="    ",
       wrap=True,
   )
   # result:
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

Full documentation
------------------

See the `full documentation <https://adamtheturtle.github.io/literalizer/>`__ for more information including how to contribute.

.. |Build Status| image:: https://github.com/adamtheturtle/literalizer/actions/workflows/ci.yml/badge.svg?branch=main
   :target: https://github.com/adamtheturtle/literalizer/actions
.. |PyPI| image:: https://badge.fury.io/py/literalizer.svg
   :target: https://badge.fury.io/py/literalizer
.. |minimum-python-version| replace:: 3.12
