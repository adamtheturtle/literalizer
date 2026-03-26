Multi-language API documentation
=================================

If you maintain a JSON API, your documentation probably needs to show
request and response examples in every language your callers use.
|project| generates those native-language literals from a single JSON
sample so you don't have to write them by hand.

Example
-------

Suppose your ``POST /users`` endpoint accepts this request body and
returns this response:

.. code-block:: json

   // Request body
   {"name": "Alice", "email": "alice@example.com"}

   // Response
   {"id": 42, "name": "Alice", "email": "alice@example.com", "created": true}

|project| converts these into native literals for each language:

.. code-block:: python

   """Generate per-language API examples."""

   from literalizer import literalize_json
   from literalizer.languages import Python

   request_json = '{"name": "Alice", "email": "alice@example.com"}'
   response_json = (
       '{"id": 42, "name": "Alice",'
       ' "email": "alice@example.com", "created": true}'
   )

   request_literal = literalize_json(
       json_string=request_json,
       error_on_coercion=False,
       language=Python(
           date_format=Python.date_formats.PYTHON,
           datetime_format=Python.datetime_formats.PYTHON,
           bytes_format=Python.bytes_formats.HEX,
           sequence_format=Python.sequence_formats.TUPLE,
           set_format=Python.set_formats.SET,
           variable_type_hints=Python.variable_type_hints_formats.NONE,
       ),
       pre_indent_level=0,
       variable_name="request_body",
       include_delimiters=True,
       new_variable=True,
   )
   assert request_literal.code == (
       "request_body = {\n"
       '    "name": "Alice",\n'
       '    "email": "alice@example.com",\n'
       "}"
   )

   response_literal = literalize_json(
       json_string=response_json,
       error_on_coercion=False,
       language=Python(
           date_format=Python.date_formats.PYTHON,
           datetime_format=Python.datetime_formats.PYTHON,
           bytes_format=Python.bytes_formats.HEX,
           sequence_format=Python.sequence_formats.TUPLE,
           set_format=Python.set_formats.SET,
           variable_type_hints=Python.variable_type_hints_formats.NONE,
       ),
       pre_indent_level=0,
       variable_name="response",
       include_delimiters=True,
       new_variable=True,
   )
   assert response_literal.code == (
       "response = {\n"
       '    "id": 42,\n'
       '    "name": "Alice",\n'
       '    "email": "alice@example.com",\n'
       '    "created": True,\n'
       "}"
   )

Pass a different language to get the same data as JavaScript, Go, Ruby, etc.

Output
------

Python
~~~~~~

.. code-block:: text

   request_body = {
       "name": "Alice",
       "email": "alice@example.com",
   }

   response = {
       "id": 42,
       "name": "Alice",
       "email": "alice@example.com",
       "created": True,
   }

JavaScript
~~~~~~~~~~

.. code-block:: text

   const request_body = {
       "name": "Alice",
       "email": "alice@example.com",
   };

   const response = {
       "id": 42,
       "name": "Alice",
       "email": "alice@example.com",
       "created": true,
   };

Go
~~

.. code-block:: text

   request_body := map[string]any{
       "name": "Alice",
       "email": "alice@example.com",
   }

   response := map[string]any{
       "id": 42,
       "name": "Alice",
       "email": "alice@example.com",
       "created": true,
   }

Ruby
~~~~

.. code-block:: text

   request_body = {
       "name" => "Alice",
       "email" => "alice@example.com",
   }

   response = {
       "id" => 42,
       "name" => "Alice",
       "email" => "alice@example.com",
       "created" => true,
   }
