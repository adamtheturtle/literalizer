-module(fixture_scalar_and_populated_sequence_erlang).
-export([x/0]).
x() ->
    My_data = [
        1,
        [2, 3]
    ],
    My_data.
