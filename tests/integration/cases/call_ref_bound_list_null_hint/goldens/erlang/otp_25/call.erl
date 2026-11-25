-module(fixture_call_ref_bound_list_null_hint_erlang_call).
-export([x/0]).
consume(_) -> ok.
x() ->
    Item = [
        1,
        2
    ],
    consume(Item).
