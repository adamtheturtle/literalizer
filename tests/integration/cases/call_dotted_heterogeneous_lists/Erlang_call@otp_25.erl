-module(fixture_call_dotted_heterogeneous_lists_erlang_call).
-export([x/0]).
'app.client.go'(_, _) -> ok.
x() ->
    'app.client.go'([1], ["text"]).
