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

   from literalizer import (
       JAVA,
       JAVASCRIPT,
       PYTHON,
       LanguageSpec,
       format_date_iso,
       format_datetime_iso,
       literalize_json,
       literalize_yaml,
   )

   # Convert a JSON array to Java literal items
   result = literalize_json(
       json_string='[true, null, "hi", [1, 2]]',
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
   result = literalize_json(
       json_string='[true, null, "hi", [1, 2]]',
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

   # Convert a JSON string to Python
   result = literalize_json(
       json_string='[true, null, "hi", [1, 2]]',
       language=PYTHON,
       prefix="",
       wrap=True,
   )
   # result:
   # (
   #     True,
   #     None,
   #     "hi",
   #     (1, 2),
   # )

   # Convert from a YAML string directly
   result = literalize_yaml(
       yaml_string="- true\n- null\n- hi\n- [1, 2]",
       language=PYTHON,
       prefix="",
       wrap=True,
   )
   # result:
   # (
   #     True,
   #     None,
   #     "hi",
   #     (1, 2),
   # )

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
       dict_open="{",
       dict_close="}",
       format_dict_entry=None,
       trailing_comma=True,
       single_element_trailing_comma=False,
       format_date=format_date_iso,
       format_datetime=format_datetime_iso,
       empty_collection=None,
       empty_dict=None,
       set_open="[",
       set_close="]",
       empty_set=None,
       format_set_entry=None,
       comment_prefix="//",
   )

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
