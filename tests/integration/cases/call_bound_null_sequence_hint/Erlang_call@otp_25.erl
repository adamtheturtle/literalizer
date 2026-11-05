-module(fixture_call_bound_null_sequence_hint_erlang_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Item = undefined,
    consume(Item).
