-module(fixture_call_carrier_member_separate_erlang_call).
-export([x/0]).
'app.go'(_, _) -> ok.
x() ->
    'app.go'([1], ["text"]).
