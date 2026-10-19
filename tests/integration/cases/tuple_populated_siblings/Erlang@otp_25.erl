-module(fixture_tuple_populated_siblings_erlang).
-export([x/0]).
x() ->
    My_data = [
        [1, [2]],
        [3, [4]]
    ],
    My_data.
