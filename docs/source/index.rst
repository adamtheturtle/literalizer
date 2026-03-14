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

   from literalizer import (
       JAVA,
       JAVASCRIPT,
       PYTHON,
       LanguageSpec,
       literalize,
       literalize_json,
       literalize_yaml,
   )

   # Convert a Python list to Java literal items
   data = [True, None, "hi", [1, 2]]
   result = literalize(
       data=data,
       language=JAVA,
       prefix="",
       wrap=False,
   )
   # result:
   # true,
   # null,
   # "hi",
   # {1, 2},

   # Convert to JavaScript/TypeScript array
   result = literalize(
       data=data,
       language=JAVASCRIPT,
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

   # Convert from a JSON string directly
   result = literalize_json(
       json_string='[true, null, "hi", [1, 2]]',
       language=PYTHON,
       prefix="",
       wrap=True,
   )
   # result:
   # [
   #     True,
   #     None,
   #     "hi",
   #     (1, 2),
   # ]

   # Convert from a YAML string directly
   result = literalize_yaml(
       yaml_string="- true\n- null\n- hi\n- [1, 2]",
       language=PYTHON,
       prefix="",
       wrap=True,
   )
   # result:
   # [
   #     True,
   #     None,
   #     "hi",
   #     (1, 2),
   # ]

   # Built-in languages: PYTHON, JAVASCRIPT, TYPESCRIPT, GO, RUBY,
   #                      CSHARP, CPP, JAVA, KOTLIN

   # Create a custom language:
   custom = LanguageSpec(
       null_literal="nil",
       true_literal="TRUE",
       false_literal="FALSE",
       collection_open="[",
       collection_close="]",
       dict_separator=": ",
   )

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
