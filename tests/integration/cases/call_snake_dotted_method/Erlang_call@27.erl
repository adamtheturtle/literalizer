-module(fixture_call_snake_dotted_method_erlang_call).
-export([x/0]).
'my_app.http_client.fetch'(_) -> ok.
x() ->
    'my_app.http_client.fetch'("hello"),
    'my_app.http_client.fetch'(42),
    'my_app.http_client.fetch'(true).
