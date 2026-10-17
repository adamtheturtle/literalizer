-module(fixture_call_carrier_nested_homogeneous_erlang_call).
-export([x/0]).
'app.client.go'(_, _) -> ok.
x() ->
    'app.client.go'([1], [2]).
