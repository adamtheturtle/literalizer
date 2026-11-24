-module(fixture_call_homogeneous_dotted_method_erlang_call).
-export([x/0]).
'app.client.fetch'(_) -> ok.
x() ->
    'app.client.fetch'("hello"),
    'app.client.fetch'("world").
