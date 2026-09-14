Multi-language API documentation
=================================

If you maintain a JSON API, your documentation probably needs to show request and response examples in every language your callers use.
|project| generates those native-language literals from a single JSON sample so you don't have to write them by hand.

Example
-------

Suppose your ``POST /users`` endpoint accepts this request body and returns this response:

.. code-block:: json

   // Request body
   {"name": "Alice", "email": "alice@example.com"}

   // Response
   {"id": 42, "name": "Alice", "email": "alice@example.com", "created": true}

|project| converts these into native literals for each language using :func:`literalizer.literalize`:

.. code-block:: python

   """Generate per-language API examples."""

   import textwrap

   from literalizer import InputFormat, NewVariable, literalize
   from literalizer.languages import Python

   request_json = '{"name": "Alice", "email": "alice@example.com"}'
   response_json = (
       '{"id": 42, "name": "Alice",'
       ' "email": "alice@example.com", "created": true}'
   )

   request_literal = literalize(
       source=request_json,
       input_format=InputFormat.JSON,
       language=Python(
           date_format=Python.date_formats.PYTHON,
           datetime_format=Python.datetime_formats.PYTHON,
           bytes_format=Python.bytes_formats.HEX,
           sequence_format=Python.sequence_formats.TUPLE,
           set_format=Python.set_formats.SET,
           variable_type_hints=Python.variable_type_hints_formats.NEVER,
       ),
       pre_indent_level=0,
       variable_form=NewVariable(
           name="request_body",
           modifiers=frozenset(),
       ),
       include_delimiters=True,
   )
   assert request_literal.code == textwrap.dedent(
       text="""\
       request_body = {
           "name": "Alice",
           "email": "alice@example.com",
       }""",
   )

   response_literal = literalize(
       source=response_json,
       input_format=InputFormat.JSON,
       language=Python(
           date_format=Python.date_formats.PYTHON,
           datetime_format=Python.datetime_formats.PYTHON,
           bytes_format=Python.bytes_formats.HEX,
           sequence_format=Python.sequence_formats.TUPLE,
           set_format=Python.set_formats.SET,
           variable_type_hints=Python.variable_type_hints_formats.NEVER,
       ),
       pre_indent_level=0,
       variable_form=NewVariable(
           name="response",
           modifiers=frozenset(),
       ),
       include_delimiters=True,
   )
   assert response_literal.code == textwrap.dedent(
       text="""\
       response = {
           "id": 42,
           "name": "Alice",
           "email": "alice@example.com",
           "created": True,
       }""",
   )

Pass a different language to get the same data as JavaScript, Go, Ruby, etc.

Output
------

Python
~~~~~~

.. code-block:: python

   """Illustrative JSON request and response payloads."""

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

   expected_id = 42
   assert request_body["name"] == "Alice"
   assert response["id"] == expected_id

JavaScript
~~~~~~~~~~

.. code-block:: javascript

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

.. code-block:: go

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

.. code-block:: ruby

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
