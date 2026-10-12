-module(fixture_call_ref_v_null_erlang_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Value = undefined,
    consume(Value).
