|Build Status| |PyPI| |CodSpeed|

literalizer
===========

``literalizer`` converts JSON, JSON5, YAML, and TOML data structures to native language literal syntax.

.. contents::
   :local:

Supported languages
-------------------

Ada, Bash, C, C#, C++, Clojure, COBOL, Common Lisp, Crystal, D, Dart, Dhall,
Elixir, Elm, Erlang, F#, Fortran, Gleam, Go, Groovy, Haskell, Haxe, HCL,
Java, JavaScript, JSON5, Jsonnet, Julia, Kotlin, Lua, MATLAB, Mojo, Nim, Norg,
Objective-C, OCaml, Occam-pi, Odin, Perl, PHP, PowerShell, PureScript, Python,
R, Racket, Raku, Roc, Ruby, Rust, Scala, Scheme, Swift, SystemVerilog, TOML,
TypeScript, Visual Basic, YAML, Zig.

Installation
------------

Requires Python |minimum-python-version|\+.

.. code-block:: sh

   pip install literalizer


Usage
-----

Pass your data, its format, and a target language:

.. code-block:: python

   """Minimal example of using literalizer."""

   from literalizer import InputFormat, literalize
   from literalizer.languages import Python

   result = literalize(
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
* Generate multi-language request/response examples for API docs (see `guide <https://adamtheturtle.github.io/literalizer/json-api-use-case.html>`__).
* Generate multi-language function call examples from data (see `guide <https://adamtheturtle.github.io/literalizer/function-call-use-case.html>`__).
* Create type-safe literal data from JSON, JSON5, YAML, or TOML config files.

CLI
---

A command-line interface is available at `literalizer-cli <https://github.com/adamtheturtle/literalizer-cli>`__.

Full documentation
------------------

See the `full documentation <https://adamtheturtle.github.io/literalizer/>`__ for more information including how to contribute.

.. |Build Status| image:: https://github.com/adamtheturtle/literalizer/actions/workflows/ci.yml/badge.svg?branch=main
   :target: https://github.com/adamtheturtle/literalizer/actions
.. |PyPI| image:: https://badge.fury.io/py/literalizer.svg
   :target: https://badge.fury.io/py/literalizer
.. |CodSpeed| image:: https://img.shields.io/endpoint?url=https://codspeed.io/badge.json
   :target: https://codspeed.io/adamtheturtle/literalizer?utm_source=badge
.. |minimum-python-version| replace:: 3.12
