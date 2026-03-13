|project|
=========

|project| converts JSON data structures to native language literal syntax
(Python, JavaScript, TypeScript, Go, Ruby, C#, C++, Java, Kotlin).

Installation
------------

Requires Python |minimum-python-version|\+.

.. code-block:: shell

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

   # Convert to JavaScript/TypeScript with wrapping
   result = convert_json_to_native_literal(
       data=data,
       language="js",
       prefix="    ",
       wrap=True,
   )

   # Supported languages: py, js, ts, go, rb, cs, cpp, java, kt

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
