-module(fixture_call_negative_int_erlang_call).
-export([x/0]).
process(_) -> ok.
x() ->
    process(-1),
    process(-2),
    process(-3).
