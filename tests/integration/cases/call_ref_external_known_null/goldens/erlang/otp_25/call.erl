-module(fixture_call_ref_external_known_null_erlang_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Item = undefined,
    consume(Item).
