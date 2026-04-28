-module(fixture_call_dotted_method_erlang_call).
-export([x/0]).
'app.client.fetch'(_) -> ok.
x() ->
    'app.client.fetch'("hello"),
    'app.client.fetch'(42),
    'app.client.fetch'(true).
