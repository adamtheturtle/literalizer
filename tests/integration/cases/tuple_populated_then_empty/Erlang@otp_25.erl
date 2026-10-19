-module(fixture_tuple_populated_then_empty_erlang).
-export([x/0]).
x() ->
    My_data = [
        [1, [3]],
        [2, []]
    ],
    My_data.
