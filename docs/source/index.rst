|project|
=========

|project| converts JSON data structures to native language literal syntax.

Supported languages
-------------------

Ada, Bash, C, C#, C++, Clojure, Crystal, D, Dart, Elixir, Erlang, F#, Go,
Groovy, Haskell, Java, JavaScript, Julia, Kotlin, Lua, MATLAB, Nim, OCaml,
Occam-pi, Perl, PHP, PowerShell, Python, R, Ruby, Rust, Scala, Swift,
TypeScript, Zig.

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
   result = literalize_yaml(
       yaml_string=yaml_config,
       language=Go(),
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

Reference
---------

.. toctree::
   :maxdepth: 3

   api-reference
   release-process
   changelog
   contributing
