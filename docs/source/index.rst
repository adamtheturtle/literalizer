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
       format_date_iso,
       format_date_java,
       format_date_python,
       format_datetime_iso,
       format_datetime_java_instant,
       format_datetime_python,
       format_datetime_ruby,
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

   # YAML comments are preserved using the target language's comment syntax
   yaml_with_comments = """\
   # Server configuration
   host: localhost  # default host
   port: 8080
   # Enable debug mode for development
   debug: true
   """
   result = literalize_yaml(
       yaml_string=yaml_with_comments,
       language=PYTHON,
       prefix="    ",
       wrap=True,
   )
   # result:
   # {
   #     # Server configuration
   #     "host": "localhost",  # default host
   #     "port": 8080,
   #     # Enable debug mode for development
   #     "debug": True,
   # }

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
       set_open="[",
       set_close="]",
       empty_set=None,
       format_set_entry=None,
       comment_prefix="//",
   )

   # Customize date/datetime formatting with built-in formatters:
   # Use Python-native date objects instead of ISO strings (via YAML)
   python_with_dates = LanguageSpec(
       null_literal="None",
       true_literal="True",
       false_literal="False",
       collection_open="(",
       collection_close=")",
       dict_separator=": ",
       dict_open="{",
       dict_close="}",
       format_dict_entry=None,
       trailing_comma=True,
       single_element_trailing_comma=False,
       format_date=format_date_python,
       format_datetime=format_datetime_python,
       empty_collection=None,
       set_open="{",
       set_close="}",
       empty_set="set()",
       format_set_entry=None,
       comment_prefix="#",
   )
   result = literalize_yaml(
       yaml_string="- 2024-01-15\n",
       language=python_with_dates,
       prefix="",
       wrap=False,
   )
   # result: datetime.date(2024, 1, 15),

   # Use Java Instant and LocalDate
   java_with_dates = LanguageSpec(
       null_literal="null",
       true_literal="true",
       false_literal="false",
       collection_open="{",
       collection_close="}",
       dict_separator=": ",
       dict_open="{",
       dict_close="}",
       format_dict_entry=None,
       trailing_comma=True,
       single_element_trailing_comma=False,
       format_date=format_date_java,
       format_datetime=format_datetime_java_instant,
       empty_collection=None,
       set_open="Set.of(",
       set_close=")",
       empty_set=None,
       format_set_entry=None,
       comment_prefix="//",
   )
   result = literalize_yaml(
       yaml_string="- 2024-01-15\n",
       language=java_with_dates,
       prefix="",
       wrap=False,
   )
   # result: LocalDate.of(2024, 1, 15),

   # Use Ruby Time objects
   ruby_with_dates = LanguageSpec(
       null_literal="nil",
       true_literal="true",
       false_literal="false",
       collection_open="[",
       collection_close="]",
       dict_separator=" => ",
       dict_open="{",
       dict_close="}",
       format_dict_entry=None,
       trailing_comma=True,
       single_element_trailing_comma=False,
       format_date=format_date_iso,
       format_datetime=format_datetime_ruby,
       empty_collection=None,
       set_open="Set.new([",
       set_close="])",
       empty_set="Set.new",
       format_set_entry=None,
       comment_prefix="#",
   )
   result = literalize_yaml(
       yaml_string="- 2024-01-15T12:30:00\n",
       language=ruby_with_dates,
       prefix="",
       wrap=False,
   )
   # result: Time.new(2024, 1, 15, 12, 30, 0),

   # Available formatters:
   # format_date_iso / format_datetime_iso (default — ISO 8601 strings)
   # format_date_python / format_datetime_python
   # format_date_java / format_datetime_java_instant / format_datetime_java_zoned
   # format_date_ruby / format_datetime_ruby
   # format_date_js / format_datetime_js
   # format_date_csharp / format_datetime_csharp
   # format_date_go / format_datetime_go
   # format_date_kotlin / format_datetime_kotlin
   # format_date_cpp / format_datetime_cpp
   # format_datetime_epoch (Unix timestamp)

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
