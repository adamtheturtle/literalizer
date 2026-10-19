-module(fixture_positional_mixed_rows_erlang).
-export([x/0]).
x() ->
    My_data = [
        [[1, "value"], [1, 2], []],
        [[], [], [3, 4]]
    ],
    My_data.
