-module(fixture_tuple_empty_mixed_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        [],
        [1, "value"],
        [2, 3]
    ],
    My_data.
