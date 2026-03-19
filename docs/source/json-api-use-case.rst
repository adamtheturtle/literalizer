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

The following script generates per-language examples for both:

.. code-block:: python

   """Generate per-language API examples."""

   from literalizer import literalize_json
   from literalizer.languages import Go, JavaScript, Python, Ruby, Language

   request_json = '{"name": "Alice", "email": "alice@example.com"}'
   response_json = (
       '{"id": 42, "name": "Alice",'
       ' "email": "alice@example.com", "created": true}'
   )

   languages: list[Language] = [Python(), JavaScript(), Go(), Ruby()]
   for language in languages:
       print(
           literalize_json(
               json_string=request_json,
               language=language,
               variable_name="request_body",
               wrap=True,
           ),
       )
       print()
       print(
           literalize_json(
               json_string=response_json,
               language=language,
               variable_name="response",
               wrap=True,
           ),
       )
       print()

Output
------

Python
~~~~~~

.. code-block:: python

   import requests

   request_body = {
       "name": "Alice",
       "email": "alice@example.com",
   }

   response = requests.post("https://api.example.com/users", json=request_body).json()
   # response = {
   #     "id": 42,
   #     "name": "Alice",
   #     "email": "alice@example.com",
   #     "created": True,
   # }

JavaScript
~~~~~~~~~~

.. code-block:: javascript

   const request_body = {
       "name": "Alice",
       "email": "alice@example.com",
   };

   const response = await fetch("https://api.example.com/users", {
       method: "POST",
       body: JSON.stringify(request_body),
   }).then(r => r.json());

   console.log(response);
   // response = {
   //     "id": 42,
   //     "name": "Alice",
   //     "email": "alice@example.com",
   //     "created": true,
   // };

Go
~~

.. code-block:: go

   request_body := map[string]any{
       "name": "Alice",
       "email": "alice@example.com",
   }

   body, _ := json.Marshal(request_body)
   resp, _ := http.Post("https://api.example.com/users", "application/json", bytes.NewBuffer(body))
   defer resp.Body.Close()
   // response := map[string]any{
   //     "id": 42,
   //     "name": "Alice",
   //     "email": "alice@example.com",
   //     "created": true,
   // }

Ruby
~~~~

.. code-block:: ruby

   require 'net/http'
   require 'json'

   request_body = {
       "name" => "Alice",
       "email" => "alice@example.com",
   }

   uri = URI("https://api.example.com/users")
   response = Net::HTTP.post(uri, request_body.to_json, { "Content-Type" => "application/json" })
   # response_body = JSON.parse(response.body)
   # # response_body = {
   # #     "id" => 42,
   # #     "name" => "Alice",
   # #     "email" => "alice@example.com",
   # #     "created" => true,
   # # }
