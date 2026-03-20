|Build Status| |PyPI|

literalizer
===========

``literalizer`` converts JSON data structures to native language literal syntax.

.. contents::
   :local:

Supported languages
-------------------

Ada, Bash, C, C#, C++, Clojure, COBOL, Common Lisp, Crystal, D, Dart, Elixir,
Erlang, F#, Go, Groovy, Haskell, HCL, Java, JavaScript, Julia, Kotlin, Lua,
MATLAB, Mojo, Nim, Norg, OCaml, Occam-pi, Perl, PHP, PowerShell, Python, R, Racket,
Ruby, Rust, Scala, Swift, TOML, TypeScript, Visual Basic, Zig.

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
   from literalizer.languages import Go

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
       error_on_coercion=False,
       language=Go(
           date_format=Go.DateFormat.ISO,
           datetime_format=Go.DatetimeFormat.ISO,
           sequence_format=Go.SequenceFormat.SLICE,
       ),
       line_prefix="",
       indent="    ",
       wrap=True,
       variable_name=None,
       new_variable=True,
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
* Generate multi-language request/response examples for JSON API docs (see `guide <https://adamtheturtle.github.io/literalizer/json-api-use-case.html>`__).
* Create type-safe literal data from JSON config files.

Full documentation
------------------

See the `full documentation <https://adamtheturtle.github.io/literalizer/>`__ for more information including how to contribute.

.. |Build Status| image:: https://github.com/adamtheturtle/literalizer/actions/workflows/ci.yml/badge.svg?branch=main
   :target: https://github.com/adamtheturtle/literalizer/actions
.. |PyPI| image:: https://badge.fury.io/py/literalizer.svg
   :target: https://badge.fury.io/py/literalizer
.. |minimum-python-version| replace:: 3.12
