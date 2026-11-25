-module(fixture_call_ref_external_empty_erlang_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Item = [
        1,
        2
    ],
    consume(Item).
