|Build Status| |PyPI| |CodSpeed|

literalizer
===========

``literalizer`` converts JSON, JSON5, YAML, and TOML data structures to native language literal syntax.

.. contents::
   :local:

Supported languages
-------------------

Ada, Bash, C, C#, C++, Clojure, COBOL, Common Lisp, Crystal, D, Dart, Dhall,
Elixir, Elm, Erlang, F#, Fortran, Gleam, Go, Groovy, Haskell, HCL, Java,
JavaScript, JSON5, Jsonnet, Julia, Kotlin, Lua, MATLAB, Mojo, Nim, Norg,
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
   result = literalize(
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
