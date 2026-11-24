-module(fixture_call_bound_sequence_null_hint_erlang_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Item = [
        1,
        2
    ],
    consume(Item).
