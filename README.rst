|Build Status| |PyPI|

literalizer
===========

``literalizer`` converts JSON data structures to native language literal syntax (Python, JavaScript, TypeScript, Go, Ruby, C#, C++, Java, Kotlin).

.. contents::
   :local:

Installation
------------

Requires Python |minimum-python-version|\+.

.. code-block:: sh

   pip install literalizer


Usage examples
--------------

.. code-block:: python

   """Examples of using literalizer."""

   from literalizer import convert_json_to_native_literal

   # Convert a JSON array to Python tuple literal
   data = [True, None, "hi", [1, 2]]
   result = convert_json_to_native_literal(
       data=data,
       language="py",
       prefix="",
       wrap=False,
   )
   # result: '(True, None, "hi", (1, 2)),'

   # Convert to JavaScript/TypeScript array
   result = convert_json_to_native_literal(
       data=data,
       language="js",
       prefix="    ",
       wrap=True,
   )
   # result:
   # [
   #     true,
   #     null,
   #     "hi",
   #     [1, 2],
   # ]

   # Supported languages: py, js, ts, go, rb, cs, cpp, java, kt

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
