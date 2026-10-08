-module(fixture_rust_tuple_empty_sibling_slot_erlang).
-export([x/0]).
x() ->
    My_data = [
        [1, []],
        [2, [3]]
    ],
    My_data.
